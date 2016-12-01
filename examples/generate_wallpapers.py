#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Generate a new set of wallpapers for all my devices.

I use the standard screen resolution for desktops/laptops, and the
parallax sizes for iOS devices: http://dekoapp.com/parallax/
"""

from specktre import create_wallpaper
from specktre.colors import RGBColor as Color
from specktre.tilings import (generate_hexagons, generate_squares, generate_triangles)


wallpaper_config = [
    # iMac: purple hexagons
    (generate_hexagons,  2560, 1440, Color(55, 19, 78),  Color(72, 27, 100), 'imac-wallpaper'),

    # MacBook: red squares
    (generate_squares,   2304, 1440, Color(178, 26, 16), Color(136, 25, 17), 'macbook-wallpaper'),

    # iPhone: blue triangles on the lock screen, black on the home screen
    (generate_triangles,  744, 1392, Color(18, 18, 18),  Color(11, 11, 11),  'iphone-lock'),
    (generate_triangles,  744, 1392, Color(13, 16, 155), Color(14, 58, 180), 'iphone-home'),

    # iPad: green triangles on the lock screen, black on the home screen
    (generate_triangles, 2524, 2524, Color(18, 18, 18),  Color(11, 11, 11),  'ipad-lock'),
    (generate_triangles, 2524, 2524, Color(11, 153, 46), Color(6, 86, 9),    'ipad-home'),

    # Demo wallpapers
    (generate_squares,   400, 400, Color(178, 26, 16), Color(136, 25, 17),   'demo_sq'),
    (generate_triangles, 400, 400, Color(255, 204, 0), Color(255, 238, 56),  'demo_tr'),
    (generate_hexagons,  400, 400, Color(56, 56, 255), Color(0, 0, 194),     'demo_hex'),
]


if __name__ == '__main__':
    for (generator, width, height, color1, color2, name) in wallpaper_config:
        filename = name + '.png'
        create_wallpaper(
            generator=generator,
            color1=color1,
            color2=color2,
            width=width,
            height=height,
            filename=filename)
        print('Saved new wallpaper as %s' % filename)
