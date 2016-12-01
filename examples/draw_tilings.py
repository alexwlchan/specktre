#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""This script demonstrates the use of the tiling generators to draw some
simple grids.

When run from the command-line, it generates three images which
demonstrate black-and-white tilings of the plain.

"""

from PIL import Image, ImageDraw

from specktre.tilings import (generate_hexagons, generate_squares,
                              generate_triangles)

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400


def draw_tiling(coord_generator, filename):
    """Given a coordinate generator and a filename, render those coordinates in
    a new image and save them to the file."""
    im = Image.new('L', size=(CANVAS_WIDTH, CANVAS_HEIGHT))
    for shape in coord_generator(CANVAS_WIDTH, CANVAS_HEIGHT):
        ImageDraw.Draw(im).polygon(shape, outline='white')
    im.save(filename)


if __name__ == '__main__':
    draw_tiling(generate_squares,   filename='tilings-squares.png')
    draw_tiling(generate_triangles, filename='tilings-triangles.png')
    draw_tiling(generate_hexagons,  filename='tilings-hexagons.png')
