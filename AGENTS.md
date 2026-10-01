# Project Guidelines

## Project Structure

- Library code lives in `src/toon_django/`.
- Framework integrations live in `src/toon_django/contrib/<framework>/` (currently `dmr`, `ninja`, `rest_framework`).
- Tests live in `tests/` and use the Django project in `tests/testapp/`.
- There are no database models or migrations; this is a pure format-integration library.

## Development Commands

- Run focused tests with `hatch run pytest tests/<test_file>.py`.
- Run the full test suite with `hatch run pytest tests/`.
- Run the full test matrix (all Python × Django version combinations) with `hatch test`.
- Run strict type checks with `hatch check types` (runs both Pyrefly and mypy).
- Run linting and code quality checks with `hatch check code`.
- Verify and apply formatting with `hatch check fmt`.

## Python and Django Conventions

- Support the Python and Django versions declared in `pyproject.toml`.
- Preserve strict typing and existing type annotations; production code is checked with both mypy and Pyrefly.
- Follow the existing Ruff configuration, including a 120-character line limit and PEP 257 docstring style.
- Python version compatibility shims live in `src/toon_django/_compat.py`; import `override`, `NotRequired`, and `Unpack` from there rather than directly from `typing` or `typing_extensions`.
- There are no custom Django settings for this library; do not introduce any.

## Framework Integrations

- Each integration is a self-contained module at `src/toon_django/contrib/<framework>/__init__.py` exposing `ToonParser` and `ToonRenderer` (or `ToonResponse` for plain Django via `src/toon_django/http.py`).
- The canonical media type is `text/toon`; use it consistently across all integrations.
- New integrations must declare a matching optional extra in `pyproject.toml` under `[project.optional-dependencies]`.

## Testing Expectations

- Add or update focused tests for every behavior change.
- Tests for optional integrations must begin with `pytest.importorskip("<framework_package>")` so they are skipped cleanly when the extra is not installed.
- Group tests for a class in a single `Test<Name>` class; prefix each test method with `test_`.
- Order test classes and methods to match the definition order in the corresponding source file.
- Run the focused test file first, then the full suite before finishing.

## Change Scope

- Keep changes minimal and consistent with neighboring code.
- Use Conventional Commits for commit messages: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, or `chore:`.
- Update `README.md` when a change affects documented behavior, public APIs, installation, or usage examples.
- Update `CHANGELOG.md` for every user-visible change under the `[Unreleased]` section before finishing. Follow the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format using the labels `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, or `Security`.
