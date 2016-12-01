# -*- encoding: utf-8 -*-
"""Utilities for parsing input from the command-line."""

import argparse
import re
import sys

from .colors import RGBColor


def parse_args(version):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='specktre.  Create checkerboard wallpaper images.')
    subparsers = parser.add_subparsers(dest='subparser_name')

    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + version)

    img_parser = subparsers.add_parser('image',
                                       description='Create a new image.')
    img_parser.add_argument('--width', type=int, default=250,
                            help='Width of the final image (pixels)')
    img_parser.add_argument('--height', type=int, default=250,
                            help='Height of the final image (pixels)')
    img_parser.add_argument('--color1', default='#ffffff',
                            help='Start of the color range (hex string)')
    img_parser.add_argument('--color2', default='#000000',
                            help='End of the color range (hex string)')
    img_parser.add_argument('--shape',
                            choices=['squares', 'triangles', 'hexagons'],
                            default='squares', help='Shape of the tiles')
    img_parser.add_argument('--filename', help='Name of the generated file')

    args = parser.parse_args()

    if not args.subparser_name:
        parser.print_help()
        sys.exit(0)

    elif args.subparser_name == 'image':

        if args.width <= 0:
            parser.error('Width must be positive; got %r.' % args.width)

        if args.height <= 0:
            parser.error('Height must be positive; got %r.' % args.height)

        try:
            args.color1 = check_color_input(args.color1)
        except ValueError as exc:
            parser.error(exc)

        try:
            args.color2 = check_color_input(args.color2)
        except ValueError as exc:
            parser.error(exc)

    return args


def check_color_input(value):
    """Check a value is a valid colour input.

    Returns a parsed `RGBColor` instance if so, raises ValueError
    otherwise.

    """
    orig_value = value
    value = value.lower()
    # Trim a leading hash
    if value.startswith('#'):
        value = value[1:]

    if len(value) != 6:
        raise ValueError(
            'Color should be six hexadecimal digits, got %r' % orig_value)

    if re.sub(r'[a-f0-9]', '', value):
        raise ValueError(
            'Color should only contain hex characters, got %r' % orig_value)

    red = int(value[0:2], base=16)
    green = int(value[2:4], base=16)
    blue = int(value[4:6], base=16)
    return RGBColor(red, green, blue)
