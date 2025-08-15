"""
Module to handle graph-building using LLMs

Note: at this stage, only Mistral models are supported
"""

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_mistralai import ChatMistralAI
from langchain_neo4j import Neo4jGraph
from langchain_neo4j.graphs.graph_document import GraphDocument
from pydantic_settings import BaseSettings

from climate_knowledge_graph.semantics import RELATIONSHIPS


class BuilderSettings(BaseSettings):
    MISTRAL_API_KEY: str
    MISTRAL_MODEL: str = "mistral-medium"


def __starter_loader() -> LLMGraphTransformer:
    llm_transformer = LLMGraphTransformer(
        llm=ChatMistralAI(temperature=0, model_name=BuilderSettings().MISTRAL_MODEL),
        allowed_relationships=RELATIONSHIPS,
    )
    return llm_transformer


def __finisher_loader(
    llm_transformer: LLMGraphTransformer, document: GraphDocument, graph: Neo4jGraph
) -> None:
    print("Converting document to graph")
    graph_documents = llm_transformer.convert_to_graph_documents(document)
    print("Done")

    print(" ")

    print("Adding to graph")
    graph.add_graph_documents(graph_documents, include_source=True)
    print("Done")


def load_markdown_file_into_graph(file_path: str, graph: Neo4jGraph) -> None:
    llm_transformer = __starter_loader()
    document = UnstructuredMarkdownLoader(file_path).load()
    return __finisher_loader(
        llm_transformer,
        document,
        graph,
    )


def load_text_file_into_graph(file_path: str, graph: Neo4jGraph) -> None:
    llm_transformer = __starter_loader()
    document = TextLoader(file_path).load()
    return __finisher_loader(
        llm_transformer,
        document,
        graph,
    )
