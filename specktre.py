#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import collections
import itertools
import math
import random
import time

from PIL import Image, ImageDraw, ImageColor


Color = collections.namedtuple('Color', ['red', 'green', 'blue'])

Settings = collections.namedtuple(
    'Settings', ['width', 'height', 'start_color', 'end_color']
)

SEED = int(time.time())
random.seed(SEED)


def filename_from_settings(settings):
    components = [
        'specktre',
        'w=%s' % settings.width,
        'h=%s' % settings.height,
        'start=%s' % '-'.join([str(s) for s in settings.start_color]),
        'end=%s' % '-'.join([str(s) for s in settings.end_color]),
        'seed=%s' % SEED,
    ]
    return '_'.join(components) + '.png'


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


def generate_squares(width, height, sq_size=25):
    """Generates the square corners, for use in PIL drawings."""
    for x in range(0, width, sq_size):
        for y in range(0, height, sq_size):
            yield [x, y, x + sq_size, y + sq_size]


def draw_speckled_wallpaper(settings):
    im = Image.new(mode='RGB', size=(settings.width, settings.height))
    squares = generate_squares(width=settings.width, height=settings.height)
    colors = random_color(settings.start_color, settings.end_color)
    for sq, color in zip(squares, colors):
        ImageDraw.Draw(im).rectangle(sq, fill=color)

    return im


if __name__ == '__main__':
    settings = Settings(
        width=400,
        height=400,
        start_color=Color(0, 0, 255),
        end_color=Color(10, 10, 160),
    )
    im = draw_speckled_wallpaper(settings)
    im.save(filename_from_settings(settings))
