from importlib.resources import files
from typing import Any

from jinja2 import Environment, FileSystemLoader

_TEMPLATE_ENV = Environment(
    loader=FileSystemLoader(
        str((files("climate_knowledge_graph.builder.templates") / "x").parent)
    )
)


def render_from_template(template: str, context: dict[str, Any]) -> str:
    x = _TEMPLATE_ENV.get_template(template)
    return x.render(context)
