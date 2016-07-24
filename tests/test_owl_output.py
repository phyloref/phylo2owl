#!/usr/bin/env python

"""test_owl_output.py: Produces output from phylo2owl.py and tests whether its"""

from test_execute import exec_phylo2owl
import rdflib
import xml.sax

def compare_example_file(basename):
    """ For a given basename, run the corresponding Newick file (basename + ".tre")
    through phylo2owl, and see if its identical to the corresponding OWL file
    (basename + ".owl")
    """
    (rc, stdout, stderr) = exec_phylo2owl([basename + ".tre"])
    assert rc == 0
    
    with open(basename + ".owl") as f:
        expected_output = f.read()

    assert expected_output == stdout

def test_example_files():
    """ List of pre-converted example files to test. """
    compare_example_file("examples/trees/pg_2357")

def validate_owl_output(tree):
    """ Use an RDF library to make sure that phylo2owl is emitting
    sensible, well-formed RDF/XML. """
    (rc, stdout, stderr) = exec_phylo2owl(["--name", "test"], tree)
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

    # TODO: This gives us an RDF triplestore to work with, which we now
    # need to validate against OWL (or make sure that the right statements
    # are being generated).

def validate_owl_output_from_file(filename):
    """ Read a tree from a file and validate the OWL that phylo2owl produces. """
    tree = ""
    with open(filename) as f:
        tree = f.read()

    validate_owl_output(tree)

def test_validate_owl_output():
    """ List of trees to parse. """
    validate_owl_output("((A, B), C);")
    validate_owl_output_from_file("examples/trees/pg_2357.tre")
