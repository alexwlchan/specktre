#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Unit tests for specktre.tilings."""

import math

import pytest

from specktre.tilings import (generate_hexagons, generate_squares,
                              generate_triangles, generate_unit_hexagons,
                              generate_unit_squares, generate_unit_triangles)


def distance(x, y):
    """Return the distance between two points in 2D space."""
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)


@pytest.mark.parametrize('generator, vertex_count', [
    (generate_hexagons, 6),
    (generate_unit_hexagons, 6),
    (generate_squares, 4),
    (generate_unit_squares, 4),
    (generate_triangles, 3),
    (generate_unit_triangles, 3),
])
def test_vertex_count_is_correct(self, generator, vertex_count):
    """Each generator produces the correct number of vertices for each tile."""
    for coords in generator(100, 100):
        assert len(coords) == vertex_count


@pytest.mark.parametrize('generator', [
    generate_unit_hexagons,
    generate_unit_squares,
    generate_unit_triangles,
])
def test_side_length_of_unit_coords(self, generator):
    """The side lengths of the shapes produced by the unit shape generators are
    approximately 1."""
    for coords in generator(100, 100):
        for x, y in zip(coords, coords[1:] + [coords[0]]):
            assert distance(x, y) == pytest.approx(1.0)
