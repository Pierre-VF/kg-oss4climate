"""
Module to build a knowledge graph focusing on open-source code development
"""

import os
from enum import Enum
from typing import Any
from urllib.parse import urlparse

import networkx as nx
import pandas as pd

# -------------------------------------------------------------------------------------
#   Fetching data to generate the knowledge graph
# -------------------------------------------------------------------------------------


def fetch_data() -> pd.DataFrame:
    from oss4climate.scripts.listing_search import (
        FILE_OUTPUT_LISTING_FEATHER,
        download_data,
    )

    if not os.path.exists(FILE_OUTPUT_LISTING_FEATHER):
        download_data()

    df_inputs = pd.read_feather(FILE_OUTPUT_LISTING_FEATHER)
    return df_inputs


# -------------------------------------------------------------------------------------
#   Key metadata definition
# -------------------------------------------------------------------------------------
class EnumRelation(Enum):
    IS_FORK_OF = "IS_FORK_OF"
    IS_A = "IS_A"
    MAINTAINED_BY = "MAINTAINED_BY"
    LICENCED_UNDER = "LICENCED_UNDER"
    HOSTED_ON = "HOSTED_ON"
    IMPLEMENTED_IN = "IMPLEMENTED_IN"

    @property
    def label(self) -> str:
        return str(self.value)


class BasicKnowledgeGraph:
    def __init__(self):
        self.__kg = nx.Graph()
        self.__df_edges = None
        self.__nodes = dict()

    def extend(
        self,
        df_edges: pd.DataFrame,
        nodes: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        self.__df_edges = df_edges
        if nodes:
            self.__nodes = self.__nodes | nodes
            self.__kg.add_nodes_from([(k, v) for k, v in nodes.items()])
        # Create a knowledge graph
        for _, row in df_edges.iterrows():
            self.__kg.add_edge(
                row["source"], row["target"], label=row["relation"].label
            )

    def get_information(self, node_name: str):
        if node_name not in self.__kg:
            raise ValueError(f"{node_name} is not a node")
        return self.__kg[node_name]

    def get_instances(self, node_name: str) -> list[str]:
        if node_name not in self.__kg:
            raise ValueError(f"{node_name} is not a node")
        return [
            i
            for i, v in self.__kg[node_name].items()
            if (v.get("label") == "IS_A") and (not i.startswith("_"))
        ]

    @property
    def graph(self):
        return self.__kg

    def plot_with_pyvis(self, out_html: str) -> None:
        try:
            from pyvis.network import Network
        except ImportError as e:
            raise ImportError("pyvis is required to execute this") from e

        nt = Network(
            height="1500px",
            width="1500px",
            notebook=False,
            filter_menu=True,
            directed=True,
        )
        nt.from_nx(self.graph)
        nt.write_html(out_html, notebook=False, open_browser=False)

    def plot_with_jaal(self) -> None:
        try:
            from jaal import Jaal
        except ImportError as e:
            raise ImportError("jaal is required to execute this") from e

        def jaal_visualisation(df: pd.DataFrame):
            node_df = pd.concat(
                [
                    pd.DataFrame(
                        data={
                            "id": [_license_node_name, _git_repo_node_name],
                            "type": "__",
                        }
                    ),
                    pd.DataFrame(
                        data={
                            "id": [
                                str(i) for i in self.get_instances(_license_node_name)
                            ],
                            "type": "License",
                        }
                    ),
                    pd.DataFrame(
                        data={
                            "id": [
                                str(i) for i in self.get_instances(_git_repo_node_name)
                            ],
                            "type": "Repository",
                        }
                    ),
                ]
            )

            Jaal(
                edge_df=df.rename(columns={"source": "from", "target": "to"})[
                    ["from", "to"]
                ],
                node_df=node_df,
            ).plot(directed=True)

        jaal_visualisation(self.__df_edges)

    def matplotlib_visualise(g: nx.Graph, out_png: str = "out.png") -> None:
        try:
            import matplotlib.pyplot as plt
        except ImportError as e:
            raise ImportError("matplotlib is required to execute this") from e

        # Visualize the knowledge graph
        pos = nx.spring_layout(g, seed=42, k=0.9)
        labels = nx.get_edge_attributes(g, "label")
        plt.figure(figsize=(12, 10))
        nx.draw(
            g,
            pos,
            with_labels=True,
            font_size=10,
            node_size=700,
            node_color="lightblue",
            edge_color="gray",
            alpha=0.6,
        )
        nx.draw_networkx_edge_labels(
            g,
            pos,
            edge_labels=labels,
            font_size=8,
            label_pos=0.3,
            verticalalignment="baseline",
        )
        plt.title("Knowledge Graph")
        plt.savefig(out_png)


if __name__ == "__main__":
    # -------------------------------------------------------------------------------------
    #   Building the knowledge graph
    # -------------------------------------------------------------------------------------
    df_inputs = fetch_data()

    licenses = df_inputs["license"].unique().tolist()

    def extend_df(
        df: pd.DataFrame | None,
        source: str,
        target: str,
        relation: EnumRelation,
    ) -> pd.DataFrame:
        return pd.concat(
            [
                df,
                pd.DataFrame(
                    data={
                        "source": [source],
                        "target": [target],
                        "relation": [relation],
                    },
                ),
            ]
        )

    nodes = {}

    # Adding all licenses
    _license_node_name = "__LICENSE__"
    df_x = None
    for i in df_inputs["license"].unique().tolist():
        if i:
            nodes[i] = {}
            df_x = extend_df(
                df_x, source=i, target=_license_node_name, relation=EnumRelation.IS_A
            )

    # Adding all licenses
    _language_node_name = "__LANGUAGE__"
    df_x = None
    for i in df_inputs["language"].unique().tolist():
        if i:
            nodes[i] = {}
            df_x = extend_df(
                df_x, source=i, target=_language_node_name, relation=EnumRelation.IS_A
            )

    # Adding all repos
    _git_repo_node_name = "__GIT_REPOSITORY__"
    for __, r in df_inputs.iterrows():
        url_i = r["url"]
        nodes[url_i] = r
        df_x = extend_df(
            df_x, source=url_i, target=_git_repo_node_name, relation=EnumRelation.IS_A
        )
        df_x = extend_df(
            df_x,
            source=url_i,
            target=urlparse(url_i).hostname,
            relation=EnumRelation.HOSTED_ON,
        )
        if r["license"]:
            df_x = extend_df(
                df_x,
                source=url_i,
                target=r["license"],
                relation=EnumRelation.LICENCED_UNDER,
            )
        if r["is_fork"]:
            df_x = extend_df(
                df_x,
                source=url_i,
                target=r["forked_from"],
                relation=EnumRelation.IS_FORK_OF,
            )
        if r["organisation"]:
            df_x = extend_df(
                df_x,
                source=url_i,
                target=r["organisation"],
                relation=EnumRelation.MAINTAINED_BY,
            )
        if r["language"]:
            df_x = extend_df(
                df_x,
                source=url_i,
                target=r["language"],
                relation=EnumRelation.IMPLEMENTED_IN,
            )

    g = BasicKnowledgeGraph()
    g.extend(df_edges=df_x, nodes=nodes)

    print("NOK")
