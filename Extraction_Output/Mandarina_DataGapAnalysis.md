# Mandarina - Data Gap Analysis

**Property:** Mandarina
**Location:** Phoenix, Arizona
**Units:** 180
**Analysis Date:** November 3, 2025
**Status:** ⚠️ INCOMPLETE - Critical Data Missing

---

## Executive Summary

The Mandarina waste management analysis is **INCOMPLETE** due to critical data gaps in the Excel consolidation file. While contract information was successfully extracted from both vendor agreements, **all invoice amounts are missing (NaN values)**, preventing accurate financial analysis and optimization assessment.

**Impact:** Limited to contract-based analysis only. Cannot validate actual spending, calculate performance benchmarks, or identify optimization opportunities.

---

## Data Availability Matrix

| Data Category | Status | Confidence | Source | Notes |
|--------------|--------|------------|--------|-------|
| **CONTRACT DATA** |
| Property Name | ✓ Available | HIGH | Both contracts | Mandarina |
| Unit Count | ✓ Available | HIGH | Ally Waste contract | 180 units |
| Vendor Information | ✓ Available | HIGH | Both contracts | WM + Ally Waste |
| Service Configuration | ✓ Available | HIGH | WM contract | 2 x 8-yard compactors, 3x/week |
| Contract Rates | ✓ Available | HIGH | Both contracts | WM: $818.86, Ally: $575.00 |
| Contract Terms | ✓ Available | HIGH | Both contracts | Renewal dates, notice periods |
| **INVOICE DATA** |
| Invoice Dates | ✓ Available | HIGH | Excel consolidation | Oct 2024 - Sep 2025 |
| Invoice Numbers | ⚠️ Partial | MEDIUM | Excel consolidation | 33 of 37 present |
| Invoice Amounts | ❌ MISSING | NONE | Excel consolidation | **All values = NaN** |
| Billing Periods | ❌ MISSING | NONE | Excel consolidation | All values = NaN |
| Service Descriptions | ❌ MISSING | NONE | Excel consolidation | All values = NaN |
| **OPERATIONAL DATA** |
| Tonnage Per Haul | ❌ MISSING | NONE | N/A | Need WM compactor invoices |
| Number of Hauls | ❌ MISSING | NONE | N/A | Need WM compactor invoices |
| Contamination Charges | ❌ MISSING | NONE | N/A | Need invoice line items |
| Overage Charges | ❌ MISSING | NONE | N/A | Need invoice line items |
| **PROPERTY DATA** |
| Property Type | ⚠️ Assumed | LOW | Assumption | Garden-Style (not in contracts) |
| Location Details | ✓ Available | HIGH | Contracts | Phoenix, AZ 85034 |
| Management Company | ✓ Available | HIGH | Ally contract | Avanti Residential |

---

## Critical Data Gaps

### 1. Invoice Amounts (🔴 CRITICAL)

**Status:** ALL MISSING (37 invoices)

**Issue:**
- Excel consolidation file contains 37 invoice records from October 2024 to September 2025
- ALL "Amount" column values = NaN
- Cannot determine actual monthly spending

**Impact:**
- ❌ Cannot calculate actual cost per door
- ❌ Cannot compare actual vs. contract rates
- ❌ Cannot identify billing errors or unauthorized charges
- ❌ Cannot analyze month-over-month cost trends
- ❌ Cannot validate invoice accuracy

**Source File:** `COMPLETE_All_Properties_UPDATED_20251103_101053.xlsx`, Sheet: "Mandarina"

**Affected Invoices:**
- Ally Waste: 12 invoices (all amounts NaN)
- WM Compactor: 12 invoices (all amounts NaN)
- WM Hauling: 13 invoices (all amounts NaN)

**Resolution Required:**
1. Locate original invoice PDF files for all 37 invoices
2. Extract invoice amounts from each PDF
3. Populate Excel consolidation file with correct amounts
4. Validate extracted amounts against contract rates

**Estimated Effort:** 4-6 hours (manual extraction from 37 PDFs)

---

### 2. Tonnage Data (🔴 CRITICAL)

**Status:** NOT AVAILABLE

**Issue:**
- No tonnage data in Excel consolidation file
- WM compactor invoices typically include tons per haul
- Critical for calculating yards/door benchmark metric

**Impact:**
- ❌ Cannot calculate yards per door (primary KPI for compactors)
- ❌ Cannot assess benchmark compliance (2.0-2.5 yards/door for garden-style)
- ❌ Cannot perform compactor optimization analysis
- ❌ Cannot determine if compactor is under-utilized
- ❌ Cannot identify over-servicing or contamination issues

**Required Data:**
- Total tons collected per month
- Number of hauls per month
- Average tons per haul
- Compactor capacity utilization

**Calculation Blocked:**
```
Yards Per Door = (Monthly Tons × 14.49) / 180 units
```

**Reference:** WasteWise_Calculations_Reference.md, Section 1

**Resolution Required:**
1. Extract tonnage from WM compactor invoices (12 invoices)
2. Calculate monthly tonnage totals
3. Determine average tons per haul
4. Enable yards/door calculation

**Estimated Effort:** 2-3 hours (extraction from 12 compactor invoices)

---

### 3. Invoice Line Item Detail (🔴 CRITICAL)

**Status:** NOT AVAILABLE

**Issue:**
- No service descriptions in Excel consolidation
- Cannot separate base charges from overages
- Cannot identify contamination fees
- Cannot analyze fee breakdown

**Impact:**
- ❌ Cannot calculate overage percentage
- ❌ Cannot perform contamination analysis (trigger: > 3% of spend)
- ❌ Cannot identify service inefficiencies
- ❌ Cannot validate billing line items against contract

**Required Fields:**
- Base service charges
- Extra pickup charges
- Contamination fees
- Environmental/regulatory fees
- Fuel surcharges
- Taxes

**Resolution Required:**
1. Extract detailed line items from all 37 invoices
2. Categorize charges (base, overage, contamination, fees)
3. Calculate category percentages
4. Identify optimization triggers

**Estimated Effort:** 6-8 hours (detailed extraction from 37 PDFs)

---

## Secondary Data Gaps

### 4. Property Type Verification (🟡 MODERATE)

**Status:** ASSUMED (Not Confirmed)

**Current Assumption:** Garden-Style multifamily

**Basis for Assumption:**
- Location in Phoenix, Arizona
- 180 units (typical garden-style size)
- 2 compactors for service (suggests lower density)
- Suburban location (85034 zip code)

**Impact if Incorrect:**
- May apply wrong yards/door benchmark
  - Garden-Style: 2.0-2.5 yards/door/month
  - Mid-Rise: 1.5-2.0 yards/door/month
  - Hi-Rise: 1.0-1.5 yards/door/month
- May affect optimization recommendations

**Resolution:**
- Confirm property type from property management records
- Verify building height and density
- Adjust benchmarks if needed

**Priority:** LOW (Garden-Style assumption is reasonable)

---

### 5. Invoice Numbers (🟡 MODERATE)

**Status:** 4 MISSING (out of 37)

**Missing Invoice Numbers:**
- 3 WM Hauling invoices (Jan, Dec, Nov 2024)
- 1 record with date only

**Impact:**
- Cannot uniquely identify 4 invoices
- May complicate data validation
- Minor issue if amounts can be extracted by date

**Resolution:**
- Extract invoice numbers from PDF files
- Match by date if invoice number unavailable
- Document any gaps in invoice sequence

**Priority:** LOW (does not block analysis if amounts are available)

---

## Data Quality Issues

### Excel Consolidation File Structure

**File:** `COMPLETE_All_Properties_UPDATED_20251103_101053.xlsx`
**Sheet:** Mandarina
**Rows:** 37

**Column Analysis:**

| Column | Expected Data Type | Actual Status | Missing Count | Notes |
|--------|-------------------|---------------|---------------|-------|
| Data Source | Text | ✓ Complete | 0 | All show "Arizona Excel" |
| Source File | Text | ✓ Complete | 0 | Excel filenames present |
| Property | Text | ✓ Complete | 0 | All show "Mandarina" |
| Vendor | Text | ✓ Complete | 0 | 3 vendor variations |
| Invoice # | Text/Number | ⚠️ Partial | 4 | Most present |
| Invoice Date | Date | ✓ Complete | 0 | Oct 2024 - Sep 2025 |
| **Amount** | **Currency** | **❌ FAIL** | **37** | **ALL NaN** |
| **Billing Period** | **Text** | **❌ FAIL** | **37** | **ALL NaN** |
| **Description** | **Text** | **❌ FAIL** | **37** | **ALL NaN** |
| **Service Type** | **Text** | **❌ FAIL** | **37** | **ALL NaN** |
| Account # | Text | ✓ Complete | 0 | All present |

**Root Cause Hypothesis:**
1. **Extraction Failure:** Original Excel-to-consolidation process failed to extract amounts
2. **Empty Source Files:** Original Excel files may not contain amount data
3. **Column Mapping Error:** Amount column may be in different position in source files
4. **Data Type Mismatch:** Source amounts may be formatted incorrectly (text vs. number)

**Investigation Needed:**
1. Check original Excel source files (if available):
   - `Mandarina - Ally Waste.xlsx`
   - `Mandarina - Waste Management Compactor.xlsx`
   - `Mandarina - Waste Management Hauling.xlsx`
2. Verify if amounts exist in source files
3. If amounts missing from Excel, revert to original PDF invoices

---

## Analysis Limitations

### What CAN Be Analyzed (Contract-Based Only)

✓ **Cost Per Door Baseline**
- Calculation: $1,393.86 / 180 = $7.74/door
- Based on contract rates (WM $818.86 + Ally $575.00)
- Limitation: NOT actual spending, just contracted rates

✓ **Service Configuration Assessment**
- 2 x 8-yard compactors
- 3x per week pickup frequency
- Dual-vendor setup (WM + Ally)

✓ **Contract Terms Analysis**
- Renewal dates and notice periods
- Rate increase provisions
- Termination clauses
- Auto-renewal tracking

✓ **Vendor Comparison (Contract Rates)**
- WM compactor service: $4.55/door
- Ally bulk service: $3.19/door
- Combined: $7.74/door

### What CANNOT Be Analyzed (Missing Data)

❌ **Actual Financial Performance**
- Cannot calculate actual monthly spending
- Cannot compare actual vs. contract variance
- Cannot identify unauthorized charges
- Cannot validate billing accuracy

❌ **Performance Benchmarking**
- Cannot calculate yards per door
- Cannot assess benchmark compliance
- Cannot identify over-servicing
- Cannot detect contamination issues

❌ **Optimization Opportunities**
- Cannot perform compactor optimization (need tons/haul)
- Cannot calculate contamination percentage (need fees)
- Cannot analyze overage frequency (need line items)
- Cannot recommend service adjustments

❌ **Trend Analysis**
- Cannot show month-over-month cost trends
- Cannot identify seasonal patterns
- Cannot forecast future costs
- Cannot detect cost anomalies

---

## Recommended Data Collection Plan

### Phase 1: Critical Data Extraction (IMMEDIATE)

**Priority:** 🔴 CRITICAL
**Timeline:** 1-2 weeks
**Estimated Effort:** 10-15 hours

#### Step 1: Locate Source Invoice Files
- [ ] Identify storage location for Mandarina invoices (Oct 2024 - Sep 2025)
- [ ] Verify all 37 invoices are available in PDF format
- [ ] Organize by vendor and date

#### Step 2: Extract Invoice Amounts
- [ ] Use PDF extraction tool or manual entry
- [ ] Extract from all 37 invoices:
  - Invoice number
  - Invoice date
  - Total amount
  - Service period
- [ ] Create structured dataset (CSV or Excel)
- [ ] Validate extracted amounts (basic reasonableness checks)

#### Step 3: Extract Tonnage Data (WM Compactor Only)
- [ ] Focus on 12 WM compactor invoices
- [ ] Extract for each invoice:
  - Total tons
  - Number of hauls
  - Tons per haul (if itemized)
  - Service dates
- [ ] Calculate monthly tonnage totals
- [ ] Calculate average tons per haul

#### Step 4: Extract Line Item Detail
- [ ] For all 37 invoices, extract:
  - Base service charges
  - Extra pickup charges
  - Contamination fees (if any)
  - Environmental/RCR fees
  - Fuel surcharges
  - Taxes
- [ ] Categorize each line item
- [ ] Calculate totals by category

### Phase 2: Data Validation (SHORT-TERM)

**Priority:** 🟡 HIGH
**Timeline:** 1 week
**Estimated Effort:** 4-6 hours

#### Step 5: Cross-Reference with Contracts
- [ ] Compare extracted amounts to contract rates
- [ ] Identify any variances
- [ ] Flag discrepancies for investigation
- [ ] Validate pickup frequency matches contract

#### Step 6: Data Quality Checks
- [ ] Verify no duplicate invoices
- [ ] Check for missing months
- [ ] Validate date sequences
- [ ] Confirm vendor assignments
- [ ] Test calculation formulas

#### Step 7: Update Consolidation File
- [ ] Populate COMPLETE_All_Properties file with extracted data
- [ ] Verify all NaN values are replaced
- [ ] Add data quality flags
- [ ] Document extraction methodology

### Phase 3: Analysis Execution (COMPLETION)

**Priority:** 🟢 MEDIUM
**Timeline:** 3-5 days
**Estimated Effort:** 6-8 hours

#### Step 8: Recalculate All Metrics
- [ ] Actual cost per door (using invoice amounts)
- [ ] Yards per door (using tonnage data)
- [ ] Benchmark compliance assessment
- [ ] Overage percentage
- [ ] Contamination percentage

#### Step 9: Perform Optimization Analysis
- [ ] Compactor optimization (tons/haul analysis)
- [ ] Contamination reduction opportunity
- [ ] Service frequency optimization
- [ ] Vendor consolidation evaluation

#### Step 10: Generate Final Reports
- [ ] Update Excel file with actual data
- [ ] Regenerate HTML dashboard with trends
- [ ] Create optimization recommendations
- [ ] Document all findings and opportunities

---

## Expected Outcomes After Data Collection

### New Calculations Enabled

| Metric | Formula | Benchmark | Use Case |
|--------|---------|-----------|----------|
| **Yards Per Door** | (Monthly Tons × 14.49) / 180 | 2.0-2.5 for Garden-Style | Assess service adequacy |
| **Actual Cost Per Door** | Total Invoice Amount / 180 | Varies by region | Track actual spending |
| **Capacity Utilization** | (Actual Tons/Haul) / Target Tons | 8-9 tons optimal | Compactor efficiency |
| **Contamination %** | Contamination Fees / Total Spend | < 3% target | Operational improvement |
| **Overage %** | Extra Pickup Charges / Total Spend | < 10% target | Service right-sizing |

### Optimization Opportunities Identifiable

1. **Compactor Optimization**
   - If avg tons/haul < 6.0 tons: Reduce pickup frequency
   - Potential savings: TBD (requires data)

2. **Contamination Reduction**
   - If contamination > 3%: Implement resident training
   - Potential savings: TBD (requires fee data)

3. **Overage Management**
   - If consistent extra pickups: Adjust service frequency
   - Potential savings: TBD (requires invoice detail)

4. **Vendor Consolidation**
   - Evaluate single-vendor quote
   - Compare management complexity vs. cost
   - Potential benefits: Simplified administration, possible discount

---

## Risk Assessment

### Risks of Continuing with Incomplete Data

| Risk | Severity | Probability | Impact |
|------|----------|-------------|--------|
| **Missed Cost Savings** | HIGH | HIGH | Cannot identify optimization opportunities |
| **Billing Errors Undetected** | MEDIUM | MEDIUM | May overpay without validation |
| **Over-Servicing** | HIGH | MEDIUM | Cannot assess if service exceeds needs |
| **Contamination Issues** | MEDIUM | LOW | Cannot identify if fees are excessive |
| **Budget Variance** | MEDIUM | HIGH | Contract rates may not match actual costs |

### Benefits of Complete Data Collection

| Benefit | Value | Timeline |
|---------|-------|----------|
| **Accurate Cost Tracking** | HIGH | Immediate |
| **Optimization Opportunities** | HIGH | 1-2 months |
| **Billing Validation** | MEDIUM | Immediate |
| **Performance Benchmarking** | HIGH | 1 month |
| **Informed Contract Decisions** | HIGH | Before renewal |

---

## Conclusion

The Mandarina waste management analysis is currently **LIMITED TO CONTRACT-BASED REVIEW ONLY** due to missing invoice data. To enable full WasteWise Analytics capabilities:

**CRITICAL ACTION REQUIRED:**
1. Extract invoice amounts from 37 PDF invoices
2. Extract tonnage data from 12 WM compactor invoices
3. Extract line item detail for categorization
4. Validate all data against contracts
5. Re-run full analysis with complete dataset

**ESTIMATED TIMELINE:** 2-3 weeks
**ESTIMATED EFFORT:** 20-30 hours total

**PRIORITY:** 🔴 HIGH

Once data gaps are filled, Mandarina will have:
- ✓ Complete financial analysis
- ✓ Performance benchmarking (yards/door)
- ✓ Optimization recommendations
- ✓ Cost savings opportunities
- ✓ Billing validation
- ✓ Trend analysis and forecasting

---

**Report Generated:** November 3, 2025
**Next Review:** After data collection completion
**Contact:** WasteWise Analytics Team
**Reference:** WasteWise_Calculations_Reference.md v2.0
