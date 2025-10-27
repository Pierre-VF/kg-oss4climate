from neo4j_viz import VisualizationGraph

from climate_knowledge_graph.graph import (
    load_graph,
)

g = load_graph()


VG = VisualizationGraph(nodes=g.nodes, relationships=g.relationships)

VG.render()
