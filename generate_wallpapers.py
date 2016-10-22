#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Generate a new set of wallpapers for all my devices.

I use the standard screen resolution for desktops/laptops, and the
parallax sizes for iOS devices: http://dekoapp.com/parallax/
"""

import os

from specktre import (
    Color,
    save_speckled_wallpaper,
    generate_hexagons,
    generate_squares,
    generate_triangles,
    Settings,
)


OUTPUT_PATH = 'output'


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
]


if __name__ == '__main__':
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    for wallpaper in wallpaper_config:
        settings = list(wallpaper)
        settings[-1] = os.path.join(OUTPUT_PATH, settings[-1] + '.png')
        settings = Settings(*settings)

        save_speckled_wallpaper(settings)
