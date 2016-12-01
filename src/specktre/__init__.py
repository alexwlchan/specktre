# -*- encoding: utf-8 -*-

from PIL import Image, ImageDraw

from .cli import parse_args
from .colors import random_color
from .tilings import generate_hexagons, generate_squares, generate_triangles
from .utils import new_filename


__version__ = '0.3.0'


def create_wallpaper(generator, color1, color2, width, height, filename):
    """Create a wallpaper and saves it to a file.

    :param generator: A function that takes two arguments `width` and `height`,
        and generates `(x, y)` coordinates for a tiling of the plane.
    :param color1: Start of the color range (`RGBColor` instance).
    :param color2: End of the color range (`RGBColor` instance).
    :param width: Width of the canvas (pixels).
    :param height: Height of the canvas (pixels).
    :param filename: Filename to save the image to.

    """
    coords = generator(width, height)
    colors = random_color(color1, color2)
    im = Image.new(mode='RGB', size=(width, height))
    for coord, color in zip(coords, colors):
        ImageDraw.Draw(im).polygon(coord, fill=color)
    im.save(filename)


def main():
    args = parse_args(version=__version__)

    generator_names = {
        'hexagons': generate_hexagons,
        'squares': generate_squares,
        'triangles': generate_triangles,
    }
    generator = generator_names[args.shape]

    if args.filename:
        filename = args.filename
    else:
        filename = new_filename()

    create_wallpaper(
        generator=generator_names[args.shape],
        color1=args.color1,
        color2=args.color2,
        width=args.width,
        height=args.height,
        filename=filename)

    print('Saved new wallpaper as %s' % filename)
