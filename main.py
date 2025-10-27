"""
Builds a basic knowledge graph from a file and stores it into Neo4j

Code from:
https://towardsdatascience.com/enterprise-ready-knowledge-graphs-96028d863e8c/
"""

from climate_knowledge_graph.builder import (
    extract_url_targets_into_graph_documents,
    load_text_file_into_graph_documents,
)
from climate_knowledge_graph.graph import (
    dump_graph_to_json,
    load_graph,
    load_graph_documents_from_json,
)

gds = load_graph_documents_from_json(".data/url_graph.json")

g = load_graph()
dump_graph_to_json(g, ".data/url_graph.json")

gd = extract_url_targets_into_graph_documents(".data/html/index.html")
g.add_graph_documents(gd)


# gd = extract_url_targets_into_graph_documents(".data/reduced-OSST-README.md")
# dump_graph_to_json(g, "new-osst-graph-with-urls.json")

raise RuntimeError("STOP here")


if True:
    load_text_file_into_graph_documents(".data/reduced-OSST-README.md", g)
    # load_text_file_into_graph()

dump_graph_to_json(g, "new-osst-graph.json")


print("Done")
