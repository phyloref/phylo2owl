#!/usr/bin/env python

"""
libreasoner.py: Library of functions for communicating with the Reasoner Java executable.
"""

import os
import subprocess
import xml.sax
import rdflib
from rdflib.namespace import RDF

def exec_reasoner(cmdline=None, stdin=""):
    """Send those command line arguments to reasoner.class.
    Returns: (exitcode, output, error)
    """

    cmdline = cmdline or [] # Use provided command line or an empty array
    environment = os.environ

    starts_with = ["java", "-jar", "tests/reasoner/target/reasoner-0.1-SNAPSHOT.jar"]

    # Based on http://stackoverflow.com/a/1996540/27310
    print starts_with
    print cmdline
    process = subprocess.Popen(
        starts_with + cmdline,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=environment)
    stdout, stderr = process.communicate(stdin)
    # print stdout
    print stderr
    return (process.returncode, stdout, stderr)

def validate_with_reasoner(tree_path, phyloref_path):
    """ Run the reasoner over the treePath and the phylorefPath, and
    then check to see if every class named 'X_expected' has the same
    set of individuals as 'X'.
        - treePath: The path to the tree, as OWL
        - phylorefPath: The path to the phyloreference, in Manchester syntax
        - expect_valid: if True, that means we're expecting a success; if
            False, that means that the OWL file is incorrect and we're
            expecting a failure.
    """
    (return_code, stdout, stderr) = exec_reasoner([tree_path, phyloref_path])
    assert return_code == 0

    # stdout should always be an ntriples document.
    graph = rdflib.Graph()
    try:
        graph.parse(format='n3', data=stdout)
    except xml.sax.SAXParseException as exception:
        print "SAXParseException parsing '{0}': {1}".format(stdout, exception)
        assert False

    # Identify all '_expected' classes, which we can test.
    all_classes = set(graph.objects(None, RDF.type))
    expected_classes = [cls for cls in all_classes if cls.endswith(u'_expected')]

    # Make sure we have at least one expected class.
    assert expected_classes, "Must have at least one expected class"

    # Running these tests are time-consuming, so it's best if we test all
    # expected classes, then report an overall success or failure. Details
    # go to stdout, which py.test captures.
    tests_failed = False
    for expected_class in expected_classes:
        test_succeeded = True

        # For every 'X_expected' class, identify the 'X' class with
        # observed values.
        observed_class = rdflib.URIRef(expected_class[:-9])

        # Obtain the list (not the set!) of all individuals belonging
        # to these two classes.
        expected_individuals = sorted(list(graph.subjects(RDF.type, expected_class)))
        observed_individuals = sorted(list(graph.subjects(RDF.type, observed_class)))

        # For debugging, write out the two lists.
        print "Comparing classes '%s' and '%s'." % (expected_class, observed_class)

        # Make sure neither class is empty
        if not expected_individuals:
            print " - TEST FAILED: expected class is empty."
            test_succeeded = False

        if not observed_individuals:
            print " - TEST FAILED: observed class is empty."
            test_succeeded = False

        # Test that these two lists are identical.
        if len(expected_individuals) != len(observed_individuals):
            print " - TEST FAILED: " \
                + "expected and observed classes have different numbers of individuals."
            test_succeeded = False
        else:
            for index, expected in enumerate(expected_individuals):
                observed = observed_individuals[index]

                if expected != observed:
                    print " - TEST FAILED: at index {0}, expected '{1}', observed '{2}'".format(
                        index, expected, observed
                    )
                    test_succeeded = False

        # If the test failed, list all individuals.
        if test_succeeded:
            print " - Test succeeded."
        else:
            tests_failed = True
            print " - " + expected_class + ":\n   - " + "\n   - ".join(expected_individuals)
            print " - " + observed_class + ":\n   - " + "\n   - ".join(observed_individuals)

        # Insert a newline before the next test.
        print ""

    if tests_failed:
        assert False, "See output for details."
