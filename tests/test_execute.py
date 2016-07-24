#!/usr/bin/env python

"""execute.py: Check whether phylo2owl.py can be executed in the current 
environment."""

import subprocess

def exec_phylo2owl(cmdline=[], stdin=""):
    """Send those command line arguments to phylo2owl.py.
    Returns: (exitcode, output, error)
    """
    starts_with = ["python", "phylo2owl.py"]

    # Based on http://stackoverflow.com/a/1996540/27310
    p = subprocess.Popen(starts_with + cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(stdin)
    return (p.returncode, stdout, stderr)

def test_execute():
    """Make sure we can execute phylo2owl.py."""

    # Can we execute phylo2owl.py?
    (rc, stdout, stderr) = exec_phylo2owl(["--version"])
    assert rc == 0
    assert stderr.startswith("phylo2owl.py ")
