"""Tests for the SuperFences fence adapter (`mkdocs_gitsvg.fence`)."""

import logging

import pytest
from mkdocs.exceptions import PluginError

from mkdocs_gitsvg.fence import make_gitsvg_fence
from mkdocs_gitsvg.plugin import GitSvgPlugin

_VALID_SOURCE = (
    '{"op": "branch", "name": "main", "label_side": "before"}\n'
    '{"op": "commit", "branch": "main", "id": "c1", "msg": "init", "hash": "auto"}'
)
_BAD_SOURCE = "this is not valid jsonl"


def _plugin(**options: object) -> GitSvgPlugin:
    """Build a configured plugin with a freshly reset id counter."""
    plugin = GitSvgPlugin()
    errors, warnings = plugin.load_config(options)
    assert errors == [] and warnings == []
    plugin._id_counter = 0
    return plugin


def _call(plugin: GitSvgPlugin, source: str) -> str:
    """Invoke the fence callable the way SuperFences would."""
    fence = make_gitsvg_fence(plugin)
    return fence(source, "gitsvg", plugin.config.css_class, {}, None)


def test_renders_block_to_wrapped_svg() -> None:
    # --- act --------------------------
    html = _call(_plugin(), _VALID_SOURCE)

    # --- assert -----------------------
    assert html.startswith('<div class="gitsvg-diagram">')
    assert "<svg" in html
    assert html.endswith("</div>")


def test_css_class_is_configurable() -> None:
    # --- act --------------------------
    html = _call(_plugin(css_class="my-graph"), _VALID_SOURCE)

    # --- assert -----------------------
    assert '<div class="my-graph">' in html


def test_on_error_raise_fails_the_build() -> None:
    # --- arrange ----------------------
    plugin = _plugin(on_error="raise")

    # --- act / assert -----------------
    with pytest.raises(PluginError):
        _call(plugin, _BAD_SOURCE)


def test_on_error_warn_emits_box_and_logs(caplog: pytest.LogCaptureFixture) -> None:
    # --- arrange ----------------------
    plugin = _plugin(on_error="warn")

    # --- act --------------------------
    with caplog.at_level(logging.WARNING):
        html = _call(plugin, _BAD_SOURCE)

    # --- assert -----------------------
    assert '<pre class="gitsvg-error">' in html
    assert any(record.levelno == logging.WARNING for record in caplog.records)


def test_on_error_show_emits_box_silently(caplog: pytest.LogCaptureFixture) -> None:
    # --- arrange ----------------------
    plugin = _plugin(on_error="show")

    # --- act --------------------------
    with caplog.at_level(logging.WARNING):
        html = _call(plugin, _BAD_SOURCE)

    # --- assert -----------------------
    assert '<pre class="gitsvg-error">' in html
    assert caplog.records == []


def test_error_box_escapes_html() -> None:
    # --- act --------------------------
    html = _call(_plugin(on_error="show"), '{"op": "<script>"}')

    # --- assert -----------------------
    assert "<script>" not in html
    assert "&lt;script&gt;" in html
