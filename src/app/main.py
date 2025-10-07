"""Main application entry point for Mangetamain.

This module serves as the primary entry point for the Streamlit application.
It initializes the application and sets up the main interface components.
"""

import streamlit as st

from mangetamain.core import get_app_config


def main():
    """Main application function.

    This function initializes the Streamlit application, sets up the page
    configuration, and renders the main interface components.
    """
    # Get application configuration
    config = get_app_config()

    # Configure the page
    st.set_page_config(
        page_title=config.name,
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Display the main title
    st.title(f"Welcome to {config.name}")
    st.markdown(f"Version: {config.version}")

    # Add a simple placeholder for the main content
    st.markdown(
        """
    ## Getting Started

    This is the main interface of the Mangetamain application.
    Here you can explore your data and perform various analyses.

    ### Features
    - Data visualization
    - Statistical analysis
    - Interactive charts
    - Export capabilities
    """
    )


if __name__ == "__main__":
    # Entry point for the Streamlit application
    main()
