import json
import os

import pandas as pd
from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel
from tqdm import tqdm

from climate_knowledge_graph.builder.templates import render_from_template
from climate_knowledge_graph.configuration import Settings

if __name__ == "__main__":
    cache = Settings.disk_cache

    input_file = os.path.expanduser("~/projects/github/kg-oss4climate/.data/orgs.csv")
    output_file = os.path.expanduser(
        "~/projects/github/kg-oss4climate/.data/orgs_classified.json"
    )
    output_file_csv = output_file.replace(".json", ".csv")

    df_orgs = pd.read_csv(input_file)

    if True:
        mm = MistralModel(Settings().MISTRAL_MODEL)
        llm_agent = Agent(mm)

        def _f(url) -> dict:
            c = cache.get(url)
            if c and (c.get("exception") is None):
                return c
            try:
                prompt = render_from_template(
                    "prompts/organisation_metadata_generation_simple.md",
                    {"WEBSITE": url},
                )
                x = llm_agent.run_sync(prompt)
                clean_x = (
                    x.output.replace("\n", "").replace("```", "").replace("json{", "{")
                )
                out = json.loads(clean_x)
            except Exception as e:
                out = dict(exception=str(e))
            out["url"] = url
            cache.add(url, out)
            return out

        x_websites = [r["organization_website"] for i, r in df_orgs.iterrows()]
        x_out = [
            _f(i)
            for i in tqdm(x_websites)
            if (isinstance(i, str) and i.startswith("https://"))
        ]

        with open(output_file, "w") as f:
            json.dump(x_out, f)

    if True:
        with open(output_file, "r") as f:
            x_dict = json.load(f)

        df_out = pd.DataFrame(x_dict).merge(
            df_orgs[
                [
                    "organization_website",
                    "form_of_organization",
                    "location_country",
                ]
            ].rename(
                columns={
                    "organization_website": "url",
                    "form_of_organization": "manual_Type",
                    "location_country": "manual_Location",
                }
            ),
            how="left",
            on="url",
        )
        df_out[
            ["url", "Confidence", "manual_Type", "Type", "manual_Location", "Location"]
        ].sort_values("Confidence", ascending=False).to_csv(output_file_csv)

    print("DONE")


"""Issues witnessed:
'https://digitalearthafrica.org': {  "Location": {    "Country": "GLOBAL",    "Continent": "AF"  // Primary operational focus on Africa, but global partnerships  },  "Type": "Non-profit",  "Confidence": 0.98}
            """
