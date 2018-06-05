#!/usr/bin/env python

"""
test_owl_output.py: Produces OWL output from phylo2owl.py and test:
    (1) If they are identical to the pre-generated OWL output we have, and
    (2) whether it is valid XML and sensible RDF/XML.
"""

import os
import xml.sax
import rdflib
import pytest
import libphylo2owl

def test_simple_phylogeny():
    """ Test if we can convert a simple phylogeny into an OWL representation."""
    validate_tree_output_as_rdfxml("((A, B), C);")

def test_produced_owl_files(path_tre):
    """
    For every Newick file, convert it into an OWL file and test whether
    it is identical to the pre-generated OWL file we have.
    """

    path_owl = path_tre[:-3] + "owl"

    if os.path.isfile(path_owl):
        print "Converting '{0}' to '{1}' using phylo2owl.".format(path_tre, path_owl)
        (return_code, stdout, stderr) = libphylo2owl.exec_phylo2owl([path_tre])
        assert return_code == 0

        with open(path_owl) as fil:
            expected_output = fil.read()

        assert expected_output == stdout
    else:
        pytest.skip(
            "Newick file '{0}' doesn't have a corresponding OWL file to test at '{1}'".format(
                path_tre,
                path_owl
            ))

def test_output_is_valid_rdfxml(path_tre):
    """ Test whether the OWL output produced by phylo2owl.py is valid RDF/XML """

    print "Validating OWL output from phylo2owl."
    with open(path_tre) as fil:
        tree = fil.read()

    validate_tree_output_as_rdfxml(tree)

def validate_tree_output_as_rdfxml(tree_content):
    """ Use an RDF library to make sure that phylo2owl emits well-formed RDF/XML
    for a given phylogeny."""
    (return_code, stdout, stderr) = libphylo2owl.exec_phylo2owl(["--name", "test"], tree_content)
    print stderr
    assert return_code == 0

    # output should now be valid OWL output!
    graph = rdflib.Graph()
    try:
        graph.parse(format='xml', data=stdout)
    except xml.sax.SAXParseException as exception:
        print "SAXParseException parsing '{0}': {1}".format(stdout, exception)
        assert False

    for subject, predicate, obj in graph:
        print "{0}\t{1}\t{2}".format(subject, predicate, obj)
