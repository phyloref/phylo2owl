#!/usr/bin/env python

"""test_shacl_shapes.py: Test SHACL shapes by querying them against failing trees."""

import os
from rdflib import BNode, URIRef
from rdflib.graph import Graph
from rdflib.namespace import RDF, RDFS
import tempfile
import libshacl

# Some URIRefs we'll need.
CDAO_Node = URIRef('http://purl.obolibrary.org/obo/CDAO_0000140') 
CDAO_hasChild = URIRef('http://purl.obolibrary.org/obo/CDAO_0000149')
phyloref_has_Sibling = URIRef('http://phyloinformatics.net/phyloref.owl#has_Sibling')

def test_shacl_shapes():
    """Test SHACL shapes that should fail SHACL validation."""

    # We start by constructing a tree that consists of a single node.
    g = Graph()
    node1 = BNode()
    g.add((node1, RDF.type, CDAO_Node))
    save_graph_and_validate(g, False)

    # If we add a non-CDAO_Node as a child, we should fail.
    non_node = BNode()
    g.add((node1, CDAO_hasChild, non_node))
    save_graph_and_validate(g, False)
    g.remove((node1, CDAO_hasChild, non_node))

    # If we add another node with another CDAO_Node, we should fail.
    node2 = BNode()
    g.add((node2, RDF.type, CDAO_Node))
    g.add((node1, RDFS.subClassOf, node2))
    save_graph_and_validate(g, False)
    g.remove((node1, RDFS.subClassOf, node2))

    # But if we add another node as a CDAO_hasChild, we should succeed.
    # TODO: This currently fails, since node2 does not have a CDAO_hasChild
    # to another node.
    g.add((node1, CDAO_hasChild, node2))
    save_graph_and_validate(g, False)
    g.add((node2, CDAO_hasChild, node1))
    save_graph_and_validate(g, True)

    # If we add a third node as a sibling, that should be fine too.
    # TODO: We should check to see if siblings mark each other.
    node3 = BNode()
    g.add((node3, RDF.type, CDAO_Node))
    g.add((node3, phyloref_has_Sibling, node2))
    save_graph_and_validate(g, True)

    # No node should be the child of itself.
    g.add((node2, CDAO_hasChild, node2))
    save_graph_and_validate(g, False)

def save_graph_and_validate(graph, expect_valid):
    """Write a graph to a temporary file, and then validate it."""

    # Create a temporary file.
    with tempfile.NamedTemporaryFile() as f:
        # Save graph to file.
        graph.serialize(f.name, format="xml")

        # Test graph against ValidationShapes.
        libshacl.validateShacl("tests/shapes/NodeShape.ttl", f.name, expect_valid=expect_valid)
    
        # TODO: This should clear the stdout gathered by pytest
        # upto this point so we only show the results of the
        # latest test, but it's not clear how to do that.

