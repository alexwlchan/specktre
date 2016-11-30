#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Generate checkerboard wallpaper images.

Usage:
  specktre.py new --size=<size> --start=<start> --end=<end> [--squares | --triangles | --hexagons] [--name=<name>]
  specktre.py -h

Options:
  -h --help          Show this screen.
  --size=<size>      Size in pixels - WxH
  --start=<start>    Start of the color range (RGB tuple, e.g '255,0,0')
  --end=<end>        End of the color range (RGB tuple, e.g. '0,255,0')
  --squares          Tile with squares.
  --triangles        Tile with triangles.
  --hexagons         Tile with hexagons.
  --name=<name>      (Optional) Name of the file to save to.
""" # noqa

import collections
import os
import random
import string
import sys

import docopt
from PIL import Image, ImageDraw

from .colors import Color, random_color
from .tilings import generate_squares, generate_triangles, generate_hexagons


Settings = collections.namedtuple('Settings', [
    'generator', 'width', 'height', 'start_color', 'end_color', 'name'])


def _positive_integer_arg(arg_value, arg_name):
    """Checks a value is a positive integer, or exists."""
    try:
        value = int(arg_value)
        if value <= 0:
            sys.exit('%s should be positive; got %r' % (arg_name, arg_value))
        return value
    except ValueError:
        sys.exit('%s should be an integer; got %r' % (arg_name, arg_value))


def _parse_color_components(arg_value, arg_name):
    """Checks a value can be parsed as an RGB tuple."""
    try:
        r, g, b = arg_value.split(',')
        r = int(r)
        g = int(g)
        b = int(b)
        if any(0 > x or 255 < x for x in (r, g, b)):
            sys.exit('Color components should be 0 < X < 255')
        return Color(r, g, b)
    except ValueError:
        sys.exit('%s should be an R,G,B tuple; got %r' % (arg_name, arg_value))


def parse_args():
    args = docopt.docopt(__doc__)

    if args['--squares']:
        generator = generate_squares
    elif args['--triangles']:
        generator = generate_triangles
    elif args['--hexagons']:
        generator = generate_hexagons
    else:
        generator = generate_squares

    try:
        width, height = args['--size'].split('x')
    except ValueError:
        sys.exit('--size should be in the form WxH; got %s' % args['--size'])

    width = _positive_integer_arg(width, arg_name='Width')
    height = _positive_integer_arg(height, arg_name='Height')

    start_color = _parse_color_components(args['--start'],
                                          arg_name='Start color')
    end_color = _parse_color_components(args['--end'], arg_name='End color')

    name = args['--name']

    return Settings(
        generator=generator,
        width=width,
        height=height,
        start_color=start_color,
        end_color=end_color,
        name=name,
    )


def _generate_filenames():
    while True:
        random_stub = ''.join([
            random.choice(string.ascii_letters + string.digits)
            for _ in range(5)
        ])
        yield 'specktre_%s.png' % random_stub


def get_new_filename():
    for filename in _generate_filenames():
        if not os.path.exists(filename):
            return filename


def draw_speckled_wallpaper(settings):
    im = Image.new(mode='RGB', size=(settings.width, settings.height))
    squares = settings.generator(settings.width, settings.height)
    colors = random_color(settings.start_color, settings.end_color)
    for sq, color in zip(squares, colors):
        ImageDraw.Draw(im).polygon(sq, fill=color)

    return im


def save_speckled_wallpaper(settings):
    im = draw_speckled_wallpaper(settings)
    if settings.name:
        filename = settings.name
    else:
        filename = get_new_filename()
    im.save(filename)
    print('Saved new wallpaper as %s' % filename)


def main():
    settings = parse_args()
    save_speckled_wallpaper(settings)
