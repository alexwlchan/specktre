#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Unit tests for specktre.colors."""

import pytest

from specktre.colors import Color


def test_using_color_gives_deprecation_warning():
    """Using the `Color` class gives a deprecation warning."""
    with pytest.warns(DeprecationWarning):
        Color(red=1, green=2, blue=3)
