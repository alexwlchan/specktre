# -*- encoding: utf-8 -*-

import sys

from PIL import Image, ImageDraw

from . import cli
from .colors import random_color
from .utils import new_filename


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
    settings = cli.parse_args(sys.argv)
    save_speckled_wallpaper(settings)
