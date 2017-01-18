#!/usr/bin/env python

"""
test_alt_inputs.py: Test whether phylo2owl supports multiple input types, 
including NEXUS and NexML. All of these file types should return exactly the 
same RDF/XML output.
"""

import libphylo2owl
import pytest

@pytest.mark.parametrize("input_file, input_format, expected_output_file", [
    ("pg_2357.tre", "newick", "pg_2357.owl"),
    ("pg_2357.nex", "NEXUS", "pg_2357.owl"),
    ("pg_2357.nexml", "NeXML", "pg_2357.owl")
])
def test_example_file(input_file, input_format, expected_output_file):
    """ 
    For a given input file and format, generate OWL output, and then compare
    it with the expected output file to make sure it's identical.
    """

    (rc, stdout, stderr) = libphylo2owl.exec_phylo2owl([
        pytest.basedir + input_file, 
        "--format", input_format
    ])
    assert rc == 0
    
    with open(pytest.basedir + expected_output_file) as f:
        expected_output = f.read()

    assert expected_output == stdout

