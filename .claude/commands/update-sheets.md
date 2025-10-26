Upload validated invoice data to Google Sheets.

# What This Command Does

1. Reads extracted invoice data from /extract-invoices run
2. Validates data before uploading
3. Batch uploads to Google Sheets
4. Updates "Invoice Data" sheet
5. Confirms successful upload

# Execution

```bash
cd "C:\Users\Richard\Downloads\Orion Data Part 2"

echo "=========================================="
echo "UPDATING GOOGLE SHEETS"
echo "=========================================="
echo ""

python Code/update_google_sheets.py

echo ""
echo "=========================================="
echo "Data uploaded to Google Sheets"
echo "=========================================="
echo ""
echo "Spreadsheet URL:"
echo "https://docs.google.com/spreadsheets/d/1oy-F3p_CPpJaGGmGUMcjQMubRIRi7p4IID7mfpNLZJQ/edit"
echo ""
echo "Updated sheet: Invoice Data"
```

# Prerequisites

- Extracted data from /extract-invoices
- All flags resolved (run /review-flags first)
- Google Sheets API access configured (or use hardcoded data mode)
- Valid spreadsheet ID in .env file

# Important Notes

**Data must be validated BEFORE upload:**
1. Run /extract-invoices
2. Run /review-flags to resolve all issues
3. Only then run /update-sheets

**Never upload flagged data:**
- Red flags must be resolved
- Yellow flags should be reviewed
- Green flags can proceed with caution

# When to Use

- After extracting new invoice data
- After resolving all data flags
- Before generating updated reports
- Monthly data refresh

# Next Steps

After updating Google Sheets:
1. Run /generate-reports to create updated reports
2. Run /validate-all to check quality
3. Distribute reports to stakeholders

# See Also

- /extract-invoices - Extract data first
- /review-flags - Resolve flags before uploading
- /generate-reports - Generate reports with new data
