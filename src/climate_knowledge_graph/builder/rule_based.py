"""
Module for rule-based graph generation
"""

import re
from enum import Enum

from langchain_neo4j.graphs.graph_document import GraphDocument, Node, Relationship
from urllib3.util import parse_url

from climate_knowledge_graph.exceptions import MissingDependencyInstall
from climate_knowledge_graph.helpers import unique_list
from climate_knowledge_graph.semantics import (
    RelationshipWithRuleBasedLogicEnum,
    ResourceTypeEnum,
)


def _f_link_is_relevant(x) -> bool:
    if parse_url(x.get("href")).host is None:
        return False
    xt = x.text
    return not (
        ("¶" in xt)
        or ("\n" in xt)
        or ("<img " in xt)
        or (len(_f_clean_link_title(xt)) <= 1)
    )


def _f_clean_link_title(x: str | list[str]) -> str:
    if isinstance(x, list):
        x = " ".join(x)
    return x.replace("\n", " ").replace("\r", "").strip()


def _extract_links_from_markdown_str(markdown_text: str):
    # Regular expression to match Markdown links: [text](url)
    pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    links = re.findall(pattern, markdown_text)
    return links


def _extract_links_from_html_str(html_text: str):
    try:
        from bs4 import BeautifulSoup
    except ImportError as e:
        raise MissingDependencyInstall("beautifulsoup4") from e

    b = BeautifulSoup(html_text, features="html.parser")
    rs = b.findAll(name="a")
    return [
        (_f_clean_link_title(x.text), x.get("href"))
        for x in rs
        if _f_link_is_relevant(x)
    ]


def _url_to_resource_type(url: str | None) -> ResourceTypeEnum | None:
    if url is None:
        return None
    parsed_url = parse_url(url)
    host = parsed_url.host
    if host is None:
        return None
    if (host in ["github.com", "bitbucket.org", "codeberg.org"]) or ("gitlab." in host):
        return ResourceTypeEnum.CODE_REPOSITORY
    elif parsed_url.path in ["", "/", None]:
        return ResourceTypeEnum.WEBSITE
    else:
        return None


def map_to_relationships_in_graph_document(
    sources: list[str],
    targets: list[str] | str | Enum,
    relationship: RelationshipWithRuleBasedLogicEnum | str,
    source_identifier: str | None = None,
) -> GraphDocument:
    if not isinstance(targets, list):
        if isinstance(targets, Enum):
            targets = targets.value
        # To support convenience passing of single target
        targets = [targets] * len(sources)
    unique_nodes = {i: Node(id=i) for i in unique_list(sources + targets)}
    if isinstance(relationship, Enum):
        relationship_str = relationship.value
    elif isinstance(relationship, str):
        relationship_str = relationship
    else:
        raise TypeError("relationship must be str or Enum")
    relations = [
        Relationship(
            source=unique_nodes[text],
            target=unique_nodes[url],
            type=relationship_str,
        )
        for text, url in zip(sources, targets)
    ]
    if source_identifier:
        kwargs = dict(source=source_identifier)
    else:
        kwargs = dict()

    gd = GraphDocument(
        nodes=list(unique_nodes.values()),
        relationships=relations,
        **kwargs,
    )
    return gd


def map_urls_to_is_available_at_url_relationships(
    urls: list[tuple[str, str]],
    source_identifier: str | None = None,
) -> GraphDocument:
    return map_to_relationships_in_graph_document(
        sources=[i[0].strip() for i in urls],
        targets=[i[1] for i in urls],
        relationship=RelationshipWithRuleBasedLogicEnum.IS_AVAILABLE_AT_URL,
        source_identifier=source_identifier,
    )


def map_urls_to_is_a_relationships(
    urls: list[tuple[str, str]],
    source_identifier: str | None = None,
) -> GraphDocument:
    x = [(_url_to_resource_type(url), text) for text, url in urls]
    return map_to_relationships_in_graph_document(
        sources=[i[1].strip() for i in x],
        targets=[i[0].value for i in x],
        relationship=RelationshipWithRuleBasedLogicEnum.IS_A,
        source_identifier=source_identifier,
    )


def full_mapping_of_urls_and_targets_in_graph_documents(
    file_path: str,
    source_identifier: str | None = None,
    filter_links: bool = True,
) -> list[GraphDocument]:
    if file_path.endswith(".md"):
        with open(file_path, "r") as f:
            md_content = f.read()
        raw_links = _extract_links_from_markdown_str(md_content)
        links = [(_f_clean_link_title(i), url) for i, url in raw_links]
    elif file_path.endswith(".html"):
        with open(file_path, "r") as f:
            html_content = f.read()
        links = _extract_links_from_html_str(html_content)
    else:
        raise ValueError("Document must be Markdown or HTML")

    if filter_links:
        # Filter the links to remove irrelevant ones (e.g. badges and intra-page links)
        links = [i for i in links if (not i[0].startswith(("!", "<")))]
        links = [i for i in links if (not i[1].startswith("#"))]

    return [
        map_urls_to_is_available_at_url_relationships(
            links,
            source_identifier=source_identifier,
        ),
        map_urls_to_is_a_relationships(
            links,
            source_identifier=source_identifier,
        ),
    ]
