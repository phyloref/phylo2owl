#!/usr/bin/env python

"""
libshacl.py: Library of functions for communicating with the SHACL Java
executable.
"""

import subprocess
import xml.sax
import rdflib

def exec_test_shacl(args):
    """
    Execute testShacl.jar with the provided command line arguments (args).
    Returns: (exitcode, stdout_as_string, stderr_as_string)

    Based on http://stackoverflow.com/a/1996540/27310
    """

    shacl_exec = ["java", "-jar", "tests/shacl/target/testShacl-0.1-SNAPSHOT.jar"]
    process = subprocess.Popen(
        shacl_exec + args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    if process.returncode == 1 and "Unable to access jarfile" in stderr:
        raise RuntimeError("Could not execute " + ' '.join(shacl_exec))
    return (process.returncode, stdout, stderr)

def validate_shacl(shape_path, owl_path, expect_valid=True):
    """
    Validate a shape file against an OWL ontology representation of a tree.
        - shapePath: the path to the shape file to validate
        - owlPath: the path to the OWL file to validate
        - expect_valid: if True, that means we're expecting a success; if
          False, that means that the OWL file is incorrect and we're
          expecting a failure.

    Uses assert() statements for its tests, so it's designed to be used
    within py.test or a similar framework.
    """
    (return_code, stdout, stderr) = exec_test_shacl([shape_path, owl_path])
    print stdout
    print stderr
    assert return_code == (0 if expect_valid else 1)

    # stdout should always be a Turtle document.
    graph = rdflib.Graph()
    try:
        graph.parse(format='turtle', data=stdout)
    except xml.sax.SAXParseException as exception:
        print "SAXParseException parsing '{0}': {1}".format(stdout, exception)
        assert False

    # There should be no triples if it's valid; otherwise, there will be some.
    if expect_valid:
        assert not graph, "Validating with Shacl should produce empty output"
    else:
        assert graph, "Validating with Shacl should find errors"
