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

import collections
import sys

import docopt
from PIL import Image, ImageDraw

from . import cli
from .colors import random_color
from .tilings import generate_hexagons, generate_squares, generate_triangles
from .utils import new_filename

Settings = collections.namedtuple('Settings', [
    'generator', 'width', 'height', 'start_color', 'end_color', 'name'])


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

    width = cli.check_positive_integer(name='Width', value=width)
    height = cli.check_positive_integer(name='Height', value=height)

    start_color = cli.check_color_input(args['--start'])
    end_color = cli.check_color_input(args['--end'])

    name = args['--name']

    return Settings(
        generator=generator,
        width=width,
        height=height,
        start_color=start_color,
        end_color=end_color,
        name=name,
    )


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
        filename = new_filename()
    im.save(filename)
    print('Saved new wallpaper as %s' % filename)


def main():
    settings = parse_args()
    save_speckled_wallpaper(settings)
