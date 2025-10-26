# Data Integrity Guide

**Version 1.0** - October 2025

## Purpose

This guide establishes the data integrity principles and validation standards for the Orion Portfolio Waste Management Analytics System. It ensures all extracted data is accurate, verifiable, and never hallucinated.

---

## Core Philosophy

### Guiding Principle

**"Realistic, data-driven insights based on actual findings"**

All analysis must be grounded in verifiable data from invoices, contracts, and historical records. Projections, estimates, and assumptions are only acceptable when explicitly labeled and based on documented patterns.

### Non-Negotiable Rules

1. **Never hallucinate data** - If a field is missing, flag it
2. **Never guess** - If data is ambiguous, ask the user
3. **Never project unrealistic savings** - Base recommendations on actual findings
4. **Always flag uncertainty** - Use the three-tier flagging system
5. **Always provide audit trail** - Document data source and confidence level

---

## Required Field Validation

### Critical Fields (Red Flag if Missing)

These fields are **absolutely required** for data integrity:

| Field | Why Critical | If Missing |
|-------|-------------|------------|
| Property Name | Identifies which property this invoice belongs to | Cannot proceed - CRITICAL FLAG |
| Invoice Date | Required for time-series analysis and payment tracking | Cannot proceed - CRITICAL FLAG |
| Total Amount | Core financial data point | Cannot proceed - CRITICAL FLAG |
| Vendor Name | Identifies service provider | Cannot proceed - CRITICAL FLAG |

**Action Required:** All critical fields must be manually reviewed and populated before proceeding.

### Important Fields (Yellow Flag if Missing/Ambiguous)

These fields are important for analysis but can be resolved:

| Field | Why Important | If Missing/Ambiguous |
|-------|--------------|---------------------|
| Pickup Frequency | Required for service optimization analysis | Flag as NEEDS REVIEW - check contract |
| Container Count | Required for capacity analysis | Flag as NEEDS REVIEW - review invoice carefully |
| Container Size | Required for yards-per-door calculations | Flag as NEEDS REVIEW - check contract |
| Service Period | Required for matching invoices to months | Flag as NEEDS REVIEW - infer from date if possible |
| Base Charges | Required for overage analysis | Flag as NEEDS REVIEW - separate from total if possible |
| Overage Charges | Critical for identifying cost inefficiencies | Flag as NEEDS REVIEW - separate from total if possible |

**Action Recommended:** Review and resolve before generating final reports.

### Calculated Fields (Green Flag - Validation Suggested)

These fields can be calculated or inferred, but should be spot-checked:

| Field | Calculation Method | Confidence Level |
|-------|-------------------|------------------|
| Cost Per Door (CPD) | Total Amount ÷ Unit Count | High (if inputs are accurate) |
| Yards Per Door (YPD) | (Container Size × Count) ÷ Units | High (if inputs are accurate) |
| Frequency (derived) | Count of pickup dates ÷ days in period | Medium (requires validation) |
| Overage (calculated) | Total Amount - Base Charges | Medium (if base charges known) |

**Action Suggested:** Spot-check 10-20% of calculated values against source invoices.

---

## Flagging System

### Three-Tier Flag Levels

#### 🔴 Red Flag: CRITICAL

**Severity:** Cannot proceed without resolution

**Triggers:**
- Missing property name
- Missing invoice date
- Missing total amount
- Missing vendor name
- Corrupt/unreadable invoice file

**Resolution:**
1. Stop extraction workflow
2. Display invoice filename and missing field
3. Prompt user for manual input
4. Document manual entry in audit log
5. Re-run validation after resolution

**Example:**
```
🔴 CRITICAL FLAG
Invoice: Orion_Prosper_Jan2025.pdf
Field: Invoice Date
Issue: Date field not found in invoice
Action: Please review invoice PDF and manually enter date

Enter Invoice Date (YYYY-MM-DD): _
```

#### 🟡 Yellow Flag: NEEDS REVIEW

**Severity:** Data exists but is ambiguous or incomplete

**Triggers:**
- "Container" mentioned but no count specified
- Frequency unclear (doesn't say weekly/monthly/etc.)
- Total amount present but can't separate base from overage
- Multiple possible values (e.g., two dates in invoice)
- Low confidence extraction (<70%)

**Resolution:**
1. Flag for user review
2. Display extracted value and context
3. Allow user to confirm, update, or skip
4. Document user decision
5. Continue with flagged item marked

**Example:**
```
🟡 NEEDS REVIEW
Invoice: Bella_Mirage_Feb2025.pdf
Field: Pickup Frequency
Current Value: (not found)
Issue: Invoice shows charges but doesn't state pickup frequency
Context: Found charges for "Compactor Service" - $7,636
Action: Check contract for frequency OR review invoice carefully

Options:
  (c) Confirm missing - will need manual entry later
  (u) Update with correct value now
  (s) Skip for now

Choice: _
```

#### 🟢 Green Flag: VALIDATION SUGGESTED

**Severity:** Low priority - spot-check recommended

**Triggers:**
- Field calculated from other fields
- Field inferred from patterns
- Confidence level 70-85%
- Field extracted successfully but should be verified

**Resolution:**
1. Allow extraction to continue
2. Mark field as "calculated" or "inferred"
3. Include in validation report
4. Recommend spot-checking 10-20% of flagged items

**Example:**
```
🟢 VALIDATION SUGGESTED
Invoice: Orion_McKinney_Apr2025.pdf
Field: Pickup Frequency
Extracted Value: Weekly
Confidence: 78%
Method: Inferred from 4 pickup dates found in invoice (4/1, 4/8, 4/15, 4/22)
Action: Spot-check recommended - verify frequency matches contract

Options:
  (c) Confirm - looks correct
  (u) Update - incorrect value
  (s) Skip - review later

Choice: _
```

---

## Extraction Scenarios

### Scenario 1: Perfect Invoice

**Invoice characteristics:**
- All fields clearly labeled
- Standard format
- No ambiguities

**Extraction result:**
```json
{
  "filename": "Orion_Prosper_Jan2025.pdf",
  "property_name": "Orion Prosper",
  "invoice_date": "2025-01-15",
  "service_period": "January 2025",
  "vendor": "Republic Services",
  "total_amount": 4308.72,
  "base_charges": 4150.00,
  "overage_charges": 158.72,
  "container_type": "Compactor",
  "container_size": 30,
  "container_count": 1,
  "pickup_frequency": "Weekly",
  "pickups_this_period": 4,
  "flags": [],
  "confidence": 95,
  "extraction_method": "direct"
}
```

**Flags:** None - proceed to next invoice

---

### Scenario 2: Missing Frequency

**Invoice characteristics:**
- Total amount shown
- Container mentioned
- No frequency stated

**Extraction result:**
```json
{
  "filename": "Bella_Mirage_Feb2025.pdf",
  "property_name": "Bella Mirage",
  "invoice_date": "2025-02-10",
  "service_period": "February 2025",
  "vendor": "Waste Management",
  "total_amount": 7636.20,
  "base_charges": null,
  "overage_charges": null,
  "container_type": "Compactor",
  "container_size": 40,
  "container_count": null,
  "pickup_frequency": null,
  "pickups_this_period": null,
  "flags": [
    {
      "level": "NEEDS_REVIEW",
      "field": "pickup_frequency",
      "message": "Invoice shows charges but doesn't state pickup frequency",
      "action": "Check contract for scheduled frequency",
      "confidence": 0
    },
    {
      "level": "NEEDS_REVIEW",
      "field": "container_count",
      "message": "Invoice mentions 'compactor service' but doesn't specify count",
      "action": "Review invoice to determine number of compactors",
      "confidence": 0
    }
  ],
  "confidence": 60,
  "extraction_method": "partial"
}
```

**Flags:** 2 yellow flags - user review required

**Resolution workflow:**
1. Run `/review-flags` command
2. User checks contract: Frequency = "2x per week"
3. User reviews invoice: Container count = 2
4. Update extraction_results.json
5. Re-run validation
6. Proceed to next invoice

---

### Scenario 3: Ambiguous Charges

**Invoice characteristics:**
- Total amount shown
- No itemization
- Can't separate base from overages

**Extraction result:**
```json
{
  "filename": "McCord_Park_Mar2025.pdf",
  "property_name": "McCord Park FL",
  "invoice_date": "2025-03-05",
  "service_period": "March 2025",
  "vendor": "Community Waste Disposal",
  "total_amount": 10911.68,
  "base_charges": null,
  "overage_charges": null,
  "container_type": "Compactor",
  "container_size": 30,
  "container_count": 1,
  "pickup_frequency": "Weekly",
  "pickups_this_period": 5,
  "flags": [
    {
      "level": "NEEDS_REVIEW",
      "field": "charge_breakdown",
      "message": "Cannot separate base charges from overage charges",
      "action": "Review invoice line items to identify if extra pickups were charged",
      "confidence": 0
    },
    {
      "level": "VALIDATION_SUGGESTED",
      "field": "pickups_this_period",
      "message": "5 pickups found in March (one extra beyond weekly contract)",
      "action": "Verify this matches invoice and identify if overage was charged",
      "confidence": 85
    }
  ],
  "confidence": 70,
  "extraction_method": "partial"
}
```

**Flags:** 1 yellow, 1 green - review recommended

**Resolution workflow:**
1. User reviews invoice PDF
2. Finds line item: "Extra pickup - 3/25/2025 - $350"
3. Updates: base_charges = 10561.68, overage_charges = 350.00
4. Confirms pickups_this_period = 5
5. Documents finding: "Found $350 overage charge for extra pickup"
6. This becomes a real insight for optimization

---

## Validation Checklist

### Pre-Extraction Checklist

Before running extraction:

- [ ] All invoice PDFs in correct folders (`Invoices/{PropertyName}/`)
- [ ] PDFs are text-based (not scanned images)
- [ ] Filenames follow naming convention
- [ ] Backup of invoices exists
- [ ] ANTHROPIC_API_KEY configured correctly

### During Extraction Checklist

While extraction is running:

- [ ] Monitor for error messages
- [ ] Note any file access issues
- [ ] Watch for unusual patterns (all missing same field)
- [ ] Check extraction_results.json is being created

### Post-Extraction Checklist

After extraction completes:

- [ ] Check flag summary (red/yellow/green counts)
- [ ] Review all red flags immediately
- [ ] Assess yellow flags for patterns
- [ ] Spot-check 10-20% of green flags
- [ ] Run `/review-flags` for interactive resolution
- [ ] Re-run validation after resolving flags
- [ ] Only proceed to `/update-sheets` after validation passes

---

## Realistic Insights Framework

### What Qualifies as a "Real Finding"?

✓ **Acceptable insights (based on actual data):**
- "Found $3,000 in overage charges across Q1 invoices"
- "McCord Park had 3 extra pickups beyond contract in February"
- "Bella Mirage's container utilization is running at 52%"
- "Current CPD is $21, which is above portfolio average of $16.15"

✗ **Unacceptable projections (not grounded in data):**
- "Could save $50,000 by eliminating one compactor"
- "Potential savings of 30% if frequency is reduced"
- "Projected annual savings of $100,000"
- "Recommend removing containers to cut costs"

### Recommendation Framework

**Format:** [Finding] + [Actual Impact] + [Grounded Recommendation]

**Examples:**

1. **Overage Finding:**
   - Finding: "Identified $2,100 in overage charges across 3 properties in Q1"
   - Actual Impact: "Extra pickups occurred in Feb (2x) and Mar (1x)"
   - Recommendation: "Review service schedule to determine if frequency adjustment would prevent future overages"

2. **Utilization Finding:**
   - Finding: "Orion Prosper compactor running at 51.7% capacity"
   - Actual Impact: "Below optimal range of 65-75%"
   - Recommendation: "Monitor usage patterns for seasonal changes; current frequency appears appropriate"

3. **Contract Finding:**
   - Finding: "McCord Park contract expires in 90 days (12/31/2025)"
   - Actual Impact: "60-day notice required, deadline approaching"
   - Recommendation: "Initiate contract renewal discussions by October 31 to meet notice deadline"

---

## Quality Assurance Process

### Level 1: Automated Validation

**Run automatically during extraction:**
- Required field checks
- Data type validation
- Range checks (e.g., dates in reasonable range)
- Duplicate detection
- File integrity checks

### Level 2: Flagged Item Review

**User-driven via `/review-flags`:**
- Interactive resolution of red flags
- Review of yellow flags
- Spot-check of green flags
- Manual correction entry
- Audit trail creation

### Level 3: Validation Report

**Generated after extraction:**
- Summary of all flags
- Confidence scores by field
- Extraction method breakdown
- Data completeness metrics
- Recommended actions

### Level 4: Report Validation

**Before distribution (via `/validate-all`):**
- Language validation (no prohibited terms)
- Data accuracy checks
- Calculation verification
- Cross-referencing with source data
- Final quality gate

---

## Audit Trail Requirements

Every extraction must maintain:

**Extraction Metadata:**
- Timestamp of extraction
- Anthropic API version used
- Extraction method (Vision API vs subagents)
- Confidence scores
- Flags generated

**User Actions:**
- Manual corrections with timestamp
- Flag resolution decisions
- Validation confirmations
- Notes or comments added

**Data Lineage:**
- Source file (invoice PDF path)
- Extraction method
- Calculation formulas (for derived fields)
- Manual vs automated designation

---

## Common Pitfalls to Avoid

### ❌ Pitfall 1: Assuming Standard Formats

**Problem:** Expecting all invoices to have same layout

**Solution:** Use robust extraction that handles variations; flag unexpected formats

### ❌ Pitfall 2: Silent Failures

**Problem:** Missing field goes unnoticed, leads to incorrect CPD calculation

**Solution:** Always flag missing required fields; never calculate with null values

### ❌ Pitfall 3: Over-Confidence in Extraction

**Problem:** Accepting all extracted values as correct

**Solution:** Use confidence scores; spot-check samples; validate against contracts

### ❌ Pitfall 4: Projecting Instead of Reporting

**Problem:** Recommending "save $X by doing Y" without proof

**Solution:** Only cite actual findings; flag opportunities for investigation

### ❌ Pitfall 5: Skipping Flag Review

**Problem:** Proceeding to analysis with unresolved flags

**Solution:** Make `/review-flags` mandatory in workflow before `/update-sheets`

---

## Summary

**Key Takeaways:**

1. **Never hallucinate** - Flag it instead
2. **Three-tier flagging** - Red/Yellow/Green
3. **Realistic insights** - Based on actual data only
4. **Quality workflow** - Extract → Flag → Review → Validate → Proceed
5. **Audit trail** - Document everything

**Commands to Remember:**

- `/extract-invoices` - Extraction with flagging
- `/review-flags` - Interactive resolution
- `/validate-all` - Final quality check

**For Questions:**

Refer to:
- This guide for validation standards
- `CLAUDE.md` for overall system documentation
- Individual command files in `.claude/commands/` for workflows

---

**Document Version:** 1.0
**Last Updated:** October 25, 2025
**Maintained By:** Orion Portfolio Analytics Team
