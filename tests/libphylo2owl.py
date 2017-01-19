#!/usr/bin/env python

"""
libphylo2owl.py: Library that provides a function to execute phylo2owl.py.
"""

import subprocess

def exec_phylo2owl(args=[], stdin=""):
    """
    Send those command line arguments to phylo2owl.py.
        - args: Command line arguments.
        - stdin: A string passed to phylo2owl.py on stdin.

    Returns: (exitcode, output_as_string, error_as_string)

    Based on http://stackoverflow.com/a/1996540/27310
    """
    phylo2owl_exec = ["python", "phylo2owl.py"]

    p = subprocess.Popen(
        phylo2owl_exec + args, 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    stdout, stderr = p.communicate(stdin)
    print stdout
    print stderr
    return (p.returncode, stdout, stderr)
