# How to View Your Reports

## Quick Start

All generated reports are located in: `Reports/HTML/`

### Option 1: Open in Browser (Recommended)

**Windows:**
```bash
# Open portfolio dashboard
start Reports/HTML/PortfolioSummaryDashboard.html

# Open all reports
start Reports/HTML/*.html
```

**Mac/Linux:**
```bash
# Open portfolio dashboard
open Reports/HTML/PortfolioSummaryDashboard.html

# Or use your default browser
firefox Reports/HTML/PortfolioSummaryDashboard.html
```

### Option 2: Navigate in File Explorer

1. Open File Explorer
2. Navigate to: `C:\Users\Richard\Downloads\Orion Data Part 2\Reports\HTML\`
3. Double-click any `.html` file to open in your default browser

---

## Report Files

### Start Here
- **PortfolioSummaryDashboard.html** - Overview of entire portfolio

### Individual Properties
- **Bella_MirageAnalysis.html** - 715 units, $10.87 CPD
- **The_Club_at_MilleniaAnalysis.html** - 560 units, $21.00 CPD
- **McCord_Park_FLAnalysis.html** - 416 units, $26.89 CPD
- **Orion_McKinneyAnalysis.html** - 453 units, $13.28 CPD
- **Orion_ProsperAnalysis.html** - 312 units, $13.81 CPD
- **Orion_Prosper_LakesAnalysis.html** - 308 units, $13.09 CPD

### Additional Reports
- **ContractAnalysisSummary.html** - Contract status and alerts
- **ExtractionSummary.html** - Invoice extraction statistics

---

## What to Look For

### In Portfolio Dashboard
- Total monthly costs across all properties
- Cost per door (CPD) comparison
- Performance scores
- Data quality indicators

### In Property Reports
- Monthly costs and key metrics
- Vendor information
- Service frequency
- Analysis findings
- Recommendations (if any)
- Container specifications (McCord Park FL)

### In Contract Analysis
- **Critical alerts:** Expired contracts, risky agreements
- Contract terms and dates
- Auto-renewal status
- Price escalation clauses

### In Extraction Summary
- Total invoices processed
- Flags by property
- Data completeness

---

## Recommended Review Order

1. **PortfolioSummaryDashboard.html** - Get the big picture
2. **ContractAnalysisSummary.html** - Identify urgent issues
3. **McCord_Park_FLAnalysis.html** - Review 15% rate increase details
4. **Bella_MirageAnalysis.html** - Expired contract details
5. **Other property reports** - Individual property deep dives
6. **ExtractionSummary.html** - Data quality verification

---

## Tips

- **Bookmarks:** Bookmark PortfolioSummaryDashboard.html for quick access
- **Printing:** Reports are print-friendly (use browser Print function)
- **Sharing:** Reports are self-contained HTML (can email or share via cloud)
- **Mobile:** Reports are responsive and work on mobile devices

---

## Next Steps After Reviewing

1. **Address Critical Issues:**
   - Bella Mirage: Negotiate new contract (expired 912 days)
   - McCord Park FL: Investigate 15% rate increase
   - Orion McKinney: Secure long-term agreement

2. **Complete Remaining Extractions:**
   - The Club at Millenia: 6 invoices
   - Orion properties: 32 invoices total

3. **Upload to Google Sheets:**
   - Requires: credentials.json file
   - Command: `/update-sheets` (or Python script)

4. **Generate PDF Versions:**
   - Command: `/convert-to-pdf`
   - Or use browser Print → Save as PDF

---

## Troubleshooting

**Reports won't open:**
- Ensure you have a web browser installed
- Right-click file → Open With → Choose browser

**Styling looks broken:**
- Reports use embedded CSS, no internet required
- Try a different browser (Chrome, Firefox, Edge)

**Need to update data:**
- Edit source JSON files (extraction_results.json, property_analysis.json)
- Re-run: `python Code/generate_portfolio_reports.py`

---

**Generated:** October 26, 2025
**Last Updated:** October 26, 2025
