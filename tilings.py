#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Generate regular tilings of the plane with PIL.
"""

import math

from PIL import Image, ImageDraw

CANVAS_WIDTH  = 400
CANVAS_HEIGHT = 400


def generate_squares(canvas_width, canvas_height, sq_side=25):
    """Generate coordinates for a tiling of squares."""
    # Iterate over the required rows and cells.  The for loops (x, y)
    # give the coordinates of the top left-hand corner of each square:
    #
    #      (x, y) +-----+ (x + 1, y)
    #             |     |
    #             |     |
    #             |     |
    #  (x, y + 1) +-----+ (x + 1, y + 1)
    #
    # Then we extend by 1 in each direction, and scale up for the length
    # of the side of the squares.
    #
    for x in range(0, int(canvas_width / sq_side) + 1):
        for y in range(0, int(canvas_height / sq_side) + 1):
            coords = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
            yield [(a * sq_side, b * sq_side) for a, b in coords]


def generate_triangles(canvas_width, canvas_height, tr_side=25):
    """Generate coordinates for a regular tiling of triangles."""
    # Our triangles lie with one side paralle to the x-axis.  Let s be
    # the length of one side, and h the height of the triangle.
    #
    # The for loops (x, y) gives the coordinates of the top left-hand corner
    # of a pair of triangles:
    #
    #           (x, y) +-----+ (x + s, y)
    #                   \   / \
    #                    \ /   \
    #    (x + s/2, y + h) +-----+ (x + 3s/2, y + h)
    #
    # On odd-numbered rows, we translate by (s/2, 0) to make the triangles
    # line up with the even-numbered rows.
    #
    # To avoid blank spaces on the edge of the canvas, the first pair of
    # triangles on each row starts at (-s, 0) -- one width before the edge
    # of the canvas.

    # Width of the triangle is just the length of one side
    tr_width = tr_side

    # Assume that one side of the triangle is parallel to the x-axis;
    # then we have sin(60°) = tr_height / tr_side
    tr_height = tr_side * math.sin(math.pi / 3)

    # Now we have a per-row height, we can iterate over the required rows.
    for x in range(-1, int(canvas_width / tr_width) + 1):
        for y in range(0, int(canvas_height / tr_height) + 1):

            # Add the half-distance offset on odd-numbered rows.  For some
            # reason, just adding directly to x screws up the other rows,
            # so I'm using x_ as a stand-in for x.
            if y % 2 == 0:
                x_ = x
            else:
                x_ = x + 0.5

            coords = [
                # \/-shaped triangle
                [(x_, y), (x_ + 1, y), (x_ + 0.5, y + 1)],

                # /\-shaped triangle
                [(x_ + 1, y), (x_ + 1.5, y + 1), (x_ + 0.5, y + 1)],
            ]

            for coord in coords:
                yield [(a * tr_width, b * tr_height) for (a, b) in coord]


def generate_hexagons(canvas_width, canvas_height, hx_side=25):
    """Generate coordinates for a regular tiling of hexagons."""
    # Let s be the length of one side of the hexagon, and h the height
    # of the entire hexagon if one side lies parallel to the x-axis.
    #
    # The for loops (x, y) give the coordinate of one coordinate of the
    # hexagon, and the remaining coordinates fall out as follows:
    #
    #                     (x, y) +-----+ (x + s, y)
    #                           /       \
    #                          /         \
    #    (x - s/2, y + h / 2) +           + (x + 3s/2, y + h/2)
    #                          \         /
    #                           \       /
    #                 (x, y + h) +-----+ (x + s, y + h)
    #
    # In each row we generate hexagons in the following pattern
    #
    #         /‾‾‾\   /‾‾‾\   /‾‾‾\
    #         \___/   \___/   \___/
    #
    # and the next row is offset to fill in the gaps. So after two rows,
    # we'd have the following pattern:
    #
    #         /‾‾‾\   /‾‾‾\   /‾‾‾\
    #         \___/‾‾‾\___/‾‾‾\___/‾‾‾\
    #             \___/   \___/   \___/
    #
    # There are offsets to ensure we fill the entire canvas.

    # The height of the entire hexagon satisfies
    #    sin(60°) = 0.5 * hx_height / hx_side
    hx_height = 2 * hx_side * math.sin(math.pi / 3)

    for x in range(-1, int(canvas_width / hx_side) + 1, 3):
        for y in range(0, int(canvas_height / hx_height) * 2 + 1):

            # Add the half-distance offset on odd-numbered rows.
            if y % 2 == 0:
                x_ = x
            else:
                x_ = x + 1.5

            # Each row should only be offset vertically by half the height
            # of the hexagon.
            y_offst = y * hx_height * 0.5

            coords = [
                (x_, y), (x_ + 1, y), (x_ + 1.5, y + 0.5),
                (x_ + 1, y + 1), (x_, y + 1), (x_ - 0.5, y + 0.5)
            ]
            yield [(a * hx_side, b * hx_height - y_offst) for (a, b) in coords]



def draw_tiling(coord_generator, filename):
    im = Image.new('L', size=(CANVAS_WIDTH, CANVAS_HEIGHT))
    for shape in coord_generator(CANVAS_WIDTH, CANVAS_HEIGHT):
        ImageDraw.Draw(im).polygon(shape, outline='white')
    im.save(filename)


if __name__ == '__main__':
    draw_tiling(generate_squares,   filename='squares.png')
    draw_tiling(generate_triangles, filename='triangles.png')
    draw_tiling(generate_hexagons,  filename='hexagons.png')
