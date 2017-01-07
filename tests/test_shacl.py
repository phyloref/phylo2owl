#!/usr/bin/env python

"""test_shacl.py: Test generated ontologies against SHACL shapes."""

import os
import fnmatch
import rdflib
import subprocess
import xml.sax
import libshacl

def test_execute(paths_owl):
    """Make sure we can execute testShacl."""

    # Can we execute testShacl at all?
    (rc, stdout, stderr) = libshacl.exec_testShacl(["--version"])
    print stdout
    print stderr
    assert rc == 0
    assert stdout.startswith("testShacl ")

    # Test all the example trees against ValidationShapes.
    examples_dir = "examples/trees"

    count_owl = 0
    count_shacl = 0
    for path_owl in paths_owl:
        path_shacl = path_owl[:-3] + "shacl.ttl"

        print "Validating " + path_owl + " against shacl/NodeShape.ttl"
        libshacl.validateShacl("tests/shapes/NodeShape.ttl", path_owl)
        count_owl += 1

        if os.path.isfile(path_shacl): 
            print "Validating " + path_owl + " against its custom SHACL file, " + path_shacl
            libshacl.validateShacl(path_shacl, path_owl)
            count_shacl += 1
    
    assert count_owl > 0
    assert count_shacl > 0

