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


def check_color_input(value):
    """Check a value is a valid colour input.

    Returns a parsed `RGBColor` instance if so, raises ValueError
    otherwise.

    """
    value = value.lower()
    # Trim a leading hash
    if value.startswith('#'):
        value = value[1:]

    if len(value) != 6:
        raise ValueError(
            'Color should be six hexadecimal digits, got %r (%s)' %
            (value, len(value)))

    if re.sub(r'[a-f0-9]', '', value):
        raise ValueError(
            'Color should only contain hex characters, got %r' % value)

    red = int(value[0:2], base=16)
    green = int(value[2:4], base=16)
    blue = int(value[4:6], base=16)
    return RGBColor(red, green, blue)
