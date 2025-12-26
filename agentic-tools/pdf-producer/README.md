# PDF Producer

LicenseCorp Markdown to PDF Converter - Professional document generation with legal and modern styling, plus official LC branding.

**Version 3.1.0** - Now with branded header/footer support for official documents.

## Features

- **Modern (VS Code) and Legal (Times New Roman) styling**
- **Official LC branding** - Logo header, confidential footer, page numbers
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

# Official branded document (LC header/footer)
python markdown_to_pdf.py proposal.md --branded --style legal --toc

# Dark theme
python markdown_to_pdf.py README.md --theme dark --output report.pdf
```

## Options

| Flag | Effect |
|------|--------|
| `--branded` | **Add LC branding** - logo, footer, page numbers |
| `--no-confidential` | Remove "Confidential" from footer |
| `--style legal` | Times New Roman, justified, Letter size |
| `--style modern` | VS Code styling (default) |
| `--toc` | Auto-generate Table of Contents |
| `--numbered` | Section numbering (1.1, 1.2.1) |
| `--theme dark` | Dark mode (modern style only) |
| `-o, --output` | Custom output path |

## Branded Documents

The `--branded` flag adds official License Corporation branding:

**Header:**
- LC logo (left)
- Document title (right)
- Orange accent border

**Footer:**
- "License Corporation - Confidential" (or just company name with `--no-confidential`)
- Page numbers (Page X of Y)
- Generation date

```bash
# Official proposal
python markdown_to_pdf.py proposal.md --branded --style legal --toc

# Contract with full formatting
python markdown_to_pdf.py contract.md --branded --style legal --toc --numbered

# Public document (no "Confidential")
python markdown_to_pdf.py whitepaper.md --branded --no-confidential --toc
```

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

## Brand Integration

See [brand/](../../brand/) for License Corporation brand guidelines and colors.

### Recommended Document Styles

| Document Type | Style | Theme | Flags |
|---------------|-------|-------|-------|
| Legal contracts | legal | light | `--toc --numbered` |
| Policies | legal | light | `--toc` |
| Technical docs | modern | dark | `--toc` |
| Client-facing | modern | light | - |
| Internal reports | modern | light/dark | - |

### IP Protection

**Everything created through this tool is License Corporation intellectual capital.**

It doesn't matter which AI assisted - if it goes through our development process, it's ours. The dev-experience repository ensures safe, compliant creation workflows.

## Origin

Consolidated from InvestorOps tools:
- `markdown_to_pdf.py` - Core converter
- `build_ppm.py` - PPM builder
- `create_numbered_version.py` - Section numbering
- `auto_generate_toc.py` - TOC generator

Version 3.0.0 - Unified for License Corporation.
