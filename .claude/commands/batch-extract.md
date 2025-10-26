Batch extract invoice data using Claude Vision API (alternative to subagent extraction).

# What This Command Does

Uses the waste-batch-extractor skill to:
1. Process multiple invoices in parallel
2. Extract data using Claude's Vision API
3. Organize results by property
4. Generate validation reports
5. Create Excel workbooks with extracted data
6. Flag missing/ambiguous data with confidence scores

# Execution

```bash
cd ~/.claude/skills/waste-batch-extractor

echo "=========================================="
echo "BATCH EXTRACTION - Claude Vision API"
echo "=========================================="
echo ""

python batch_extractor.py \
  --input "C:\Users\Richard\Downloads\Orion Data Part 2\Invoices" \
  --output "C:\Users\Richard\Downloads\Orion Data Part 2\Reports\Batch_Extraction" \
  --validate \
  --confidence-threshold 70

echo ""
echo "=========================================="
echo "BATCH EXTRACTION COMPLETE"
echo "=========================================="
echo ""
echo "Results saved to: Reports/Batch_Extraction/"
echo ""
echo "Output files:"
echo "  - consolidated_data.xlsx (all properties)"
echo "  - validation_report.xlsx (flagged items)"
echo "  - property_specific/ (individual Excel files)"
echo "  - csv_exports/ (database-ready CSVs)"
echo ""
echo "Next: Review validation_report.xlsx for flagged items"
```

# Data Quality Features

**Automatic Flagging:**
- Identifies missing required fields
- Flags ambiguous data
- Creates review queue

**Confidence Scoring:**
- Each extracted field gets confidence score (0-100%)
- Low confidence fields automatically flagged
- Threshold: <70% confidence = NEEDS REVIEW

**Validation Report:**
- Excel sheet with all flags
- Color-coded by severity (Red/Yellow/Green)
- Includes invoice thumbnails for quick reference

# Output Format

**consolidated_data.xlsx:**
- Sheet 1: All invoices consolidated
- Sheet 2: Property A data
- Sheet 3: Property B data
- ... (one sheet per property)

**validation_report.xlsx:**

| Invoice | Field | Value | Confidence | Flag | Action |
|---------|-------|-------|-----------|------|--------|
| Orion_Prosper_Jan.pdf | Frequency | (missing) | 0% | Red | Review invoice |
| Bella_Mirage_Feb.pdf | Container Count | 2 | 65% | Yellow | Verify count |
| McKinney_Mar.pdf | Overage | $350 | 85% | Green | Spot-check |

# Comparison: /extract-invoices vs /batch-extract

| Feature | /extract-invoices | /batch-extract |
|---------|------------------|----------------|
| Method | Subagent orchestration | Claude Vision API |
| Output | JSON → Google Sheets | Excel + CSV |
| Speed | Sequential | Parallel |
| Validation | Manual review | Automated flagging |
| Best For | Production workflow | Quick analysis |

# When to Use

- Alternative to /extract-invoices (Vision API vs subagents)
- Batch processing multiple properties at once
- When you need Excel output directly
- For quick validation of extraction accuracy
- Testing new invoice formats

# See Also

- /extract-invoices - Subagent-based extraction
- /review-flags - Resolve flagged data
- ~/.claude/skills/waste-batch-extractor/README.md
