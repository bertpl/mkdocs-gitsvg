# mkdocs-gitsvg

An MkDocs plugin that renders [gitsvg](https://github.com/bertpl/gitsvg)
git-graph diagrams from fenced code blocks to inline SVG at build time — no
client-side JavaScript, works in offline and PDF exports.

## Quick start

Install the plugin and enable it in `mkdocs.yml`:

```yaml
plugins:
  - gitsvg
```

Then draw a git graph in any page with a ` ```gitsvg ` fenced block whose body
is a gitsvg JSONL op-stream:

````markdown
```gitsvg
{"op": "branch", "name": "main", "label_side": "before"}
{"op": "commit", "branch": "main", "id": "c1", "msg": "initial commit", "hash": "auto"}
{"op": "commit", "branch": "main", "id": "c2", "msg": "add README", "hash": "auto"}
```
````

It renders inline at build time:

```gitsvg
{"op": "branch", "name": "main", "label_side": "before"}
{"op": "commit", "branch": "main", "id": "c1", "msg": "initial commit", "hash": "auto"}
{"op": "commit", "branch": "main", "id": "c2", "msg": "add README", "hash": "auto"}
```

See [Examples](examples.md) for more, and [Configuration](configuration.md) for
the available options.
