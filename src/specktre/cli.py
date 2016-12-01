# -*- encoding: utf-8 -*-
"""Utilities for parsing input from the command-line."""

import re

from .colors import RGBColor


def check_positive_integer(name, value):
    """Check a value is a positive integer.

    Returns the value if so, raises ValueError otherwise.

    """
    try:
        value = int(value)
        is_positive = (value > 0)
    except ValueError:
        raise ValueError('%s should be an integer; got %r' % (name, value))

    if is_positive:
        return value
    else:
        raise ValueError('%s should be positive; got %r' % (name, value))


def _parse_rgb_color_component(value):
    """Check a value is a valid RGB colour specification.

    Returns a parsed `RGBColor` instance if so, raises ValueError otherwise.
    """
    # RGB tuple is specified as rgb(255, 0, 255)
    rgb_match = re.match(
        r'^rgb\('
        r'\s*(?P<red>[0-9]+)\s*,'
        r'\s*(?P<green>[0-9]+)\s*,'
        r'\s*(?P<blue>[0-9]+)\s*\)$',
        value)
    if rgb_match:
        # We know that the values are numeric, so parse as integers.
        red = int(rgb_match.group('red').lstrip('0') or '0')
        green = int(rgb_match.group('green').lstrip('0') or '0')
        blue = int(rgb_match.group('blue').lstrip('0') or '0')
        if max((red, green, blue)) > 255:
            raise ValueError(
                'RGB components should be integers between 0 and 255; got %r' %
                value)
        return RGBColor(red, green, blue)
    else:
        raise ValueError('Invalid RGB colour: %r' % value)


def parse_color_input(value):
    """Check a value is a valid colour input.

    Returns a parsed `RGBColor` instance if so, raises ValueError
    otherwise.

    """
    value = value.lower().strip()
    if value.startswith('rgb'):
        return _parse_rgb_color_component(value)

    raise ValueError('Unrecognised colour: %r' % value)
