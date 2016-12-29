#!/usr/bin/env python

"""libshacl.py: Library of functions for communicating with the SHACL Java executable."""

import os
import rdflib
import subprocess
import xml.sax

def exec_testShacl(cmdline=[], stdin=""):
    """Send those command line arguments to testShacl.class.
    Returns: (exitcode, output, error)
    """

    # We need to add JENAHOME to the classpath so testShacl can find
    # the JENA library.
    environment = os.environ

    starts_with = ["java", "-jar", "target/testShacl-0.1-SNAPSHOT.jar"]

    # Based on http://stackoverflow.com/a/1996540/27310
    print starts_with
    print cmdline
    p = subprocess.Popen(starts_with + cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=environment, cwd="tests/shacl")
    stdout, stderr = p.communicate(stdin)
    print stdout
    print stderr
    return (p.returncode, stdout, stderr)

def validateShacl(shapePath, owlPath, expect_valid=True):
    """Validate a shape against an OWL ontology representation of a tree.
        - expect_valid: if True, that means we're expecting a success; if 
            False, that means that the OWL file is incorrect and we're 
            expecting a failure.
    """
    (rc, stdout, stderr) = exec_testShacl([shapePath, owlPath])
    assert rc == (0 if expect_valid else 1)

    # stdout should always be a Turtle document.
    graph = rdflib.Graph()
    try:
        graph.parse(format='turtle', data=stdout)
    except xml.sax.SAXParseException as e:
        print "SAXParseException parsing '{0}': {1}".format(tree, e)
        assert False

    # There should be no triples.
    if expect_valid:
        assert len(graph) == 0
    else:
        assert len(graph) > 0
