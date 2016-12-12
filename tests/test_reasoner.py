#!/usr/bin/env python

"""
test_reasoner.py: Test phyloreferences against reasoner.
"""

from libreasoner import validateWithReasoner

def test_phylorefs_using_reasoner(path_owl):
    """ Validate tree against its phyloreferences. """

    path_phylorefs = path_owl[:-3] + "phylorefs.omn"

    validateWithReasoner(path_owl, path_phylorefs)

