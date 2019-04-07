#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Unit tests for specktre.cli."""

import pytest
from hypothesis import strategies as st
from hypothesis import assume, given

from specktre import cli
from specktre.colors import RGBColor
from specktre.tilings import (
    generate_hexagons,
    generate_squares,
    generate_triangles
)


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
        assume(not all(c in '-0123456789 ' for c in value))
        with pytest.raises(ValueError) as exc:
            cli.check_positive_integer(name='test', value=value)
        assert 'should be an integer' in exc.value.args[0]


class TestColorParsing(object):
    """Unit tests for `check_color_input`."""

    @given(
        red=st.integers(min_value=0, max_value=255),
        green=st.integers(min_value=0, max_value=255),
        blue=st.integers(min_value=0, max_value=255),
    )
    @pytest.mark.parametrize('leading_hash', [True, False])
    @pytest.mark.parametrize('uppercase', [True, False])
    def test_parsing_hex_string(self, red, green, blue,
                                leading_hash, uppercase):
        """Parsing a color string returns the correct value."""
        string = '%02x%02x%02x' % (red, green, blue)
        if leading_hash:
            string = '#' + string
        if uppercase:
            string = string.upper()
        expected = RGBColor(red, green, blue)
        assert cli.check_color_input(string) == expected

    @given(st.text())
    def test_bad_length_strings(self, string):
        """Strings that are too long or too short are rejected with
        `ValueError`."""
        assume(not string.startswith('#'))
        assume(len(string) != 6)
        with pytest.raises(ValueError) as exc:
            cli.check_color_input(string)
        assert 'six hexadecimal digits' in exc.value.args[0]

    @given(st.text(min_size=6, max_size=6))
    def test_bad_hex_strings(self, string):
        """Strings that contain non-hex characters are rejected with
        `ValueError`."""
        assume(len(string.lower()) == 6)
        assume(not string.startswith('#'))
        assume(any(x not in '0123456789abcdef' for x in string.lower()))
        with pytest.raises(ValueError) as exc:
            cli.check_color_input(string)
        assert 'only contain hex characters' in exc.value.args[0]

    @given(st.text())
    def test_bad_color_strings(self, string):
        """Parsing a color string either raises a `ValueError` or returns an
        RGBColor instance."""
        try:
            color = cli.check_color_input(string)
            assert isinstance(color, RGBColor)
        except ValueError:
            assert True


class TestArgParsing:

    def test_default_generator_is_squares(self):
        settings = cli.parse_args([
            "new", "--size", "10x10", "--start", "000000", "--end", "000000"
        ])
        assert settings.generator == generate_squares

    def test_selects_squares(self):
        settings = cli.parse_args([
            "new", "--squares",
            "--size", "10x10", "--start", "000000", "--end", "000000"
        ])
        assert settings.generator == generate_squares

    def test_selects_hexagons(self):
        settings = cli.parse_args([
            "new", "--hexagons",
            "--size", "10x10", "--start", "000000", "--end", "000000"
        ])
        assert settings.generator == generate_hexagons

    def test_selects_triangles(self):
        settings = cli.parse_args([
            "new", "--triangles",
            "--size", "10x10", "--start", "000000", "--end", "000000"
        ])
        assert settings.generator == generate_triangles

    @pytest.mark.parametrize("bad_size", ["10x", "x10", "x", "1y1"])
    def test_invalid_size_is_systemexit(self, bad_size):
        with pytest.raises(SystemExit, match="size should be in the form WxH"):
            cli.parse_args([
                "new", "--size", bad_size,
                "--start", "000000", "--end", "000000"
            ])
