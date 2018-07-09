#!/usr/bin/env python

"""
test_alt_inputs.py: Test whether phylo2owl supports multiple input types,
including NEXUS and NexML. All of these file types should return exactly the
same RDF/XML output.
"""

import os
import pytest
import libphylo2owl

def test_newick_convert_to_OWL(path_tre):
    """
    Test all .tre files by comparing them to the corresponding .owl file.
    """

    # This might seem redundant, but it tests that '--format newick' works.

    path_owl = path_tre[:-4] + '.owl'
    if os.path.isfile(path_tre):
        compare_example_file(path_tre, 'Newick', path_owl)
    else:
        pytest.skip("Newick file '{0}' does not have a comparable OWL file at {1}.".format(
            path_tre,
            path_owl
        ))

def test_nexus_convert_to_OWL(path_nex):
    """ Test all .nex files by comparing them to the corresponding .owl file. """

    path_owl = path_nex[:-4] + '.owl'
    if os.path.isfile(path_owl):
        compare_example_file(path_nex, 'NEXUS', path_owl)
    else:
        pytest.skip("Nexus file '{0}' does not have a comparable OWL file at {1}.".format(
            path_nex,
            path_owl
        ))

def test_nexml_convert_to_OWL(path_nexml):
    """ Test all .nexml files by comparing them to the corresponding .owl file. """

    path_owl = path_nexml[:-6] + '.owl'
    if os.path.isfile(path_owl):
        compare_example_file(path_nexml, 'NeXML', path_owl)
    else:
        pytest.skip("NeXML file '{0}' does not have a comparable OWL file at {1}.".format(
            path_nexml,
            path_owl
        ))

def compare_example_file(input_file, input_format, expected_output_file):
    """
    For a given input file and format, generate OWL output, and then compare
    it with the expected output file to make sure it's identical.
    """

    (return_code, stdout, stderr) = libphylo2owl.exec_phylo2owl(
        [
            input_file, "--format", input_format
        ])
    assert return_code == 0

    with open(expected_output_file) as fil:
        expected_output = fil.read()

    assert expected_output == stdout
