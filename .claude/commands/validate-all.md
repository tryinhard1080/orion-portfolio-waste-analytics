Validate all generated reports for prohibited language and data accuracy.

# What This Command Does

**CRITICAL STEP** - Must run before distributing reports to clients.

Validates:
1. No "cost savings" or prohibited terms
2. Data accuracy (CPD calculations, unit counts)
3. Performance scores within 0-100 range
4. All 6 properties included
5. Portfolio totals calculated correctly
6. HTML structure valid

# Execution

```bash
cd "C:\Users\Richard\Downloads\Orion Data Part 2"

echo "=========================================="
echo "VALIDATING REPORTS"
echo "=========================================="
echo ""

python Code/validate_reports.py

echo ""
echo "=========================================="
echo "Review validation results above"
echo "Fix any issues before distributing reports"
echo "=========================================="
```

# Expected Output

**If validation passes:**
```
[OK] Language validation passed - no prohibited terms found
[OK] Data accuracy validation passed
[OK] HTML structure validation passed
[OK] All 6 properties included
[OK] Portfolio totals correct

=== ALL VALIDATIONS PASSED ===
Reports ready for distribution
```

**If validation fails:**
```
[ERROR] Validation failed:
  - Found prohibited term "cost savings" in OrionProsperAnalysis.html:L234
  - CPD calculation incorrect in BellaMirageAnalysis.html
  - Expected CPD: $10.68, Found: $10.85

ACTION REQUIRED: Fix issues above and re-run validation
```

# Prohibited Language

**DO NOT use these terms in reports:**
- "cost savings"
- "savings opportunity"
- "reduce costs by"
- "save $X per month"
- "potential savings"

**USE instead:**
- "performance gaps"
- "cost efficiency opportunity"
- "areas for improvement"
- "benchmark comparison"

See Documentation/REPORT_CORRECTION_SUMMARY.md for complete rules.

# When to Use

- **ALWAYS** before distributing reports
- After regenerating reports
- Before monthly client deliverables

# See Also

- /generate-reports - Generate reports to validate
- Documentation/REPORT_CRITERIA_ANALYSIS.md
