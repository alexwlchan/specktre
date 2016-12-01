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

    @given(red=st.integers(min_value=0, max_value=255),
           green=st.integers(min_value=0, max_value=255),
           blue=st.integers(min_value=0, max_value=255))
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

    @pytest.mark.parametrize('string, expected', [
        # Simple examples to start with
        ('hsl(0, 100, 100)', (255, 255, 255)),
        ('hsl(360, 100, 100)', (255, 255, 255)),
        ('hsl(25, 100, 41)', (209, 87, 0)),
        ('hsl(123, 100, 50)', (0, 255, 12)),

        # Mucking about with the case is okay
        ('HSL(0, 100, 100)', (255, 255, 255)),
        ('hSl(0, 100, 100)', (255, 255, 255)),
        ('HsL(0, 100, 100)', (255, 255, 255)),

        # As is varying the amount of whitespace
        ('hsl(151,100,50)', (0, 255, 131)),
        ('hsl(151,   100,   50)', (0, 255, 131)),
        ('hsl(151,100,    50)', (0, 255, 131)),

        # And percentage signs on saturation/lightness
        ('hsl(126, 100%, 50)', (0, 255, 25)),
        ('hsl(126, 100, 50%)', (0, 255, 25)),
        ('hsl(126, 100%, 50%)', (0, 255, 25)),
    ])
    def test_parsing_hsl_value(self, string, expected):
        """Test parsing HSL colour values."""
        assert cli.parse_color_input(string) == RGBColor(*expected)

    @given(hue=st.integers(min_value=0, max_value=255),
           saturation=st.integers(min_value=0, max_value=100),
           lightness=st.integers(min_value=0, max_value=100))
    def test_parsing_constructed_hsl_value(self, hue, saturation, lightness):
        """Test parsing constructed HSL values doesn't crash."""
        string = 'hsl(%d, %d, %d)' % (hue, saturation, lightness)
        cli.parse_color_input(string)

    @pytest.mark.parametrize('bad_string', [
        'hsl(361, 0, 0)',
        'hsl(400, 0, 0)',
        'hsl(1000, 0, 0)',
    ])
    def test_bad_hsl_hue(self, bad_string):
        """An HSL with hue >360 is rejected with `ValueError`."""
        with pytest.raises(ValueError) as exc:
            cli.parse_color_input(bad_string)
        assert 'Hue should be between 0 and 360' in exc.value.args[0]

    @pytest.mark.parametrize('bad_string', [
        'hsl(0, 101, 0)',
        'hsl(0, 200, 0)',
        'hsl(0, 364, 0)',
    ])
    def test_bad_hsl_saturation(self, bad_string):
        """An HSL with saturation >100 is rejected with `ValueError`."""
        with pytest.raises(ValueError) as exc:
            cli.parse_color_input(bad_string)
        assert 'Saturation should be between 0 and 100' in exc.value.args[0]

    @pytest.mark.parametrize('bad_string', [
        'hsl(0, 0, 101)',
        'hsl(0, 0, 200)',
        'hsl(0, 0, 364)',
    ])
    def test_bad_hsl_lightness(self, bad_string):
        """An HSL with lightness >100 is rejected with `ValueError`."""
        with pytest.raises(ValueError) as exc:
            cli.parse_color_input(bad_string)
        assert 'Lightness should be between 0 and 100' in exc.value.args[0]

    @given(st.text())
    def test_bad_rgb_string(self, bad_string):
        """Something that looks like an RGB colour but isn't is rejected
        with `ValueError`."""
        with pytest.raises(ValueError) as exc:
            cli.parse_color_input('rgb' + bad_string)
        assert 'Invalid RGB colour' in exc.value.args[0]

    @given(st.text())
    def test_bad_hsl_string(self, bad_string):
        """Something that looks like an HSL colour but isn't is rejected
        with `ValueError`."""
        with pytest.raises(ValueError) as exc:
            cli.parse_color_input('hsl' + bad_string)
        assert 'Invalid HSL colour' in exc.value.args[0]

    @given(st.text())
    def test_bad_color_strings(self, bad_string):
        """Test that any strings that don't look correct are rejected with
        `ValueError`."""
        assume(not bad_string.lower().strip().startswith(('rgb', 'hsl', '#')))
        with pytest.raises(ValueError) as exc:
            cli.parse_color_input(bad_string)
        assert 'Unrecognised colour:' in exc.value.args[0]
