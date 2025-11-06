# Invoice Extraction Verification Report

**Generated:** 2025-11-03
**Purpose:** Verify invoice extraction completeness across all properties

---

## Executive Summary

**CRITICAL FINDING:** Significant data extraction gaps identified across multiple properties.

| Property | PDFs Available | Invoices Extracted | Extraction Rate | Status |
|----------|---------------|-------------------|----------------|--------|
| **Orion Prosper Lakes** | **10** | **2** | **20%** | **❌ INCOMPLETE** |
| **Orion Prosper** | **16** | **1** | **6%** | **❌ INCOMPLETE** |
| Orion McKinney | 16 | 17 | 106% | ✅ Complete |
| Orion McCord (FL) | 8 | 9 | 112% | ✅ Complete |
| Bella Mirage | N/A | 10 | N/A | ⚠️ Needs folder check |
| The Club at Millenia | N/A | 6 | N/A | ⚠️ Needs folder check |

**Properties Not Checked (No dedicated invoice folders found):**
- Mandarina (3 invoices extracted)
- Pavilions at Arrowhead (2 invoices extracted)
- Springs at Alta Mesa (2 invoices extracted)
- Tempe Vista (2 invoices extracted)

---

## Detailed Analysis

### 1. Orion Prosper Lakes

**Invoice Folder Check:**
- Folder: `C:\Users\Richard\Downloads\Orion Data Part 2\Invoices\Orion Prosper Lakes Trash Bills\`
- PDF Files Found: **10**
- File Names:
  1. Republic Services-16302837_01-2025.pdf (01-2025)
  2. Republic Services-16338020_02-2025.pdf (02-2025)
  3. Republic Services-16390081_02-2025.pdf (02-2025)
  4. Republic Services-16396172_03-2025.pdf (03-2025)
  5. Republic Services-16512062_04-2025.pdf (04-2025)
  6. Republic Services-16569213_04-2025.pdf (04-2025)
  7. Republic Services-16605042_05-2025.pdf (05-2025)
  8. Republic Services-16660697_05-2025.pdf (05-2025)
  9. Republic Services-16750431_06-2025.pdf (06-2025)
  10. Republic Services-16834748_07-2025.pdf (07-2025)

**Extracted Data Check:**
- Excel Sheet: "Orion Prosper Lakes"
- Total Rows: 17 (multiple line items per invoice)
- Unique Invoices Extracted: **2**
- Invoice Numbers/Dates:
  1. 0615-002267720 - 2025-01-31 (Republic Services-16302837_01-2025.pdf) ✅
  2. 0615-002353052 - 2025-04-30 (Republic Services-16605042_05-2025.pdf) ✅

**Comparison:**
- Match Status: **❌ INCOMPLETE - CRITICAL GAP**
- PDFs vs Extracted: 10 files → 2 invoices extracted (20% extraction rate)
- Missing: 8 invoices (80% of available data)

**Missing Invoices:**
1. ❌ Republic Services-16338020_02-2025.pdf (February)
2. ❌ Republic Services-16390081_02-2025.pdf (February)
3. ❌ Republic Services-16396172_03-2025.pdf (March)
4. ❌ Republic Services-16512062_04-2025.pdf (April)
5. ❌ Republic Services-16569213_04-2025.pdf (April)
6. ❌ Republic Services-16660697_05-2025.pdf (May)
7. ❌ Republic Services-16750431_06-2025.pdf (June)
8. ❌ Republic Services-16834748_07-2025.pdf (July)

**Root Cause:**
The extraction process only captured 2 out of 10 available invoices. This suggests:
- Partial batch processing failure
- Process interruption during extraction
- Selective extraction (only certain months processed)
- File access or reading errors not logged

**Impact:**
- Missing 7 months of invoice data (Feb-Jul 2025, excluding partial coverage in April-May)
- Unable to calculate accurate monthly costs
- Cannot identify trends or seasonal patterns
- Performance metrics incomplete

**Recommendation:**
**URGENT - RE-EXTRACT ALL ORION PROSPER LAKES INVOICES**
1. Run extraction specifically for the 8 missing invoices
2. Validate each extraction for completeness
3. Update Excel file with complete dataset
4. Regenerate property performance reports

---

### 2. Orion Prosper

**Invoice Folder Check:**
- Folder: `C:\Users\Richard\Downloads\Orion Data Part 2\Invoices\Orion Prosper Trash Bills\`
- PDF Files Found: **16**
- File Names:
  1. Republic Services-16282934_01-2025.pdf (01-2025)
  2. Republic Services-16282935_01-2025.pdf (01-2025)
  3. Republic Services-16375230_02-2025.pdf (02-2025)
  4. Republic Services-16375231_02-2025.pdf (02-2025)
  5. Republic Services-16465536_03-2025.pdf (03-2025)
  6. Republic Services-16465537_03-2025.pdf (03-2025)
  7. Republic Services-16551031_04-2025.pdf (04-2025)
  8. Republic Services-16551032_04-2025.pdf (04-2025)
  9. Republic Services-16640472_05-2025.pdf (05-2025)
  10. Republic Services-16640473_05-2025.pdf (05-2025)
  11. Republic Services-16730675_06-2025.pdf (06-2025)
  12. Republic Services-16730676_06-2025.pdf (06-2025)
  13. Republic Services-16817842_07-2025.pdf (07-2025)
  14. Republic Services-16817843_07-2025.pdf (07-2025)
  15. Republic Services-16904288_08-2025.pdf (08-2025)
  16. Republic Services-16904289_08-2025.pdf (08-2025)

**Pattern:** Two invoices per month (Jan-Aug 2025) - likely separate service addresses or billing cycles

**Extracted Data Check:**
- Excel Sheet: "Orion Prosper"
- Total Rows: 4 (line items from single invoice)
- Unique Invoices Extracted: **1**
- Invoice Number/Date:
  1. 0615-002262594 - 2025-01-25 (Republic Services-16282934_01-2025.pdf) ✅

**Comparison:**
- Match Status: **❌ INCOMPLETE - CRITICAL GAP**
- PDFs vs Extracted: 16 files → 1 invoice extracted (6% extraction rate)
- Missing: 15 invoices (94% of available data)

**Missing Invoices:**
1. ❌ Republic Services-16282935_01-2025.pdf (January - second invoice)
2. ❌ Republic Services-16375230_02-2025.pdf (February)
3. ❌ Republic Services-16375231_02-2025.pdf (February - second invoice)
4. ❌ Republic Services-16465536_03-2025.pdf (March)
5. ❌ Republic Services-16465537_03-2025.pdf (March - second invoice)
6. ❌ Republic Services-16551031_04-2025.pdf (April)
7. ❌ Republic Services-16551032_04-2025.pdf (April - second invoice)
8. ❌ Republic Services-16640472_05-2025.pdf (May)
9. ❌ Republic Services-16640473_05-2025.pdf (May - second invoice)
10. ❌ Republic Services-16730675_06-2025.pdf (June)
11. ❌ Republic Services-16730676_06-2025.pdf (June - second invoice)
12. ❌ Republic Services-16817842_07-2025.pdf (July)
13. ❌ Republic Services-16817843_07-2025.pdf (July - second invoice)
14. ❌ Republic Services-16904288_08-2025.pdf (August)
15. ❌ Republic Services-16904289_08-2025.pdf (August - second invoice)

**Root Cause:**
Extreme extraction failure - only 1 invoice out of 16 processed (6%). This indicates:
- Critical batch processing failure
- Early termination of extraction process
- File path or naming issues preventing access
- Systematic error in extraction logic

**Impact:**
- **SEVERE DATA GAP** - Missing 8 months of complete invoice data
- Only January partially captured (1 of 2 invoices)
- Cannot calculate accurate Cost Per Door (CPD)
- Unable to identify service patterns or trends
- Performance scoring invalid
- Budget projections unreliable

**Recommendation:**
**CRITICAL - IMMEDIATE RE-EXTRACTION REQUIRED**
1. Prioritize Orion Prosper as highest-impact data gap
2. Extract all 16 invoices systematically
3. Verify dual-invoice pattern (2 per month)
4. Validate service address or billing cycle differences
5. Update Excel file with complete dataset
6. Regenerate all reports and performance metrics

---

### 3. Orion McKinney

**Invoice Folder Check:**
- Folder: `C:\Users\Richard\Downloads\Orion Data Part 2\Invoices\Orion McKinney Trash Bills\`
- PDF Files Found: **16**
- File Names (sample):
  1. Frontier Waste-16275266_01-2025.pdf
  2. CITY OF MCKINNEY-16338246_02-2025.pdf
  3. Frontier Waste-16355627_02-2025.pdf
  4. CITY OF MCKINNEY-16433228_03-2025.pdf
  ... (16 total)

**Extracted Data Check:**
- Excel Sheet: "Orion McKinney"
- Total Rows: 95
- Unique Invoices Extracted: **17**

**Comparison:**
- Match Status: **✅ COMPLETE (106% extraction rate)**
- PDFs vs Extracted: 16 files → 17 invoices extracted
- Note: 1 additional invoice may be from different source or duplicate month

**Root Cause:**
N/A - Extraction successful and complete

**Impact:**
None - Data complete and ready for analysis

**Recommendation:**
✅ No action required - Verify 17th invoice source if needed

---

### 4. McCord Park FL (Orion McCord Trash Bills)

**Invoice Folder Check:**
- Folder: `C:\Users\Richard\Downloads\Orion Data Part 2\Invoices\Orion McCord Trash Bills\`
- PDF Files Found: **8**
- File Names:
  1. Community Waste Disposal, LP-16239646_01-2025.pdf (January)
  2. Community Waste Disposal, LP-16325555_02-2025.pdf (February)
  3. Community Waste Disposal, LP-16423855_03-2025.pdf (March)
  4. Community Waste Disposal, LP-16502663_04-2025.pdf (April)
  5. Community Waste Disposal, LP-16589192_05-2025.pdf (May)
  6. Community Waste Disposal, LP-16681937_06-2025.pdf (June)
  7. Community Waste Disposal, LP-16777493_07-2025.pdf (July)
  8. Community Waste Disposal, LP-16856537_08-2025.pdf (August)

**Extracted Data Check:**
- Excel Sheet: "McCord Park FL"
- Total Rows: 42
- Unique Invoices Extracted: **9**

**Comparison:**
- Match Status: **✅ COMPLETE (112% extraction rate)**
- PDFs vs Extracted: 8 files → 9 invoices extracted
- Note: 1 additional invoice may be from different source or prior month

**Root Cause:**
N/A - Extraction successful and complete

**Impact:**
None - Data complete and ready for analysis

**Recommendation:**
✅ No action required - Verify 9th invoice source if needed

---

### 5. Other Properties (No Dedicated Invoice Folders)

The following properties have extracted data but no dedicated invoice folders were found in the main Invoices directory:

#### Bella Mirage
- Extracted invoices: 10
- Total rows: 102
- Status: ⚠️ **Needs investigation** - Where are source PDFs stored?

#### The Club at Millenia
- Extracted invoices: 6
- Total rows: 146
- Status: ⚠️ **Needs investigation** - Where are source PDFs stored?

#### Mandarina
- Extracted invoices: 3
- Total rows: 37
- Status: ⚠️ **Needs investigation** - Limited data, verify completeness

#### Pavilions at Arrowhead
- Extracted invoices: 2
- Total rows: 47
- Status: ⚠️ **Needs investigation** - Very limited data

#### Springs at Alta Mesa
- Extracted invoices: 2
- Total rows: 203
- Status: ⚠️ **Needs investigation** - Very limited invoices but high row count

#### Tempe Vista
- Extracted invoices: 2
- Total rows: 23
- Status: ⚠️ **Needs investigation** - Very limited data

**Note:** These properties may have invoices stored in:
- Root Invoices/ folder (loose PDFs found)
- Different naming convention folders
- External sources not yet organized
- May explain the loose PDFs in the main Invoices/ directory:
  - invoice (1).pdf through invoice (10).pdf (Bella Mirage?)
  - TCAM *.pdf files (The Club at Millenia)

---

## Summary Dashboard

### Extraction Completeness by Property

| Property | Available PDFs | Extracted | Completeness | Priority |
|----------|---------------|-----------|--------------|----------|
| Orion Prosper | 16 | 1 | 6% | 🔴 CRITICAL |
| Orion Prosper Lakes | 10 | 2 | 20% | 🔴 CRITICAL |
| Mandarina | ? | 3 | ? | 🟡 REVIEW |
| Pavilions at Arrowhead | ? | 2 | ? | 🟡 REVIEW |
| Springs at Alta Mesa | ? | 2 | ? | 🟡 REVIEW |
| Tempe Vista | ? | 2 | ? | 🟡 REVIEW |
| Orion McKinney | 16 | 17 | 106% | 🟢 COMPLETE |
| McCord Park FL | 8 | 9 | 112% | 🟢 COMPLETE |
| Bella Mirage | ? | 10 | ? | 🟢 LIKELY OK |
| The Club at Millenia | ? | 6 | ? | 🟢 LIKELY OK |

### Critical Gaps Identified

**Total Missing Invoices:** 23 invoices (8 + 15)

**Properties Requiring Re-Extraction:**
1. **Orion Prosper** - Missing 15 of 16 invoices (94% gap)
2. **Orion Prosper Lakes** - Missing 8 of 10 invoices (80% gap)

**Properties Requiring Investigation:**
3. Mandarina - Verify invoice source location
4. Pavilions at Arrowhead - Verify invoice source location
5. Springs at Alta Mesa - Verify invoice source location
6. Tempe Vista - Verify invoice source location

---

## Recommended Action Plan

### Phase 1: Critical Re-Extraction (IMMEDIATE)

**Priority 1: Orion Prosper**
```bash
# Extract all 16 missing invoices
python Code/orchestrate_extraction.py --property "Orion Prosper" --force-reprocess
```

**Expected Result:** 16 invoices extracted, ~32-64 rows (2 invoices/month × 8 months × 2-4 line items each)

**Priority 2: Orion Prosper Lakes**
```bash
# Extract 8 missing invoices
python Code/orchestrate_extraction.py --property "Orion Prosper Lakes" --force-reprocess
```

**Expected Result:** 10 invoices extracted, ~40-50 rows (1 invoice/month × 10 months × 4-5 line items each)

### Phase 2: Invoice Organization (SHORT-TERM)

1. **Locate Missing Invoice Sources:**
   - Check if loose PDFs in Invoices/ root belong to other properties
   - Identify TCAM files (The Club at Millenia?)
   - Identify invoice (1-10).pdf files (Bella Mirage?)

2. **Organize Into Property Folders:**
   - Create folders for missing properties
   - Move loose PDFs to appropriate property folders
   - Standardize naming convention

3. **Verify Completeness:**
   - Count expected invoices per property
   - Identify date range coverage
   - Flag any missing months

### Phase 3: Complete Re-Validation (POST-EXTRACTION)

```bash
# After re-extraction, validate all data
python Code/validate_extracted_data.py

# Update Google Sheets with complete dataset
python Code/update_google_sheets.py

# Regenerate all reports
python Code/generate_reports_from_sheets.py
python Code/generate_contract_reports.py

# Final validation
python Code/validate_reports.py
```

---

## Technical Details

### Extraction Statistics

**Total Properties in Excel:** 11 (10 properties + 1 portfolio summary)

**Total Rows Extracted:** 816 rows across all properties

**Total Unique Invoices:** 61 invoices extracted

**Estimated Missing Invoices:** 23+ invoices (based on folder analysis)

**Data Quality Issues:**
- 2 properties with <10% extraction rate (critical failure)
- 4 properties with unknown source file locations
- Inconsistent folder naming conventions
- Loose PDFs in root directory not processed

### File Path Analysis

**Consistent Folder Structure (4 properties):**
- Orion Prosper Trash Bills/
- Orion Prosper Lakes Trash Bills/
- Orion McKinney Trash Bills/
- Orion McCord Trash Bills/

**Missing Folder Structure (6 properties):**
- Bella Mirage (data exists, folder location unknown)
- The Club at Millenia (data exists, folder location unknown)
- Mandarina (data exists, folder location unknown)
- Pavilions at Arrowhead (data exists, folder location unknown)
- Springs at Alta Mesa (data exists, folder location unknown)
- Tempe Vista (data exists, folder location unknown)

**Recommendation:** Create standardized folder structure for all properties:
```
Invoices/
├── Bella Mirage Trash Bills/
├── Mandarina Trash Bills/
├── McCord Park FL Trash Bills/
├── Orion McKinney Trash Bills/
├── Orion Prosper Trash Bills/
├── Orion Prosper Lakes Trash Bills/
├── Pavilions at Arrowhead Trash Bills/
├── Springs at Alta Mesa Trash Bills/
├── Tempe Vista Trash Bills/
└── The Club at Millenia Trash Bills/
```

---

## Conclusion

**Critical Action Required:** The extraction process has significant gaps that must be addressed before reports can be considered reliable.

**Immediate Next Steps:**
1. ✅ Re-extract Orion Prosper invoices (15 missing)
2. ✅ Re-extract Orion Prosper Lakes invoices (8 missing)
3. ⚠️ Locate and organize loose invoice PDFs
4. ⚠️ Validate all property data sources
5. ⚠️ Update Google Sheets with complete dataset
6. ⚠️ Regenerate all performance reports

**Timeline:**
- Phase 1 (Re-extraction): 1-2 hours
- Phase 2 (Organization): 2-4 hours
- Phase 3 (Validation): 1 hour
- **Total Estimated Time:** 4-7 hours

**Impact of Completion:**
- Accurate Cost Per Door (CPD) calculations
- Reliable performance benchmarking
- Complete trend analysis
- Valid portfolio-level metrics
- Trustworthy client-facing reports

---

**Report Generated By:** Data Verification Agent
**Date:** 2025-11-03
**Status:** ❌ Critical gaps identified - Action required
**Next Review:** After Phase 1 re-extraction completion
