#!/usr/bin/env python

"""test_shacl.py: Test generated ontologies against SHACL shapes."""

import os
import fnmatch
import rdflib
import subprocess
import xml.sax
import libshacl

def test_execute():
    """Make sure we can execute testShacl."""

    # Can we execute testShacl at all?
    (rc, stdout, stderr) = libshacl.exec_testShacl(["--version"])
    assert rc == 0
    assert stderr.startswith("testShacl ")

    # Test all the example trees against ValidationShapes.
    examples_dir = "examples/trees"

    count_owl = 0
    count_shacl = 0
    for file_owl in os.listdir(examples_dir):
        if fnmatch.fnmatch(file_owl, "*.owl"):
            path_owl = examples_dir + "/" + file_owl
            path_shacl = examples_dir + "/" + file_owl[:-3] + "shacl.ttl"

            print "Validating " + path_owl + " against shacl/NodeShape.ttl"
            libshacl.validateShacl("../shapes/NodeShape.ttl", "../" + path_owl)
            count_owl += 1

            if os.path.isfile(path_shacl): 
                print "Validating " + path_owl + " against its custom SHACL file, " + path_shacl
                libshacl.validateShacl("../" + path_shacl, "../" + path_owl)
                count_shacl += 1
    
    assert count_owl > 0
    assert count_shacl > 0

