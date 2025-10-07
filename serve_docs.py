#!/usr/bin/env python3
"""Simple script to serve the built documentation locally."""

import http.server
import os
import socketserver
import webbrowser
from pathlib import Path


def main():
    """Serve the documentation locally."""
    docs_dir = Path("docs/_build/html")

    if not docs_dir.exists():
        print("Documentation not built. Please run 'make docs' first.")
        return

    os.chdir(docs_dir)

    PORT = 8000

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(docs_dir), **kwargs)

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving documentation at http://localhost:{PORT}")
        print("Press Ctrl+C to stop the server.")

        # Open browser automatically
        webbrowser.open(f"http://localhost:{PORT}")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


if __name__ == "__main__":
    main()
