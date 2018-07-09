"""
conftest.py: Sets up some fixures to simplify test writing.
"""

import os
import fnmatch

EXAMPLES_DIR = "examples/trees"

def pytest_namespace():
    """ Set some global pytest variables, accessible as e.g. pytest.basedir """
    return {
        'basedir': EXAMPLES_DIR + '/'
    }

def pytest_generate_tests(metafunc):
    """ Add hooks for tests that need a parametrized list of paths with a
    particular extension. """

    extensions = {
        'path_tre': 'tre',
        'path_owl': 'owl',
        'path_nex': 'nex',
        'path_nexml': 'nexml'
    }

    for key in extensions:
        if key in metafunc.fixturenames:
            metafunc.parametrize(key, paths_by_extension(extensions[key]))

def paths_by_extension(extension):
    """ Return a list of files in the examples directory that has a particular extension. """

    paths = []
    for filename in os.listdir(EXAMPLES_DIR):
        if fnmatch.fnmatch(filename, "*." + extension):
            paths.append(os.path.join(EXAMPLES_DIR, filename))

    return paths
