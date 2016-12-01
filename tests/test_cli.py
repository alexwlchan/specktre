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
        assert cli.parse_color_input(string) == expected

    @given(st.text())
    def test_bad_length_strings(self, string):
        """Strings that are too long or too short are rejected with `ValueError`."""
        assume(not string.startswith('#'))
        assume(len(string) != 6)
        with pytest.raises(ValueError) as exc:
            cli.parse_color_input(string)
        assert 'six hexadecimal digits' in exc.value.args[0]

    @given(st.text(min_size=6, max_size=6))
    def test_bad_hex_strings(self, string):
        """Strings that contain non-hex characters are rejected with
        `ValueError`."""
        # This can be false on 'interesting' Unicode strings
        assume(len(string) == 6)
        with open('awlc.txt', 'a', encoding='utf-8') as f:
            f.write('%s %d\n' % (string, len(string)))
            f.write('%s %d\n' % (string.lower(), len(string.lower())))

        assume(not string.startswith('#'))
        assume(any(x not in '0123456789abcdef' for x in string.lower()))
        with pytest.raises(ValueError) as exc:
            cli.parse_color_input(string)
        assert 'only contain hex characters' in exc.value.args[0]

    @given(st.text())
    def test_bad_color_strings(self, string):
        """Parsing a color string either raises a `ValueError` or returns
        an RGBColor instance."""
        try:
            color = cli.parse_color_input(string)
            assert isinstance(color, RGBColor)
        except ValueError:
            assert True
