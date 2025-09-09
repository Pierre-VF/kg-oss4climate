"""
Module for LLM-based graph generation
"""

from langchain_neo4j import Neo4jGraph
from langchain_neo4j.graphs.graph_document import GraphDocument

from climate_knowledge_graph.configuration import Settings
from climate_knowledge_graph.exceptions import MissingDependencyInstall
from climate_knowledge_graph.semantics import RELATIONSHIPS

try:
    from langchain_mistralai import ChatMistralAI
except ImportError as e:
    raise MissingDependencyInstall("langchain_mistralai") from e

try:
    from langchain_community.document_loaders import (
        TextLoader,
        UnstructuredMarkdownLoader,
    )
except ImportError as e:
    raise MissingDependencyInstall("langchain_community") from e

try:
    from langchain_experimental.graph_transformers import LLMGraphTransformer
except ImportError as e:
    raise MissingDependencyInstall("langchain_experimental") from e


def __starter_loader() -> LLMGraphTransformer:
    llm_transformer = LLMGraphTransformer(
        llm=ChatMistralAI(temperature=0, model_name=Settings().MISTRAL_MODEL),
        allowed_relationships=RELATIONSHIPS,
    )
    return llm_transformer


def __finisher_loader(
    llm_transformer: LLMGraphTransformer,
    document: GraphDocument,
) -> list[GraphDocument]:
    print("Converting document to graph")
    graph_documents = llm_transformer.convert_to_graph_documents(document)
    print("Done")
    return graph_documents


def load_markdown_file_into_graph_documents(
    file_path: str,
) -> list[GraphDocument]:
    llm_transformer = __starter_loader()
    document = UnstructuredMarkdownLoader(file_path).load()
    return __finisher_loader(
        llm_transformer,
        document,
    )


def load_text_file_into_graph_documents(
    file_path: str,
) -> list[GraphDocument]:
    llm_transformer = __starter_loader()
    document = TextLoader(file_path).load()
    return __finisher_loader(
        llm_transformer,
        document,
    )


def add_graph_documents_to_graph(
    graph: Neo4jGraph,
    graph_documents: list[GraphDocument],
):
    print("Adding to graph")
    graph.add_graph_documents(graph_documents, include_source=True)
    print("Done")
