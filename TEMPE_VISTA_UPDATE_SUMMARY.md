# Tempe Vista Service Configuration Update

**Date:** November 10, 2025
**Source:** Waste Management Agreement S0009750102
**Effective Date:** 1/12/2018
**Salesperson:** Brittney Sappington

---

## Update Applied

### Previous Configuration (INCORRECT)
- 6x 4 YD Dumpster @ 3x/week
- 1x 6 YD Dumpster @ 3x/week
- 1x 8 YD Dumpster @ 3x/week

**Total: 8 containers**

### Corrected Configuration (from WM Agreement)
- ✅ **1x 4 YD FEL (Recycling) @ 1x/week**
- ✅ **3x 3 YD FEL @ 3x/week**
- ✅ **5x 4 YD FEL @ 3x/week**

**Total: 9 containers** (+1 container)

---

## Agreement Details

**WM Agreement:** S0009750102
**Customer ID:** Tempe Vista
**Account Name:** Tempe Vista
**Address:** 2045 E Broadway Rd, Tempe, AZ 85282-1734
**County/Parish:** Maricopa

**Service Description & Recurring Rates:**

| Quantity | Equipment | Material Stream | Frequency | Monthly Rate |
|----------|-----------|----------------|-----------|--------------|
| 1 | 4 Yard FEL Recycling | Single Stream Recycling | 1x Per Week | $37.08 + $3.40 |
| 3 | 3 Yard FEL | MSW Commercial | 3x Per Week | $0.00 |
| 5 | 4 Yard FEL | MSW Commercial | 3x Per Week | $657.14 + $50.33 |

**Monthly Grand Total:** $757.95

**Contract Term:** 1 year from Effective Date, automatically renews for additional 12-month terms unless terminated

---

## Impact on Portfolio

### Container Count Change
- **Previous Portfolio Total:** 69 containers
- **Current Portfolio Total:** **70 containers**
- **Change:** +1 container (Tempe Vista correction)

### Service Line Items
- **Previous:** 19 line items
- **Current:** 19 line items (same, just different configuration for Tempe Vista)

---

## Files Updated

**Master Data File:** `Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx`

**Sheets Modified:**
1. **Service Details** - Tempe Vista entries updated (3 line items)
2. **Property Overview** - Tempe Vista container count changed from 8 to 9

---

## Key Takeaway

Following the principle established with Bella Mirage: **"Invoices/Agreements Trump Contracts"**

While we didn't have recent invoices for Tempe Vista, we **did have the actual WM Service Agreement** which provides the contractual service configuration. This is more reliable than estimated or assumed data.

**Previous data source:** Unknown/estimated
**Current data source:** WM Agreement S0009750102 (Official contract document)

---

## Script Created

**`Code/update_tempe_vista_service.py`**
- Reads WM Agreement service configuration
- Updates Service Details sheet
- Updates Property Overview sheet
- Verifies changes applied correctly

---

## Verification

**Final Tempe Vista Configuration Confirmed:**
```
Tempe Vista: 9 containers
  1x 4 YD Dumpster (FEL) @ 1x/week
  3x 3 YD Dumpster (FEL) @ 3x/week
  5x 4 YD Dumpster (FEL) @ 3x/week
```

✅ **Update Complete**
✅ **Master File Updated**
✅ **Portfolio Total: 70 containers**

---

**Updated By:** Portfolio Data Validation System
**Date:** November 10, 2025
**Status:** ✅ Complete
