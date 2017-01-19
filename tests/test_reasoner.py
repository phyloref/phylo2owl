#!/usr/bin/env python

"""test_reasoner.py: Test phyloreferences against reasoner."""

import os
import libreasoner
import pytest

def test_execute(path_owl):
    """ Validate a tree against its phyloreferences. """
    path_phylorefs = path_owl[:-4] + '.phylorefs.omn'
    if os.path.isfile(path_phylorefs):
        libreasoner.validateWithReasoner(path_owl, path_phylorefs)
    else:
        pytest.skip("OWL file '{0}' doesn't have a corresponding phylorefs file '{1}'".format(
            path_owl,
            path_phylorefs
        ))

