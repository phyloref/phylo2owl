#!/usr/bin/env python

"""test_shacl.py: Test generated ontologies against SHACL shapes."""

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

    # Figure out the classpath.
    if 'JENAHOME' in environment:
        # Include environment['JENAHOME']/libexec in the classpath.
        classpath = ["shacl-0.0.1-SNAPSHOT.jar", environment['JENAHOME'] + '/libexec/lib/*', "."]
    else:
        # Assume that Jena is already in the classpath
        classpath = ["shacl-0.0.1-SNAPSHOT.jar", "."]

    if 'CLASSPATH' in environment:
        classpath = classpath + environment['CLASSPATH']

    starts_with = ["java", "-cp", ":".join(classpath),  "testShacl"]

    # Based on http://stackoverflow.com/a/1996540/27310
    # print starts_with
    # print cmdline
    p = subprocess.Popen(starts_with + cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=environment, cwd="tests/java")
    stdout, stderr = p.communicate(stdin)
    print stdout
    print stderr
    return (p.returncode, stdout, stderr)

def test_execute():
    """Make sure we can execute testShacl."""

    # Can we execute testShacl at all?
    (rc, stdout, stderr) = exec_testShacl(["--version"])
    assert rc == 0
    assert stderr.startswith("testShacl ")

    # Test all the example trees against ValidationShapes.
    (rc, stdout, stderr) = exec_testShacl(["../ValidationShapes.ttl", "../../examples/trees/pg_2357.owl"])
    assert rc == 0

    # stdout should always be a Turtle document.
    graph = rdflib.Graph()
    try:
        graph.parse(format='turtle', data=stdout)
    except xml.sax.SAXParseException as e:
        print "SAXParseException parsing '{0}': {1}".format(tree, e)
        assert False

    # There should be no triples.
    assert len(graph) == 0
        

