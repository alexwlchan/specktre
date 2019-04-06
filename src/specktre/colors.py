# -*- encoding: utf-8 -*-
"""Generate random colors between two other colors."""

import random

import attr


@attr.s
class RGBColor(object):
    red = attr.ib()
    green = attr.ib()
    blue = attr.ib()


def random_color(start, end):
    d_red = (start.red - end.red)
    d_green = (start.green - end.green)
    d_blue = (start.blue - end.blue)
    while True:
        chosen_d = random.uniform(0, 1)
        yield RGBColor(
            start.red - int(d_red * chosen_d),
            start.green - int(d_green * chosen_d),
            start.blue - int(d_blue * chosen_d)
        )
