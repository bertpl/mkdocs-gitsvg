"""The mkdocs-gitsvg MkDocs plugin: wiring + build-scoped state.

`GitSvgPlugin` auto-registers a SuperFences custom fence so authors
activate the plugin with just ``plugins: [gitsvg]`` — no hand-editing of
``markdown_extensions``. The plugin owns the cross-fence state a bare
SuperFences callable can't: a per-build id counter yielding a unique
``id_prefix`` per diagram, reset each build so ``mkdocs serve`` rebuilds
start clean.
"""

from importlib import resources

from mkdocs.config import config_options
from mkdocs.config.base import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File, Files

from .fence import make_gitsvg_fence

_SUPERFENCES = "pymdownx.superfences"

# Site-relative location of the bundled stylesheet, used both as the
# generated file's dest and as the extra_css link.
_CSS_URI = "assets/gitsvg/style.css"


class GitSvgConfig(Config):
    """Typed configuration schema for `GitSvgPlugin`."""

    fence_name = config_options.Type(str, default="gitsvg")
    css_class = config_options.Type(str, default="gitsvg-diagram")
    on_error = config_options.Choice(("raise", "warn", "show"), default="warn")


class GitSvgPlugin(BasePlugin[GitSvgConfig]):
    """Renders ` ```gitsvg ` fenced blocks to inline SVG at build time."""

    # ----------------------------------------------------------------------
    #  Build-scoped id namespacing
    # ----------------------------------------------------------------------
    def next_id_prefix(self) -> str:
        """Return a unique-per-build SVG id prefix (``gsvg1-``, ``gsvg2-``, …)."""
        self._id_counter += 1
        return f"gsvg{self._id_counter}-"

    def on_pre_build(self, *, config: MkDocsConfig) -> None:
        """Reset the id counter so each build (and serve rebuild) starts clean."""
        self._id_counter = 0

    # ----------------------------------------------------------------------
    #  Fence registration
    # ----------------------------------------------------------------------
    def on_config(self, config: MkDocsConfig) -> MkDocsConfig:
        """Register the gitsvg custom fence, auto-wiring SuperFences."""
        self._id_counter = 0
        self._require_pymdownx()
        if _SUPERFENCES not in config["markdown_extensions"]:
            config["markdown_extensions"].append(_SUPERFENCES)
        fences = config["mdx_configs"].setdefault(_SUPERFENCES, {}).setdefault("custom_fences", [])
        # Drop a stale entry from a previous serve rebuild before re-adding,
        # so the fence is registered exactly once.
        fences[:] = [fence for fence in fences if fence.get("name") != self.config.fence_name]
        fences.append(
            {
                "name": self.config.fence_name,
                "class": self.config.css_class,
                "format": make_gitsvg_fence(self),
            }
        )
        if _CSS_URI not in config["extra_css"]:
            config["extra_css"].append(_CSS_URI)
        return config

    # ----------------------------------------------------------------------
    #  Bundled stylesheet
    # ----------------------------------------------------------------------
    def on_files(self, files: Files, *, config: MkDocsConfig) -> Files:
        """Emit the bundled stylesheet into the site at `_CSS_URI`."""
        css = resources.files(__package__).joinpath("style.css").read_text(encoding="utf-8")
        files.append(File.generated(config, _CSS_URI, content=css))
        return files

    @staticmethod
    def _require_pymdownx() -> None:
        """Fail with an actionable message if pymdown-extensions is missing."""
        try:
            import pymdownx.superfences  # noqa: F401
        except ImportError as err:
            raise PluginError(
                "mkdocs-gitsvg requires pymdown-extensions; install it to use the gitsvg plugin."
            ) from err
