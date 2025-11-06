# Arizona Invoice Consolidation Summary

**Extraction Date:** 2025-11-03 08:39:13
**Extractor Script:** `Code/consolidate_arizona_invoices.py`
**Source Directory:** `rearizona4packtrashanalysis/`

---

## Executive Summary

Successfully consolidated **310 invoices** from **9 Excel files** covering **4 Arizona properties** with **5 different vendors**.

**Total Invoice Amount:** $302,693.51
**Date Range:** October 15, 2024 - October 2, 2025
**Data Quality:** 100% complete (no missing critical fields)

---

## Property Breakdown

| Property | Invoice Count | Total Amount | Avg Invoice |
|----------|--------------|--------------|-------------|
| **Mandarina** | 37 | $34,460.72 | $931.37 |
| **Pavilions at Arrowhead** | 47 | $42,323.46 | $900.50 |
| **Springs at Alta Mesa** | 203 | $192,171.15 | $946.66 |
| **Tempe Vista** | 23 | $33,738.18 | $1,466.88 |
| **TOTAL** | **310** | **$302,693.51** | **$976.43** |

---

## Vendor Breakdown

| Vendor | Invoice Count | Total Amount | Avg Invoice |
|--------|--------------|--------------|-------------|
| **Ally Waste** | 45 | $24,817.41 | $551.50 |
| **City of Glendale** | 36 | $36,811.62 | $1,022.54 |
| **City of Mesa** | 192 | $186,806.73 | $973.37 |
| **Waste Management - Compactor** | 12 | $6,018.14 | $501.51 |
| **Waste Management - Hauling** | 25 | $48,239.61 | $1,929.58 |
| **TOTAL** | **310** | **$302,693.51** | **$976.43** |

---

## Source Files Processed

### Mandarina (37 invoices, $34,460.72)
1. `Mandarina - Ally Waste.xlsx` - 12 invoices
2. `Mandarina - Waste Management Compactor.xlsx` - 12 invoices
3. `Mandarina - Waste Management Hauling.xlsx` - 13 invoices

### Pavilions at Arrowhead (47 invoices, $42,323.46)
4. `Pavilions - Ally Waste.xlsx` - 11 invoices
5. `Pavilions - City of Glendale Trash.xlsx` - 36 invoices

### Springs at Alta Mesa (203 invoices, $192,171.15)
6. `Springs at Alta Mesa - Ally Waste.xlsx` - 11 invoices
7. `Springs at Alta Mesa - City of Mesa Trash.xlsx` - 192 invoices

### Tempe Vista (23 invoices, $33,738.18)
8. `Tempe Vista - Ally Waste.xlsx` - 11 invoices
9. `Tempe Vista - Waste Management Hauling.xlsx` - 12 invoices

---

## Data Structure

### Consolidated JSON Schema

Each invoice record contains the following fields:

**Property & Vendor Information:**
- `property_name` - Property name (normalized)
- `vendor_name` - Service provider name

**Invoice Identification:**
- `invoice_number` - Invoice number from vendor
- `control_number` - Internal control number
- `account_number` - Account identifier

**Financial Data:**
- `amount` - Invoice total amount
- `invoice_date` - Invoice issue date (YYYY-MM-DD)
- `service_start` - Service period start date
- `service_end` - Service period end date
- `due_date` - Payment due date
- `paid_date` - Actual payment date

**Service Details:**
- `service_address` - Property service address
- `utility_type` - Service type (e.g., "Trash 6")
- `meter_number` - Meter/service identifier
- `provider` - Provider name

**Accounting:**
- `gl_code` - General ledger code
- `funding_requested` - Funding request date
- `funding_received` - Funding receipt date
- `processed_date` - Invoice processing date

**References:**
- `dna_link` - DNA portal link (where available)
- `source_file` - Original Excel filename
- `extraction_date` - Timestamp of extraction

---

## Data Quality Report

### Completeness Analysis

| Field | Missing Count | Missing % | Status |
|-------|--------------|-----------|--------|
| Invoice Numbers | 0 | 0.0% | ✓ Complete |
| Invoice Dates | 0 | 0.0% | ✓ Complete |
| Invoice Amounts | 0 | 0.0% | ✓ Complete |
| Service Start Dates | 0 | 0.0% | ✓ Complete |
| Service End Dates | 0 | 0.0% | ✓ Complete |

**Overall Data Quality: 100% - Excellent**

All critical fields are present for all 310 invoice records.

---

## Output Files

### 1. JSON Consolidated Data
**File:** `arizona_invoices_consolidated.json` (293 KB)

**Structure:**
```json
{
  "metadata": {
    "extraction_date": "2025-11-03 08:39:13",
    "source_directory": "...",
    "file_count": 9,
    "extractor": "consolidate_arizona_invoices.py",
    "validation_summary": { ... }
  },
  "invoices": [ 310 invoice records ]
}
```

### 2. CSV Summary
**File:** `arizona_invoices_summary.csv` (118 KB)

Flat CSV format with all invoice fields for easy import into Excel, Google Sheets, or database systems.

---

## Sample Invoice Record

```json
{
  "property_name": "Mandarina",
  "vendor_name": "Ally Waste",
  "invoice_number": "72866",
  "invoice_date": "2025-09-01",
  "service_start": "2025-09-01",
  "service_end": "2025-09-30",
  "amount": 575.00,
  "due_date": "2025-10-01",
  "paid_date": "2025-10-09",
  "account_number": "AW-mn48",
  "control_number": "HMA25092500005",
  "service_address": "5402 E WASHINGTON ST",
  "utility_type": "Trash 6",
  "gl_code": "5300-1400",
  "provider": "Ally Waste",
  "funding_requested": "2025-10-01",
  "funding_received": "2025-10-09",
  "processed_date": "2025-09-25",
  "dna_link": "https://dna.conservice.com/...",
  "meter_number": "trash",
  "source_file": "Mandarina - Ally Waste.xlsx",
  "extraction_date": "2025-11-03 08:39:13"
}
```

---

## Key Insights

### Invoice Volume by Property
- **Springs at Alta Mesa** has the highest invoice volume (203 invoices, 65.5% of total)
- This is primarily from City of Mesa municipal services (192 invoices)

### Cost Analysis
- **Tempe Vista** has the highest average invoice amount ($1,466.88)
- Driven by Waste Management Hauling services ($1,929.58 avg)

### Vendor Concentration
- **City of Mesa** represents 61.9% of total invoice volume (192 invoices)
- **City of Mesa** accounts for 61.7% of total spend ($186,806.73)
- Municipal services (Mesa + Glendale) = 73.5% of total invoices

### Service Patterns
- Date range spans approximately 12 months (Oct 2024 - Oct 2025)
- All invoices have complete payment tracking (paid dates recorded)
- 100% data completeness indicates high-quality source data

---

## Next Steps / Recommendations

1. **Data Integration**
   - Import consolidated JSON into main analytics database
   - Update Google Sheets with Arizona property data
   - Cross-reference with existing Texas property data

2. **Analysis Opportunities**
   - Calculate Cost Per Door (CPD) for each property
   - Analyze municipal vs. private vendor pricing
   - Identify seasonal trends in service costs
   - Compare Arizona properties to Texas portfolio benchmarks

3. **Contract Review**
   - Review multiple vendor arrangements at Mandarina (3 vendors)
   - Evaluate consolidation opportunities
   - Analyze municipal service agreements vs. private contracts

4. **Performance Monitoring**
   - Set up monthly tracking for these 4 properties
   - Create Arizona-specific performance dashboards
   - Monitor vendor performance and pricing trends

---

## Technical Notes

### Script Details
- **Script Location:** `C:\Users\Richard\Downloads\Orion Data Part 2\Code\consolidate_arizona_invoices.py`
- **Execution Time:** < 5 seconds
- **Dependencies:** pandas, openpyxl (for Excel reading)
- **Python Version:** 3.12

### Data Normalization Applied
1. Property names standardized (e.g., "Pavilions" → "Pavilions at Arrowhead")
2. Vendor names normalized with service type qualifiers
3. All dates converted to YYYY-MM-DD format
4. Amounts converted to float with 2 decimal precision
5. Missing values handled gracefully (converted to empty strings or None)

### Validation Rules Applied
- All invoice amounts > $0 validated
- All dates within reasonable range (2024-2025)
- No duplicate invoice numbers within same vendor
- Service period consistency (end >= start)

---

## File Locations

**Source Data:**
`C:\Users\Richard\Downloads\Orion Data Part 2\rearizona4packtrashanalysis\`

**Output Files:**
`C:\Users\Richard\Downloads\Orion Data Part 2\Extraction_Output\`
- `arizona_invoices_consolidated.json` (293 KB)
- `arizona_invoices_summary.csv` (118 KB)
- `ARIZONA_CONSOLIDATION_SUMMARY.md` (this file)

**Processing Script:**
`C:\Users\Richard\Downloads\Orion Data Part 2\Code\consolidate_arizona_invoices.py`

---

**Report Generated:** 2025-11-03
**Status:** ✓ Complete - Ready for integration and analysis
