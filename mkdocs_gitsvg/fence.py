"""SuperFences custom-fence adapter for ` ```gitsvg ` blocks.

SuperFences invokes the callable built by `make_gitsvg_fence` once per
fenced block. The adapter pulls a unique id prefix from the plugin's
build-scoped counter, runs the MkDocs-agnostic render core, wraps the
SVG in the configured container, and returns HTML. Validation failures
are routed through the plugin's ``on_error`` policy.
"""

import html
from typing import TYPE_CHECKING, Callable

from mkdocs.exceptions import PluginError
from mkdocs.plugins import get_plugin_logger

from .render import GitsvgValidationError, render_gitsvg

if TYPE_CHECKING:
    from .plugin import GitSvgPlugin

log = get_plugin_logger(__name__)


def make_gitsvg_fence(plugin: "GitSvgPlugin") -> Callable[..., str]:
    """Build the SuperFences format callable bound to a plugin instance.

    The returned callable matches SuperFences' custom-fence signature
    ``(source, language, class_name, options, md, **kwargs)`` and closes
    over `plugin` so it can reach the build-scoped id counter and config.
    """

    def gitsvg_fence(source: str, language: str, class_name: str, options: dict, md: object, **kwargs: object) -> str:
        return _render_block(plugin, source)

    return gitsvg_fence


def _render_block(plugin: "GitSvgPlugin", source: str) -> str:
    """Render one fenced block to HTML, applying the id prefix and error policy."""
    id_prefix = plugin.next_id_prefix()
    try:
        svg = render_gitsvg(source, id_prefix=id_prefix)
    except GitsvgValidationError as err:
        return _handle_error(plugin.config.on_error, err)
    return f'<div class="{plugin.config.css_class}">{svg}</div>'


def _handle_error(mode: str, err: GitsvgValidationError) -> str:
    """Apply the configured ``on_error`` mode to a validation failure.

    Args:
        mode: One of ``raise`` / ``warn`` / ``show``.
        err: The validation error to surface.

    Returns:
        An error-box ``<pre>`` for ``warn`` / ``show``.

    Raises:
        PluginError: When `mode` is ``raise`` — fails the build immediately.
    """
    message = str(err)
    if mode == "raise":
        raise PluginError(message)
    if mode == "warn":
        log.warning(message)
    return f'<pre class="gitsvg-error">{html.escape(message)}</pre>'
