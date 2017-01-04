#!/usr/bin/env python

"""test_owl_output.py: Produces output from phylo2owl.py and tests whether its
valid XML, sensible RDF/XML and OWL.
"""

import os
import fnmatch
from test_execute import exec_phylo2owl
import rdflib
import xml.sax

def compare_example_file(path_tre, path_owl):
    """ For a given basename, run the corresponding Newick file (path_tre)
    through phylo2owl, and see if its identical to the corresponding OWL file
    (path_owl).
    """
    (rc, stdout, stderr) = exec_phylo2owl([path_tre])
    assert rc == 0
 
    with open(path_owl) as f:
        expected_output = f.read()

    assert expected_output == stdout

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

def validate_owl_output_from_file(filename):
    """ Read a tree from a file and validate the OWL that phylo2owl 
    produces. """
    tree = ""
    with open(filename) as f:
        tree = f.read()

    validate_owl_output(tree)

def test_example_files():
    """ List of pre-converted example files to test. """

    examples_dir = "examples/trees";

    count = 0
    for file_tre in os.listdir(examples_dir):
        if fnmatch.fnmatch(file_tre, "*.tre"): 
            path_tre = examples_dir + "/" + file_tre
            path_owl = examples_dir + "/" + file_tre[:-3] + "owl"

            if os.path.isfile(path_owl):
                print "Converting " + path_tre + " to " + path_owl + " using phylo2owl."
                compare_example_file(path_tre, path_owl)
                count += 1

    assert count > 0

def test_validate_owl_output():
    """ List of trees to parse. """
    validate_owl_output("((A, B), C);")

    examples_dir = "examples/trees";

    count = 0
    for file_tre in os.listdir(examples_dir):
        if fnmatch.fnmatch(file_tre, "*.tre"):
            path_tre = examples_dir + "/" + file_tre
            path_owl = examples_dir + "/" + file_tre[:-3] + "owl"

            if os.path.isfile(path_owl):
                print "Validating OWL output from phylo2owl."
                validate_owl_output_from_file("examples/trees/pg_2357.tre")
                count += 1

    assert count > 0
