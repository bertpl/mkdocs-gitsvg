"""Tests for the gitsvg render core (`mkdocs_gitsvg.render`)."""

import pytest

from mkdocs_gitsvg.render import GitsvgValidationError, render_gitsvg

# A minimal valid op-stream: one branch with a couple of commits.
_VALID_SOURCE = (
    '{"op": "branch", "name": "main", "label_side": "before"}\n'
    '{"op": "commit", "branch": "main", "id": "c1", "msg": "initial commit", "hash": "auto"}\n'
    '{"op": "commit", "branch": "main", "id": "c2", "msg": "add README", "hash": "auto"}'
)


def test_renders_valid_source_to_embeddable_svg() -> None:
    # --- act --------------------------
    svg = render_gitsvg(_VALID_SOURCE)

    # --- assert -----------------------
    assert "<svg" in svg
    assert "<?xml" not in svg  # embeddable: no XML prolog


def test_invalid_source_raises_with_report() -> None:
    # --- arrange ----------------------
    source = "this is not valid jsonl"

    # --- act / assert -----------------
    with pytest.raises(GitsvgValidationError) as excinfo:
        render_gitsvg(source)
    assert not excinfo.value.report.is_clean()


def test_import_op_is_rejected() -> None:
    # --- arrange ----------------------
    source = '{"op": "import", "path": "other.gitsvg.jsonl"}'

    # --- act / assert -----------------
    with pytest.raises(GitsvgValidationError):
        render_gitsvg(source)


def test_id_prefix_is_forwarded_to_gitsvg(monkeypatch: pytest.MonkeyPatch) -> None:
    # gitsvg emits no ids today, so the prefix can't be observed in the
    # output — assert instead that it reaches the renderer (the namespacing
    # contract the plugin's per-build counter relies on).
    # --- arrange ----------------------
    captured: dict[str, str] = {}

    def fake_render_text(source: str, *, id_prefix: str = "") -> str:
        captured["id_prefix"] = id_prefix
        return "<svg/>"

    monkeypatch.setattr("mkdocs_gitsvg.render.render_text", fake_render_text)

    # --- act --------------------------
    render_gitsvg(_VALID_SOURCE, id_prefix="gsvg7-")

    # --- assert -----------------------
    assert captured["id_prefix"] == "gsvg7-"


def test_id_prefix_does_not_break_real_render() -> None:
    # --- act --------------------------
    svg = render_gitsvg(_VALID_SOURCE, id_prefix="gsvg1-")

    # --- assert -----------------------
    assert "<svg" in svg
