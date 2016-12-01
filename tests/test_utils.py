#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Unit tests for specktre.utils."""

import os
import random

from specktre.utils import new_filename


def test_new_filename_always_gives_non_existent_file(tmpdir):
    """Calling `new_filename()` always returns a filename that doesn't exist
    yet."""
    old_dir = os.curdir
    tmpdir.chdir()

    seeds = list(range(10))

    for _ in range(100):
        # Re-seed random, so `new_filename()` will sometimes start by guessing
        # a filename it's already used.
        random.seed(random.choice(seeds))
        f = new_filename()
        assert not os.path.exists(f)
        open(f, 'w').write('')

    os.chdir(old_dir)
