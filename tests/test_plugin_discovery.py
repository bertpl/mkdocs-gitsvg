"""Smoke tests: the plugin is registered and discoverable by MkDocs."""

from importlib.metadata import entry_points

from mkdocs.plugins import BasePlugin

from mkdocs_gitsvg.plugin import GitSvgPlugin


def test_plugin_registered_as_entry_point() -> None:
    # --- arrange ----------------------
    plugins = {ep.name: ep for ep in entry_points(group="mkdocs.plugins")}

    # --- act --------------------------
    ep = plugins.get("gitsvg")

    # --- assert -----------------------
    assert ep is not None
    assert ep.load() is GitSvgPlugin


def test_plugin_is_baseplugin_subclass() -> None:
    # --- arrange / act / assert -------
    assert issubclass(GitSvgPlugin, BasePlugin)
