# -*- encoding: utf-8 -*-
"""Utility functions."""

import os
import random
import string


def _candidate_filenames():
    """Generates filenames of the form 'specktre_123AB.png'.

    The random noise is five characters long, which allows for
    62^5 = 916 million possible filenames.

    """
    while True:
        random_stub = ''.join([
            random.choice(string.ascii_letters + string.digits)
            for _ in range(5)
        ])
        yield 'specktre_%s.png' % random_stub


def new_filename():
    """Returns a filename for a new specktre image.

    This filename is of the form 'specktre_123AB.png' and does not
    already exist when this function is called.

    """
    for filename in _candidate_filenames():
        if not os.path.exists(filename):
            return filename

    # Since _candidate_filenames() is an infinite generator and produces
    # millions of options, this branch should never be hit in practice.
    # Keeps coverage happy.
    else:
        assert False, 'Should not be reachable'
