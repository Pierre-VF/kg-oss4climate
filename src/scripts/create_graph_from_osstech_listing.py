import os

from climate_knowledge_graph.builder.rule_based import (
    full_mapping_of_urls_and_targets_in_graph_documents,
)
from climate_knowledge_graph.configuration import Settings
from climate_knowledge_graph.graph import add_graph_documents_to_graph, load_graph

s = Settings()
g = load_graph(s)

gdocs = full_mapping_of_urls_and_targets_in_graph_documents(
    file_path=os.path.expanduser(
        "~/projects/github/kg-oss4climate/.data/OSST-README.md"
    ),
)
add_graph_documents_to_graph(g, graph_documents=gdocs)

print("Done with import")
