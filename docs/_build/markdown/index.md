# Welcome to Mangetamain’s documentation!

![Mangetamain Logo](images/logo.jpeg)

Mangetamain is a modern Streamlit-based web application designed for data analysis and visualization. This documentation provides comprehensive information about the application’s architecture, installation, usage, and API reference.

# Contents:

* [Installation Guide](installation/index.md)
  * [Prerequisites](installation/prerequisites.md)
    * [Installing Python 3.12](installation/prerequisites.md#installing-python-3-12)
    * [For Linux (Ubuntu/Debian)](installation/prerequisites.md#for-linux-ubuntu-debian)
    * [Installing Poetry](installation/prerequisites.md#installing-poetry)
    * [Installing Git](installation/prerequisites.md#installing-git)
  * [Environment Setup](installation/setup.md)
    * [Method 1: Using Poetry (Recommended)](installation/setup.md#method-1-using-poetry-recommended)
    * [Method 2: Using Docker](installation/setup.md#method-2-using-docker)
    * [Method 3: Using Docker Compose](installation/setup.md#method-3-using-docker-compose)
    * [Verification](installation/setup.md#verification)
    * [Troubleshooting](installation/setup.md#troubleshooting)
    * [Next Steps](installation/setup.md#next-steps)
* [Development Guide](development/index.md)
  * [Getting Started with Development](development/getting_started.md)
    * [Prerequisites](development/getting_started.md#prerequisites)
    * [Development Setup](development/getting_started.md#development-setup)
  * [Project Structure](development/project_structure.md)
  * [Code Style and Standards](development/code_style.md)
    * [Code Formatting](development/code_style.md#code-formatting)
    * [Docstring Style](development/code_style.md#docstring-style)
    * [Type Hints](development/code_style.md#type-hints)
    * [Testing](development/code_style.md#testing)
    * [Writing Tests](development/code_style.md#writing-tests)
  * [Docker Development](development/docker.md)
  * [Git Workflow](development/git.md)
    * [Branching Strategy](development/git.md#branching-strategy)
    * [Commit Guidelines](development/git.md#commit-guidelines)
    * [Pull Request Process](development/git.md#pull-request-process)
* [Usage Guide](usage/index.md)
  * [Getting Started](usage/getting_started.md)
    * [Starting the Application](usage/getting_started.md#starting-the-application)
  * [Application Interface](usage/interface.md)
  * [Key Features](usage/interface.md#key-features)
  * [Advanced Usage](usage/interface.md#advanced-usage)
  * [Performance Optimization](usage/interface.md#performance-optimization)
  * [Best Practices](usage/interface.md#best-practices)
  * [Troubleshooting](usage/interface.md#troubleshooting)
  * [Getting Help](usage/interface.md#getting-help)
  * [Next Steps](usage/interface.md#next-steps)
* [API Reference](api/index.md)
  * [mangetamain package](api/mangetamain.md)
    * [Subpackages](api/mangetamain.md#subpackages)
    * [Submodules](api/mangetamain.md#submodules)
    * [mangetamain.core module](api/mangetamain.md#module-mangetamain.core)
    * [Module contents](api/mangetamain.md#module-mangetamain)
* [Changelog](changelog.md)
  * [Recent Changes](changelog.md#recent-changes)
  * [Version 1.0.0 - Production Release](changelog.md#version-1-0-0-production-release)
    * [Highlights](changelog.md#highlights)
    * [New Features](changelog.md#new-features)
    * [Improvements](changelog.md#improvements)
    * [Fixes](changelog.md#fixes)
  * [Version 0.1.0 - Documentation System](changelog.md#version-0-1-0-documentation-system)
    * [New Features](changelog.md#id1)
    * [Improvements](changelog.md#id2)
    * [Technical Details](changelog.md#technical-details)
    * [Breaking Changes](changelog.md#breaking-changes)
    * [Migration Guide](changelog.md#migration-guide)
  * [Full Changelog](changelog.md#full-changelog)
  * [Key Milestones](changelog.md#key-milestones)
  * [Future Releases](changelog.md#future-releases)
  * [Contributing to Changelog](changelog.md#contributing-to-changelog)

## Features

* **Modern Web Interface**: Built with Streamlit for an intuitive user experience
* **Data Analysis**: Comprehensive tools for data exploration and visualization
* **Docker Support**: Easy deployment with containerization
* **Testing**: Comprehensive test suite with unit and integration tests
* **Code Quality**: Automated linting, formatting, and pre-commit hooks

## Quick Start

If you’re eager to get started quickly:

```bash
# Clone the repository
git clone https://github.com/Hugosh71/Projet_Mangetamain.git
cd Projet_Mangetamain

# Install dependencies
make requirements

# Run the application
make run

# or use docker
docker compose up app
```

The application will be available at http://localhost:8501.

## Indices and tables

* [Index](genindex.md)
* [Module Index](py-modindex.md)
* [Search Page](search.md)
