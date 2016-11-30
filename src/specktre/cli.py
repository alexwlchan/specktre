# -*- encoding: utf-8 -*-
"""Utilities for parsing input from the command-line."""


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
