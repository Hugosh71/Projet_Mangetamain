Changelog
=========

This page contains a detailed history of all changes made to the Mangetamain project.

.. toctree::
   :maxdepth: 2

Recent Changes
--------------

Version 1.0.0 - Production Release
----------------------------------

**Release Date**: October 2025

Highlights
~~~~~~~~~~

* First production-ready release with a complete end-to-end data pipeline, clustering, ratings analysis, and improved developer experience.

New Features
~~~~~~~~~~~~

* End-to-end pipeline orchestrator to download datasets, preprocess features, run clustering, and simulate S3 upload
* Clustering pipeline with PCA and KMeans across nutrition, seasonality, and complexity features; Streamlit integration and data reload button
* Ratings module with analysers/strategies, report generation, and top-recipes caching; extensive unit and integration tests
* Centralized logging configuration with typed settings and comprehensive tests

Improvements
~~~~~~~~~~~~

* Restructured preprocessing into analysers and strategies; standardized imports and path handling; renamed ``datasets/`` to ``data/``
* Updated Streamlit pages for clustering and ratings with improved UX and formatting
* CI workflow and Docker build improvements; Poetry dependency groups and lock management

Fixes
~~~~~

* Docker and CI configuration issues (PYTHONPATH, ``.streamlit`` directory, test images)
* Missing datasets in container and assorted path typos

Version 1.0.0 - Production Release
----------------------------------

**Release Date**: October 2025

Highlights
~~~~~~~~~~

* First production-ready release with a complete end-to-end data pipeline, clustering, ratings analysis, and improved developer experience.

New Features
~~~~~~~~~~~~

* End-to-end pipeline orchestrator to download datasets, preprocess features, run clustering, and simulate S3 upload
* Clustering pipeline with PCA and KMeans across nutrition, seasonality, and complexity features; Streamlit integration and data reload button
* Ratings module with analysers/strategies, report generation, and top-recipes caching; extensive unit and integration tests
* Centralized logging configuration with typed settings and comprehensive tests

Improvements
~~~~~~~~~~~~

* Restructured preprocessing into analysers and strategies; standardized imports and path handling; renamed ``datasets/`` to ``data/``
* Updated Streamlit pages for clustering and ratings with improved UX and formatting
* CI workflow and Docker build improvements; Poetry dependency groups and lock management

Fixes
~~~~~

* Docker and CI configuration issues (PYTHONPATH, ``.streamlit`` directory, test images)
* Missing datasets in container and assorted path typos

Version 0.1.0 - Documentation System
------------------------------------

**Release Date**: November 2025

This release introduces a comprehensive documentation system and significant improvements to code quality and developer experience.

New Features
~~~~~~~~~~~~

* **Complete Documentation System**: 
  - Sphinx-based documentation with professional theme
  - Auto-generated API documentation from docstrings
  - Comprehensive installation and usage guides
  - Developer and contributing guidelines

* **Enhanced Code Quality**:
  - Google-style docstrings throughout the codebase
  - Type hints for all functions and methods
  - Comprehensive code comments for complex sections
  - Automated code formatting and linting

* **Development Tools**:
  - Documentation build system with automated scripts
  - Enhanced testing framework
  - Improved development workflow
  - Better dependency management

* **Project Structure**:
  - Professional documentation layout
  - Clear API reference
  - Installation guides for all platforms
  - Usage examples and best practices

Improvements
~~~~~~~~~~~~

* **Code Documentation**: All classes, methods, and functions now have comprehensive docstrings
* **Type Safety**: Added type hints throughout the codebase
* **Developer Experience**: Improved development tools and workflows
* **Project Organization**: Better structure and organization of project files

Technical Details
~~~~~~~~~~~~~~~~~

* **Documentation**: Sphinx 7.4.7+ with Read the Docs theme
* **Code Quality**: Black, Ruff, and Flake8 for formatting and linting
* **Testing**: pytest with comprehensive test coverage
* **Docker**: Containerized development and deployment
* **CI/CD**: Automated testing and quality checks

Breaking Changes
~~~~~~~~~~~~~~~~

None in this release.

Migration Guide
~~~~~~~~~~~~~~~

No migration required for this release.

Full Changelog
--------------

For a complete history of all changes, see the `CHANGELOG.md <../CHANGELOG.md>`_ file in the project root.

Key Milestones
--------------

* **v0.1.0**: Complete documentation system and enhanced code quality
* **v0.0.1**: Initial project setup and basic structure

Future Releases
---------------

Planned features for upcoming releases:

* **v0.2.0**: Enhanced data visualization features
* **v0.3.0**: Advanced analytics capabilities
* **v1.0.0**: Production-ready release with full feature set

Contributing to Changelog
-------------------------

When contributing to the project, please update the changelog following these guidelines:

1. **Add entries under the appropriate version section**
2. **Use clear, descriptive language**
3. **Include relevant issue numbers when applicable**
4. **Follow the established format and categories**
5. **Update version information when releasing**
