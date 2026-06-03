.PHONY: help dev-setup build test format lint update-deps release

help:
	@echo 'Commands:'
	@echo '  dev-setup    One-time: sync dev deps, install pre-commit hooks'
	@echo '  build        Build package'
	@echo '  test         Run pytest'
	@echo '  format       Format and fix with ruff'
	@echo '  lint         Ruff check'
	@echo '  update-deps  Re-resolve uv.lock to latest versions'
	@echo '  release      Bump version, validate, tag, push (VERSION=X.Y.Z)'

dev-setup:
	uv sync --group dev
	uv run pre-commit install

build:
	uv build

test:
	uv run pytest

format:
	uv run ruff format mkdocs_gitsvg tests scripts
	uv run ruff check --fix mkdocs_gitsvg tests scripts

lint:
	uv run ruff check mkdocs_gitsvg tests scripts

update-deps:
	uv lock --upgrade

release:
	@test -n "$(VERSION)" || (echo "Usage: make release VERSION=X.Y.Z" && exit 1)
	$(MAKE) test
	uv run python scripts/release.py $(VERSION)
