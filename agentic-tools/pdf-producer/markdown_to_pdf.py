#!/usr/bin/env python3
"""
LicenseCorp Markdown to PDF Converter
Consolidated professional markdown-to-PDF with legal document support

Features:
  - Modern (VS Code) and Legal (Times New Roman) styling
  - Auto-generate Table of Contents
  - Auto-number sections (1.1, 1.2.1, etc.)
  - Mermaid diagram rendering
  - Light/dark themes

Usage:
    python markdown_to_pdf.py document.md
    python markdown_to_pdf.py document.md --style legal --toc --numbered
    python markdown_to_pdf.py document.md --theme dark --output report.pdf

Origin: Consolidated from InvestorOps (markdown_to_pdf.py, build_ppm.py,
        create_numbered_version.py, auto_generate_toc.py)
"""

import asyncio
import argparse
import sys
import re
from pathlib import Path

__version__ = "3.1.0"
__project__ = "LicenseCorp"

# ============================================================
# BRAND CONFIGURATION
# ============================================================

LC_BRAND = {
    "logo_url": "https://storage.googleapis.com/a4ee1cbc43b25bc8-public-website-prod/LC_Logo_Black.png",
    "company_name": "License Corporation",
    "colors": {
        "primary_orange": "#ef6820",
        "primary_purple": "#7839ee",
        "charcoal": "#1e1a1c",
        "accent_green": "#26da42",
        "accent_blue": "#4440ff",
    },
    "confidential_text": "License Corporation - Confidential",
    "footer_text": "License Corporation | Proprietary & Confidential",
}

# ============================================================
# PREPROCESSING: TOC and Numbering
# ============================================================

def create_anchor_link(header_text):
    """Create GitHub-style anchor link from header text"""
    # Remove any existing numbers
    clean_text = re.sub(r'^\d+(\.\d+)*\.?\s+', '', header_text)
    anchor = clean_text.lower()
    anchor = re.sub(r'[^\w\s-]', '', anchor)
    anchor = re.sub(r'\s+', '-', anchor)
    anchor = re.sub(r'-+', '-', anchor)
    return anchor.strip('-')


def extract_headers(content, skip_headers=None):
    """Extract headers from markdown content"""
    if skip_headers is None:
        skip_headers = ['Table of Contents']

    headers = []
    lines = content.split('\n')

    for line_num, line in enumerate(lines, 1):
        match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()

            if not any(skip.lower() in text.lower() for skip in skip_headers):
                headers.append({
                    'level': level,
                    'text': text,
                    'line': line_num,
                    'anchor': create_anchor_link(text)
                })

    return headers


def generate_toc_markdown(headers, max_level=2):
    """Generate TOC markdown from headers list"""
    toc_lines = ["## Table of Contents", ""]

    for header in headers:
        if header['level'] <= max_level:
            indent = "  " * (header['level'] - 1)
            # Remove any existing numbering from display
            clean_text = re.sub(r'^\d+(\.\d+)*\.?\s+', '', header['text'])
            link = f"{indent}- [{clean_text}](#{header['anchor']})"
            toc_lines.append(link)

    toc_lines.append("")
    return '\n'.join(toc_lines)


def add_section_numbering(content, skip_headers=None):
    """Add hierarchical section numbering to headers"""
    if skip_headers is None:
        skip_headers = ['Table of Contents']

    lines = content.split('\n')
    numbered_lines = []

    # Counters for each level
    counters = [0] * 7  # h1-h6 + buffer

    for line in lines:
        match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()

            # Check if should skip
            if any(skip.lower() in text.lower() for skip in skip_headers):
                numbered_lines.append(line)
                continue

            # Remove existing numbering
            clean_text = re.sub(r'^\d+(\.\d+)*\.?\s+', '', text)

            # Increment counter for this level, reset deeper levels
            counters[level] += 1
            for i in range(level + 1, 7):
                counters[i] = 0

            # Build number string
            number_parts = [str(counters[i]) for i in range(1, level + 1) if counters[i] > 0]
            number_string = '.'.join(number_parts)

            numbered_lines.append(f"{'#' * level} {number_string}. {clean_text}")
        else:
            numbered_lines.append(line)

    return '\n'.join(numbered_lines)


def insert_toc(content, toc_markdown):
    """Insert TOC after first header or at beginning"""
    lines = content.split('\n')

    # Find first h1
    for i, line in enumerate(lines):
        if line.startswith('# '):
            # Insert TOC after first header
            lines.insert(i + 1, '\n' + toc_markdown)
            return '\n'.join(lines)

    # No h1 found, insert at beginning
    return toc_markdown + '\n' + content


# ============================================================
# CONVERTER CLASS
# ============================================================

class LCMarkdownConverter:
    """Consolidated markdown-to-PDF converter with legal document support"""

    def __init__(self, style="modern", theme="light", branded=False, confidential=True):
        self.style = style  # "modern" or "legal"
        self.theme = theme  # "light" or "dark"
        self.branded = branded  # Add LC branding (header/footer)
        self.confidential = confidential  # Mark as confidential
        self.mermaid_diagrams_found = 0

    def _get_header_template(self, title=""):
        """Generate branded header HTML for PDF"""
        if not self.branded:
            return ""

        return f"""
        <div style="width: 100%; font-size: 9px; padding: 5px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid {LC_BRAND['colors']['primary_orange']}; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <img src="{LC_BRAND['logo_url']}" style="height: 24px; width: auto;" />
            </div>
            <div style="color: {LC_BRAND['colors']['charcoal']}; font-family: 'Inter', -apple-system, sans-serif;">
                {title}
            </div>
        </div>
        """

    def _get_footer_template(self):
        """Generate branded footer HTML for PDF"""
        if not self.branded:
            return ""

        conf_text = LC_BRAND['confidential_text'] if self.confidential else LC_BRAND['company_name']

        return f"""
        <div style="width: 100%; font-size: 8px; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #e0e0e0; color: #666; font-family: 'Inter', -apple-system, sans-serif;">
            <div>{conf_text}</div>
            <div>Page <span class="pageNumber"></span> of <span class="totalPages"></span></div>
            <div style="color: {LC_BRAND['colors']['primary_orange']};">Generated <span class="date"></span></div>
        </div>
        """

    def get_css(self):
        """Get CSS based on style and theme"""
        if self.style == "legal":
            return self._get_legal_css()
        else:
            return self._get_modern_css()

    def _get_legal_css(self):
        """Legal document styling - Times New Roman, justified, formal"""
        return """
/* LicenseCorp Legal Document Styling */
@page {
    size: letter;
    margin: 1in;
}

body {
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt;
    line-height: 1.5;
    color: #000;
    margin: 0;
    padding: 0 20px;
    background-color: #fff;
}

h1 {
    font-size: 18pt;
    font-weight: bold;
    margin-top: 24pt;
    margin-bottom: 12pt;
    text-align: center;
    color: #000;
}

h2 {
    font-size: 14pt;
    font-weight: bold;
    margin-top: 18pt;
    margin-bottom: 6pt;
    color: #000;
}

h3 {
    font-size: 12pt;
    font-weight: bold;
    margin-top: 12pt;
    margin-bottom: 6pt;
    color: #000;
}

h4, h5, h6 {
    font-size: 12pt;
    font-weight: bold;
    margin-top: 12pt;
    margin-bottom: 3pt;
    color: #000;
}

p {
    margin: 6pt 0;
    text-align: justify;
}

ul, ol {
    margin: 6pt 0;
    padding-left: 24pt;
}

li {
    margin: 3pt 0;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 12pt 0;
    font-size: 11pt;
}

th, td {
    border: 1pt solid #000;
    padding: 6pt 10pt;
    text-align: left;
}

th {
    background-color: #f0f0f0;
    font-weight: bold;
}

a {
    color: #000;
    text-decoration: underline;
}

hr {
    border: none;
    border-top: 1pt solid #000;
    margin: 12pt 0;
}

blockquote {
    border-left: 3pt solid #666;
    margin: 12pt 0;
    padding-left: 12pt;
    font-style: italic;
}

pre, code {
    font-family: 'Courier New', Courier, monospace;
    font-size: 10pt;
    background-color: #f5f5f5;
    padding: 2pt 4pt;
}

pre {
    padding: 12pt;
    margin: 12pt 0;
    border: 1pt solid #ddd;
    overflow-x: auto;
}

pre code {
    background: none;
    padding: 0;
}

/* Print optimization */
@media print {
    body { padding: 0; margin: 0; }
    h1, h2, h3 { page-break-after: avoid; }
    pre, blockquote, table { page-break-inside: avoid; }
}
"""

    def _get_modern_css(self):
        """Modern VS Code-style styling"""
        colors = {
            "light": {
                "bg": "#ffffff", "text": "#333333", "border": "#e1e4e8",
                "code_bg": "#f6f8fa", "blockquote": "#656d76", "link": "#0969da"
            },
            "dark": {
                "bg": "#1e1e1e", "text": "#cccccc", "border": "#3c3c3c",
                "code_bg": "#2d2d30", "blockquote": "#8e8e93", "link": "#4fc3f7"
            }
        }
        c = colors[self.theme]

        return f"""
/* LicenseCorp Modern Styling */
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    font-size: 12px;
    padding: 0 20px;
    line-height: 1.5;
    color: {c['text']};
    background-color: {c['bg']};
}}

h1 {{
    font-size: 20px;
    font-weight: 600;
    padding-bottom: 0.3em;
    border-bottom: 1px solid {c['border']};
    margin-top: 24px;
    margin-bottom: 16px;
}}

h2 {{
    font-size: 16px;
    font-weight: 600;
    padding-bottom: 0.3em;
    border-bottom: 1px solid {c['border']};
    margin-top: 24px;
    margin-bottom: 16px;
}}

h3 {{ font-size: 14px; font-weight: 600; margin-top: 24px; margin-bottom: 16px; }}
h4, h5, h6 {{ font-size: 12px; font-weight: 600; margin-top: 16px; margin-bottom: 12px; }}
p {{ margin: 12px 0; }}
ul, ol {{ margin: 12px 0; padding-left: 24px; }}
li {{ margin: 4px 0; }}

pre {{
    background-color: {c['code_bg']};
    border-radius: 6px;
    font-size: 10px;
    padding: 12px;
    margin: 12px 0;
    border: 1px solid {c['border']};
    font-family: 'Courier New', monospace;
    overflow: auto;
}}

code {{
    background-color: {c['code_bg']};
    border-radius: 3px;
    font-size: 10px;
    padding: 0.2em 0.4em;
    font-family: 'Courier New', monospace;
}}

pre code {{ background: transparent; border: none; padding: 0; }}

table {{
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
    font-size: 12px;
}}

th, td {{
    border: 1px solid {c['border']};
    padding: 6px 10px;
    text-align: left;
}}

th {{ background-color: {c['code_bg']}; font-weight: 600; }}
a {{ color: {c['link']}; text-decoration: none; }}
blockquote {{
    border-left: 0.25em solid {c['border']};
    color: {c['blockquote']};
    margin: 12px 0;
    padding: 0 1em;
}}

hr {{ background-color: {c['border']}; border: 0; height: 0.25em; margin: 20px 0; }}

.mermaid {{ text-align: center; margin: 20px 0; min-height: 100px; }}
.mermaid svg {{ max-width: 100%; height: auto; }}

@media print {{
    body {{ padding: 0; margin: 0; -webkit-print-color-adjust: exact; }}
    .mermaid, pre, blockquote, table {{ page-break-inside: avoid; }}
    h1, h2, h3 {{ page-break-after: avoid; }}
}}
"""

    def create_html_template(self, html_content, title="Document", base_href=None):
        """Create complete HTML document with Mermaid support"""
        css = self.get_css()
        base_tag = f'<base href="{base_href}">' if base_href else ""
        mermaid_theme = 'dark' if self.theme == 'dark' else 'default'

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {base_tag}
    <style>{css}</style>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
</head>
<body>
    <div id="content">{html_content}</div>
    <script>
        mermaid.initialize({{
            startOnLoad: false,
            theme: '{mermaid_theme}',
            securityLevel: 'loose',
            flowchart: {{ useMaxWidth: true, htmlLabels: true, curve: 'basis' }},
            sequence: {{ useMaxWidth: true, wrap: true }}
        }});

        document.addEventListener('DOMContentLoaded', function() {{
            let count = 0;
            document.querySelectorAll('pre code').forEach(function(block) {{
                const text = block.textContent.trim();
                const patterns = [/^(graph|flowchart)/, /^sequenceDiagram/, /^gantt/,
                                  /^classDiagram/, /^stateDiagram/, /^erDiagram/,
                                  /^journey/, /^pie/, /^gitGraph/];
                if (patterns.some(p => p.test(text))) {{
                    const div = document.createElement('div');
                    div.className = 'mermaid';
                    div.textContent = text;
                    block.closest('pre').replaceWith(div);
                    count++;
                }}
            }});
            if (count > 0) {{
                mermaid.run().then(() => {{ window.mermaidComplete = true; }})
                       .catch(() => {{ window.mermaidComplete = true; }});
            }} else {{
                window.mermaidComplete = true;
            }}
            window.mermaidDiagramCount = count;
        }});
    </script>
</body>
</html>"""

    def convert_markdown_to_html(self, markdown_text):
        """Convert markdown to HTML using markdown-it-py"""
        try:
            from markdown_it import MarkdownIt
        except ImportError:
            print("📦 Installing markdown-it-py...")
            import subprocess
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'markdown-it-py'], check=True)
            from markdown_it import MarkdownIt

        md = MarkdownIt('commonmark', {
            'breaks': True, 'html': True, 'linkify': True
        }).enable(['table', 'strikethrough'])

        return md.render(markdown_text)

    def _inline_local_images(self, html: str, base_dir: Path) -> str:
        """Replace local image src with data URIs"""
        import base64, mimetypes

        def repl(m):
            src = m.group(1)
            if src.startswith(('http://', 'https://', 'data:')):
                return m.group(0)
            try:
                p = (base_dir / src).resolve()
                if not p.exists():
                    return m.group(0)
                mime = mimetypes.guess_type(str(p))[0] or 'image/png'
                b64 = base64.b64encode(p.read_bytes()).decode('ascii')
                return m.group(0).replace(src, f"data:{mime};base64,{b64}")
            except Exception:
                return m.group(0)

        return re.sub(r'<img[^>]*src="([^"]+)"', repl, html)

    async def generate_pdf(self, html_content, output_path, title, base_href=None):
        """Generate PDF using Playwright"""
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            print("📦 Installing playwright...")
            import subprocess
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'playwright'], check=True)
            subprocess.run([sys.executable, '-m', 'playwright', 'install', 'chromium'], check=True)
            from playwright.async_api import async_playwright

        async with async_playwright() as p:
            print("🚀 Launching browser...")
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
            page = await browser.new_page()

            full_html = self.create_html_template(html_content, title, base_href)
            await page.set_content(full_html, wait_until='networkidle')

            print("⏳ Processing Mermaid diagrams...")
            try:
                await page.wait_for_function("window.mermaidComplete === true", timeout=25000)
                self.mermaid_diagrams_found = await page.evaluate("window.mermaidDiagramCount || 0")
                if self.mermaid_diagrams_found > 0:
                    await page.wait_for_timeout(2000)
            except Exception as e:
                print(f"⚠️  Mermaid timeout: {e}")

            # Use letter size for legal, A4 for modern
            page_format = 'Letter' if self.style == 'legal' else 'A4'

            # PDF options
            pdf_options = {
                'path': str(output_path),
                'format': page_format,
                'print_background': True,
            }

            # Branded documents get header/footer with adjusted margins
            if self.branded:
                print("🏷️  Adding LC branding...")
                pdf_options['display_header_footer'] = True
                pdf_options['header_template'] = self._get_header_template(title)
                pdf_options['footer_template'] = self._get_footer_template()
                pdf_options['margin'] = {
                    'top': '1.25in',      # Extra space for header
                    'right': '0.75in',
                    'bottom': '1in',      # Extra space for footer
                    'left': '0.75in'
                }
            else:
                pdf_options['margin'] = {
                    'top': '0.75in',
                    'right': '0.75in',
                    'bottom': '0.75in',
                    'left': '0.75in'
                }

            print("🖨️  Generating PDF...")
            await page.pdf(**pdf_options)
            await browser.close()

    async def convert(self, markdown_file, output_file=None, add_toc=False, add_numbering=False):
        """Main conversion method"""
        markdown_path = Path(markdown_file).resolve()

        if not markdown_path.exists():
            raise FileNotFoundError(f"File not found: {markdown_file}")

        output_path = Path(output_file).resolve() if output_file else markdown_path.with_suffix('.pdf')

        print(f"📖 Converting: {markdown_path.name}")
        print(f"📍 Location: {markdown_path.parent}")
        print(f"🎨 Style: {self.style} | Theme: {self.theme}")
        if self.branded:
            print(f"🏢 Branding: License Corporation | Confidential: {self.confidential}")

        # Read markdown
        content = markdown_path.read_text(encoding='utf-8')

        # Preprocessing
        if add_numbering:
            print("🔢 Adding section numbering...")
            content = add_section_numbering(content)

        if add_toc:
            print("📋 Generating table of contents...")
            headers = extract_headers(content)
            toc = generate_toc_markdown(headers)
            content = insert_toc(content, toc)

        # Convert
        html_content = self.convert_markdown_to_html(content)
        html_content = self._inline_local_images(html_content, markdown_path.parent)
        base_href = markdown_path.parent.as_uri() + "/"

        await self.generate_pdf(html_content, output_path, markdown_path.stem, base_href)

        file_size = output_path.stat().st_size
        print(f"\n✅ Success! PDF created: {output_path}")
        print(f"📄 Size: {file_size / 1024:.1f} KB | Mermaid: {self.mermaid_diagrams_found}")
        return True


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description=f"LicenseCorp Markdown to PDF v{__version__}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic conversion
  python markdown_to_pdf.py document.md

  # Legal document with TOC and numbering
  python markdown_to_pdf.py contract.md --style legal --toc --numbered

  # Official branded document (LC header/footer)
  python markdown_to_pdf.py proposal.md --branded --style legal --toc

  # Branded but not confidential
  python markdown_to_pdf.py public-doc.md --branded --no-confidential

  # Dark theme
  python markdown_to_pdf.py README.md --theme dark --output docs/readme.pdf
        """
    )

    parser.add_argument('markdown_file', help='Markdown file to convert')
    parser.add_argument('-o', '--output', help='Output PDF path')
    parser.add_argument('-s', '--style', choices=['modern', 'legal'], default='modern',
                        help='Styling: modern (VS Code) or legal (Times New Roman)')
    parser.add_argument('-t', '--theme', choices=['light', 'dark'], default='light',
                        help='Color theme (modern style only)')
    parser.add_argument('--toc', action='store_true', help='Auto-generate table of contents')
    parser.add_argument('--numbered', action='store_true', help='Add section numbering (1.1, 1.2.1)')
    parser.add_argument('--branded', action='store_true',
                        help='Add LC branding: logo header, confidential footer, page numbers')
    parser.add_argument('--no-confidential', action='store_true',
                        help='Remove "Confidential" from footer (use with --branded)')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')

    args = parser.parse_args()

    print("🎯 LICENSECORP MARKDOWN TO PDF")
    print("=" * 50)
    print(f"Version {__version__} - Modern + Legal + Branded Document Support")
    print()

    converter = LCMarkdownConverter(
        style=args.style,
        theme=args.theme,
        branded=args.branded,
        confidential=not args.no_confidential
    )

    try:
        success = asyncio.run(converter.convert(
            args.markdown_file,
            args.output,
            add_toc=args.toc,
            add_numbering=args.numbered
        ))
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
