#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Unit tests for specktre.cli."""

from hypothesis import assume, given, strategies as st
import pytest

from specktre import cli
from specktre.colors import RGBColor


class TestCheckPositiveInteger(object):
    """Unit tests for `cli.check_positive_integer`."""

    @given(st.integers(min_value=1))
    def test_positive_integers_are_allowed(self, value):
        """Positive integers go through `check_positive_integer` unmodified."""
        assert cli.check_positive_integer(name='test', value=value) == value

    @given(st.integers(max_value=0))
    def test_non_positive_integers_are_valueerror(self, value):
        """Negative or zero integers are rejected with a `ValueError`."""
        with pytest.raises(ValueError) as exc:
            cli.check_positive_integer(name='test', value=value)
        assert 'should be positive' in exc.value.args[0]

    @given(st.text())
    def test_non_integers_are_valuerror(self, value):
        """Values that cannot be coerced to an integer are rejected with a
        `ValueError`."""
        assume(not value.strip().isdigit())
        with pytest.raises(ValueError) as exc:
            cli.check_positive_integer(name='test', value=value)
        assert 'should be an integer' in exc.value.args[0]


class TestColorParsing(object):
    """Unit tests for `parse_color_input`."""

    @pytest.mark.parametrize('string, expected', [
        # Simple examples to start with
        ('rgb(255, 255, 255)', (255, 255, 255)),
        ('rgb(1, 2, 3)', (1, 2, 3)),
        ('rgb(100, 200, 100)', (100, 200, 100)),

        # Mucking about with the case is okay
        ('RGB(1, 2, 3)', (1, 2, 3)),
        ('rGb(1, 2, 3)', (1, 2, 3)),
        ('RgB(1, 2, 3)', (1, 2, 3)),

        # As is varying the amount of whitespace
        ('rgb(1,2,3)', (1, 2, 3)),
        ('rgb(1,   2,   3)', (1, 2, 3)),
        ('rgb(1,2,   3)', (1, 2, 3)),

        # And leading zeroes
        ('rgb(01, 02, 03)', (1, 2, 3)),
        ('rgb(1, 2, 003)', (1, 2, 3)),
        ('rgb(0001, 002, 03)', (1, 2, 3)),
    ])
    def test_parsing_rgb_value(self, string, expected):
        """Test parsing RGB colour values."""
        assert cli.parse_color_input(string) == RGBColor(*expected)

    @given(st.integers(min_value=0, max_value=255),
           st.integers(min_value=0, max_value=255),
           st.integers(min_value=0, max_value=255))
    def test_parsing_constructed_rgb_value(self, red, green, blue):
        """Test parsing constructed RGB values."""
        string = 'rgb(%d, %d, %d)' % (red, green, blue)
        expected = RGBColor(red, green, blue)
        assert cli.parse_color_input(string) == expected

    @pytest.mark.parametrize('bad_string', [
        'rgb(256, 0, 0)',
        'rgb(0, 256, 0)',
        'rgb(0, 0, 256)',
        'rgb(1000, 100, 55)',
        'rgb(15, 200, 300)',
    ])
    def test_bad_rgb_components(self, bad_string):
        """An RGB colour component >255 is rejected with `ValueError`."""
        with pytest.raises(ValueError) as exc:
            cli.parse_color_input(bad_string)
        assert 'between 0 and 255' in exc.value.args[0]

    @given(st.text())
    def test_bad_rgb_string(self, bad_string):
        """Something that looks like an RGB colour but isn't is rejected
        with `ValueError`."""
        with pytest.raises(ValueError) as exc:
            cli.parse_color_input('rgb' + bad_string)
        assert 'Invalid RGB colour' in exc.value.args[0]
