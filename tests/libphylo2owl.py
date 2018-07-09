#!/usr/bin/env python

"""
libphylo2owl.py: Library that provides a function to execute phylo2owl.py.
"""

import subprocess

def exec_phylo2owl(args=None, stdin=""):
    """
    Send those command line arguments to phylo2owl.py.
        - args: Command line arguments.
        - stdin: A string passed to phylo2owl.py on stdin.

    Returns: (exitcode, output_as_string, error_as_string)

    Based on http://stackoverflow.com/a/1996540/27310
    """
    phylo2owl_exec = ["python", "phylo2owl.py"]

    # Use the provided args or default to []
    args = args or []

    process = subprocess.Popen(
        phylo2owl_exec + args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate(stdin)
    print stdout
    print stderr
    return (process.returncode, stdout, stderr)
