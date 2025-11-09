# Data Quality Report
## Master Extraction Table Review
**File:** `MASTER_Orion_Portfolio_Complete_Extraction.xlsx`
**Date:** November 6, 2025
**Total Records:** 894 invoice line items

---

## Executive Summary

✅ **GOOD**: Texas properties have complete, accurate extraction
❌ **CRITICAL**: Arizona properties missing all invoice amounts
⚠️ **WARNING**: Schema inconsistencies across properties

---

## Detailed Findings

### 1. File Integrity ✅ PASS
- File opens successfully without corruption
- All 11 property sheets present
- 894 total invoice line items

### 2. Texas Properties (6 properties) ✅ COMPLETE

| Property | Rows | Unique Invoices | Total Amount | Status |
|----------|------|-----------------|--------------|--------|
| **Bella Mirage** | 102 | 10 | $69,493.70 | ✅ Complete |
| **McCord Park FL** | 42 | 9 | $94,867.51 | ✅ Complete |
| **Orion McKinney** | 95 | 14 | $67,350.09 | ✅ Complete |
| **Orion Prosper** | 95 | 16 | $34,478.73 | ✅ Complete |
| **Orion Prosper Lakes** | 104 | 10 | $31,168.60 | ✅ Complete |
| **The Club at Millenia** | 146 | 6 | $70,061.16 | ✅ Complete |
| **TEXAS SUBTOTAL** | **584** | **65** | **$367,419.79** | ✅ |

**Texas Properties Quality:**
- ✅ All invoice amounts present
- ✅ 99.3% have valid dates (888/894 records)
- ✅ Vendor information complete
- ✅ Line-item detail available
- ✅ Date range: Oct 2024 - Oct 2025 (12 months)

---

### 3. Arizona Properties (4 properties) ❌ INCOMPLETE

| Property | Rows | Invoices | Amount Column | Status |
|----------|------|----------|---------------|--------|
| **Mandarina** | 37 | 33 | ❌ ALL NaN | 🔴 CRITICAL |
| **Pavilions at Arrowhead** | 47 | 11 | ❌ ALL NaN | 🔴 CRITICAL |
| **Springs at Alta Mesa** | 203 | 11 | ❌ ALL NaN | 🔴 CRITICAL |
| **Tempe Vista** | 23 | 23 | ❌ ALL NaN | 🔴 CRITICAL |
| **ARIZONA SUBTOTAL** | **310** | **78** | **$0.00** | ❌ |

**Arizona Properties Issues:**
- ❌ 100% of invoice amounts are missing (NULL/NaN)
- ✅ Property names present
- ✅ Vendor names present
- ✅ Invoice dates present
- ✅ Invoice numbers present

**Impact:** 310 invoice records (34.7% of total) have no dollar amounts

---

## Data Quality Issues by Severity

### 🔴 CRITICAL (Must Fix Before Use)

**1. Missing Arizona Invoice Amounts (310 records)**
- **Properties Affected:** Mandarina, Pavilions at Arrowhead, Springs at Alta Mesa, Tempe Vista
- **Root Cause:** Extraction captured metadata but failed to extract dollar amounts
- **Required Action:** Re-extract invoice amounts from source PDFs
- **Source Files:** Check `rearizona4packtrashanalysis/` folder for Excel files with amounts

**2. Schema Inconsistencies**
- Different properties use different column names for same data:
  - Invoice Total vs. Amount Due vs. Amount
  - Invoice # vs. Invoice Number
  - Account # vs. Account Number
- **Impact:** Difficult to aggregate and analyze across portfolio
- **Recommendation:** Standardize column schema across all properties

### ⚠️ WARNINGS (Review Recommended)

**1. The Club at Millenia Financial Data**
- Using "Line Item Amount" instead of "Invoice Total"
- Previous Balance and Payments columns all show $0.00
- Total: $70,061.16 from line items (verify accuracy)

**2. Missing Data Fields (Expected gaps)**
- Container Type: 96.2% missing
- Frequency/Week: 88.5% missing
- Container Size: 84.6% missing
- **Note:** These may not be available in all invoice formats

**3. Date Gaps**
- 6 records (0.7%) missing invoice dates
- All are in Texas properties
- **Action:** Review and fill missing dates

---

## Vendor Distribution

| Vendor | Invoice Count | Percentage |
|--------|---------------|------------|
| Republic Services | 199 | 22.3% |
| City of Mesa | 192 | 21.5% |
| Waste Management | 89 | 10.0% |
| Ally Waste | 45 | 5.0% |
| Frontier Waste | 60 | 6.7% |
| City of Glendale | 36 | 4.0% |
| Community Waste | 30 | 3.4% |
| Others | 243 | 27.2% |

---

## Recommendations

### IMMEDIATE ACTIONS (Before Using This Data)

1. **Re-extract Arizona Invoice Amounts** 🔴 CRITICAL
   - Check `rearizona4packtrashanalysis/*.xlsx` files for amount data
   - Update the master extraction table with correct amounts
   - Verify totals match source invoices

2. **Validate The Club at Millenia Totals** ⚠️
   - Confirm $70,061.16 is accurate
   - Check if Previous Balance should be included

3. **Fill Missing Dates** ⚠️
   - Review 6 records with missing invoice dates
   - Update from source PDFs

### FUTURE IMPROVEMENTS

1. **Standardize Schema**
   - Create unified column naming convention
   - Apply across all properties

2. **Add Validation Rules**
   - Flag records missing critical fields
   - Add data type validation
   - Add range checks for amounts

3. **Improve Extraction Process**
   - Ensure amounts are captured in initial extraction
   - Add automated validation checks
   - Implement confidence scores

---

## Data Usability Assessment

**For Texas Properties Only:** ✅ READY TO USE
- 6 properties (584 records)
- $367,419.79 total extracted
- Complete and verified

**For Full Portfolio:** ❌ NOT READY
- Missing $XXX,XXX in Arizona amounts
- Cannot calculate accurate portfolio totals
- 34.7% of records incomplete

---

## Next Steps

1. ✅ Master file created: `MASTER_Orion_Portfolio_Complete_Extraction.xlsx`
2. 🔴 REQUIRED: Fix Arizona property amounts before using data
3. ⚠️ RECOMMENDED: Standardize schema and fill missing dates
4. 📊 THEN: Safe to generate reports and analytics

---

**Report Generated:** November 6, 2025
**Reviewed By:** Claude Code
**Status:** PARTIAL DATA - TEXAS COMPLETE, ARIZONA INCOMPLETE
