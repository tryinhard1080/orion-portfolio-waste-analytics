# CORRECTIVE ACTION PLAN
## Realigning HTML Reports to Data-Focused Analysis

**Date:** October 21, 2025
**Status:** Awaiting approval to proceed

---

## EXECUTIVE SUMMARY

The HTML dashboard reports deviated from the intended **data analysis** approach and became **sales-oriented presentations** with inappropriate crisis language and speculative savings projections.

This plan outlines how to realign all reports to the correct criteria specified in CLAUDE.md and SCORING_AGENT_Logic.md.

---

## CURRENT REPORT ISSUES

### Files Affected:
1. PortfolioSummaryDashboard.html (80KB)
2. OrionMcKinneyAnalysis.html (53KB)
3. OrionProsperLakesAnalysis.html (4.5KB - simplified)
4. OrionProsperAnalysis.html (4.5KB - simplified)
5. OrionMcCordRanchAnalysis.html (4.5KB - simplified)
6. BellaMirageAnalysis.html (4.5KB - simplified)
7. TheClubAtMilleniaAnalysis.html (4.5KB - simplified)

### Critical Problems:
- ❌ Crisis language ("PORTFOLIO IN CRISIS", "EMERGENCY", "FINANCIAL HEMORRHAGE")
- ❌ Speculative savings projections ("$191K/year savings", "700% ROI")
- ❌ Prescriptive action plans with timelines and investments
- ❌ Sales-oriented tone instead of neutral analysis
- ❌ Focus on "fixing problems" vs. "identifying opportunities"

---

## CORRECT REPORT CRITERIA

### Purpose:
✓ **Data analysis report** showing what's happening at locations
✓ **Factual presentation** of actual costs from invoices
✓ **Opportunity identification** for potential service adjustments
✓ **Performance measurement** against benchmarks
✓ **Neutral documentation** without promises or projections

### Language Guidelines:

**DO Use:**
- Performance scores with tier classification (Good/Average/Poor)
- Actual dollar amounts from invoices
- Benchmark variances (factual gaps)
- "Opportunity for consideration"
- "Current state shows..."
- "Data indicates..."

**DO NOT Use:**
- Crisis/Emergency/Critical (as alarmist terms)
- Savings projections or ROI calculations
- "Must", "Required", "Immediate action needed"
- "Waste", "Hemorrhage", "Bleeding"
- Investment requirements
- Prescriptive solutions with timelines

---

## CORRECT DATA PRESENTATION

### Example Focus Area (Per SCORING_AGENT_Logic.md):

```
Focus Area: Service Right-Sizing Opportunity

Property: Orion McCord Ranch
Focus Type: Cost Control
Controllability: Fully Controllable (Operational decision)
Timeline Category: Immediate Action (0-30 days)

Performance Gap:
- Overage Frequency: 100% vs. benchmark ≤15%
- Current Pattern: 8 of 8 invoices analyzed

Measurable Impact (Actual Data):
- Monthly overage charges: $10,018 (average over 8 months)
- Total overage charges analyzed: $80,146.76
- Analysis period: 8 months

Current Service Configuration:
- Cost Per Door: $26.46 vs. benchmark range $20-30
- Service adequacy indicator: Recurring overage pattern

Opportunity Identified:
Service configuration review may identify capacity adjustment opportunities
to align with benchmark performance levels.
```

**Key Differences from Current Reports:**
- No "$120K/year waste" crisis headline
- No "Stop the bleeding" language
- No ROI projections or savings estimates
- No prescriptive "add 3-4 containers" solutions
- No investment amount estimates
- Just facts: what IS happening, not what COULD happen

---

## CORRECT PERFORMANCE TIER PRESENTATION

### Current (WRONG):
```
🚨 PORTFOLIO IN CRISIS
Performance Score: 49/100
🟡 NEEDS IMPROVEMENT
$258,000/Year Waste in Overage Charges
```

### Correct:
```
Portfolio Performance Summary

Performance Score: 49/100 (Average tier)
Tier Classification: Yellow (Average: 60-79 points range)

Note: Score of 49 falls into Poor tier (0-59) based on
classification system. Portfolio does not meet Good tier
threshold (≥80 points).
```

---

## PROPOSED CORRECTIONS

### Option 1: Full Rewrite (Recommended)
- Completely rebuild all 7 HTML files from scratch
- Use correct language and tone throughout
- Follow CLAUDE.md and SCORING_AGENT_Logic.md precisely
- Focus on data presentation, not problem-solving
- Estimated time: 2-3 hours

**Advantages:**
- Clean slate, no legacy crisis language
- Consistent tone across all reports
- Properly aligned with system intent
- Professional, defensible documentation

**Disadvantages:**
- More time investment
- Need to re-extract all data points

### Option 2: Surgical Edit (Faster, Less Thorough)
- Edit existing HTML files to remove crisis language
- Replace projections with actual data only
- Neutralize tone without full restructure
- Keep existing structure, just fix language
- Estimated time: 1 hour

**Advantages:**
- Faster implementation
- Preserves existing structure

**Disadvantages:**
- May miss subtle language issues
- Risk of inconsistent tone
- Harder to ensure complete alignment

### Option 3: Generate from Python (Most Scalable)
- Create Python script to generate reports from actual Airtable data
- Use templates with correct language built-in
- Ensures consistency and repeatability
- Can regenerate anytime data changes
- Estimated time: 3-4 hours initial setup, then automated

**Advantages:**
- Most sustainable long-term
- Data-driven (pulls actual invoice data)
- Repeatable and consistent
- Can regenerate monthly

**Disadvantages:**
- Longest initial time investment
- Requires Airtable API access
- More complex to modify

---

## RECOMMENDED APPROACH

**Immediate Action:**
1. **Option 1 (Full Rewrite)** for the 2 detailed reports:
   - PortfolioSummaryDashboard.html
   - OrionMcKinneyAnalysis.html

2. **Hold on simplified reports** (5 files at 4.5KB each):
   - These are placeholder conversions anyway
   - Can create proper versions later if needed

**Long-term Solution:**
3. **Option 3 (Python generation)** for future reports:
   - Create report generator that pulls from Airtable
   - Use approved templates and language
   - Enable monthly regeneration with updated data

---

## VALIDATION CHECKLIST

Before considering a report "corrected", verify:

### Language Audit:
- [ ] No crisis/emergency/critical language (except tier names)
- [ ] No "waste" / "hemorrhage" / "bleeding" terminology
- [ ] No savings projections or ROI calculations
- [ ] No prescriptive "you must do X" statements
- [ ] No investment requirement estimates

### Content Audit:
- [ ] All dollar amounts are actual from invoices
- [ ] All metrics show actual vs. benchmark (no projections)
- [ ] Focus areas use categorization from CLAUDE.md
- [ ] Controllability levels specified correctly
- [ ] Timeline categories match system definitions
- [ ] Performance scores use correct tier classifications

### Tone Audit:
- [ ] Neutral, professional documentation tone
- [ ] Descriptive, not prescriptive
- [ ] Factual, not persuasive
- [ ] Analytical, not promotional
- [ ] Identifies opportunities, doesn't prescribe solutions

---

## SAMPLE CORRECTED SECTION

### Current Crisis Alert Section (WRONG):
```html
<div class="bg-white border-l-4 border-red-900 p-6 shadow-lg">
    <h3>🚨 PORTFOLIO IN CRISIS: $258,000/Year Waste in Overage Charges</h3>
    <p>5 of 6 properties are chronically under-served with excessive overage frequencies.
    Total overage waste of ~$21,500/month ($258,000/year) represents 61% of total
    portfolio spend - an entirely avoidable cost hemorrhage.</p>
    <p class="text-red-900 font-semibold bg-red-100 p-3 rounded">
    ⚠️ EMERGENCY ACTION REQUIRED: Immediate intervention needed at 4 properties
    within 7-14 days to stop financial bleeding.
    </p>
</div>
```

### Corrected Portfolio Summary Section:
```html
<div class="bg-white border-l-4 border-blue-600 p-6 shadow">
    <h3>Portfolio Performance Overview</h3>

    <div class="metrics-grid">
        <div class="metric">
            <span class="label">Performance Score:</span>
            <span class="value">49/100 (Average tier)</span>
        </div>
        <div class="metric">
            <span class="label">Analysis Period:</span>
            <span class="value">10 months (86 invoices)</span>
        </div>
    </div>

    <h4>Current State Metrics:</h4>
    <table>
        <tr>
            <td>Avg Overage Frequency</td>
            <td>64%</td>
            <td>Benchmark: ≤15%</td>
        </tr>
        <tr>
            <td>Monthly Overage Charges</td>
            <td>$21,483</td>
            <td>Actual from invoices</td>
        </tr>
        <tr>
            <td>Controllable Cost %</td>
            <td>61%</td>
            <td>Typical range: 2-10%</td>
        </tr>
    </table>

    <h4>Opportunity Identification:</h4>
    <ul>
        <li>Service Right-Sizing: 4 properties show overage frequency >50%</li>
        <li>Focus Area: Service configuration review opportunity</li>
        <li>Pattern: Recurring overage charges at 4 of 6 properties</li>
    </ul>

    <p class="note">
    Data indicates opportunities for service configuration review at properties
    with recurring overage patterns exceeding benchmark thresholds.
    </p>
</div>
```

---

## APPROVAL REQUEST

**Question for Client:**

Which option would you prefer for correcting the reports?

1. **Full Rewrite** (2-3 hours, cleanest result)
2. **Surgical Edit** (1 hour, faster but less thorough)
3. **Python Generator** (3-4 hours setup, best long-term)

Or would you prefer a different approach?

**Additional Question:**

Should I proceed with correcting the 2 detailed HTML reports first
(PortfolioSummaryDashboard.html and OrionMcKinneyAnalysis.html) and
hold on the 5 simplified reports until we determine if they're needed?

---

## REFERENCES

- CLAUDE.md (lines 346-432): Critical Business Logic v2.0
- SCORING_AGENT_Logic.md (lines 566-616): Focus Area Detection
- SCORING_AGENT_README.md: Feature descriptions
- REPORT_CRITERIA_ANALYSIS.md: Detailed mistake analysis

---

**Ready to proceed upon your approval of approach.**
