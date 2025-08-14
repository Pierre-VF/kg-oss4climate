"""
Builds a basic knowledge graph from a file and stores it into Neo4j

Code from:
https://towardsdatascience.com/enterprise-ready-knowledge-graphs-96028d863e8c/
"""

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_mistralai import ChatMistralAI
from langchain_neo4j import Neo4jGraph
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    MISTRAL_API_KEY: str


graph = Neo4jGraph(
    url="neo4j://localhost",
    # database="",
    username="neo4j",
    password="your_password",
    driver_config=dict(),
)


llm_transformer = LLMGraphTransformer(
    llm=ChatMistralAI(temperature=0, model_name="mistral-small")
)


document = TextLoader(".data/sample.txt").load()

print("Converting document to graph")
graph_documents = llm_transformer.convert_to_graph_documents(document)
print("Done")

print(" ")

print("Adding to graph")
graph.add_graph_documents(graph_documents)
print("Done")
