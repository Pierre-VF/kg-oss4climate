"""
Module for rule-based graph generation
"""

import re

from langchain_neo4j.graphs.graph_document import GraphDocument, Node, Relationship

from climate_knowledge_graph.builder.helpers import unique_list
from climate_knowledge_graph.semantics import RelationshipEnum


def _extract_markdown_links(markdown_text: str):
    # Regular expression to match Markdown links: [text](url)
    pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    links = re.findall(pattern, markdown_text)
    return links


def _f_interesting_link(x):
    if isinstance(x, list):
        x = x[0]
    return not (("¶" in x) or ("\n" in x) or ("<img " in x))


def _extract_html_links(html_text: str):
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print(
            "beautifulsoup4 not installed (make sure to install all dependency groups)"
        )

    b = BeautifulSoup(html_text, features="html.parser")
    rs = b.findAll(name="a")
    return [(x.contents, x.get("href")) for x in rs if _f_interesting_link(x.contents)]


def extract_url_targets_into_graph_documents(
    file_path: str,
    source_identifier: str | None = None,
) -> list[GraphDocument]:
    if file_path.endswith(".md"):
        with open(file_path, "r") as f:
            md_content = f.read()
        links = _extract_markdown_links(md_content)
    if file_path.endswith(".html"):
        with open(file_path, "r") as f:
            html_content = f.read()
        links = _extract_html_links(html_content)
    else:
        raise ValueError("Document must be Markdown")

    names = [i[0] for i in links]
    urls = [i[1] for i in links]
    unique_nodes = {i: Node(id=i) for i in unique_list(names + urls)}
    rel_type = RelationshipEnum.IS_AVAILABLE_AT_URL.value
    relations = [
        Relationship(
            source=unique_nodes[text],
            target=unique_nodes[url],
            type=rel_type,
        )
        for text, url in links
    ]

    if source_identifier:
        kwargs = dict(source=file_path)
    else:
        kwargs = dict()

    gd = GraphDocument(
        nodes=list(unique_nodes.values()),
        relationships=relations,
        **kwargs,
    )
    return [gd]
