# Phyloreferencing Test Suite

## Usage
> py.test tests/

## Description
This test suite is designed to be used to validate the outputs of the `phylo2owl.py` script. It does this in two ways:

 1. By comparing an output file with its expected output, and reporting an error if they differ.
 2. By validating an output OWL file against a set of SHACL shapes.

You can examine [previous runs of this test suite](https://travis-ci.org/phyloref/phylo2owl) on Travis-CI.

## Test scripts

 - `conftest.py`: A py.test configuration file that sets up the fixtures.
 - `test_execute.py`: Test whether the `phylo2owl.py` script can be executed at all.
 - `test_alt_inputs.py`: Test whether alternate input formats (NEXUS and NeXML) produce the expected outputs.
 - `test_owl_output.py`: Test whether the OWL produced by `phylo2owl.py` is identical to the expected output, and whether it is syntactically correct RDF/XML.
 - `test_shacl.py`: Test whether every expected output OWL file can be validated against a generic Node shape, as well as any file-specific SHACL shapes that have been written.
 - `test_shacl_shapes.py`: A self-contained file that deliberately constructs phylogenies that should fail the generic Node shape, and then tests to make sure they actually do.
