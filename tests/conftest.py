"""
conftest.py: Sets up some fixures to simplify test writing. 
"""

import pytest
import os
import fnmatch

examples_dir = "examples/trees"

def pytest_namespace():
    """ Set some global pytest variables, accessible as e.g. pytest.basedir """
    return {
        'basedir': examples_dir + '/'
    }

def pytest_generate_tests(metafunc):
    """ Add hooks for tests with parameters 'path_tre' or 'path_owl'. """

    # If a test contains 'path_tre', parametrize() each filename so that
    # each tested file appears in the logs.
    if 'path_tre' in metafunc.fixturenames:
        metafunc.parametrize('path_tre', paths_tre())
    
    # If a test contains 'path_owl', parametrize() each filename so that
    # each tested file appears in the logs.
    if 'path_owl' in metafunc.fixturenames:
        metafunc.parametrize('path_owl', paths_owl())

@pytest.fixture(scope="module")
def paths_tre():
    """ If a test contains 'paths_tre', it becomes a list of Newick files. """

    paths_tre = []
    for file_tre in os.listdir(examples_dir):
        if fnmatch.fnmatch(file_tre, "*.tre"):
            path_tre = examples_dir + "/" + file_tre
            paths_tre.append(path_tre)

    return paths_tre

@pytest.fixture(scope="module")
def paths_owl():
    """ If a test contains 'paths_owl', it becomes a list of OWL files. """

    paths_owl = []
    for file_owl in os.listdir(examples_dir):
        if fnmatch.fnmatch(file_owl, "*.owl"):
            path_owl = examples_dir + "/" + file_owl
            paths_owl.append(path_owl)
    
    return paths_owl
