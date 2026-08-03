# Changelog

## 1.0.0

First stable release. The major bump signals the breaking change below, and leaves the
`0.x` range where dependency resolvers treat every release as potentially breaking (#8).

### Breaking changes

- `template_file` no longer overrides the loader on a user-supplied `jinja_env` (#17).
  Previously, passing `jinja_env` caused the task to set `env.loader = FileSystemLoader(path)`
  on every run, mutating the caller's environment. This caused wrong-template and
  template-not-found errors when a single `jinja_env` was shared across threads rendering
  from different paths (#5).
- `path` is now optional (`path: Optional[str] = None`) and is **ignored when `jinja_env`
  is provided**. If you pass a `jinja_env`, you are responsible for configuring its loader.
- Calling `template_file` with neither `path` nor `jinja_env` now raises `ValueError`.

#### Who is affected

Anyone calling `template_file(jinja_env=<env without a loader>, path=<dir>)` and relying on
the task to wire up the loader from `path`. After 1.0.0 that environment must carry its own
loader, otherwise `get_template` raises `TypeError`.

#### Migration

Before:

```python
task.run(template_file, template=tpl, jinja_env=my_env, path=f"templates/{platform}")
```

After — set the loader on your own environment. A per-path factory also avoids the
shared-mutation race:

```python
def env_for(path):
    return Environment(
        loader=FileSystemLoader(path),
        undefined=StrictUndefined,
        trim_blocks=True,
    )

task.run(template_file, template=tpl, jinja_env=env_for(f"templates/{platform}"))
```

The `path`-only usage is unchanged:

```python
task.run(template_file, template=tpl, path="templates")
```

### Other changes

- Python 3.10 through 3.14 are supported and tested; Python 3.8 and 3.9 are dropped (#18, #26).
- The project builds with `uv` instead of Poetry, and all tooling configuration now lives in
  `pyproject.toml` (#23, #25, #27).
- Formatting and linting moved from black/pylama to ruff (#20, #25).
- Fixed the spelling of `template_string` (#11).

## 0.2.0

- Bumped to jinja2 3 (#7).
- Fixed handling of a custom jinja environment (#3).

## 0.1.0

Initial release.
