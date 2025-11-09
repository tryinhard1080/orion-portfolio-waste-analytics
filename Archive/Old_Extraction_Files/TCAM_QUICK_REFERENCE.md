# The Club at Millenia (TCAM) - Extraction Quick Reference

## ✓ Task Completed Successfully

**Date:** November 3, 2025 10:10 AM
**Status:** COMPLETE
**Invoices Extracted:** 6 invoices (April - September 2025)
**Total Amount:** $70,061.16

---

## 📁 Output Files

### Updated Excel File (PRIMARY OUTPUT)
**File:** `COMPLETE_All_Properties_UPDATED_20251103_101053.xlsx`
**Location:** `C:\Users\Richard\Downloads\Orion Data Part 2\Extraction_Output\`
**Size:** 53 KB
**Sheets:** 11 total (10 properties + Portfolio Summary)

### Documentation
**Summary:** `TCAM_EXTRACTION_SUMMARY.txt` (detailed extraction report)
**Quick Reference:** This file (`TCAM_QUICK_REFERENCE.md`)

---

## 📊 What Was Extracted

### Invoice Coverage
- **Period:** April 2025 - September 2025 (6 months)
- **Property:** The Club at Millenia
- **Units:** 560 units
- **Service Provider:** (Extracted from invoices)

### Files Processed
1. TCAM 4.15.25.pdf → Invoice #1549125W460 ($11,426.50)
2. TCAM 5.15.25.pdf → Invoice #1553243W460 ($11,333.68)
3. TCAM 6.15.25.pdf → Invoice #1557411W460 ($10,830.71)
4. TCAM 7.15.25 (1).pdf → Invoice #1561532W460 ($12,906.08)
5. TCAM 8.15.25.pdf → Invoice #1565608W460 ($11,880.45)
6. TCAM 9.15.25.pdf → Invoice #1569687W460 ($11,683.74)

**Note:** Generic invoice files (invoice (1-10).pdf) were correctly identified as Bella Mirage and excluded.

---

## 📈 Key Metrics

### Financial Summary
- **6-Month Total:** $70,061.16
- **Average Monthly Cost:** $11,676.86
- **Average Cost Per Door:** $20.85/month
- **Lowest Month:** June 2025 ($10,830.71)
- **Highest Month:** July 2025 ($12,906.08)

### Data Quality
- **Extraction Success Rate:** 100% (6/6 invoices)
- **Property Validation:** 100% match verified
- **Critical Fields Extracted:** 100%
- **Validation Flags:** 0 critical issues

---

## 🔍 Excel File Structure

### Sheet: "The Club at Millenia"
**Total Rows:** 146 (including line item details)
**Columns:** 19 fields per row

**Key Columns:**
- Property Name
- Invoice Number
- Invoice Date
- Service Period Start/End
- Service Provider
- Total Amount
- Line Item Description
- Service Type
- Validation Flags
- Source File

### Portfolio Summary Sheet
Updated to include TCAM data with:
- Total invoices
- Total amount
- Average invoice amount
- Reference to property sheet

---

## 💡 How to Use the Data

### 1. Open Excel File
```bash
# File location
C:\Users\Richard\Downloads\Orion Data Part 2\Extraction_Output\
COMPLETE_All_Properties_UPDATED_20251103_101053.xlsx
```

### 2. Navigate to TCAM Sheet
- Open the Excel file
- Click on "The Club at Millenia" tab
- Review extracted invoice data

### 3. Analyze Performance
Use the data to:
- Calculate monthly Cost Per Door (CPD)
- Compare to portfolio benchmarks
- Identify cost trends
- Budget for future periods
- Generate performance reports

### 4. Verify Data Accuracy
- Cross-reference with original PDF invoices
- Check validation flags column
- Verify totals match source documents

---

## 📋 Monthly Cost Per Door (CPD) Analysis

| Month | Total Cost | CPD | vs. Avg |
|-------|------------|-----|---------|
| April 2025 | $11,426.50 | $20.40 | -2.2% |
| May 2025 | $11,333.68 | $20.24 | -2.9% |
| June 2025 | $10,830.71 | $19.34 | -7.2% ⭐ Best |
| July 2025 | $12,906.08 | $23.05 | +10.6% ⚠️ Highest |
| August 2025 | $11,880.45 | $21.22 | +1.8% |
| September 2025 | $11,683.74 | $20.86 | +0.0% |
| **6-Mo Avg** | **$11,676.86** | **$20.85** | **Baseline** |

**CPD Formula:** Monthly Cost ÷ 560 units

---

## 🎯 Comparison to Project Documentation

### From CLAUDE.md (Project Documentation)
**Property:** The Club at Millenia
**Units:** 560
**Monthly Cost:** $11,760.00 (documented baseline)
**CPD:** $21.00 (documented baseline)
**Status:** ✓ Verified

### Actual Data (6-Month Average)
**Average Monthly Cost:** $11,676.86
**Average CPD:** $20.85
**Variance:** -$83.14/month (-0.7%) ⭐ **Better than documented**

The extracted data shows TCAM is performing **slightly better** than the documented baseline, with an average CPD of $20.85 vs. the $21.00 baseline.

---

## ⚙️ Technical Details

### Extraction Method
- **API:** Claude Vision API (Anthropic)
- **Model:** claude-sonnet-4-20250514
- **Approach:** Document analysis with structured JSON extraction
- **Validation:** Automated property name matching and field completeness

### Scripts Used
**Primary Script:** `Code/extract_tcam_only.py`
**Location:** `C:\Users\Richard\Downloads\Orion Data Part 2\Code\`

### To Re-Run Extraction
```bash
cd "C:\Users\Richard\Downloads\Orion Data Part 2"
python Code/extract_tcam_only.py
```

---

## ✅ Next Steps

1. **Review Data**
   - Open Excel file
   - Verify TCAM sheet data
   - Check Portfolio Summary

2. **Validate Accuracy**
   - Compare totals with PDF invoices
   - Review validation flags column
   - Verify service period coverage

3. **Use for Analysis**
   - Generate performance reports
   - Calculate portfolio metrics
   - Compare to other properties
   - Identify optimization opportunities

4. **Update Documentation**
   - Confirm baseline metrics
   - Update property data if needed
   - Document any findings

---

## 📞 Support Information

### File Locations
- **Excel Output:** `Extraction_Output/COMPLETE_All_Properties_UPDATED_20251103_101053.xlsx`
- **Extraction Summary:** `Extraction_Output/TCAM_EXTRACTION_SUMMARY.txt`
- **Source Invoices:** `Invoices/TCAM *.pdf` (6 files)
- **Extraction Script:** `Code/extract_tcam_only.py`

### Key Files
- **Project Guide:** `CLAUDE.md`
- **Property Data:** Google Sheets (Spreadsheet ID: 1oy-F3p_CPpJaGGmGUMcjQMubRIRi7p4IID7mfpNLZJQ)
- **Documentation:** `Documentation/` folder

---

## 📝 Summary

✓ **Task:** Extract The Club at Millenia invoices
✓ **Invoices:** 6 PDFs processed (April - September 2025)
✓ **Output:** Updated Excel file with TCAM sheet
✓ **Data Quality:** 100% extraction success, 0 critical issues
✓ **Total Amount:** $70,061.16 over 6 months
✓ **Average CPD:** $20.85 (better than $21.00 baseline)

**All TCAM invoices have been successfully extracted and added to the comprehensive Excel file. The data is ready for analysis and reporting.**

---

*Last Updated: November 3, 2025 10:15 AM*
