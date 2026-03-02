# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, adapted to the existing project release history.

## [Unreleased]

## [1.0.0]

### Added
- Dedicated `CHANGELOG.md` for structured release tracking.
- Modern React/TypeScript frontend with Monaco editor.
- FastAPI backend with OpenAPI/Swagger documentation.
- Docker Compose setup for frontend and backend.

### Changed
- Consolidate RTD user/API content to Markdown canonical sources (`docs/docs.md`, `docs/api.md`).
- Include project README in RTD navigation via `docs/readme.md`.
- Add release notes page in RTD navigation via `docs/RELEASE.md`.
- Update RTD index page to explicitly list WASM, Docker, and Python usage modes.
- Enable Markdown parsing in Sphinx with `myst-parser`.
- Update docs build dependency installation in CI to use `docs/requirements.txt`.
- Remove duplicate `.rst` content pages that diverged from Markdown pages.
- CI coverage expanded for modern backend/frontend workflows.
- Python CI matrix updated to 3.12 and 3.13 with 3.14-dev experimental.

### Fixed
- Resolve CI/RTD docs build failure: `No module named 'myst_parser'`.
- Simplify parser grammar by removing unreachable `SPACE` and `NEWLINE` statement productions.


## [0.9.0]

### Fixed
- CSV handling error correction.

## [0.8.0]

### Added
- Spreadsheet support (`.ods`, `.xls`, `.xlsx`).
- GitHub workflow support.

### Changed
- Code style cleanup (PEP8 / pycodestyle).

## [0.7.0]

### Added
- Support for multiple input CSV files from CLI.
- `--run` option to start web application from CLI.

## [0.6.0]

### Changed
- Reorganized CLI argument parsing and web app code into `shexstatements/`.
- Prepared packaging configuration for `pip`.

## [0.5.0]

### Added
- Public API support with JSON input/output format.
- CSV file upload support in web interface.
- API documentation.

## [0.4.0]

### Added
- Flask-based web interface for online ShEx generation.
- Support for `IMPORT`, `><` (`CLOSED`), `++` (`EXTRA`), and `#` in node names.
- Code coverage and GitHub Actions test integration.
- Additional examples including datasets, API/SPARQL endpoints, and hospital example.

### Fixed
- Shift-reduce parser conflict.
- Unit test updates and Python 3.5 removal.

## [0.3.0]

### Added
- Installation and virtualenv documentation improvements.
- Additional cardinality forms (`?`, `m,`).
- Negative statements.
- Case-insensitive node kinds (`Literal`, `BNode`, `NonLiteral`, `IRI`).
- Type support in third column (`@@` prefix).

## [0.2.0]

### Added
- CSV header skipping (`--skipheader` / `-s`).
- ShExJ generation from CSV (`--shexj` / `-j`).
- Application profile input support (`--applicationprofile` / `-ap`).
- Additional cardinality forms (`number`, `number,number`).

## [0.1.0]

### Added
- Initial ShEx generation from CSV files.
- Prefix support and keywords such as `EXTRA` and `CLOSED`.
