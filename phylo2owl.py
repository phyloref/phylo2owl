#!/usr/bin/env python

"""phylo2owl.py: Convert phylogenies into OWL ontologies expressed in RDF/XML."""

import argparse
import dendropy
import os.path
import pystache
import sys

__version__ = "0.1"
__author__ = "Gaurav Vaidya"
__copyright__ = "Copyright 2016 The Phyloreferencing Project"

# Global variables
FLAG_VERBOSE = False
output_name = 'example'

# Based on formats supported by DendroPy, 
# see https://pythonhosted.org/DendroPy/schemas/index.html#specifying-the-data-source-format
INPUT_FORMATS = ["newick", "nexus", "nexml"]

# Step 1. Parse command line arguments
input_file = sys.stdin
output_file = sys.stdout

cmdline_parser = argparse.ArgumentParser(
    description="Convert phylogenies into OWL ontologies expressed in RDF/XML."
)
cmdline_parser.add_argument(
    'input_filename', metavar='input.tre', type=str, nargs='?',
    help='Phylogeny file to parse'
)
cmdline_parser.add_argument(
    '-f', '--format', dest='input_format', nargs='?',
    choices=INPUT_FORMATS,
    type=str.lower, # Lowercase input type name.
    default='newick',
    help='Input format (for input filename or standard input)'
)
cmdline_parser.add_argument(
    '-o', dest='output_filename', metavar='output.owl', type=str,
    help='Ontology file to output'
)
cmdline_parser.add_argument(
    '-n', '--name', dest='output_name', metavar='output_name', type=str,
    help='Name of the resource to emit'
)
cmdline_parser.add_argument(
    '-v', '--version',
    action='version', version='%(prog)s ' + __version__
)
cmdline_parser.add_argument(
    '--verbose', 
    dest='flag_verbose', default=False, action='store_true', 
    help='Display debugging information'
)
args = cmdline_parser.parse_args()

# Set up FLAG_VERBOSE.
FLAG_VERBOSE = args.flag_verbose

# Step 2. Set up input and output streams.
# Try opening the input file.
if args.input_filename:
    input_file = open(args.input_filename, 'r')

# Figure out where the output should go, as well as the output name.
if args.output_filename:
    output_file = open(args.output_filename, 'w')
    output_name = os.path.splitext(os.path.basename(args.output_filename))[0]
elif args.input_filename:
    output_name = os.path.splitext(os.path.basename(args.input_filename))[0]

# But override output name if explicitly provided.
if args.output_name:
    output_name = args.output_name

# TODO: Make sure output_name is a valid entity name, probably as defined
# here -- https://www.w3.org/TR/REC-xml/#NT-NameChar

if FLAG_VERBOSE:
    sys.stderr.write("Output name: {0}\n".format(output_name))
    sys.stderr.write("Input file: {0}\n".format(input_file))
    sys.stderr.write("Output file: {0}\n".format(output_file))

# Step 2. Use DendroPy to read input tree.
try:
    tree = dendropy.Tree.get(file=input_file, schema=args.input_format)
except dendropy.utility.error.DataParseError as err:
    sys.stderr.write("Error: could not parse input!\n{0}\n".format(err))
    sys.exit(1)

if FLAG_VERBOSE:
    sys.stderr.write("Tree read successfully: {0}\n".format(tree))

# Step 3. Set up pystache to read templates.
render = pystache.Renderer(missing_tags='strict', search_dirs=os.path.dirname(os.path.abspath(__file__)) + '/templates')

# Step 4. Write out the header.
xmlbase = "http://phyloinformatics.net/phylo/{0}".format(output_name)
xmlns = xmlbase + '#'
output_file.write(render.render_name('header', {
    'name': output_name,
    'xmlbase': xmlbase,
    'xmlns': xmlbase + '#'
}))

# Step 5. Make a list of names for every node on this tree.
node_names = dict()
node_count = 1
for node in tree:
    name = node.label

    if node.taxon:
        name = node.taxon.label.replace(' ', '_')

    if name is None:
        name = 'Node_{0}'.format(node_count)
        node_count += 1

    node_names[node] = name

if FLAG_VERBOSE:
    sys.stderr.write("Names assigned to {0} tree nodes:\n".format(len(node_names)))
    for (node, name) in node_names.items():
        sys.stderr.write(" - {0}: {1}\n".format(name, node))
    sys.stderr.write("\n")

# Step 6. Write out each node on the tree.
import inspect
node_count = 1
for node in tree:
    output_file.write(render.render_name('individual', {
        'xmlns': xmlns,
        'term': node_names[node],
        'name': output_name,
        'children': [{'child': node_names[n]} for n in node.child_nodes()],
        'siblings': [{'sibling': node_names[n]} for n in node.sibling_nodes()]
    }))

# Step 7. Write out the footer.
output_file.write(render.render_name('footer'))
sys.exit(0)
