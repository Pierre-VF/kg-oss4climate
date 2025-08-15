"""
Module to handle graph-building using LLMs

Note: at this stage, only Mistral models are supported
"""

from langchain_community.document_loaders import TextLoader
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_mistralai import ChatMistralAI
from langchain_neo4j import Neo4jGraph
from pydantic_settings import BaseSettings


class BuilderSettings(BaseSettings):
    MISTRAL_API_KEY: str
    MISTRAL_MODEL: str = "mistral-medium"


def load_text_file_into_graph(txt_file_path: str, graph: Neo4jGraph) -> None:
    llm_transformer = LLMGraphTransformer(
        llm=ChatMistralAI(temperature=0, model_name=BuilderSettings().MISTRAL_MODEL)
    )

    document = TextLoader(txt_file_path).load()

    print("Converting document to graph")
    graph_documents = llm_transformer.convert_to_graph_documents(document)
    print("Done")

    print(" ")

    print("Adding to graph")
    graph.add_graph_documents(graph_documents, include_source=True)
    print("Done")
