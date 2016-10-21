#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Generate checkerboard wallpaper images.

Usage:
  specktre.py new --size=<size> --start=<start> --end=<end>
  specktre.py -h

Options:
  -h --help          Show this screen.
  --size=<size>      Size in pixels - WxH
  --start=<start>    Start of the color range (RGB tuple, e.g '255,0,0')
  --end=<end>        End of the color range (RGB tuple, e.g. '0,255,0')
"""

import collections
import math
import random
import sys

import docopt
from PIL import Image, ImageDraw

from tilings import generate_squares, generate_triangles


Color = collections.namedtuple('Color', ['red', 'green', 'blue'])

Settings = collections.namedtuple(
    'Settings', ['width', 'height', 'start_color', 'end_color']
)


def parse_args():
    args = docopt.docopt(__doc__)

    try:
        width, height = args['--size'].split('x')
    except ValueError:
        sys.exit('--size should be in the form WxH; got %s' % args['--size'])

    try:
        width = int(width)
        if width <= 0:
            sys.exit('Width should be positive; got %s' % width)
    except ValueError:
        sys.exit('Width should be an integer; got %s' % width)

    try:
        height = int(height)
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


def draw_speckled_wallpaper(settings):
    im = Image.new(mode='RGB', size=(settings.width, settings.height))
    squares = generate_squares(settings.width, settings.height)
    colors = random_color(settings.start_color, settings.end_color)
    for sq, color in zip(squares, colors):
        ImageDraw.Draw(im).polygon(sq, fill=color)

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
