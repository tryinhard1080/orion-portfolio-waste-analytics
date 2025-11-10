# Service Data Gap Analysis

**Generated:** November 9, 2025  
**Purpose:** Identify properties missing key service details (container count, size, frequency, type)

---

## EXECUTIVE SUMMARY

**Service Data Completeness:**
- ✅ **1/10 properties** have complete service data (4/4 fields)
- ⚠️ **5/10 properties** have partial service data (1-3/4 fields)
- ❌ **4/10 properties** are missing all service data (0/4 fields)

**Critical Gaps:**
- **4 properties** missing container count
- **8 properties** missing container size
- **8 properties** missing service frequency
- **7 properties** missing container type

---

## DETAILED PROPERTY BREAKDOWN

### ✅ COMPLETE SERVICE DATA (1 property)

**Orion McKinney** - 4/4 fields ✓
- ✓ Container Count: 56/95 records (58.9%)
- ✓ Container Size: 36/95 records (37.9%)
- ✓ Service Frequency: 18/95 records (18.9%)
- ✓ Container Type: 22/95 records (23.2%)

---

### ⚠️ PARTIAL SERVICE DATA (5 properties)

**Bella Mirage** - 3/4 fields
- ✓ Container Count: 94/102 records (92.2%)
- ✓ Container Size: 102/102 records (100.0%)
- ✓ Service Frequency: 85/102 records (83.3%)
- ❌ Container Type: MISSING

**McCord Park FL** - 2/4 fields
- ✓ Container Count: 42/42 records (100.0%)
- ❌ Container Size: Column exists but 0% populated
- ❌ Service Frequency: Column exists but 0% populated
- ✓ Container Type: 12/42 records (28.6%)

**The Club at Millenia** - 2/4 fields
- ✓ Container Count: 146/146 records (100.0%)
- ❌ Container Size: MISSING
- ❌ Service Frequency: MISSING
- ✓ Container Type: 146/146 records (100.0%)

**Orion Prosper** - 1/4 fields
- ✓ Container Count: 61/95 records (64.2%)
- ❌ Container Size: MISSING
- ❌ Service Frequency: MISSING
- ❌ Container Type: MISSING

**Orion Prosper Lakes** - 1/4 fields
- ✓ Container Count: 82/104 records (78.8%)
- ❌ Container Size: MISSING
- ❌ Service Frequency: MISSING
- ❌ Container Type: MISSING

---

### ❌ MISSING ALL SERVICE DATA (4 properties)

**Mandarina** - 0/4 fields
- ❌ Container Count: MISSING
- ❌ Container Size: MISSING
- ❌ Service Frequency: MISSING
- ❌ Container Type: Column exists but 0% populated

**Pavilions at Arrowhead** - 0/4 fields
- ❌ Container Count: MISSING
- ❌ Container Size: MISSING
- ❌ Service Frequency: MISSING
- ❌ Container Type: Column exists but 0% populated

**Springs at Alta Mesa** - 0/4 fields
- ❌ Container Count: MISSING
- ❌ Container Size: MISSING
- ❌ Service Frequency: MISSING
- ❌ Container Type: Column exists but 0% populated

**Tempe Vista** - 0/4 fields
- ❌ Container Count: MISSING
- ❌ Container Size: MISSING
- ❌ Service Frequency: MISSING
- ❌ Container Type: Column exists but 0% populated

---

## GAP SUMMARY BY FIELD

### Container Count
**Missing in 4/10 properties:**
1. Mandarina
2. Pavilions at Arrowhead
3. Springs at Alta Mesa
4. Tempe Vista

### Container Size
**Missing in 8/10 properties:**
1. Orion Prosper
2. McCord Park FL (column exists but empty)
3. The Club at Millenia
4. Orion Prosper Lakes
5. Mandarina
6. Pavilions at Arrowhead
7. Springs at Alta Mesa
8. Tempe Vista

### Service Frequency
**Missing in 8/10 properties:**
1. Orion Prosper
2. McCord Park FL (column exists but empty)
3. The Club at Millenia
4. Orion Prosper Lakes
5. Mandarina
6. Pavilions at Arrowhead
7. Springs at Alta Mesa
8. Tempe Vista

### Container Type
**Missing in 7/10 properties:**
1. Orion Prosper
2. Bella Mirage (column exists but empty)
3. Orion Prosper Lakes
4. Mandarina (column exists but empty)
5. Pavilions at Arrowhead (column exists but empty)
6. Springs at Alta Mesa (column exists but empty)
7. Tempe Vista (column exists but empty)

---

## RECOMMENDATIONS

### Priority 1: Arizona Properties (4 properties - MISSING ALL DATA)

These properties need complete service data extraction:

1. **Mandarina** (37 records)
   - Action: Review contracts and invoices for container details
   - Source: Excel files in property folder

2. **Pavilions at Arrowhead** (47 records)
   - Action: Review contracts and invoices for container details
   - Source: Excel files in property folder

3. **Springs at Alta Mesa** (203 records)
   - Action: Review contracts and invoices for container details
   - Source: Excel files + PDF in property folder

4. **Tempe Vista** (23 records)
   - Action: Review contracts and invoices for container details
   - Source: Excel files in property folder

### Priority 2: Texas Properties (2 properties - PARTIAL DATA)

These properties need container size, frequency, and type:

5. **Orion Prosper** (95 records)
   - Has: Container count (64.2%)
   - Needs: Container size, frequency, type
   - Source: 16 PDF invoices

6. **Orion Prosper Lakes** (104 records)
   - Has: Container count (78.8%)
   - Needs: Container size, frequency, type
   - Source: 10 PDF invoices

### Priority 3: Fill Remaining Gaps (3 properties)

7. **McCord Park FL** (42 records)
   - Has: Container count (100%), Container type (28.6%)
   - Needs: Container size, frequency (columns exist but empty)
   - Source: 9 PDF invoices

8. **The Club at Millenia** (146 records)
   - Has: Container count (100%), Container type (100%)
   - Needs: Container size, frequency
   - Source: 17 PDF invoices

9. **Bella Mirage** (102 records)
   - Has: Container count (92.2%), Size (100%), Frequency (83.3%)
   - Needs: Container type
   - Source: 1 Excel file

---

## DATA SOURCES FOR EXTRACTION

### Where to Find Service Details

**Contracts:**
- Container count (number of containers on-site)
- Container size (yard capacity)
- Service frequency (pickups per week)
- Container type (dumpster, compactor, etc.)

**Invoices:**
- Line item descriptions often include:
  - "30 YD" or "40 YD" = container size
  - "3x/week" or "Weekly" = frequency
  - "FEL" (Front-End Loader) = container type
  - Quantity field = container count

**Property Folders:**
- Check `Properties/{PropertyName}/` for contracts
- Review PDF invoices for service descriptions
- Check Excel files for existing service data

---

## IMPACT ON REPORTING

### Metrics Requiring Service Data

**Yards Per Door (YPD):**
- Requires: Container count + Container size
- Currently calculable for: 2/10 properties (Orion McKinney, Bella Mirage)
- Missing for: 8/10 properties

**Service Efficiency:**
- Requires: Service frequency
- Currently calculable for: 2/10 properties (Orion McKinney, Bella Mirage)
- Missing for: 8/10 properties

**Container Utilization:**
- Requires: Container count + Container size + Service frequency
- Currently calculable for: 2/10 properties (Orion McKinney, Bella Mirage)
- Missing for: 8/10 properties

---

## NEXT STEPS

1. **Review Contracts** - Extract service details from existing contracts
2. **Parse Invoice Descriptions** - Extract container info from line item descriptions
3. **Update Master File** - Add missing service data to property tabs
4. **Validate Calculations** - Recalculate YPD and efficiency metrics
5. **Generate Reports** - Create performance reports with complete data

---

## NOTES

- Some properties have columns created but not populated (e.g., McCord Park FL has "Container Size" column but 0% populated)
- Arizona properties (4) appear to use different invoice formats (Excel-based) which may not have structured service fields
- Texas/Florida properties (6) use PDF invoices which may have service details in description fields
- Only 1/10 properties (Orion McKinney) has all 4 service fields populated

---

**For questions or to run this analysis again:**
```bash
python Code/check_service_details.py
```

