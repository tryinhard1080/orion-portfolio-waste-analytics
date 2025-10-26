Extract invoice data from PDFs using AI-powered subagent extraction workflow.

# What This Command Does

Orchestrates multi-step AI extraction with strict data validation:
1. Scans Invoices/{property}/ folders for new PDFs
2. Uses specialized AI agents for field extraction
3. Validates extracted data quality
4. Flags missing or ambiguous data
5. Generates extraction confidence scores
6. Outputs structured data ready for Google Sheets

# Data Integrity Rules

**NEVER:**
- Hallucinate missing frequencies
- Guess container counts
- Make up charges that aren't itemized
- Estimate dates or amounts

**ALWAYS:**
- Flag missing required fields as NEEDS REVIEW
- Prompt user for ambiguous data
- Extract exact text from invoice (don't interpret)
- Mark calculated values explicitly

# Execution

```bash
cd "C:\Users\Richard\Downloads\Orion Data Part 2"

echo "=========================================="
echo "EXTRACTING INVOICE DATA"
echo "=========================================="
echo ""

# Run orchestrated extraction
echo "[1/2] Running AI extraction..."
python Code/orchestrate_extraction.py

echo ""
echo "[2/2] Validating extracted data..."
python Code/validate_extracted_data.py

echo ""
echo "=========================================="
echo "EXTRACTION COMPLETE - REVIEW FLAGS"
echo "=========================================="
echo ""
echo "Check extraction_results.json for:"
echo "  - Red flags (CRITICAL) - manual review required"
echo "  - Yellow flags (NEEDS REVIEW) - verify data"
echo "  - Green flags (VALIDATION SUGGESTED) - spot-check"
echo ""
echo "Next step: Run /review-flags to resolve issues"
```

# Flagging System

**Red Flag (CRITICAL)** - Cannot proceed without this data
- Missing property name
- Missing invoice amount
- Missing date

**Yellow Flag (NEEDS REVIEW)** - Data exists but ambiguous
- "Container" mentioned but no count
- Frequency unclear (weekly vs monthly)
- Charges not itemized (can't separate base from overage)

**Green Flag (VALIDATION SUGGESTED)** - Data extracted with medium confidence
- Calculated field (e.g., derived frequency from pickup dates)
- Inferred from pattern
- Needs spot-check

# Example Flag Output

```
Red Flag (CRITICAL): Orion_Prosper_Jan2025.pdf
   Field: Container Count
   Issue: Invoice says 'compactor service' but doesn't specify number
   Action: Please review invoice and add container count manually

Yellow Flag (NEEDS REVIEW): Bella_Mirage_Feb2025.pdf
   Field: Pickup Frequency
   Issue: Invoice shows charges but doesn't state frequency
   Action: Check contract or previous invoices

Green Flag (VALIDATE): Orion_McKinney_Apr2025.pdf
   Field: Frequency
   Value: Calculated as 'weekly' based on 4 pickup dates
   Action: Spot-check to confirm
```

# Prerequisites

- Invoice PDFs in Invoices/{PropertyName}/ folders
- Invoices should be text-based PDFs (not scanned images)

# When to Use

- Monthly invoice processing
- New property onboarding
- Historical data backfill

# See Also

- /review-flags - Interactive flag resolution
- /update-sheets - Upload validated data
- Documentation/SUBAGENT_EXTRACTION_STRATEGY.md
- Documentation/SUBAGENT_QUICK_START.md
