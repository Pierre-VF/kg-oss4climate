"""
Module for I/O to Oss4climate
"""

import os

import pandas as pd
from oss4climate.src.config import (
    FILE_OUTPUT_OPTIMISED_LISTING_FEATHER,
)
from oss4climate.src.log import log_info, log_warning
from oss4climate.src.nlp.search import SearchResults


def load_oss4climate_data_as_dataframe(include_readme: bool = False) -> pd.DataFrame:
    SEARCH_RESULTS = SearchResults()
    force_refresh = False

    if force_refresh or not os.path.exists(FILE_OUTPUT_OPTIMISED_LISTING_FEATHER):
        from oss4climate.src.search import listing_search

        log_warning("- Listing not found, downloading again")
        listing_search.download_listing_data_for_app()

    log_info("- Loading documents")

    rows = []

    # Make sure to coordinate the below with the app start procedure
    for r in SEARCH_RESULTS.iter_documents(
        FILE_OUTPUT_OPTIMISED_LISTING_FEATHER,
        load_in_object_without_readme=True,
        display_tqdm=True,
        memory_safe=True,
    ):
        rows.append(r)

    df = pd.DataFrame(data=rows)
    if include_readme:
        if "readme" not in df.keys():
            raise RuntimeError("No readme found in columns")
    return df
