"""End-to-end tests: a real MkDocs build of a gitsvg-using site."""

from pathlib import Path

from click.testing import CliRunner
from mkdocs.__main__ import cli
from mkdocs.commands.build import build
from mkdocs.config import load_config

_DIAGRAM = (
    "```gitsvg\n"
    '{"op": "branch", "name": "main", "label_side": "before"}\n'
    '{"op": "commit", "branch": "main", "id": "c1", "msg": "init", "hash": "auto"}\n'
    "```\n"
)
_BAD_DIAGRAM = "```gitsvg\nthis is not valid jsonl\n```\n"


def _write_site(root: Path, body: str) -> Path:
    """Lay out a minimal MkDocs project (plugins: [gitsvg]) and return its config path."""
    (root / "docs").mkdir()
    (root / "docs" / "index.md").write_text(f"# Test\n\n{body}")
    config_path = root / "mkdocs.yml"
    config_path.write_text("site_name: test\nplugins:\n  - gitsvg\n")
    return config_path


def _build_index_html(tmp_path: Path, body: str) -> str:
    """Build the site and return the rendered index.html."""
    config_path = _write_site(tmp_path, body)
    site_dir = tmp_path / "site"
    config = load_config(str(config_path), site_dir=str(site_dir))
    build(config)
    return (site_dir / "index.html").read_text()


def test_build_renders_multiple_diagrams(tmp_path: Path) -> None:
    # --- act --------------------------
    html = _build_index_html(tmp_path, _DIAGRAM + "\n" + _DIAGRAM)

    # --- assert -----------------------
    assert html.count("<svg") == 2
    assert html.count('class="gitsvg-diagram"') == 2


def test_build_warn_mode_emits_error_box(tmp_path: Path) -> None:
    # --- act --------------------------
    html = _build_index_html(tmp_path, _BAD_DIAGRAM)

    # --- assert -----------------------
    assert 'class="gitsvg-error"' in html


def test_build_emits_and_links_stylesheet(tmp_path: Path) -> None:
    # --- arrange ----------------------
    config_path = _write_site(tmp_path, _DIAGRAM)
    site_dir = tmp_path / "site"

    # --- act --------------------------
    build(load_config(str(config_path), site_dir=str(site_dir)))

    # --- assert -----------------------
    assert (site_dir / "assets" / "gitsvg" / "style.css").is_file()
    assert "assets/gitsvg/style.css" in (site_dir / "index.html").read_text()


def test_strict_build_fails_on_bad_diagram(tmp_path: Path) -> None:
    # --- arrange ----------------------
    config_path = _write_site(tmp_path, _BAD_DIAGRAM)

    # --- act --------------------------
    result = CliRunner().invoke(
        cli,
        ["build", "--strict", "-f", str(config_path), "-d", str(tmp_path / "site")],
    )

    # --- assert -----------------------
    assert result.exit_code != 0
