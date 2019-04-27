import arcade
import random
from math import sin, cos, pi

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
RADIUS = 10
COUNT_SQUARES_X = 20
COUNT_SQUARES_Y = 2

WIDTH_SQUARES = SCREEN_WIDTH / COUNT_SQUARES_X
HEIGHT_SQUARES = WIDTH_SQUARES / 2
MAX_A = 30

bmp_background = arcade.load_texture('img/1 lvl.jpg')
bmp_platform = arcade.load_texture('img/platform1.png')
bmp_ball = arcade.load_texture('img/ball.png')

# from tkinter import *

# root = Tk()
# root.title("GUI на Python")
# root.geometry("800x600")

# main_menu = Menu()
# main_menu.add_cascade(label="File")
# main_menu.add_cascade(label="Edit")
# main_menu.add_cascade(label="View")
#
# root.config(menu=main_menu)
# root.mainloop()


class Platform:
    def __init__(self):
        self.x = SCREEN_WIDTH / 2
        self.y = 10
        self.width = 170
        self.color = arcade.color.BLACK_LEATHER_JACKET

    def draw(self):
        arcade.draw_line(self.x - self.width / 2, self.y,
                         self.x + self.width / 2, self.y,
                         self.color, 5)
        arcade.draw_texture_rectangle(self.x, self.y, self.width, 30, bmp_platform)

    def move_to(self, x):
        if self.width / 2 < x < SCREEN_WIDTH - self.width / 2:
            self.x = x
        # if self.width / 2 < y < SCREEN_HEIGHT - self.width / 2:
            pass

    def ball_collision_update(self, ball):
        if self.x - self.width * 0.5 < ball.x < self.x + self.width * 0.5 \
                and self.y + ball.r > ball.y:
            dx = self.x - ball.x
            ball.reflect_y()
            # корректируем направление в зависимости от места столкновения с платформой
            dAlpha = MAX_A * dx / (self.width * 0.5)
            ball.correct_dir(dAlpha)
            ball.y = self.y + ball.r

        if ball.y < 0:
            return 'game_over'

class Ball:
    def __init__(self):
        self.r = RADIUS
        self.x = SCREEN_WIDTH / 2
        self.y = RADIUS + 10
        self.speed = 12
        self.dir = 90
        self.dx = cos(self.dir * pi / 180)
        self.dy = sin(self.dir * pi / 180)
        self.color = arcade.color.GRAY

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        if not(self.r <= self.x <= SCREEN_WIDTH - self.r):
            self.reflect_x()
        if not (self.y <= SCREEN_HEIGHT - self.r):
            self.reflect_y()

    def reflect_x(self):
        self.dir = 180 - self.dir
        self.dx = cos(self.dir * pi / 180)
        self.dy = sin(self.dir * pi / 180)

    def reflect_y(self):
        self.dir *= -1
        self.dx = cos(self.dir * pi / 180)
        self.dy = sin(self.dir * pi / 180)

    def correct_dir(self, change_dir=0):
        self.dir += change_dir
        self.dx = cos(self.dir * pi / 180)
        self.dy = sin(self.dir * pi / 180)

    def set_dir(self, dir):
        self.dir = dir
        self.dx = cos(self.dir * pi / 180)
        self.dy = sin(self.dir * pi / 180)

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.r, self.color)
        arcade.draw_texture_rectangle(self.x, self.y, self.r * 6, self.r * 6, bmp_ball)


class Squares:
    def __init__(self, x, y):
        self.x = x + WIDTH_SQUARES / 2
        self.y = y + HEIGHT_SQUARES / 2
        self.w = WIDTH_SQUARES
        self.h = HEIGHT_SQUARES
        self.color = [119, 253, 1]

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.w - 5, self.h - 5, self.color)

    def is_collision(self, ball):
        if (abs(ball.y - self.y) <= self.h / 2 + ball.r) \
                and (abs(ball.x - self.x) <= self.w / 2 + ball.r):
            return True
        else:
            return False


class MyGame(arcade.Window):
    """ Главный класс приложения. """
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE_SMOKE)
        self.set_mouse_visible(False)
        self.squares_list = []


    def setup(self):
        # Настроить игру здесь
        self.score = 0
        self.game_over = False
        #  'game_run', 'game_win', 'game_over'
        self.game_state = 'game_run'

        self.platform = Platform()
        self.ball = Ball()
        print(self.platform.width)
        for i in range(COUNT_SQUARES_X):
            for j in range(COUNT_SQUARES_Y):
                self.squares_list.append(Squares(i * WIDTH_SQUARES, HEIGHT_SQUARES * j + SCREEN_HEIGHT - HEIGHT_SQUARES * COUNT_SQUARES_Y))
        pass

    def get_info(self):
        st = 'Score: {}\n\n'.format(self.score)
        return st

    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()
        # Здесь код рисунка
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT,
                                      bmp_background)
        arcade.draw_text(self.get_info(), 30, 30, arcade.color.WHITE_SMOKE, 18)

        self.platform.draw()
        for square in self.squares_list:
            square.draw()
        self.ball.draw()

        if self.game_state == 'game_win':
            arcade.draw_text('YOU WIN!!!', SCREEN_HEIGHT / 20, SCREEN_WIDTH / 3, [119, 253, 1], 100)
        elif self.game_state == 'game_over':
            arcade.draw_text('GAME OVER!!!', SCREEN_HEIGHT / 20, SCREEN_WIDTH / 3, [119, 253, 1], 100)

    def update(self, delta_time):
        """ Здесь вся игровая логика и логика перемещения."""
        if self.game_state == 'game_run':
            self.ball.move()
            for brick in self.squares_list:
                if brick.is_collision(self.ball):
                    self.ball.reflect_y()
                    self.squares_list.remove(brick)
                    self.score += 1
                    break

            if self.platform.ball_collision_update(self.ball) == 'game_over':
                self.game_over = True
                self.game_state = 'game_over'
            if len(self.squares_list) == 0:
                self.game_state = 'game_win'


    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.platform.move_to(x)


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, 'Super ball')
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()

