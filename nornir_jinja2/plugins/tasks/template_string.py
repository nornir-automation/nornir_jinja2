from collections.abc import Callable
from typing import Any

from nornir.core.task import Result, Task

from jinja2 import Environment, StrictUndefined


FiltersDict = dict[str, Callable[..., str]]


def template_string(
    task: Task,
    template: str,
    jinja_filters: FiltersDict | None = None,
    jinja_env: Environment | None = None,
    **kwargs: Any,
) -> Result:
    """
    Renders a string with jinja2. All the host data is available in the template

    Arguments:
        template (string): template string
        jinja_filters (dict): jinja filters to enable. Defaults to nornir.config.jinja2.filters
        **kwargs: additional data to pass to the template

    Returns:
        Result object with the following attributes set:
          * result (``string``): rendered string
    """
    jinja_filters = jinja_filters or {}

    if jinja_env:
        env = jinja_env
    else:
        env = Environment(
            undefined=StrictUndefined,
            trim_blocks=True,
        )
    env.filters.update(jinja_filters)
    t = env.from_string(template)
    text = t.render(host=task.host, **kwargs)

    return Result(host=task.host, result=text)
