#!/usr/bin/env python

"""test_reasoner.py: Test phyloreferences against reasoner."""

import os
import rdflib
import subprocess
import xml.sax
from libreasoner import validateWithReasoner

def test_execute():
    """ Validate one tree against its phyloreferences. """
    validateWithReasoner('../../examples/trees/pg_2357.owl', '../../examples/trees/pg_2357.phylorefs.omn')

