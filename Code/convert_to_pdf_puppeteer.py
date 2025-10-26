"""
Convert HTML Reports to PDF using Puppeteer
Orion Portfolio Waste Management Analytics

This script generates a batch file to convert HTML reports to PDF
using the Puppeteer MCP server (headless Chrome).
"""

from pathlib import Path

def main():
    """Generate list of HTML files to convert."""
    html_dir = Path("Reports/Contract_Comparison")

    if not html_dir.exists():
        print(f"[ERROR] HTML reports directory not found: {html_dir}")
        return

    # Find all HTML files
    html_files = list(html_dir.glob("*.html"))

    if not html_files:
        print(f"[ERROR] No HTML files found in {html_dir}")
        return

    print("=" * 60)
    print("HTML REPORTS READY FOR PDF CONVERSION")
    print("=" * 60)
    print()
    print(f"Found {len(html_files)} reports:")
    print()

    for html_file in sorted(html_files):
        abs_path = html_file.resolve()
        pdf_name = html_file.stem + ".pdf"
        print(f"  - {html_file.name}")
        print(f"    Path: file:///{abs_path}")
        print(f"    PDF:  {pdf_name}")
        print()

    print("=" * 60)
    print("Use Claude Code with Puppeteer MCP to convert these files")
    print("=" * 60)

if __name__ == "__main__":
    main()
