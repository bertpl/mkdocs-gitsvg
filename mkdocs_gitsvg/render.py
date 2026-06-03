"""MkDocs-agnostic render core: gitsvg op-stream → inline SVG string.

This module is the seam between the MkDocs plugin and the ``gitsvg``
renderer. Everything MkDocs-specific — fences, configuration, error
policy, HTML wrapping — lives elsewhere; this module knows only how to
turn an op-stream string into an embeddable SVG string, so it stays
independently testable.

It delegates to gitsvg's public ``render_text`` façade rather than
composing gitsvg's pipeline internals. ``GitsvgValidationError`` is
re-exported so the rest of the plugin can treat this module as the single
boundary to gitsvg.
"""

from gitsvg import GitsvgValidationError, render_text

__all__ = ["GitsvgValidationError", "render_gitsvg"]


def render_gitsvg(source: str, *, id_prefix: str = "") -> str:
    """Render a gitsvg JSONL op-stream to an inline-embeddable SVG string.

    Args:
        source: The op-stream as ``.gitsvg.jsonl`` text (one JSON op per
            line). An ``import`` op has no base path to resolve against in
            a fenced block and fails validation; inline the imported ops
            instead.
        id_prefix: Prefix applied to element ids in the emitted SVG so
            multiple inline diagrams on one page can't collide. Empty (the
            default) keeps gitsvg's default ids.

    Returns:
        The SVG document as a string, with no XML prolog and no injected
        ``<style>`` / ``<script>`` — ready to inline into HTML.

    Raises:
        GitsvgValidationError: If ``source`` fails to parse or validate;
            the attached ``report`` carries the individual errors.
    """
    return render_text(source, id_prefix=id_prefix)
