#!/usr/bin/env python

"""test_shacl.py: Test generated ontologies against SHACL shapes."""

import os
import libshacl

def test_execute_testShacl():
    """ Can we execute testShacl at all? """
    (rc, stdout, stderr) = libshacl.exec_testShacl(["--version"])
    print stdout
    print stderr
    assert rc == 0
    assert stdout.startswith("testShacl ")

def test_execute(path_owl):
    """ Execute testShacl on every OWL file against NodeShape.ttl, and -- if
    they have a corresponding shacl.ttl file -- that as well. """

    path_shacl = path_owl[:-3] + "shacl.ttl"

    print "Validating {0} against shacl/NodeShape.ttl".format(path_owl)
    libshacl.validateShacl("tests/shapes/NodeShape.ttl", path_owl)

    if os.path.isfile(path_shacl): 
        print "Validating {0} against its custom SHACL file, {1}".format(path_owl, path_shacl)
        libshacl.validateShacl(path_shacl, path_owl)
