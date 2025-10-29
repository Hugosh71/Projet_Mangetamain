# Changelog

All notable changes to the Mangetamain project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-10-29

### Added
- End-to-end pipeline orchestrator `src/app/run_all.py` for dataset download, preprocessing, clustering, and S3 upload simulation (0ed2d93, 121b82f)
- Clustering pipeline with PCA and KMeans using nutrition, seasonality, and complexity features; Streamlit integration and data reload button (5561907, 191f81b)
- Rating module with analysers/strategies, report generation, top recipes caching, and comprehensive unit/integration tests (f4562f4, fdaa369, cfe50e8, 3ce60c2)
- Centralized logging configuration with `LoggingSettings` and robust tests (cc5c91d, 5c7578d, dd17272)
- CI workflow and Docker build; Poetry dependency groups and lock management (ba18f78, d719223, e760ad9)

### Changed
- Restructured preprocessing into `src/mangetamain/preprocessing/*` with analysers and strategies; renamed `datasets/` to `data/`; standardized imports and path handling (9f7fd03, cc37526, 3d52ae0, 5a79cc0)
- Updated Streamlit pages for clustering and ratings, improved formatting and layout, and integrated pipeline features (82caece, 16fe8c2, 191f81b)

### Fixed
- Docker and CI configuration issues (PYTHONPATH, `.streamlit` dir, test images) (fdbccac, 0fd75ef, 79c4b40)
- Missing datasets in container and assorted path typos (52fc738, 8a91c2b)

### Documentation
- Expanded Sphinx docs and README usage; improved changelog and documentation structure (4bdf6d5, 0e6b6e2, 091b130)

### Added
- Comprehensive Sphinx documentation system with professional theme
- API documentation with auto-generated docs from docstrings
- Installation guide for Windows, macOS, and Linux platforms
- Usage guide with best practices and troubleshooting
- Development guide for contributors with setup instructions
- Contributing guidelines and community standards
- Documentation build system with automated scripts
- Google-style docstrings throughout the codebase
- Type hints for all functions and methods
- Code comments for complex sections
- Changelog system for tracking project changes
- Documentation serving scripts for local development
- Enhanced project structure with clear organization

### Changed
- Enhanced `src/mangetamain/core.py` with comprehensive docstrings
- Improved `src/app/main.py` with proper documentation and comments
- Updated project dependencies to include Sphinx and documentation tools
- Refactored code formatting to follow project standards
- Improved project structure with better organization
- Enhanced development workflow with documentation tools

### Documentation
- Added comprehensive Sphinx documentation system
- Created detailed installation and usage guides
- Added API documentation with auto-generation
- Implemented development and contributing guides
- Added changelog system for project tracking
- Created documentation build and serving scripts

### Fixed
- Code formatting inconsistencies
- Missing documentation for core modules
- Incomplete API documentation
- Lack of development guidelines

### Added
- Initial project structure with Python package layout
- Core configuration system with `AppConfig` class
- Streamlit application entry point
- Basic test suite with unit and integration tests
- Docker support with Dockerfile and docker-compose.yml
- Poetry configuration for dependency management
- Pre-commit hooks for code quality
- Makefile for common development tasks
- CI/CD pipeline with automated testing
- Project logo and branding assets

### Features
- **Core Module**: Application configuration and utilities
- **Streamlit App**: Modern web interface for data analysis
- **Testing**: Comprehensive test coverage with pytest
- **Docker**: Containerized deployment support
- **Code Quality**: Automated linting and formatting
- **Development**: Pre-commit hooks and development tools

### Technical Details
- Python 3.12+ support
- Streamlit 1.49.1+ for web interface
- Poetry for dependency management
- Docker for containerization
- pytest for testing
- Black and Ruff for code formatting
- Pre-commit for automated quality checks

## [0.0.1] - 2024-01-XX

### Added
- Initial project setup
- Basic project structure
- Git repository initialization
- Initial README.md

---

## Release Notes

### Version 0.1.0
This is the first stable release of Mangetamain, featuring:

- **Complete Documentation System**: Comprehensive Sphinx-based documentation with installation guides, usage instructions, API reference, and development guidelines
- **Enhanced Code Quality**: Google-style docstrings, type hints, and comprehensive code comments
- **Developer Experience**: Automated build system, testing framework, and development tools
- **Production Ready**: Docker support, CI/CD pipeline, and deployment configurations

### Key Improvements in 0.1.0
- 📚 **Documentation**: Complete documentation system with Sphinx
- 🔧 **Code Quality**: Enhanced docstrings and type hints
- 🚀 **Development**: Improved development workflow and tools
- 📦 **Packaging**: Better dependency management and build system
- 🐳 **Deployment**: Docker support and containerization
- ✅ **Testing**: Comprehensive test suite and quality checks

### Breaking Changes
None in this release.

### Migration Guide
No migration required for this initial release.

---

## Contributing to the Changelog

When adding new features or fixes, please update this changelog following these guidelines:

1. **Add entries under the appropriate version section**
2. **Use the following categories:**
   - `Added` for new features
   - `Changed` for changes in existing functionality
   - `Deprecated` for soon-to-be removed features
   - `Removed` for now removed features
   - `Fixed` for any bug fixes
   - `Security` for vulnerability fixes

3. **Follow the format:**
   ```markdown
   ### Added
   - Description of the new feature
   
   ### Changed
   - Description of what changed
   
   ### Fixed
   - Description of the bug fix
   ```

4. **Keep entries concise but descriptive**
5. **Include relevant issue numbers when applicable**
6. **Update the version date when releasing**

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

## Release Process

1. Update version numbers in `pyproject.toml`
2. Update this changelog with the new version
3. Create a git tag for the release
4. Push changes and tags to the repository
5. Create a GitHub release with release notes
