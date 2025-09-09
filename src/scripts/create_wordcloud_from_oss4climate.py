import os

from oss4climate.src.config import (
    FILE_OUTPUT_OPTIMISED_LISTING_FEATHER,
)
from oss4climate.src.log import log_info, log_warning
from oss4climate.src.nlp.search import SearchResults
from wordcloud import WordCloud

from climate_knowledge_graph.configuration import Settings
from climate_knowledge_graph.data_sources.oss4climate_io import (
    load_oss4climate_data_as_dataframe,
)
from climate_knowledge_graph.graph import load_graph

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
licences = [(str(r["name"]), str(r["license"])) for i, r in df.iterrows()]
organisations = [(str(r["name"]), str(r["organisation"])) for i, r in df.iterrows()]


readme_collated = " ".join(df["description"].apply(str).to_list())
# readme_collated = " ".join(df["readme"].apply(str).to_list())

# -------------------------------------------------------------------------------------
#   / Loading data
# -------------------------------------------------------------------------------------


w = WordCloud(height=600, width=1000).generate(readme_collated)

w.to_file(".data/first_wordcloud.png")
