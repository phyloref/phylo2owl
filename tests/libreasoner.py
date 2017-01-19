#!/usr/bin/env python

"""libreasoner.py: Library of functions for communicating with the Reasoner Java executable."""

import os
import rdflib
import subprocess
import xml.sax
from rdflib.namespace import RDF

def exec_reasoner(cmdline=[], stdin=""):
    """Send those command line arguments to reasoner.class.
    Returns: (exitcode, output, error)
    """

    environment = os.environ

    starts_with = ["java", "-jar", "target/reasoner-0.1-SNAPSHOT.jar"]

    # Based on http://stackoverflow.com/a/1996540/27310
    print starts_with
    print cmdline
    p = subprocess.Popen(starts_with + cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=environment, cwd="tests/reasoner")
    stdout, stderr = p.communicate(stdin)
    # print stdout
    print stderr
    return (p.returncode, stdout, stderr)

def validateWithReasoner(treePath, phylorefPath):
    """ Run the reasoner over the treePath and the phylorefPath, and
    then check to see if every class named 'X_expected' has the same
    set of individuals as 'X'.
        - treePath: The path to the tree, as OWL
        - phylorefPath: The path to the phyloreference, in Manchester syntax
        - expect_valid: if True, that means we're expecting a success; if 
            False, that means that the OWL file is incorrect and we're 
            expecting a failure.
    """
    (rc, stdout, stderr) = exec_reasoner([treePath, phylorefPath])
    assert rc == 0

    # stdout should always be an ntriples document.
    graph = rdflib.Graph()
    try:
        graph.parse(format='n3', data=stdout)
    except xml.sax.SAXParseException as e:
        print "SAXParseException parsing '{0}': {1}".format(tree, e)
        assert False

    # Identify all '_expected' classes, which we can test.
    allClasses = set(graph.objects(None, RDF.type))
    expectedClasses = filter(lambda x: x.endswith(u'_expected'), allClasses)

    # Make sure we have at least one expected class.
    assert len(expectedClasses) > 0

    for cl in expectedClasses:
        # For every 'X_expected' class, identify the 'X' class with
        # observed values.
        expectedClass = cl
        observedClass = rdflib.URIRef(cl[:-9])

        # Obtain the list (not the set!) of all individuals belonging
        # to these two classes.
        expectedIndividuals = sorted(list(graph.subjects(RDF.type, expectedClass)))
        observedIndividuals = sorted(list(graph.subjects(RDF.type, observedClass)))

        # Make sure neither class is empty
        assert len(expectedIndividuals) > 0
        assert len(observedIndividuals) > 0
        
        # For debugging, write out the two lists.
        print "Comparing classes '%s' and '%s'." % (expectedClass, observedClass)
        print " - " + expectedClass + ":\n   - " + "\n   - ".join(expectedIndividuals)
        print " - " + observedClass + ":\n   - " + "\n   - ".join(observedIndividuals)

        # Test that these two lists are identical.
        assert len(expectedIndividuals) == len(observedIndividuals)
        assert expectedIndividuals == observedIndividuals

