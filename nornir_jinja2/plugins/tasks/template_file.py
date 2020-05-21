from typing import Any, Optional, Dict, Callable

from nornir.core.task import Result, Task

from jinja2 import Environment, FileSystemLoader, StrictUndefined

FiltersDict = Optional[Dict[str, Callable[..., str]]]


def template_file(
    task: Task,
    template: str,
    path: str,
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
            loader=FileSystemLoader(path), undefined=StrictUndefined, trim_blocks=True,
        )
    env.filters.update(jinja_filters)
    t = env.get_template(template)
    text = t.render(host=task.host, **kwargs)

    return Result(host=task.host, result=text)
