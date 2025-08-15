"""
This is the most basic test, which just consists in ensuring that all packages can be imported
"""


def test_import_base():
    import climate_knowledge_graph
    from climate_knowledge_graph import graph, semantics

    assert isinstance(climate_knowledge_graph.__name__, str)
    assert isinstance(semantics.__name__, str)
    assert isinstance(graph.__name__, str)


def test_import_builder_features():
    from climate_knowledge_graph import builder
    from climate_knowledge_graph.builder import llm_based, rule_based

    assert isinstance(builder.__name__, str)
    assert isinstance(llm_based.__name__, str)
    assert isinstance(rule_based.__name__, str)
