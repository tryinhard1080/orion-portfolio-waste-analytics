Execute the complete monthly invoice processing and reporting workflow.

# What This Command Does

Orchestrates the full monthly cycle:
1. Extract invoice data from new PDFs
2. Validate extracted data (flag missing/ambiguous fields)
3. Resolve all flags interactively
4. Update Google Sheets
5. Generate all reports (performance + contracts)
6. Validate reports
7. Convert to PDF (optional)

# Execution

```bash
cd "C:\Users\Richard\Downloads\Orion Data Part 2"

echo "=========================================="
echo "MONTHLY WORKFLOW - Orion Portfolio"
echo "=========================================="
echo ""

# Step 1: Extract invoices
echo "Step 1/7: Extracting invoice data..."
python Code/orchestrate_extraction.py

echo ""
# Step 2: Validate extraction
echo "Step 2/7: Validating extracted data..."
python Code/validate_extracted_data.py

echo ""
# Step 3: Review flags (if any)
echo "Step 3/7: Checking for data flags..."
echo ""
echo "IMPORTANT: Review any flags above"
echo "Red flags (CRITICAL) must be resolved before proceeding"
echo "Yellow flags (NEEDS REVIEW) should be reviewed"
echo ""
read -p "All flags resolved? Continue to update sheets? (y/n): " CONTINUE

if [ "$CONTINUE" != "y" ]; then
  echo "Workflow paused. Resolve flags and re-run."
  exit 1
fi

echo ""
# Step 4: Update Google Sheets
echo "Step 4/7: Updating Google Sheets..."
python Code/update_google_sheets.py

echo ""
# Step 5: Generate reports
echo "Step 5/7: Generating reports..."
python Code/generate_reports_from_sheets.py
python Code/generate_contract_reports.py

echo ""
# Step 6: Validate reports
echo "Step 6/7: Validating reports..."
python Code/validate_reports.py

echo ""
# Step 7: Convert to PDF (optional)
read -p "Convert reports to PDF? (y/n): " CONVERT
if [ "$CONVERT" == "y" ]; then
  echo "Step 7/7: Converting to PDF..."
  python Code/convert_to_pdf_puppeteer.py
else
  echo "Step 7/7: Skipped PDF conversion"
fi

echo ""
echo "=========================================="
echo "MONTHLY WORKFLOW COMPLETE"
echo "=========================================="
echo ""
echo "Summary:"
echo "  - Invoices extracted and validated"
echo "  - Google Sheets updated"
echo "  - Reports generated and validated"
if [ "$CONVERT" == "y" ]; then
  echo "  - PDFs created"
fi
echo ""
echo "Reports available in: Reports/"
echo ""
echo "Next steps:"
echo "1. Review reports in Reports/ folder"
echo "2. Verify all data is accurate"
echo "3. Distribute to stakeholders"
```

# Prerequisites

- New invoice PDFs in Invoices/{property}/ folders
- Google Sheets access configured
- All dependencies installed

# Important Notes

**This workflow will pause if:**
- Red flags (CRITICAL) are found in extraction
- Data validation fails
- You choose not to proceed

**You can resume by:**
- Resolving flagged data
- Re-running the workflow from the paused step

# When to Use

- Monthly reporting cycle
- First week of new month
- After receiving all property invoices
- Regular operational workflow

# Estimated Time

- With no flags: 5-10 minutes
- With flags to resolve: 15-30 minutes (depending on complexity)

# See Also

- /extract-invoices - Run step 1 independently
- /review-flags - Interactive flag resolution
- /generate-reports - Run step 5 independently
- /validate-all - Run step 6 independently
