"""
Builds a basic knowledge graph from a file and stores it into Neo4j

Code from:
https://towardsdatascience.com/enterprise-ready-knowledge-graphs-96028d863e8c/
"""

from climate_knowledge_graph.graph import (
    load_graph_documents_from_json,
)

gds = load_graph_documents_from_json(".data/url_graph.json")

print("Data was loaded in the Neo4j database")
