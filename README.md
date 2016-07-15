# phylo2owl

## Synopsis

```
phylo2owl [input.(tre|phy|xml|...)] [-o output.owl]
```

## Command line options

* *Default:* read from standard input, write to standard output
* *Input files:* Tree files to convert

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
* Write out a standard header based on
  https://github.com/hlapp/phyloref/blob/master/Campanulaceae.owl
* For each node in the tree:
    - Write out the node using
      https://github.com/hlapp/phyloref/blob/master/Campanulaceae.owl
      as a guide.
    - (Bonus!) Write out any other metadata associated with that node
    in OWL.
* Write out a standard footer based on
  https://github.com/hlapp/phyloref/blob/master/Campanulaceae.owl

## Tests

* Load valid Newick file successfully
* Load invalid Newick file and report a useful error (with error type
  and line number)
* Detect cases where output OWL would be logically inconsistent (a
  node being the child of itself, for instance).

## Language options

* Python probably has a huge advantage, just because it’s easier to
  install a script in Python (`easy_install phylo2owl` on most Unixes)
  than in NodeJS (need to install nodejs first, then `npm install
  phylo2owl`). And it’s pretty easy to install Python to both Windows
  and MacOS X with homebrew.
    - That said, npm can install to bin (see
      https://docs.npmjs.com/files/package.json#bin), so this is
      definitely an option.
    - System Python on MacOS X is 2.7, which is a pain but supportable.

## Library options

* Python:
    - DendroPy: https://pythonhosted.org/DendroPy/ 
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
