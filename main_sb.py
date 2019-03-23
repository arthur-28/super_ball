import arcade
import random
from math import sin, cos, pi

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RADIUS = 10
WIDTH_SQUARES = 50
HEIGHT_SQUARES = 50

class Ball:
    def __init__(self):
        self.r = RADIUS
        self.x = SCREEN_WIDTH / 2
        self.y = RADIUS / 2


class Squares:
    def __init__(self, x, y):
        color_list = [arcade.color.BLUE, [125, 10, 200], [125, 10, 10]]
        self.x = x
        self.y = y
        self.w = WIDTH_SQUARES
        self.h = HEIGHT_SQUARES
        self.color = random.choice(color_list)

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.w, self.h, self.color)


class MyGame(arcade.Window):
    """ Главный класс приложения. """

    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    def setup(self):
        # Настроить игру здесь
        pass

    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()
        # Здесь код рисунка

    def update(self, delta_time):
        """ Здесь вся игровая логика и логика перемещения."""
        pass



def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()