import random
import arcade
from math import sin, cos, pi

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RADIUS = 10
WIDTH_SQUARES = 50
HEIGHT_SQUARES = 50


class Platform:
    def __init__(self):
        self.x = SCREEN_WIDTH / 2
        self.y = 10
        self.width = 100
        self.color = arcade.color.GREEN

    def draw(self):
        arcade.draw_line(self.x - self.width / 2, self.y,
                         self.x + self.width / 2, self.y,
                         self.color, 5)

    def move_to(self, x):
        if self.width / 2 < x < SCREEN_WIDTH - self.width / 2:
            self.x = x

class Ball:
    def __init__(self):
        self.r = RADIUS
        self.x = SCREEN_WIDTH / 2
        self.y = RADIUS + 10
        self.speed = 2
        self.dir = 90
        self.dx = cos(self.dir * pi / 180)
        self.dy = sin(self.dir * pi / 180)
        self.color = arcade.color.ROSE_RED

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.r, self.color)


class Squares:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = WIDTH_SQUARES
        self.h = HEIGHT_SQUARES


class MyGame(arcade.Window):
    """ Главный класс приложения. """

    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    def setup(self):
        # Настроить игру здесь
        self.platform = Platform()
        self.ball = Ball()
        print(self.platform.width)
        pass

    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()
        # Здесь код рисунка
        self.platform.draw()
        self.ball.draw()


    def update(self, delta_time):
        """ Здесь вся игровая логика и логика перемещения."""
        self.ball.move()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.platform.move_to(x)


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
