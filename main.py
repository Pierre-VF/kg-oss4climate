"""
Builds a basic knowledge graph from a file and stores it into Neo4j

Code from:
https://towardsdatascience.com/enterprise-ready-knowledge-graphs-96028d863e8c/
"""

from climate_knowledge_graph.builder import load_text_file_into_graph
from climate_knowledge_graph.graph import dump_graph_to_json, load_graph

g = load_graph()
dump_graph_to_json(g, "graph.json")

if False:
    load_text_file_into_graph(".data/sample.txt", g)

print("Done")
