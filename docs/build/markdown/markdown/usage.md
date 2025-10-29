# Usage Guide

This guide explains how to use the Mangetamain application effectively.

# Getting Started

## Starting the Application

After installation, start the application using one of these methods:

**Using Poetry (Recommended for development):**

```bash
make run
```

**Using Docker:**

```bash
docker compose up app
```

**Using Docker directly:**

```bash
make docker-run
```

The application will be available at http://localhost:8501.

# Application Interface

The Mangetamain application provides a modern, intuitive web interface built with Streamlit. The interface includes:

* **Navigation**: Easy-to-use sidebar navigation
* **Data Visualization**: Interactive charts and graphs
* **Data Analysis**: Comprehensive data exploration tools
* **Export Features**: Download results in various formats

# Key Features

## Data Analysis

Mangetamain provides powerful data analysis capabilities:

* **Data Loading**: Support for various data formats (CSV, Excel, JSON)
* **Data Exploration**: Statistical summaries and data profiling
* **Visualization**: Interactive charts and graphs
* **Filtering**: Advanced filtering and search capabilities

## Visualization Tools

The application includes comprehensive visualization tools:

* **Charts**: Bar charts, line charts, scatter plots, and more
* **Interactive Elements**: Zoom, pan, and hover interactions
* **Customization**: Color schemes, themes, and styling options
* **Export**: Save visualizations as images or PDFs

## Data Management

* **Data Import**: Load data from various sources
* **Data Cleaning**: Tools for data preprocessing
* **Data Transformation**: Reshape and transform data
* **Data Export**: Save processed data in multiple formats

# Advanced Usage

## Configuration

The application can be configured through environment variables or configuration files:

**Environment Variables:**

```bash
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

**Configuration File:**

Create a .streamlit/config.toml file:

```toml
[server]
port = 8501
address = "0.0.0.0"

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
```

## Customization

The application can be customized for different use cases:

* **Themes**: Custom color schemes and styling
* **Layout**: Adjustable sidebar and main content areas
* **Components**: Add or remove interface components
* **Data Sources**: Configure different data sources

# Performance Optimization

For large datasets, consider these optimization strategies:

* **Data Sampling**: Use data sampling for initial exploration
* **Caching**: Enable Streamlit caching for repeated operations
* **Memory Management**: Monitor memory usage with large datasets
* **Parallel Processing**: Use multiprocessing for intensive computations

# Best Practices

## Data Handling

* **Data Validation**: Always validate data before processing
* **Error Handling**: Implement proper error handling for data operations
* **Data Backup**: Keep backups of important datasets
* **Version Control**: Use version control for data processing scripts

## User Experience

* **Loading Indicators**: Use loading indicators for long operations
* **Error Messages**: Provide clear, actionable error messages
* **Help Text**: Include helpful descriptions and tooltips
* **Responsive Design**: Ensure the interface works on different screen sizes

# Security Considerations

* **Data Privacy**: Ensure sensitive data is handled securely
* **Access Control**: Implement appropriate access controls
* **Data Encryption**: Use encryption for sensitive data
* **Audit Logging**: Log important operations for security auditing

# Troubleshooting

## Common Issues

**Application won’t start:**

```bash
# Check if port is available
netstat -an | grep 8501

# Use a different port
streamlit run src/app/main.py --server.port=8502
```

**Memory issues with large datasets:**

```python
# Use data sampling
import pandas as pd
df_sample = df.sample(n=10000)  # Sample 10k rows
```

**Slow performance:**

```python
# Enable caching
@st.cache_data
def expensive_computation(data):
    return data.process()
```

**Browser compatibility issues:**

* Use modern browsers (Chrome, Firefox, Safari, Edge)
* Enable JavaScript
* Clear browser cache if needed

# Getting Help

If you encounter issues:

1. **Check the logs**: Look for error messages in the console
2. **Review documentation**: Check this guide and API documentation
3. **Community support**: Check GitHub issues and discussions
4. **Report bugs**: Create an issue on the project repository

# Next Steps

After mastering the basic usage:

1. Explore the [API Reference](api/index.md) for detailed API documentation
2. Check the development guide for contributing to the project
3. Learn about advanced features and customization options
