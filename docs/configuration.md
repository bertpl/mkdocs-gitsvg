# Configuration

The plugin works with no configuration. To customize, pass options under the
`gitsvg` entry in `mkdocs.yml`:

```yaml
plugins:
  - gitsvg:
      fence_name: gitsvg
      css_class: gitsvg-diagram
      on_error: warn
```

| Option | Default | Meaning |
|---|---|---|
| `fence_name` | `gitsvg` | The fenced-block language tag to intercept. |
| `css_class` | `gitsvg-diagram` | Class on the wrapper `<div>` around each diagram. |
| `on_error` | `warn` | How to handle a diagram that fails to render — see below. |

## Error handling

When a block's op-stream fails to parse or validate, `on_error` decides what
happens:

- **`warn`** (default) — render a visible error box in place of the diagram
  *and* log a warning. `mkdocs build --strict` turns that warning into a build
  failure, so broken diagrams are caught in CI; `mkdocs serve` keeps running
  and shows the error inline.
- **`raise`** — fail the build immediately, even without `--strict`.
- **`show`** — render the error box but log nothing (silent in CI).

The error box uses the `gitsvg-error` class.

## Styling

The plugin ships a small stylesheet (centering and responsive sizing for
diagrams, styling for the error box) and links it automatically. Override the
`.gitsvg-diagram` / `.gitsvg-error` rules in your own `extra_css` to restyle.

## Requirements

The plugin builds on [SuperFences](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/)
from `pymdown-extensions`, which it registers automatically — no
`markdown_extensions` editing required.
