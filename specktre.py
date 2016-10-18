#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import collections
import itertools
import math
import random

from PIL import Image, ImageDraw, ImageColor


Color = collections.namedtuple('Color', ['red', 'green', 'blue'])


def random_rgb_value(lower, upper):
    """
    Returns a random value between (lower, upper), where ``lower``
    and ``upper`` are RGB values in [0, 255].
    """
    # Normalise to a scale 0.0 - 1.0
    lower /= 255.0
    upper /= 255.0
    
    # Next square both values.  We'll take the average of the squares, then
    # take the square root again.  I'm trying to get a better sample of the
    # overall colour space.  See https://www.youtube.com/watch?v=LKnqECcg6Gw
    lower **= 2
    upper **= 2
    
    # Pick a random value, then normalise to get back to 0-255 values
    value = random.uniform(lower, upper)
    return int(math.sqrt(value) * 255)


def random_color(start, end):
    """Generates random colours between ``start`` and ``end``."""
    while True:
        red   = random_rgb_value(*sorted([start.red,   end.red]))
        green = random_rgb_value(*sorted([start.green, end.green]))
        blue  = random_rgb_value(*sorted([start.blue,  end.blue]))
        yield Color(red=red, green=green, blue=blue)


def generate_squares(sq_size, width, height):
    """Generates the square corners, for use in PIL drawings."""
    for x in range(0, width, sq_size):
        for y in range(0, height, sq_size):
            print(x, y)
            yield [x, y, x + sq_size, y + sq_size]


def draw_speckled_wallpaper(width=200, height=200):
    image = Image.new(mode='RGB', size=(width, height))
    n = 5
    draw_square = ImageDraw.Draw(image).rectangle
    squares = generate_squares(40, 200, 200)
    for sq, color in zip(squares, random_color(
        Color(255, 0, 0),
        Color(0, 255, 0),
    )):
        draw_square(sq, fill=color)

    image.save("chessboard-pil.png")


if __name__ == '__main__':
    draw_speckled_wallpaper()
