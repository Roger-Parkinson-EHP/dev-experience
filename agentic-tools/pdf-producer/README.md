# PDF Producer

Convert Markdown documents to professional PDFs.

## Why

Legal documents, policies, and proposals often need PDF format for:
- Signatures and formal distribution
- Consistent rendering across devices
- Archival and compliance

## Quick Start

### Option 1: Pandoc (Recommended)

```bash
# Install (one-time)
# Windows: winget install pandoc
# macOS: brew install pandoc
# Linux: apt install pandoc

# Convert
pandoc legal/AI-POLICY-v2.md -o AI-POLICY-v2.pdf
```

### Option 2: VS Code Extension

1. Install "Markdown PDF" extension
2. Open any `.md` file
3. `Ctrl+Shift+P` → "Markdown PDF: Export (pdf)"

### Option 3: Python (markdown-pdf)

```bash
pip install markdown-pdf
markdown-pdf legal/AI-POLICY-v2.md
```

## Batch Conversion

Convert all markdown in a folder:

```bash
# PowerShell
Get-ChildItem legal/*.md | ForEach-Object { pandoc $_.FullName -o ($_.BaseName + ".pdf") }

# Bash
for f in legal/*.md; do pandoc "$f" -o "${f%.md}.pdf"; done
```

## Styling

For branded PDFs, use a custom template:

```bash
pandoc doc.md -o doc.pdf --template=templates/lc-template.tex
```

## Integration with CI/CD

Add to GitHub Actions to auto-generate PDFs on legal document changes:

```yaml
- name: Generate PDFs
  run: |
    sudo apt-get install -y pandoc texlive-latex-base
    pandoc legal/AI-POLICY-v2.md -o legal/AI-POLICY-v2.pdf
```

## Related

- [Pandoc Documentation](https://pandoc.org/)
- [LaTeX Templates](https://www.latextemplates.com/)
