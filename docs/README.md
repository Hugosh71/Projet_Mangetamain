# Mangetamain Documentation

This directory contains the complete documentation for the Mangetamain project, built using Sphinx.

## Quick Start

### Prerequisites

- Python 3.12+
- Poetry (for dependency management)

### Building the Documentation

1. **Install dependencies:**

```bash
# From the project root
poetry install --with dev

# Or install documentation dependencies directly
pip install -r docs/requirements.txt
```

2. **Build the documentation:**

```bash
# Using Make (from project root)
make docs

# Or manually
cd docs
sphinx-build -b html . _build/html
```

3. **View the documentation:**

```bash
# Open the built documentation
open docs/_build/html/index.html

# Or serve it locally
make docs-serve
```

## Documentation Structure

```
docs/
├── conf.py              # Sphinx configuration
├── index.rst            # Main documentation page
├── installation.rst     # Installation guide
├── usage.rst           # Usage guide
├── development.rst      # Development guide
├── contributing.rst    # Contributing guide
├── api/                # API documentation
│   ├── index.rst       # API index
│   ├── core.rst        # Core module docs
│   └── app.rst         # App module docs
├── images/             # Documentation images
│   └── logo.jpeg       # Project logo
├── requirements.txt    # Documentation dependencies
├── build_docs.py       # Documentation build script
└── README.md           # This file
```

## Building Documentation

### Using Make (Recommended)

From the project root:

```bash
# Build documentation
make docs

# Build and serve documentation
make docs-serve

# Clean documentation build
make docs-clean
```

### Using Python Script

From the docs directory:

```bash
# Clean build directory
python build_docs.py clean

# Build documentation
python build_docs.py build

# Build and serve documentation
python build_docs.py serve
```

### Manual Build

```bash
cd docs
sphinx-build -b html . _build/html
```

## Documentation Features

- **Auto-generated API docs**: Automatically generated from docstrings
- **Cross-references**: Links between different sections
- **Search functionality**: Built-in search capability
- **Responsive design**: Works on desktop and mobile
- **Theme**: Uses the Read the Docs theme

## Writing Documentation

### Adding New Pages

1. Create a new `.rst` file in the appropriate directory
2. Add it to the relevant `index.rst` file
3. Update the main `index.rst` if needed

### API Documentation

API documentation is automatically generated from docstrings. To add new API docs:

1. Add the module to `docs/api/`
2. Create a new `.rst` file for the module
3. Use Sphinx autodoc directives to include the documentation

Example:

```rst
Module Name
===========

.. automodule:: module_name
   :members:
   :undoc-members:
   :show-inheritance:
```

### Images and Media

- Place images in the `images/` directory
- Use relative paths in documentation
- Optimize images for web display

## Documentation Standards

### Docstring Style

We use Google-style docstrings throughout the project:

```python
def example_function(param1: str, param2: int) -> bool:
    """Brief description of the function.

    More detailed description of what the function does and how it works.

    Args:
        param1 (str): Description of the first parameter.
        param2 (int): Description of the second parameter.

    Returns:
        bool: Description of the return value.

    Raises:
        ValueError: Description of when this exception is raised.

    Example:
        >>> result = example_function("hello", 42)
        >>> print(result)
        True
    """
    return True
```

### reStructuredText Guidelines

- Use proper heading hierarchy
- Include cross-references where appropriate
- Use code blocks for examples
- Include table of contents for long documents

## Troubleshooting

### Common Issues

**Import errors during build:**

```bash
# Ensure the package is installed
poetry install
```

**Missing dependencies:**

```bash
# Install documentation dependencies
pip install -r docs/requirements.txt
```

**Build errors:**

```bash
# Clean and rebuild
make docs-clean
make docs
```

**Theme issues:**

```bash
# Ensure the theme is installed
pip install sphinx-rtd-theme
```

### Getting Help

If you encounter issues with the documentation:

1. Check the Sphinx documentation: https://www.sphinx-doc.org/
2. Review the project's development guide
3. Create an issue on the project repository
4. Ask questions in project discussions

## Contributing to Documentation

We welcome contributions to improve the documentation! Please see the main contributing guide for details on how to contribute.

### Documentation Contributions

- Fix typos and grammatical errors
- Improve clarity and organization
- Add examples and code snippets
- Update outdated information
- Add new sections as needed

### Review Process

All documentation changes go through the same review process as code changes:

1. Create a feature branch
2. Make your changes
3. Test the documentation build
4. Submit a pull request
5. Address review feedback

## License

The documentation is licensed under the same terms as the main project.
