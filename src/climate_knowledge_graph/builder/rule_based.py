"""
Module for rule-based graph generation
"""

import re

from langchain_neo4j.graphs.graph_document import GraphDocument, Node, Relationship
from urllib3.util import parse_url

from climate_knowledge_graph.builder.helpers import unique_list
from climate_knowledge_graph.exceptions import MissingDependencyInstall
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


def _url_to_resource_type(url: str) -> ResourceTypeEnum | None:
    parsed_url = parse_url(url)
    host = parsed_url.host
    if (host in ["github.com", "bitbucket.org", "codeberg.org"]) or ("gitlab." in host):
        return ResourceTypeEnum.CODE_REPOSITORY
    elif parsed_url.path in ["", "/", None]:
        return ResourceTypeEnum.WEBSITE
    else:
        return None


def extract_url_targets_into_graph_documents(
    file_path: str,
    source_identifier: str | None = None,
) -> list[GraphDocument]:
    if file_path.endswith(".md"):
        with open(file_path, "r") as f:
            md_content = f.read()
        raw_links = _extract_links_from_markdown_str(md_content)
        links = [(_f_clean_link_title(i), url) for i, url in raw_links]
    if file_path.endswith(".html"):
        with open(file_path, "r") as f:
            html_content = f.read()
        links = _extract_links_from_html_str(html_content)
    else:
        raise ValueError("Document must be Markdown")

    names = [i[0] for i in links]
    urls = [i[1] for i in links]
    unique_nodes = {
        i: Node(id=i)
        for i in unique_list(names + urls) + [i.value for i in ResourceTypeEnum]
    }
    rel_type = RelationshipWithRuleBasedLogicEnum.IS_AVAILABLE_AT_URL.value
    rel_is_a_type = RelationshipWithRuleBasedLogicEnum.IS_A.value
    relations = [
        Relationship(
            source=unique_nodes[text],
            target=unique_nodes[url],
            type=rel_type,
        )
        for text, url in links
    ]

    resource_types = [(_url_to_resource_type(url), text) for text, url in links]
    relations += [
        Relationship(
            source=unique_nodes[text],
            target=unique_nodes[t.value],
            type=rel_is_a_type,
        )
        for t, text in resource_types
        if (t is not None)
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
