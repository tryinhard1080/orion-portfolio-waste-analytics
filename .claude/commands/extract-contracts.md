Extract contract terms, dates, and pricing from contract PDFs.

# What This Command Does

Uses waste-contract-extractor skill to:
1. Process contract PDFs in Contracts/ folder
2. Extract key terms (start date, end date, pricing, services)
3. Identify auto-renewal clauses
4. Flag expiration dates
5. Generate contract comparison reports

# Execution

```bash
cd ~/.claude/skills/waste-contract-extractor

echo "=========================================="
echo "EXTRACTING CONTRACT DATA"
echo "=========================================="
echo ""

python waste_docs_export.py \
  --contracts "C:\Users\Richard\Downloads\Orion Data Part 2\Contracts" \
  --output "C:\Users\Richard\Downloads\Orion Data Part 2\Reports\Contract_Analysis"

echo ""
echo "=========================================="
echo "CONTRACT EXTRACTION COMPLETE"
echo "=========================================="
echo ""
echo "Analysis saved to: Reports/Contract_Analysis/"
echo ""
echo "Output files:"
echo "  - contract_summary.xlsx"
echo "  - contract_comparison.html"
echo "  - expiration_alerts.json"
echo ""
echo "Review contract_summary.xlsx for extracted data"
```

# Extracted Fields

**Contract Terms:**
- Contract start date
- Contract end date
- Contract duration
- Auto-renewal terms
- Notice period requirements

**Service Details:**
- Monthly base cost
- Service frequency
- Container type and size
- Number of containers
- Additional services included

**Pricing Information:**
- Base monthly rate
- Overage charges
- Price escalation clauses
- CPI adjustments
- Special rates/discounts

**Important Dates:**
- Expiration date
- Renewal date
- Notice deadline
- Rate increase dates

# Example Output

**contract_summary.xlsx:**

| Property | Vendor | Start | End | Monthly Cost | Frequency | Auto-Renew | Notice Period |
|----------|--------|-------|-----|--------------|-----------|------------|---------------|
| Orion Prosper | Republic Services | 01/01/2024 | 12/31/2026 | $4,308 | Weekly | Yes | 90 days |
| Bella Mirage | Waste Mgmt | 04/20/2023 | 04/19/2026 | $7,636 | 2x/week | Yes | 60 days |

# Alerts Generated

**Expiration Alerts:**
```
[WARNING] McCord Park FL contract expires in 90 days (12/31/2025)
[INFO] Bella Mirage auto-renews in 180 days
[CRITICAL] The Club at Millenia - notice period deadline in 30 days
```

# When to Use

- New contract onboarding
- Contract renewal analysis
- Pricing comparison across properties
- Expiration date tracking
- Budget planning
- Vendor negotiation preparation

# See Also

- /generate-reports - Generate contract comparison reports
- Code/generate_contract_reports.py - Alternative method
- ~/.claude/skills/waste-contract-extractor/README.md
