# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-10-01

### Added

- Django Ninja integration (`toon_django.contrib.ninja`).

### Changed

- The canonical media type is now `text/toon` across all integrations (was `application/x-toon`).

## [0.0.1] - 2026-08-13

### Added

- `ToonResponse`: a `JsonResponse`-style shortcut for returning TOON-encoded responses from plain Django views.
- Django Modern REST integration (`toon_django.contrib.dmr`).
- Django REST Framework integration (`toon_django.contrib.rest_framework`).

[Unreleased]: https://github.com/hartungstenio/toon-django/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/hartungstenio/toon-django/compare/0.0.1...v0.1.0
[0.0.1]: https://github.com/hartungstenio/toon-django/releases/tag/0.0.1
