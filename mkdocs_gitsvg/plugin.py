"""The mkdocs-gitsvg MkDocs plugin.

Scaffold placeholder: a no-op MkDocs ``BasePlugin`` subclass registered
under the ``gitsvg`` plugin name (via the ``mkdocs.plugins`` entry
point) so MkDocs discovers it. Fenced-block rendering, configuration,
and styling are added in later layers.
"""

from mkdocs.plugins import BasePlugin


class GitSvgPlugin(BasePlugin):
    """No-op MkDocs plugin placeholder for mkdocs-gitsvg."""
