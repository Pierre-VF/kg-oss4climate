import os

import requests

from climate_knowledge_graph.builder.rule_based import (
    extract_url_targets_into_graph_documents,
)
from climate_knowledge_graph.graph import (
    load_graph,
)

filename = ".data/reduced-OSST-README.md"
if not os.path.exists(filename):
    # Download the file
    response = requests.get(
        "https://raw.githubusercontent.com/protontypes/open-sustainable-technology/refs/heads/main/README.md"
    )
    response.raise_for_status()
    with open(filename, "w") as f:
        f.write(response.text)
    print(f"File downloaded successfully as {filename}")


gds = extract_url_targets_into_graph_documents(filename)
print(f"Found {len(gds[0].nodes)} nodes")
print(f"Found {len(gds[0].relationships)} relationships")

g = load_graph()
g.add_graph_documents(gds)


print("DONE with parsing")
