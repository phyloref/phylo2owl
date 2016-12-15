#!/usr/bin/env python

"""test_shacl.py: Test generated ontologies against SHACL shapes."""

import os
import rdflib
import subprocess
import xml.sax
from libshacl import exec_testShacl, validateShacl

def test_execute():
    """Make sure we can execute testShacl."""

    # Can we execute testShacl at all?
    (rc, stdout, stderr) = exec_testShacl(["--version"])
    assert rc == 0
    assert stderr.startswith("testShacl ")

    # Test all the example trees against ValidationShapes.
    validateShacl("../ValidationShapes.ttl", "../../examples/trees/pg_2357.owl")

    # Test each tree against its customized validation.
    validateShacl("../../examples/trees/pg_2357.shacl.ttl", "../../examples/trees/pg_2357.owl")

