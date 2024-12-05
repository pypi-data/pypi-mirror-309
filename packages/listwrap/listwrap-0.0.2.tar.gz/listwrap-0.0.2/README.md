# listwrap

Formatting lists of strings.

Use cases include subtasks of automatic config generation or any other highly structured context such as programmatically constructing human-readable SQL statements.

We're [on pypi](https://pypi.org/project/listwrap/), so `pip install listwrap`.

## Examples

```
>>> from listwrap import align
>>> print(align(["a", "b", "c"]))
    "a",
    "b",
    "c",
>>> print(align(["a", "b", "c"], quote=None))
    a,
    b,
    c,
>>> print(align(["a", "b", "c"], indent=1))
 "a",
 "b",
 "c",
>>> print(align(["a", "b", "c"], indent=0, vertical=False))
"a","b","c",
```
Several formatting other options are supported; see the `align` method docstring.

## Development

```
git clone git@github.com:zkurtz/listwrap.git
pip install uv
uv sync
source .venv/bin/activate
```
