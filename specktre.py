#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Generate checkerboard wallpaper images.

Usage:
  specktre.py new --width=<width> --height=<height> --start=<start> --end=<end>
  specktre.py -h

Options:
  -h --help          Show this screen.
  --width=<width>    Width (in pixels)
  --height=<height>  Height (in pixels)
  --start=<start>    Start of the color range (RGB tuple, e.g '255,0,0')
  --end=<end>        End of the color range (RGB tuple, e.g. '0,255,0')
"""

import collections
import itertools
import math
import random
import sys
import time

import docopt
from PIL import Image, ImageDraw, ImageColor


Color = collections.namedtuple('Color', ['red', 'green', 'blue'])

Settings = collections.namedtuple(
    'Settings', ['width', 'height', 'start_color', 'end_color']
)

SEED = int(time.time())
random.seed(SEED)


def parse_args():
    args = docopt.docopt(__doc__)

    try:
        width = int(args['--width'])
        if width <= 0:
            sys.exit('Width should be positive; got %s' % width)
    except ValueError:
        sys.exit('Width should be an integer; got %s' % width)
    
    try:
        height = int(args['--height'])
        if height <= 0:
            sys.exit('Height should be positive; got %s' % height)
    except ValueError:
        sys.exit('Height should be an integer; got %s' % height)
    
    try:
        r, g, b = args['--start'].split(',')
        r = int(r); g = int(g); b = int(b)
        if any(0 > x or 255 < x for x in (r, g, b)):
            sys.exit('Color components should be 0 < X < 255')
        start_color = Color(r, g, b)
    except ValueError:
        sys.exit('Start color should be an X,Y,Z tuple; got %s' % height)

    try:
        r, g, b = args['--end'].split(',')
        r = int(r); g = int(g); b = int(b)
        if any(0 > x or 255 < x for x in (r, g, b)):
            sys.exit('Color components should be 0 < X < 255')
        end_color = Color(r, g, b)
    except ValueError:
        sys.exit('End color should be an X,Y,Z tuple; got %s' % height)
    
    return Settings(
        width=width,
        height=height,
        start_color=start_color,
        end_color=end_color,
    )


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


def generate_triangles(width, height, tr_height=25):
    """Generate the triangle vertices, for use in PIL drawings."""
    tr_width = 2 * tr_height / math.sqrt(3)
    for x in range(-1, int(width / tr_width) + 1):
        x *= tr_width
        for y in range(0, int(height / tr_height) + 1):
            if y % 2 == 0:
                y *= tr_height
                yield [(x, y), (x + tr_width, y), (x + tr_width * 0.5, y + tr_height)]
                yield [(x + tr_width, y), (x + tr_width * 0.5, y + tr_height), (x + tr_width * 1.5, y + tr_height)]
            else:
                y *= tr_height
                yield [(x + tr_width * 0.5, y), (x, y + tr_height), (x - tr_width * 0.5, y)]
                yield [(x + tr_width * 0.5, y), (x, y + tr_height), (x + tr_width, y + tr_height)]


def draw_speckled_wallpaper(settings):
    im = Image.new(mode='RGB', size=(settings.width, settings.height))
    squares = generate_squares(width=settings.width, height=settings.height)
    colors = random_color(settings.start_color, settings.end_color)
    for sq, color in zip(squares, colors):
        ImageDraw.Draw(im).rectangle(sq, fill=color)

    return im


if __name__ == '__main__':
    settings = parse_args()
    im = draw_speckled_wallpaper(settings)
    filename = filename_from_settings(settings)
    im.save(filename)
    print('Saved new wallpaper as %s' % filename)

    im = Image.new(mode='RGB', size=(100, 100))
    triangles = generate_triangles(100, 100)
    colors = random_color(settings.start_color, settings.end_color)
    for sq, color in zip(triangles, colors):
        ImageDraw.Draw(im).polygon(sq, fill=color)

    im.save('triangles.png')
