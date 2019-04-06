# -*- encoding: utf-8 -*-
"""Generate checkerboard wallpaper images.

Usage:
  specktre.py new --size=<size> --start=<start> --end=<end> [--squares | --triangles | --hexagons] [--name=<name>]
  specktre.py -h

Options:
  -h --help          Show this screen.
  --size=<size>      Size in pixels - WxH (e.g. 100x200)
  --start=<start>    Start of the color range (hex, e.g. #01ab23)
  --end=<end>        End of the color range (hex, e.g. #01ab23)
  --squares          Tile with squares.
  --triangles        Tile with triangles.
  --hexagons         Tile with hexagons.
  --name=<name>      (Optional) Name of the file to save to.

"""  # noqa

import re
import sys

import attr
import docopt

from .colors import RGBColor
from .tilings import generate_hexagons, generate_squares, generate_triangles


@attr.s
class Settings(object):
    generator = attr.ib()
    width = attr.ib()
    height = attr.ib()
    start_color = attr.ib()
    end_color = attr.ib()
    name = attr.ib()


def check_positive_integer(name, value):
    """Check a value is a positive integer.

    Returns the value if so, raises ValueError otherwise.

    """
    try:
        value = int(value)
        is_positive = (value > 0)
    except ValueError:
        raise ValueError('%s should be an integer; got %r' % (name, value))

    if is_positive:
        return value
    else:
        raise ValueError('%s should be positive; got %r' % (name, value))


def check_color_input(value):
    """Check a value is a valid colour input.

    Returns a parsed `RGBColor` instance if so, raises ValueError
    otherwise.

    """
    value = value.lower()
    # Trim a leading hash
    if value.startswith('#'):
        value = value[1:]

    if len(value) != 6:
        raise ValueError(
            'Color should be six hexadecimal digits, got %r (%s)' %
            (value, len(value)))

    if re.sub(r'[a-f0-9]', '', value):
        raise ValueError(
            'Color should only contain hex characters, got %r' % value)

    red = int(value[0:2], base=16)
    green = int(value[2:4], base=16)
    blue = int(value[4:6], base=16)
    return RGBColor(red, green, blue)


def parse_args(argv):
    args = docopt.docopt(__doc__, argv)

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
        width = check_positive_integer(name='Width', value=width)
        height = check_positive_integer(name='Height', value=height)
    except ValueError:
        sys.exit('--size should be in the form WxH; got %s' % args['--size'])

    start_color = check_color_input(args['--start'])
    end_color = check_color_input(args['--end'])

    name = args['--name']

    return Settings(
        generator=generator,
        width=width,
        height=height,
        start_color=start_color,
        end_color=end_color,
        name=name,
    )
