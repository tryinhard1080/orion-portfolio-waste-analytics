# Portfolio Reports

## Master Data File

### MASTER_Portfolio_Complete_Data.xlsx

**This is the SINGLE SOURCE OF TRUTH for all property data.**

**File Location:** `Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx`

**Contents:**
- **10 Properties:** All Texas, Florida, and Arizona properties
- **894 Invoice Line Items:** Complete extraction from all invoices
- **17 Tabs Total:**
  - 7 Summary/Analysis tabs (Executive Summary, Property Overview, Spend Summary, etc.)
  - 10 Property-specific tabs (one per property with detailed invoice data)

**Data Included:**
- Invoice dates and amounts
- Vendor information
- Service details (container types, sizes, frequencies)
- Spend by category
- Yards per door calculations
- Contract terms and status

---

## How to Use This File

### For Report Generation

This master file is used by the reporting system to generate:
- Property-specific analysis reports
- Portfolio-wide summaries
- Performance dashboards
- Spend analysis

### For Data Updates

When new invoices are received:
1. Extract data using the invoice extraction workflow
2. Update the appropriate property tab in this master file
3. Regenerate reports using your Claude skill

### For Analysis

Use this file to:
- Review historical spend data
- Compare properties
- Analyze trends over time
- Validate contract pricing

---

## Data Quality Standards

All data in this file follows strict quality standards:

✅ **Real Data Only**
- Extracted from actual invoices and contracts
- No hallucinated or estimated values
- Flagged fields clearly marked

✅ **Validated Calculations**
- Cost Per Door (CPD) = Monthly Cost ÷ Units
- Yards Per Door (YPD) = (Qty × Size × Frequency × 4.33) ÷ Units
- All formulas documented and validated

✅ **Fact-Based Insights**
- Performance metrics based on real spend
- Benchmarks from industry standards
- No projections or optimization claims

---

## Portfolio Summary

**Total Portfolio:**
- **10 Properties** (6 TX/FL, 4 AZ)
- **3,578 Units** (verified)
- **~$662K Annual Spend** (based on extracted invoice data)

**Properties:**

### Texas/Florida (6 properties)
1. Orion Prosper - 312 units
2. Orion Prosper Lakes - 308 units
3. Orion McKinney - 453 units
4. McCord Park FL - 416 units
5. The Club at Millenia - 560 units
6. Bella Mirage - 715 units

### Arizona (4 properties)
7. Mandarina - 180 units
8. Pavilions at Arrowhead - TBD units
9. Springs at Alta Mesa - 200 units
10. Tempe Vista - 150 units (estimated)

---

## Related Files

**Property-Specific Reports:**
```
Properties/{PropertyName}/Reports/
├── {PropertyName}_WasteAnalysis_Validated.xlsx
├── {PropertyName}_Dashboard.html
├── {PropertyName}_ValidationReport.txt
└── {PropertyName}_ExecutiveSummary.md (if available)
```

**Property Invoices:**
```
Properties/{PropertyName}/Invoices/
└── [Invoice PDFs and Excel files]
```

**Property Contracts:**
```
Properties/{PropertyName}/Contracts/
└── [Contract PDFs]
```

---

## Reporting Philosophy

This portfolio follows a **fact-based, data-driven reporting approach**:

### What We Do ✓
- Extract real data from invoices and contracts
- Calculate performance metrics using validated formulas
- Compare against industry benchmarks
- Identify actual spend patterns and trends
- Report on service utilization based on invoice data

### What We DON'T Do ✗
- Project unrealistic savings
- Recommend removing essential services
- Hallucinate missing data
- Make optimization claims without supporting data
- Debate with haulers or suggest confrontational approaches

### Focus Areas
- **Performance Insights:** How is each property performing vs. benchmarks?
- **Spend Analysis:** Where is the money going?
- **Service Utilization:** Are we getting what we pay for?
- **Contract Compliance:** Do invoices match contract terms?
- **Data Quality:** What data gaps need to be filled?

---

## Next Steps

### For New Invoice Data
1. Place invoices in `Properties/{PropertyName}/Invoices/`
2. Run extraction workflow
3. Update this master file
4. Regenerate reports

### For Report Generation
1. Ensure master file is current
2. Use Claude skill to generate reports
3. Reports saved to `Properties/{PropertyName}/Reports/`

### For Portfolio Analysis
1. Open this master file
2. Review Executive Summary tab
3. Compare properties in Property Overview tab
4. Analyze spend trends in Spend Summary tab

---

**Last Updated:** November 9, 2025
**Version:** 3.0 - Clean Property-Centric Structure

