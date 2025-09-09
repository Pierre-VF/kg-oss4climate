import os

from oss4climate.src.config import (
    FILE_OUTPUT_OPTIMISED_LISTING_FEATHER,
)
from oss4climate.src.log import log_info, log_warning
from oss4climate.src.nlp.search import SearchResults

from climate_knowledge_graph.builder.rule_based import (
    RelationshipWithRuleBasedLogicEnum,
    ResourceTypeEnum,
    map_to_relationships_in_graph_document,
    map_urls_to_is_a_relationships,
    map_urls_to_is_available_at_url_relationships,
)
from climate_knowledge_graph.configuration import Settings
from climate_knowledge_graph.graph import add_graph_documents_to_graph, load_graph

SEARCH_RESULTS = SearchResults()
force_refresh = False

if force_refresh or not os.path.exists(FILE_OUTPUT_OPTIMISED_LISTING_FEATHER):
    from oss4climate.src.search import listing_search

    log_warning("- Listing not found, downloading again")
    listing_search.download_listing_data_for_app()

log_info("- Loading documents")

urls = []
licences = []
organisations = []
# Make sure to coordinate the below with the app start procedure
for r in SEARCH_RESULTS.iter_documents(
    FILE_OUTPUT_OPTIMISED_LISTING_FEATHER,
    load_in_object_without_readme=True,
    display_tqdm=True,
    memory_safe=True,
):
    urls.append((r["name"], r["url"]))
    if isinstance(r["license"], str):
        licences.append((r["name"], r["license"]))
    if isinstance(r["organisation"], str):
        organisations.append((r["name"], r["organisation"]))


s = Settings()
g = load_graph(s)

gdocs = [
    map_to_relationships_in_graph_document(
        [i[0] for i in licences],
        [i[1] for i in licences],
        RelationshipWithRuleBasedLogicEnum.IS_LICENSED_UNDER,
    ),
    map_to_relationships_in_graph_document(
        [i[1] for i in organisations],
        ResourceTypeEnum.ORGANISATION,
        RelationshipWithRuleBasedLogicEnum.IS_A,
    ),
    map_urls_to_is_available_at_url_relationships(urls),
    map_urls_to_is_a_relationships(urls),
]

add_graph_documents_to_graph(g, graph_documents=gdocs)

print("Done with import")
