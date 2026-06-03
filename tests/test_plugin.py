"""Tests for plugin wiring and state (`mkdocs_gitsvg.plugin`)."""

import sys
from pathlib import Path

import pytest
from mkdocs.config import load_config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError

from mkdocs_gitsvg.plugin import _CSS_URI, GitSvgPlugin

_SUPERFENCES = "pymdownx.superfences"


def _plugin(**options: object) -> GitSvgPlugin:
    """Build a configured plugin."""
    plugin = GitSvgPlugin()
    errors, warnings = plugin.load_config(options)
    assert errors == [] and warnings == []
    return plugin


def _config(tmp_path: Path) -> MkDocsConfig:
    """Load a real minimal MkDocs config (the path that populates mdx_configs)."""
    (tmp_path / "docs").mkdir(exist_ok=True)
    config_path = tmp_path / "mkdocs.yml"
    config_path.write_text("site_name: test\n")
    return load_config(str(config_path))


def _custom_fences(config: MkDocsConfig) -> list[dict]:
    return config["mdx_configs"].get(_SUPERFENCES, {}).get("custom_fences", [])


def test_config_defaults() -> None:
    # --- act --------------------------
    plugin = _plugin()

    # --- assert -----------------------
    assert plugin.config.fence_name == "gitsvg"
    assert plugin.config.css_class == "gitsvg-diagram"
    assert plugin.config.on_error == "warn"


def test_on_error_rejects_unknown_mode() -> None:
    # --- arrange ----------------------
    plugin = GitSvgPlugin()

    # --- act --------------------------
    errors, _ = plugin.load_config({"on_error": "explode"})

    # --- assert -----------------------
    assert errors


def test_on_config_registers_superfences_and_fence(tmp_path: Path) -> None:
    # --- arrange ----------------------
    plugin = _plugin()
    config = _config(tmp_path)

    # --- act --------------------------
    plugin.on_config(config)

    # --- assert -----------------------
    assert _SUPERFENCES in config["markdown_extensions"]
    fences = _custom_fences(config)
    assert [fence["name"] for fence in fences] == ["gitsvg"]
    assert callable(fences[0]["format"])


def test_on_config_is_idempotent_across_rebuilds(tmp_path: Path) -> None:
    # --- arrange ----------------------
    plugin = _plugin()
    config = _config(tmp_path)

    # --- act --------------------------
    plugin.on_config(config)
    plugin.on_config(config)

    # --- assert -----------------------
    assert config["markdown_extensions"].count(_SUPERFENCES) == 1
    assert len(_custom_fences(config)) == 1


def test_on_config_honors_custom_fence_name(tmp_path: Path) -> None:
    # --- arrange ----------------------
    plugin = _plugin(fence_name="gitgraph")
    config = _config(tmp_path)

    # --- act --------------------------
    plugin.on_config(config)

    # --- assert -----------------------
    assert _custom_fences(config)[0]["name"] == "gitgraph"


def test_id_prefix_increments_and_resets(tmp_path: Path) -> None:
    # --- arrange ----------------------
    plugin = _plugin()
    config = _config(tmp_path)
    plugin.on_config(config)

    # --- act / assert -----------------
    assert plugin.next_id_prefix() == "gsvg1-"
    assert plugin.next_id_prefix() == "gsvg2-"
    plugin.on_pre_build(config=config)
    assert plugin.next_id_prefix() == "gsvg1-"


def test_missing_pymdownx_raises_clear_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # --- arrange ----------------------
    plugin = _plugin()
    config = _config(tmp_path)
    monkeypatch.setitem(sys.modules, _SUPERFENCES, None)

    # --- act / assert -----------------
    with pytest.raises(PluginError, match="pymdown-extensions"):
        plugin.on_config(config)


def test_on_config_links_stylesheet(tmp_path: Path) -> None:
    # --- arrange ----------------------
    plugin = _plugin()
    config = _config(tmp_path)

    # --- act --------------------------
    plugin.on_config(config)
    plugin.on_config(config)  # rebuild: must not double-link

    # --- assert -----------------------
    assert config["extra_css"].count(_CSS_URI) == 1
