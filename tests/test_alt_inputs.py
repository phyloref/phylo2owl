#!/usr/bin/env python

"""test_alt_inputs.py: Test whether phylo2owl supports 
multiple input types, including NEXUS and NexML. All
of these file types should return exactly the same
RDF/XML output.
"""

from test_execute import exec_phylo2owl
import rdflib
import xml.sax

def compare_example_file(basename, ext, input_type):
    """ For a given basename, run the corresponding Newick 
    file (basename + ext with type input_type) through phylo2owl, 
    and see if its identical to the corresponding OWL file (basename + ".owl")
    """
    (rc, stdout, stderr) = exec_phylo2owl([basename + ext, "--format", input_type])
    print(stderr)
    assert rc == 0
    
    with open(basename + ".owl") as f:
        expected_output = f.read()

    assert expected_output == stdout

def test_example_files():
    """ List of pre-converted example files to test. """
    compare_example_file("examples/trees/pg_2357", ".tre", "newick")
    compare_example_file("examples/trees/pg_2357", ".nex", "NEXUS")
    compare_example_file("examples/trees/pg_2357", ".nexml", "NeXML")
