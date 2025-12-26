#
# LicenseCorp Markdown to PDF Converter - Windows Convenience Script
# Usage: .\md2pdf.ps1 document.md [--style legal] [--toc] [--numbered]
#

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$ScriptDir\markdown_to_pdf.py" @args
