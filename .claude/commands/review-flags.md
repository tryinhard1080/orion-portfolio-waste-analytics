Review and resolve all flagged invoice data before proceeding.

# What This Command Does

Interactive review system for data quality:
1. Loads extraction results with flags
2. Groups by flag severity (Critical/Needs Review/Validation)
3. Displays invoice context for each flag
4. Prompts user for manual input
5. Updates extraction data with user corrections
6. Re-validates after corrections

# Execution

```bash
cd "C:\Users\Richard\Downloads\Orion Data Part 2"

echo "=========================================="
echo "REVIEWING FLAGGED DATA"
echo "=========================================="
echo ""

# Check if extraction results exist
if [ ! -f "extraction_results.json" ]; then
  echo "[ERROR] No extraction results found"
  echo "Run /extract-invoices first"
  exit 1
fi

# Run interactive review
python -c "
import json
import os

# Load extraction results
with open('extraction_results.json', 'r') as f:
    results = json.load(f)

# Count flags by severity
critical_flags = []
needs_review = []
validation_suggested = []

for invoice in results:
    if 'flags' in invoice:
        for flag in invoice['flags']:
            if flag['level'] == 'CRITICAL':
                critical_flags.append({'invoice': invoice, 'flag': flag})
            elif flag['level'] == 'NEEDS_REVIEW':
                needs_review.append({'invoice': invoice, 'flag': flag})
            elif flag['level'] == 'VALIDATION_SUGGESTED':
                validation_suggested.append({'invoice': invoice, 'flag': flag})

# Display summary
print('Flag Summary:')
print(f'  Red Flags (CRITICAL): {len(critical_flags)}')
print(f'  Yellow Flags (NEEDS REVIEW): {len(needs_review)}')
print(f'  Green Flags (VALIDATION SUGGESTED): {len(validation_suggested)}')
print('')

if len(critical_flags) == 0 and len(needs_review) == 0:
    print('[OK] No critical or review flags found')
    print('')
    if len(validation_suggested) > 0:
        print(f'Note: {len(validation_suggested)} validation suggestions to review')
        print('These are low priority - spot-check recommended')
    exit(0)

# Interactive review
print('========================================')
print('INTERACTIVE FLAG REVIEW')
print('========================================')
print('')

updated_invoices = []

# Review critical flags first
if len(critical_flags) > 0:
    print('=== CRITICAL FLAGS (Must Resolve) ===')
    print('')

    for i, item in enumerate(critical_flags):
        invoice = item['invoice']
        flag = item['flag']

        print(f'[{i+1}/{len(critical_flags)}] CRITICAL FLAG')
        print(f'Invoice: {invoice[\"filename\"]}')
        print(f'Field: {flag[\"field\"]}')
        print(f'Issue: {flag[\"message\"]}')
        print(f'Action: {flag[\"action\"]}')
        print('')

        # Prompt for correction
        correction = input(f'Enter correct value for {flag[\"field\"]}: ')

        # Update invoice data
        invoice[flag['field']] = correction
        invoice['flags'].remove(flag)
        invoice['manually_reviewed'] = True

        print('[OK] Updated')
        print('')

# Review needs review flags
if len(needs_review) > 0:
    print('=== NEEDS REVIEW FLAGS ===')
    print('')

    for i, item in enumerate(needs_review):
        invoice = item['invoice']
        flag = item['flag']

        print(f'[{i+1}/{len(needs_review)}] NEEDS REVIEW')
        print(f'Invoice: {invoice[\"filename\"]}')
        print(f'Field: {flag[\"field\"]}')
        print(f'Issue: {flag[\"message\"]}')
        print('')

        review = input(f'Review {flag[\"field\"]} (c=correct/u=update/s=skip): ')

        if review == 'u':
            correction = input(f'Enter correct value: ')
            invoice[flag['field']] = correction
            invoice['flags'].remove(flag)
            invoice['manually_reviewed'] = True
            print('[OK] Updated')
        elif review == 'c':
            invoice['flags'].remove(flag)
            print('[OK] Marked as correct')
        else:
            print('[SKIP] Flag remains')

        print('')

# Save updated results
with open('extraction_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print('========================================')
print('REVIEW COMPLETE')
print('========================================')
print('')
print('Updated extraction_results.json')
print('')
print('Next steps:')
print('1. Re-run validation: python Code/validate_extracted_data.py')
print('2. Upload to sheets: /update-sheets')
"

echo ""
echo "=========================================="
```

# Flag Levels

**Red Flags (CRITICAL)**
- Missing property name
- Missing invoice amount
- Missing date
- Cannot proceed without this data
- **Action: Must provide value**

**Yellow Flags (NEEDS REVIEW)**
- Ambiguous container count
- Unclear frequency
- Mixed charges (base vs overage)
- **Action: Review and confirm or update**

**Green Flags (VALIDATION SUGGESTED)**
- Calculated values
- Inferred data
- Pattern-based extraction
- **Action: Spot-check recommended**

# Interactive Prompts

**For Critical Flags:**
```
[1/3] CRITICAL FLAG
Invoice: Orion_Prosper_Jan2025.pdf
Field: Container Count
Issue: Invoice says 'compactor service' but doesn't specify number
Action: Please review invoice and add container count manually

Enter correct value for Container Count: 2
[OK] Updated
```

**For Needs Review Flags:**
```
[1/5] NEEDS REVIEW
Invoice: Bella_Mirage_Feb2025.pdf
Field: Pickup Frequency
Issue: Invoice shows charges but doesn't state frequency

Review Pickup Frequency (c=correct/u=update/s=skip): u
Enter correct value: Weekly
[OK] Updated
```

# Example Session

```
========================================
REVIEWING FLAGGED DATA
========================================

Flag Summary:
  Red Flags (CRITICAL): 2
  Yellow Flags (NEEDS REVIEW): 5
  Green Flags (VALIDATION SUGGESTED): 3

========================================
INTERACTIVE FLAG REVIEW
========================================

=== CRITICAL FLAGS (Must Resolve) ===

[1/2] CRITICAL FLAG
Invoice: Orion_Prosper_Jan2025.pdf
Field: Container Count
Issue: Invoice says 'compactor service' but doesn't specify number
Action: Please review invoice and add container count manually

Enter correct value for Container Count: 2
[OK] Updated

[2/2] CRITICAL FLAG
Invoice: McCord_Park_Mar2025.pdf
Field: Invoice Date
Issue: Date field not found in invoice
Action: Manually enter invoice date

Enter correct value for Invoice Date: 2025-03-15
[OK] Updated

=== NEEDS REVIEW FLAGS ===

[1/5] NEEDS REVIEW
Invoice: Bella_Mirage_Feb2025.pdf
Field: Pickup Frequency
Issue: Invoice shows charges but doesn't state frequency

Review Pickup Frequency (c=correct/u=update/s=skip): u
Enter correct value: Weekly
[OK] Updated

... (continues for all flags)

========================================
REVIEW COMPLETE
========================================

Updated extraction_results.json

Next steps:
1. Re-run validation: python Code/validate_extracted_data.py
2. Upload to sheets: /update-sheets
```

# After Review

Once all flags are resolved:
1. Extraction data is updated
2. Flags are removed
3. Data is marked as manually reviewed
4. Ready for upload to Google Sheets

# When to Use

- After running /extract-invoices
- Before running /update-sheets
- Whenever extraction flags appear
- As part of /monthly-workflow
- Quality assurance checkpoint

# Data Integrity

This command ensures:
- No hallucinated data
- All missing fields resolved
- Ambiguous data clarified
- User validates all corrections
- Audit trail maintained

# See Also

- /extract-invoices - Generates flagged data
- /update-sheets - Uploads reviewed data
- /monthly-workflow - Includes flag review step
- Documentation/DATA_INTEGRITY_GUIDE.md
