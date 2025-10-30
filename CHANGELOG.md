# Changelog

All notable changes to the Mangetamain project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3]

### Changed
- Logging configuration improvements and cleanup across modules
- README clarity and structure improvements

### Documentation
- Sphinx docs updates (pages and formatting)
- Additional docstrings for analysers and steps

## [1.0.2] - 2025-10-29

### Documentation
- Add usage guide to docs
- Add Markdown documentation pages
- Update Sphinx docs
- Add docstrings to nutrition analyser

## [1.0.1] - 2025-10-29

### Added
- `scripts/run_pipeline.sh` helper script
- `__init__` in feature package
- Methodology page and navigation updates in the app

### Changed
- Update Streamlit pages (UX and layout)

### Fixed
- Address lint errors

### Documentation
- Update README
- Add/extend docstrings in analysers
- General docs improvements

## [1.0.0] - 2025-10-29

### Added
- End-to-end pipeline orchestrator `src/app/run_all.py` for dataset download, preprocessing, clustering, and S3 upload simulation
- Clustering pipeline with PCA and KMeans using nutrition, seasonality, and complexity features; Streamlit integration and data reload
- Rating module with analysers/strategies, report generation, top recipes caching, and extensive unit/integration tests
- Centralized logging settings and configuration
- CI workflow, Docker build, and Poetry dependency groups

### Changed
- Restructure preprocessing into analysers and strategies under `src/mangetamain/preprocessing/*`
- Rename `datasets/` to `data/`; standardize imports and path handling
- Update Streamlit pages for clustering and ratings with improved UX/formatting

### Fixed
- Docker/CI configuration issues (PYTHONPATH, `.streamlit` directory, test images)
- Missing datasets in container and assorted path typos

### Documentation
- Expanded Sphinx docs and README usage; improved documentation structure

## [0.0.1] - 2024-01-XX

### Added
- Initial project setup and structure
- Git repository initialization
- Initial README

---

## How to perform a release on GitHub

1) Prepare the release branch from `develop`:
```powershell
git fetch origin
git checkout -b release/vX.Y.Z origin/develop
poetry version X.Y.Z
# Also align src\mangetamain\__init__.py -> __version__ = "X.Y.Z"
```

2) Update the changelog and commit:
```powershell
git add pyproject.toml src\mangetamain\__init__.py CHANGELOG.md
git commit -m "chore(release): bump to vX.Y.Z and update changelog"
git push -u origin release/vX.Y.Z
```

3) Open a PR `release/vX.Y.Z` → `main`, ensure CI is green, then merge.

4) Tag on `main` (annotated) and push:
```powershell
git checkout main
git pull origin main
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

5) Create the GitHub Release using tag `vX.Y.Z` with notes from `CHANGELOG.md`.

6) Sync `main` back to `develop`:
```powershell
git checkout develop
git pull origin develop
git merge --no-ff main
git push origin develop
```

Tip: for hotfixes, branch from `main` (`hotfix/vX.Y.Z`), tag, then merge back to both `main` and `develop`.
