#!/usr/bin/env python

"""
test_shacl.py: Test generated ontologies against SHACL shapes.
"""

import os
import pytest
import libshacl

def test_execute_test_shacl():
    """ Can we execute testShacl at all? """
    (return_code, stdout, stderr) = libshacl.exec_test_shacl(["--version"])
    print stdout
    print stderr
    assert return_code == 0
    assert stdout.startswith("testShacl ")

def test_validate_shacl_shapes(path_owl):
    """ Execute testShacl on every OWL file against NodeShape.ttl. """

    # path_shacl = path_owl[:-3] + "shacl.ttl"

    libshacl.validate_shacl("tests/shapes/NodeShape.ttl", path_owl)

def test_validate_shacl_custom(path_owl):
    """ Execute testShacl on the corresponding shacl.ttl file, if one exists. """

    path_shacl = path_owl[:-3] + "shacl.ttl"

    if os.path.isfile(path_shacl):
        print "Validating {0} against its custom SHACL file, {1}".format(path_owl, path_shacl)
        libshacl.validate_shacl(path_shacl, path_owl)
    else:
        pytest.skip("OWL file '{0}' doesn't have a custom SHACL file to test at '{1}'".format(
            path_owl,
            path_shacl
        ))
