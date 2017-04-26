# phylo2owl - convert phylogenies to OWL ontologies

[![Build Status](https://travis-ci.org/phyloref/phylo2owl.svg?branch=master)](https://travis-ci.org/phyloref/phylo2owl)

phylo2owl is a tool that takes a phylogeny as input and converts it into an OWL ontology, using several ancillary ontologies (such as [CDAO], [Phyloref]) to express relationships (edges) between entities (vertices).

Converting phylogenies into OWL ontologies is one of the foundational steps in using an OWL reasoner to resolve a phyloreference expression (which is a series of OWL axioms) against a phylogeny.

## Synopsis

```
phylo2owl [input.(tre|nex|xml|...)] [-f format] [-o output.owl]
```

## Command line options

* *Default*: read a Newick tree from standard input, 
  write an OWL representation of the tree to standard output.
* *Input files*: Tree files to convert.
* *Output* (`-o`): Where the output ontology should be written. 
  The base name of this file (e.g. 'output' in 'output.owl')
  is used as the short prefix for nodes in this ontology in the
  output file.
* *Output name* (`-n` or `--name`): A short name for the ontology. 
  Defaults to the name of the output file.
* *Format* (`-f` or `--format`): Currently, 
  '[newick](http://en.wikipedia.org/wiki/Newick_format)', 
  '[nexus](http://en.wikipedia.org/wiki/Nexus_file)' and 
  '[nexml](http://en.wikipedia.org/wiki/NeXML_format)' are 
  supported.
* *Help* (`-h` or `--help`): Describes the usage of the program and
  every command line option.

## Requirements

* Read single tree in Newick format
    - Read multiple trees in Newick format?
* Should be easy to modify outputs -- we’re going to spend a lot of
  time iterating on the best way to represent trees in OWL!
* Phyloreferences will not be represented at this stage: we’ll write
  another tool to write phyloreferences in OWL, and then a third tool
  to query a phyloreference (in OWL) on a tree (in OWL).
    - A [separate test suite](https://docs.google.com/document/d/1uOox6rqGZKafOtno0eSssMqbfM9wVtA1EtzdgoNH36o/edit?usp=sharing)
      will test the outputs. Alternatively, we could include a
      owl2phylo file, and then test to see if we can convert files in
      one direction and then the other.

## Algorithm

* Use library (see below) to load input tree file in a node-based
  representation.
* Write out [a standard header](templates/header.txt) based on
  https://github.com/hlapp/phyloref/blob/master/Campanulaceae.owl
* For each node in the tree:
    - Write out the node using [our individual template](templates/individual.txt)
    - (Bonus!) Write out any other metadata associated with that node
    in OWL.
* Write out [a standard footer](templates/footer.txt).

## Testing

We use the [py.test](http://www.pytest.org) testing framework. You can
run the tests by running `py.tests tests` from this directory.

## Library options

We currently use [DendroPy](https://pythonhosted.org/DendroPy/). Some other
libraries we considered include:

* Python:
    - ETE Toolkit: http://etetoolkit.org/
    - Biopython: http://biopython.org/DIST/docs/tutorial/Tutorial.html#htoc204 
    - Ontospy: https://pypi.python.org/pypi/ontospy 
* NodeJS:
    - Tnt.tree: http://tntvis.github.io/tnt.tree/
    - jsPhyloSVG: http://www.jsphylosvg.com/documentation.php
    - phylotree.js: https://github.com/veg/phylotree.js/tree/master
    - Phylocanvas: https://github.com/phylocanvas/phylocanvas/wiki
* Java:
    - https://github.com/biojava/biojava/
    - https://github.com/nexml/nexml.java 
    - https://github.com/cmzmasek/forester/tree/master/forester/java/src/org/forester/io/parsers 
    - http://owlapi.sourceforge.net/ 

[CDAO]: http://www.ontobee.org/ontology/CDAO
[Phyloref]: https://github.com/hlapp/phyloref
