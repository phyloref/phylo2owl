#!/usr/bin/env python

"""
test_owl_output.py: Produces OWL output from phylo2owl.py and test:
    (1) If they are identical to the pre-generated OWL output we have, and
    (2) whether it is valid XML and sensible RDF/XML.
"""

import libphylo2owl
import rdflib
import os
import xml.sax
import pytest

def test_simple_owl():
    """ Test if we can convert a simple phylogeny into an OWL representation."""
    validate_owl_output("((A, B), C);")

def test_example_files(path_tre):
    """ 
    For every Newick file, convert it into an OWL file and test whether
    it is identical to the pre-generated OWL file we have.
    """

    path_owl = path_tre[:-3] + "owl"

    if os.path.isfile(path_owl):
        print "Converting '{0}' to '{1}' using phylo2owl.".format(path_tre, path_owl)
        (rc, stdout, stderr) = libphylo2owl.exec_phylo2owl([path_tre])
        assert rc == 0
     
        with open(path_owl) as f:
            expected_output = f.read()

        assert expected_output == stdout

def test_validate_owl_output(path_tre):
    path_owl = path_tre[:-3] + "owl"

    if os.path.isfile(path_owl):
        print "Validating OWL output from phylo2owl."
        with open(path_tre) as f:
            tree = f.read()

        validate_owl_output(tree)

def validate_owl_output(tree):
    """ Use an RDF library to make sure that phylo2owl is emitting
    sensible, well-formed RDF/XML. """
    (rc, stdout, stderr) = libphylo2owl.exec_phylo2owl(["--name", "test"], tree)
    print stderr
    assert rc == 0

    # output should now be valid OWL output!
    graph = rdflib.Graph()
    try:
        graph.parse(format='xml', data=stdout)
    except xml.sax.SAXParseException as e:
        print "SAXParseException parsing '{0}': {1}".format(tree, e)
        assert False

    for s, p, o in graph:
        print "{0}\t{1}\t{2}".format(s, p, o)

