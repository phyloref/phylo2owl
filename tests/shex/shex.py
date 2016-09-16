import sys
from antlr4.InputStream import InputStream

sys.path.append("../../../../shexypy/scripts")
sys.path.append("../../../../shexypy")

import shex_eval
from shexypy.utils.xmlutils import prettyxml
import rdflib
from rdflib.namespace import RDF

with open('Node.shexml') as x: shex = x.read()
with open('../../examples/trees/pg_2357.ttl') as x: ttl = x.read()

graph = rdflib.Graph()
graph.parse(format='turtle', data=ttl)

class BlankOpts:
    def BlankOpts():
        pass

    def __getattr__(self, name):
        return False

# Find all nodes.
for s, p, o in graph.triples((None, RDF.type, rdflib.URIRef("http://purl.obolibrary.org/obo/CDAO_0000140"))):
    result = shex_eval.eval_shexml(shex, "Node", s, graph, BlankOpts())
    print("{0}: {1}".format(s, result))
    
