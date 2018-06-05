#!/usr/bin/env python

"""
test_execute.py: Check whether phylo2owl.py can be executed in the current
environment.
"""

import libphylo2owl

def test_execute_phylo2owl_py():
    """Make sure we can execute phylo2owl.py."""

    # Can we execute phylo2owl.py?
    (return_code, stdout, stderr) = libphylo2owl.exec_phylo2owl(["--version"])
    assert return_code == 0
    assert stderr.startswith("phylo2owl.py ")
