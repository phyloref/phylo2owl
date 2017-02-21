#!/usr/bin/env python

"""test_reasoner.py: Test phyloreferences against reasoner."""

import os
import rdflib
import subprocess
import xml.sax
from libreasoner import validateWithReasoner

def test_phylorefs_using_reasoner(path_owl):
    """ Validate tree against its phyloreferences. """

    path_phylorefs = path_owl[:-3] + "phylorefs.omn"

    validateWithReasoner(path_owl, path_phylorefs)

