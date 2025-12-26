#!/bin/bash
#
# LicenseCorp Markdown to PDF Converter - Convenience Script
# Usage: ./md2pdf document.md [--theme light|dark] [--output custom.pdf]
# Can be called from anywhere in the project
#

# Find the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Try to find and activate a virtual environment
if [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
elif [ -f "$SCRIPT_DIR/../.venv/bin/activate" ]; then
    source "$SCRIPT_DIR/../.venv/bin/activate"
fi

# Call the Python script with all arguments
python "$SCRIPT_DIR/markdown_to_pdf.py" "$@"
