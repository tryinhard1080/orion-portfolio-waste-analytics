Generate all performance and contract analysis reports for the Orion portfolio.

# What This Command Does

Executes the complete report generation workflow:
1. Reads data from Google Sheets (or fallback to hardcoded data)
2. Generates portfolio summary dashboard
3. Generates 6 property-specific analysis reports
4. Generates 6 contract comparison reports
5. Outputs all reports to Reports/ folder

# Execution

```bash
# Change to project directory
cd "C:\Users\Richard\Downloads\Orion Data Part 2"

echo "=========================================="
echo "GENERATING REPORTS"
echo "=========================================="
echo ""

# Generate performance reports
echo "[1/2] Generating performance reports..."
python Code/generate_reports_from_sheets.py

# Generate contract comparison reports
echo "[2/2] Generating contract comparison reports..."
python Code/generate_contract_reports.py

echo ""
echo "=========================================="
echo "REPORT GENERATION COMPLETE"
echo "=========================================="
echo ""
echo "Reports available in: Reports/"
echo ""
echo "Generated files:"
echo "  - PortfolioSummaryDashboard.html"
echo "  - BellaMirageAnalysis.html"
echo "  - McCordParkFLAnalysis.html"
echo "  - OrionMcKinneyAnalysis.html"
echo "  - OrionProsperAnalysis.html"
echo "  - OrionProsperLakesAnalysis.html"
echo "  - TheClubAtMilleniaAnalysis.html"
echo "  - Contract_Comparison/ (6 property reports)"
echo ""
echo "Next steps:"
echo "1. Review reports in Reports/ folder"
echo "2. Run /validate-all to check quality"
echo "3. Distribute to stakeholders"
```

# When to Use

- Monthly reporting cycle
- After updating Google Sheets data
- After extracting new invoice data
- On-demand analysis requests

# See Also

- /validate-all - Validate reports before distribution
- /convert-to-pdf - Convert HTML reports to PDF
