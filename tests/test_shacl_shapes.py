#!/usr/bin/env python

"""
test_shacl_shapes.py: Test SHACL shapes by querying them against failing trees.
"""

import tempfile
from rdflib import BNode, URIRef
from rdflib.graph import Graph
from rdflib.namespace import RDF, RDFS
import libshacl

# Some URIRefs we'll need.
CDAO_NODE = URIRef('http://purl.obolibrary.org/obo/CDAO_0000140')
CDAO_HAS_CHILD = URIRef('http://purl.obolibrary.org/obo/CDAO_0000149')
PHYLOREF_HAS_SIBLING = URIRef('http://phyloinformatics.net/phyloref.owl#has_Sibling')

def test_shacl_shapes():
    """Test SHACL shapes that should fail SHACL validation."""

    # We start by constructing a tree that consists of a single node.
    graph = Graph()
    node1 = BNode()
    graph.add((node1, RDF.type, CDAO_NODE))
    save_graph_and_validate(graph, False)

    # If we add a non-CDAO_Node as a child, we should fail.
    non_node = BNode()
    graph.add((node1, CDAO_HAS_CHILD, non_node))
    save_graph_and_validate(graph, False)
    graph.remove((node1, CDAO_HAS_CHILD, non_node))

    # If we add another node with another CDAO_Node, we should fail.
    node2 = BNode()
    graph.add((node2, RDF.type, CDAO_NODE))
    graph.add((node1, RDFS.subClassOf, node2))
    save_graph_and_validate(graph, False)
    graph.remove((node1, RDFS.subClassOf, node2))

    # But if we add another node as a CDAO_hasChild, we should succeed.
    # TODO: This currently fails, since node2 does not have a CDAO_hasChild
    # to another node.
    graph.add((node1, CDAO_HAS_CHILD, node2))
    save_graph_and_validate(graph, False)
    graph.add((node2, CDAO_HAS_CHILD, node1))
    save_graph_and_validate(graph, True)

    # If we add a third node as a sibling, that should be fine too.
    # TODO: We should check to see if siblings mark each other.
    node3 = BNode()
    graph.add((node3, RDF.type, CDAO_NODE))
    graph.add((node3, PHYLOREF_HAS_SIBLING, node2))
    save_graph_and_validate(graph, True)

    # No node should be the child of itself.
    graph.add((node2, CDAO_HAS_CHILD, node2))
    save_graph_and_validate(graph, False)

def save_graph_and_validate(graph, expect_valid):
    """Write a graph to a temporary file, and then validate it."""

    # Create a temporary file.
    with tempfile.NamedTemporaryFile() as fil:
        # Save graph to file.
        graph.serialize(fil.name, format="xml")

        # Test graph against ValidationShapes.
        libshacl.validate_shacl("tests/shapes/NodeShape.ttl", fil.name, expect_valid=expect_valid)

        # TODO: This should clear the stdout gathered by pytest
        # upto this point so we only show the results of the
        # latest test, but it's not clear how to do that.
