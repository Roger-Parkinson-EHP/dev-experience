# PDF Producer

LicenseCorp Markdown to PDF Converter - Professional document generation with legal and modern styling.

## Features

- **Modern (VS Code) and Legal (Times New Roman) styling**
- **Auto-generate Table of Contents**
- **Auto-number sections** (1.1, 1.2.1, etc.)
- **Mermaid diagram rendering**
- **Light/dark themes**

## Quick Start

```bash
# Basic conversion
python markdown_to_pdf.py document.md

# Legal document with TOC and numbering
python markdown_to_pdf.py contract.md --style legal --toc --numbered

# Dark theme
python markdown_to_pdf.py README.md --theme dark --output report.pdf
```

## Options

| Flag | Effect |
|------|--------|
| `--style legal` | Times New Roman, justified, Letter size |
| `--style modern` | VS Code styling (default) |
| `--toc` | Auto-generate Table of Contents |
| `--numbered` | Section numbering (1.1, 1.2.1) |
| `--theme dark` | Dark mode (modern style only) |
| `-o, --output` | Custom output path |

## Examples

```bash
# Convert AI Policy to PDF
python markdown_to_pdf.py ../../legal/AI-POLICY-v2.md --style legal --toc

# Generate dark-themed README
python markdown_to_pdf.py ../../README.md --theme dark

# Legal contract with full formatting
python markdown_to_pdf.py contract.md --style legal --toc --numbered -o contracts/final.pdf
```

## Dependencies

```bash
pip install playwright markdown-it-py
playwright install chromium
```

The script auto-installs missing dependencies on first run.

## Convenience Scripts

```bash
# Unix/macOS
./md2pdf document.md

# Windows
.\md2pdf.ps1 document.md
```

## Origin

Consolidated from InvestorOps tools:
- `markdown_to_pdf.py` - Core converter
- `build_ppm.py` - PPM builder
- `create_numbered_version.py` - Section numbering
- `auto_generate_toc.py` - TOC generator

Version 3.0.0 - Unified for License Corporation.
