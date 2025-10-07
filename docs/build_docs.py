#!/usr/bin/env python3
"""Build script for Sphinx documentation.

This script automates the documentation building process and provides
additional functionality for documentation management.
"""

import shutil
import subprocess
import sys
from pathlib import Path


def run_command(command, cwd=None):
    """Run a shell command and return the result.

    Args:
        command (str): The command to run.
        cwd (str, optional): Working directory for the command.

    Returns:
        subprocess.CompletedProcess: The result of the command execution.
    """
    print(f"Running: {command}")
    result = subprocess.run(
        command, shell=True, cwd=cwd, capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)

    return result


def clean_docs():
    """Clean the documentation build directory."""
    build_dir = Path("_build")
    if build_dir.exists():
        print("Cleaning documentation build directory...")
        shutil.rmtree(build_dir)
        print("Build directory cleaned.")


def build_docs():
    """Build the Sphinx documentation."""
    print("Building documentation...")

    # Check if we're in the docs directory
    if not Path("conf.py").exists():
        print(
            "Error: conf.py not found. Please run this script from the docs directory."
        )
        sys.exit(1)

    # Build the documentation
    run_command("sphinx-build -b html . _build/html")
    print("Documentation built successfully!")


def serve_docs():
    """Serve the documentation locally."""
    build_dir = Path("_build/html")
    if not build_dir.exists():
        print("Documentation not built. Building first...")
        build_docs()

    print("Serving documentation at http://localhost:8000")
    print("Press Ctrl+C to stop the server.")

    try:
        run_command("python -m http.server 8000", cwd=str(build_dir))
    except KeyboardInterrupt:
        print("\nServer stopped.")


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python build_docs.py [clean|build|serve]")
        print("  clean: Clean the build directory")
        print("  build: Build the documentation")
        print("  serve: Build and serve the documentation")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "clean":
        clean_docs()
    elif command == "build":
        build_docs()
    elif command == "serve":
        serve_docs()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: clean, build, serve")
        sys.exit(1)


if __name__ == "__main__":
    main()
