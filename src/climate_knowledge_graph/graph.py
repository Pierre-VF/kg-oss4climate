"""
Modules to manage graphs (centered around Neo4j graphs)
"""

import json

from langchain_neo4j import Neo4jGraph

from climate_knowledge_graph import Settings


def load_graph(settings: Settings | None = None) -> Neo4jGraph:
    if settings is None:
        settings = Settings()

    graph = Neo4jGraph(
        url=f"neo4j://{settings.NEO4J_URL}",
        username=settings.NEO4J_USERNAME,
        password=settings.NEO4J_PASSWORD,
        driver_config=dict(),
    )
    return graph


def dump_graph_to_json(g: Neo4jGraph, output_json: str) -> None:
    nodes_result = g.query("MATCH (n) RETURN n")
    relationships_result = g.query("MATCH (a)-[r]->(b) RETURN a, r, b")

    nodes = [dict(record["n"]) for record in nodes_result]
    relationships = [
        {
            "source_id": record["a"].get("id"),
            "relationship_type": record["r"][1],
            "target_id": record["b"].get("id"),
            # "properties": dict(record["r"]),
        }
        for record in relationships_result
    ]

    data = {"nodes": nodes, "relationships": relationships}
    with open(output_json, "w") as file:
        json.dump(data, file, indent=4)
    return
