# -*- encoding: utf-8 -*-

from PIL import Image, ImageDraw

from .cli import parse_args
from .colors import random_color
from .tilings import generate_hexagons, generate_squares, generate_triangles
from .utils import new_filename


def main():
    args = parse_args()

    generator_names = {
        'hexagons': generate_hexagons,
        'squares': generate_squares,
        'triangles': generate_triangles,
    }

    # Get the coordinates of the tiling
    generator = generator_names[args.shape]
    coords = generator(args.width, args.height)

    # And the random colors
    colors = random_color(args.color1, args.color2)

    im = Image.new(mode='RGB', size=(args.width, args.height))
    for coord, color in zip(coords, colors):
        ImageDraw.Draw(im).polygon(coord, fill=color)

    if args.filename:
        filename = args.filename
    else:
        filename = new_filename()
    im.save(filename)
    print('Saved new wallpaper as %s' % filename)
