"""
Named entity extraction from readmes
"""

import os
import re

import pandas as pd
import spacy
from tqdm import tqdm


def fetch_data() -> pd.DataFrame:
    from oss4climate.scripts.listing_search import (
        FILE_OUTPUT_LISTING_FEATHER,
        download_data,
    )

    if not os.path.exists(FILE_OUTPUT_LISTING_FEATHER):
        download_data()

    df_inputs = pd.read_feather(FILE_OUTPUT_LISTING_FEATHER)
    return df_inputs


nlp = spacy.load("en_core_web_sm")  # "en_core_web_sm" or "en_core_web_trf"


def _f_clean(x: str) -> str:
    x = re.sub(r"\s+", " ", x)
    x = x.replace("'s", "")
    return x.strip()


mapped_references = dict()
out = dict()
for i, r in tqdm(fetch_data().iterrows()):
    doc = nlp(r["readme"].replace("\n", ""))

    url_i = r["url"]
    x_i = {
        (_f_clean(i.text), i.label_)
        for i in doc.ents
        if i.label_ not in ["CARDINAL", "PERCENT"]
    }
    out[url_i] = x_i
    for j in x_i:
        j0 = j[0]
        if j0 in mapped_references:
            mapped_references[j0].append(url_i)
        else:
            mapped_references[j0] = [url_i]


print(out)
