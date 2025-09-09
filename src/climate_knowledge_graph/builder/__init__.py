"""
Module to handle graph-building using LLMs

Note: at this stage, only Mistral models are supported
"""

from climate_knowledge_graph.builder.llm_based import (  # noqa: F401
    load_markdown_file_into_graph_documents,
    load_text_file_into_graph_documents,
)
from climate_knowledge_graph.builder.rule_based import (  # noqa: F401
    full_mapping_of_urls_and_targets_in_graph_documents,
)
