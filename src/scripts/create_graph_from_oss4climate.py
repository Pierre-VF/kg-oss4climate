import os

from langchain_neo4j.graphs.graph_document import Node
from oss4climate.src.config import (
    FILE_OUTPUT_OPTIMISED_LISTING_FEATHER,
)
from oss4climate.src.log import log_info, log_warning
from oss4climate.src.nlp.search import SearchResults
from urllib3.util import parse_url

from climate_knowledge_graph.builder.rule_based import (
    RelationshipWithRuleBasedLogicEnum,
    ResourceTypeEnum,
    map_to_relationships_in_graph_document,
)
from climate_knowledge_graph.configuration import Settings
from climate_knowledge_graph.data_sources.oss4climate_io import (
    load_oss4climate_data_as_dataframe,
)
from climate_knowledge_graph.graph import add_graph_documents_to_graph, load_graph

s = Settings()
g = load_graph(s)

# -------------------------------------------------------------------------------------
#   Loading data
# -------------------------------------------------------------------------------------

SEARCH_RESULTS = SearchResults()
force_refresh = False

if force_refresh or not os.path.exists(FILE_OUTPUT_OPTIMISED_LISTING_FEATHER):
    from oss4climate.src.search import listing_search

    log_warning("- Listing not found, downloading again")
    listing_search.download_listing_data_for_app()

log_info("- Loading documents")

df = load_oss4climate_data_as_dataframe(include_readme=False)

urls = [(str(r["name"]), str(r["url"])) for i, r in df.iterrows()]
languages = [
    (str(r["name"]), r["language"])
    for i, r in df.iterrows()
    if isinstance(r["language"], str)
]
licenses = [(str(r["name"]), str(r["license"])) for i, r in df.iterrows()]
organisations = [(str(r["name"]), str(r["organisation"])) for i, r in df.iterrows()]
readme_collated = " ".join(df["description"].apply(str).to_list())


repo = ResourceTypeEnum.CODE_REPOSITORY.value
license = ResourceTypeEnum.SOFTWARE_LICENSE.value
language = ResourceTypeEnum.PROGRAMMING_LANGUAGE.value
nodes = (
    [
        Node(id=r["name"], type=repo, properties={"url": r["url"]})
        for i, r in df.iterrows()
    ]
    + [Node(id=i, type=language) for i in df["language"].unique() if isinstance(i, str)]
    + [Node(id=i, type=license) for i in df["license"].unique() if isinstance(i, str)]
)

# -------------------------------------------------------------------------------------
#   / Loading data
# -------------------------------------------------------------------------------------


gdocs = [
    map_to_relationships_in_graph_document(
        [i[0] for i in urls],
        [parse_url(i[1]).host for i in urls],
        "IS_HOSTED_ON_DOMAIN",
        nodes=nodes,
    ),
    map_to_relationships_in_graph_document(
        [i[0] for i in languages],
        [i[1] for i in languages],
        "IS_IMPLEMENTED_IN",
        nodes=nodes,
    ),
    map_to_relationships_in_graph_document(
        [i[0] for i in licenses],
        [i[1] for i in licenses],
        RelationshipWithRuleBasedLogicEnum.IS_LICENSED_UNDER,
        nodes=nodes,
    ),
    map_to_relationships_in_graph_document(
        [i[0] for i in organisations],
        [i[1] for i in organisations],
        RelationshipWithRuleBasedLogicEnum.IS_FROM_ORGANISATION,
        nodes=nodes,
    ),
]

add_graph_documents_to_graph(g, graph_documents=gdocs)

print("Done with import")
