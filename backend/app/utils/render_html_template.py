from typing import Any
from pathlib import Path
from jinja2 import Template


def render_html_template(*, path_file_template: str, context: dict[str, Any]) -> str:
    """
    Render an HTML template from a file with the provided context.

    Args:
        path_file_template (str): The file path of the template to render.
        context (dict[str, Any]): The context to pass to the template for rendering.

    Returns:
        str: The rendered HTML content as a string.
    """
    template_str = Path(path_file_template).read_text()
    html_content = Template(template_str).render(context)
    return html_content
