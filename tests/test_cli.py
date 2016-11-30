#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Unit tests for specktre.cli."""

from hypothesis import assume, given, strategies as st
import pytest

from specktre import cli


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
        assume(not value.isdigit())
        with pytest.raises(ValueError) as exc:
            cli.check_positive_integer(name='test', value=value)
        assert 'should be an integer' in exc.value.args[0]
