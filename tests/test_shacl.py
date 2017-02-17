#!/usr/bin/env python

"""test_shacl.py: Test generated ontologies against SHACL shapes."""

import os
import libshacl
import pytest

def test_execute_testShacl():
    """ Can we execute testShacl at all? """
    (rc, stdout, stderr) = libshacl.exec_testShacl(["--version"])
    print stdout
    print stderr
    assert rc == 0
    assert stdout.startswith("testShacl ")

def test_validate_shacl_against_nodeshape(path_owl):
    """ Execute testShacl on every OWL file against NodeShape.ttl. """

    path_shacl = path_owl[:-3] + "shacl.ttl"

    libshacl.validateShacl("tests/shapes/NodeShape.ttl", path_owl)

def test_validate_shacl_against_custom_shacl(path_owl):
    """ Execute testShacl on the corresponding shacl.ttl file, if one exists. """

    path_shacl = path_owl[:-3] + "shacl.ttl"

    if os.path.isfile(path_shacl): 
        print "Validating {0} against its custom SHACL file, {1}".format(path_owl, path_shacl)
        libshacl.validateShacl(path_shacl, path_owl)
    else:
        pytest.skip("OWL file '{0}' doesn't have a custom SHACL file to test at '{1}'".format(
            path_owl,
            path_shacl
        ))
