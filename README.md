# mkdocs-gitsvg

MkDocs plugin that renders [gitsvg](https://github.com/bertpl/gitsvg) git-graph
diagrams from fenced code blocks to inline SVG at build time.

[![CI](https://img.shields.io/github/actions/workflow/status/bertpl/mkdocs-gitsvg/push_to_main.yml?branch=main&label=CI)](https://github.com/bertpl/mkdocs-gitsvg/actions/workflows/push_to_main.yml)
[![PyPI](https://img.shields.io/pypi/v/mkdocs-gitsvg.svg)](https://pypi.org/project/mkdocs-gitsvg/)
[![Python](https://img.shields.io/pypi/pyversions/mkdocs-gitsvg.svg)](https://pypi.org/project/mkdocs-gitsvg/)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/bertpl/mkdocs-gitsvg/blob/main/LICENSE)

> **Status:** early development. The package scaffold and release pipeline are
> in place; diagram rendering is being built out.

## Installation

```bash
pip install mkdocs-gitsvg
```

## Usage

Enable the plugin in `mkdocs.yml`:

```yaml
plugins:
  - gitsvg
```

Then draw a git graph in any page with a ` ```gitsvg ` fenced block whose body
is a [gitsvg](https://github.com/bertpl/gitsvg) JSONL op-stream:

````markdown
```gitsvg
{"op": "branch", "name": "main", "label_side": "before"}
{"op": "commit", "branch": "main", "id": "c1", "msg": "initial commit", "hash": "auto"}
{"op": "commit", "branch": "main", "id": "c2", "msg": "add README", "hash": "auto"}
```
````

The block renders to an inline SVG git graph in the built site.

## License

MIT — see [LICENSE](LICENSE).
