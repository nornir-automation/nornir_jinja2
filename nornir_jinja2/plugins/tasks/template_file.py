from typing import Any, Optional, Dict, Callable

from nornir.core.task import Result, Task

from jinja2 import Environment, FileSystemLoader, StrictUndefined

import json
import xml.etree.ElementTree as elementTree
import xml.dom.minidom as minidom
import re

FiltersDict = Optional[Dict[str, Callable[..., str]]]


def template_file(
    task: Task,
    template: str,
    path: str,
    format_json = False,
    format_xml = False,
    jinja_filters: Optional[FiltersDict] = None,
    jinja_env: Optional[Environment] = None,
    **kwargs: Any
) -> Result:
    """
    Renders contants of a file with jinja2. All the host data is available in the template

    Arguments:
        template: filename
        path: path to dir with templates
        jinja_filters: jinja filters to enable. Defaults to nornir.config.jinja2.filters
        jinja_env: A fully configured jinja2 environment
        format_json: formats rendered JSON files containing extra whitespace or indentation
        format_xml: formats rendered XML files containing extra whitespace or indentation
        **kwargs: additional data to pass to the template

    Returns:
        Result object with the following attributes set:
          * result (``string``): rendered string
    """
    jinja_filters = jinja_filters or {}

    if jinja_env:
        env = jinja_env
        env.loader = FileSystemLoader(path)
    else:
        env = Environment(
            loader=FileSystemLoader(path), undefined=StrictUndefined, trim_blocks=True,
        )
    env.filters.update(jinja_filters)
    t = env.get_template(template)
    text = t.render(host=task.host, **kwargs)


    if format_json and is_json(text):
        reform = json.dumps(json.loads(text), indent=4)

        return Result(host=task.host, result=reform)


    if format_xml and is_xml(text):
        reform = minidom.parseString(text).toprettyxml(indent="      ")
        reform = re.sub(r'^<\?xml.*?\?>', '', reform).strip()
        reform = re.sub(r'\n\s*\n', '\n', reform)
        reform = re.sub(r'&quot;', '"', reform)

        return Result(host=task.host, result=reform)

    return Result(host=task.host, result=text)


def is_json(text):
    try:
        json.loads(text)
    except ValueError as e:
        return False
    return True


def is_xml(text):
    try:
        elementTree.fromstring(text)
    except elementTree.ParseError as e:
        return False
    return True
