import arcade
import random
from math import sin, cos, pi

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RADIUS = 10
WIDTH_SQUARES = 50
HEIGHT_SQUARES = 25

bmp_background = arcade.load_texture('img/1 lvl.jpg')
bmp_platform = arcade.load_texture('img/platform1.png')


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
        if self.x - self.width /2 < ball.x < self.x + self.width / 2 and self.y + ball.r  >= ball.y:
            ball.reflect_y()
        if ball.y < 0:
            return 'game_over'

class Ball:
    def __init__(self):
        self.r = RADIUS
        self.x = SCREEN_WIDTH / 2
        self.y = RADIUS + 10
        self.speed = 10
        self.dir = 45
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
        self.dx *= -1

    def reflect_y(self):
        self.dy *= -1

    def set_dir(self, dir):
        self.dir = dir
        self.dx = cos(self.dir * pi / 180)
        self.dy = sin(self.dir * pi / 180)

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.r, self.color)


class Squares:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = WIDTH_SQUARES
        self.h = HEIGHT_SQUARES
        self.color = [119, 253, 1]

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.w - 5, self.h - 5, self.color)

    def is_collision(self, ball):
        if (abs(ball.y - self.y) <= self.h / 2 + ball.r) and (abs(ball.x - self.x) <= self.w / 2 + ball.r):
            return True
        else:
            return False


class MyGame(arcade.Window):
    """ Главный класс приложения. """
    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.WHITE_SMOKE)
        self.squares_list = []
        self.score = 0
        self.game_over = False

    def setup(self):
        # Настроить игру здесь
        self.platform = Platform()
        self.ball = Ball()
        print(self.platform.width)
        for i in range(16):
            for j in range(3):
                self.squares_list.append(Squares(i * 50 + 20, j * 25 + 537))
        pass

    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()
        # Здесь код рисунка
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT// 2, SCREEN_WIDTH, SCREEN_HEIGHT, bmp_background)
        if not self.game_over:
            self.platform.draw()
            for square in self.squares_list:
                square.draw()
            self.ball.draw()
        else:
            arcade.draw_text('GAME OVER!!!', SCREEN_HEIGHT / 20, SCREEN_WIDTH / 3, [200, 0, 0], 100)

    def update(self, delta_time):
        """ Здесь вся игровая логика и логика перемещения."""
        self.ball.move()
        for brick in self.squares_list:
            if brick.is_collision(self.ball):
                self.ball.reflect_y()
                self.squares_list.remove(brick)

        if self.platform.ball_collision_update(self.ball) == 'game_over':
            self.game_over = True

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.platform.move_to(x)


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
