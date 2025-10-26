Convert all HTML reports to PDF using Puppeteer MCP.

# What This Command Does

1. Scans Reports/ folder for HTML files
2. Uses Puppeteer MCP for high-quality conversion
3. Preserves styling and formatting
4. Outputs PDFs to Reports/PDF/ folder

# Execution

```bash
cd "C:\Users\Richard\Downloads\Orion Data Part 2"

echo "=========================================="
echo "CONVERTING REPORTS TO PDF"
echo "=========================================="
echo ""

# Create PDF output directory
mkdir -p Reports/PDF

python Code/convert_to_pdf_puppeteer.py

echo ""
echo "=========================================="
echo "PDF CONVERSION COMPLETE"
echo "=========================================="
echo ""
echo "PDFs available in: Reports/PDF/"
echo ""
echo "Converted files:"
echo "  - PortfolioSummaryDashboard.pdf"
echo "  - BellaMirageAnalysis.pdf"
echo "  - McCordParkFLAnalysis.pdf"
echo "  - OrionMcKinneyAnalysis.pdf"
echo "  - OrionProsperAnalysis.pdf"
echo "  - OrionProsperLakesAnalysis.pdf"
echo "  - TheClubAtMilleniaAnalysis.pdf"
```

# Prerequisites

- HTML reports generated (/generate-reports)
- Puppeteer MCP server configured

# When to Use

- Before client distribution (PDF preferred format)
- For archival purposes
- When email-friendly format needed
- For printing hard copies

# Notes

- PDF files maintain all styling from HTML
- Charts and graphs render correctly
- File sizes are optimized
- Print-friendly layout

# See Also

- /generate-reports - Generate HTML reports first
- /validate-all - Validate before converting
