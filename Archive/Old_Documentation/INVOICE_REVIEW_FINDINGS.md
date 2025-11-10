# Invoice Review Findings - Service Details Extraction Gap Analysis

**Generated:** November 9, 2025  
**Purpose:** Determine if service details exist in source documents but were missed during extraction

---

## EXECUTIVE SUMMARY

**Key Finding:** Service details ARE present in source documents but were NOT extracted to the master file.

**Properties with Extractable Service Data:**
- ✅ **Orion McKinney** - Contract has container sizes (8 YD, 10 YD) and frequency (3x/week)
- ✅ **The Club at Millenia** - Invoices have container sizes (4 YD, 6 YD, 8 YD), frequency (Weekly), and type (Dumpster)
- ⚠️ **Orion Prosper** - Invoices lack service details (need contract review)
- ⚠️ **Orion Prosper Lakes** - Contract is image-based PDF (needs OCR or manual entry)
- ⚠️ **McCord Park FL** - Invoices lack service details (need contract review)
- ✅ **Bella Mirage** - Excel file has all data already extracted

---

## DETAILED FINDINGS BY PROPERTY

### ✅ **Orion McKinney** - DATA AVAILABLE IN CONTRACT

**Source:** `McKinney Frontier Trash Agreement.pdf`

**Service Details Found:**
- ✓ **Container Sizes:** 8 YD and 10 YD
- ✓ **Container Count:** 8 containers (8 YD) + 2 containers (10 YD) = 10 total
- ✓ **Service Frequency:** 3x per week
- ✓ **Container Type:** FL (Front Loader) - explicitly stated
- ✓ **Monthly Cost:** $5,767.72

**Contract Extract:**
```
Qty Service Type Frequency Service Rate
8   08 Yard FL Trash Service   3x per week   2,157.84 per month
8   08 Yard Trash Disposal     3XW           1,789.44 per month
2   10 Yard FL Trash Service   3x per week     770.06 per month
2   10 Yard Trash Disposal     3XW             529.38 per month
```

**Action Required:**
- ✅ Data exists in contract
- ❌ NOT fully extracted to master file (only partial data)
- 🔧 **NEEDS RE-EXTRACTION** from contract

**Expected Master File Updates:**
- Container Count: 10 (8x 8YD + 2x 10YD)
- Container Size: 8 YD (primary), 10 YD (secondary)
- Frequency: 3x/week
- Container Type: Front End Loader (FEL)

---

### ✅ **The Club at Millenia** - DATA AVAILABLE IN INVOICES

**Source:** Invoice PDFs (e.g., `invoice (1).pdf`)

**Service Details Found:**
- ✓ **Container Sizes:** 4 YD, 6 YD, 8 YD (multiple sizes)
- ✓ **Service Frequency:** Weekly (4x per week based on "Weekly x4")
- ✓ **Container Type:** Dumpster
- ✓ **Service Descriptions:** Detailed line items with size, type, frequency

**Invoice Extract:**
```
7/1/2025 - 7/31/2025 Trash Pickup 8 Yards Dumpster Weekly x4 Permanent $1,933.14
7/1/2025 - 7/31/2025 Trash Pickup 8 Yards Dumpster Weekly x4 Permanent $1,626.75
7/1/2025 - 7/31/2025 Trash Pickup 6 Yards Dumpster Weekly x4 Permanent $1,027.24
7/1/2025 - 7/31/2025 Trash Pickup 8 Yards Dumpster Weekly x4 Permanent $1,004.28
7/1/2025 - 7/31/2025 Trash Pickup 8 Yards Dumpster Weekly x4 Permanent $668.40
7/1/2025 - 7/31/2025 Trash Pickup 4 Yards Dumpster Weekly x4 Permanent $409.56
```

**Action Required:**
- ✅ Data exists in invoices
- ❌ NOT extracted to master file
- 🔧 **NEEDS RE-EXTRACTION** from invoices

**Expected Master File Updates:**
- Container Count: 6 containers (based on 6 line items)
- Container Size: 4 YD, 6 YD, 8 YD (mixed sizes)
- Frequency: 4x/week (Weekly x4)
- Container Type: Dumpster

---

### ⚠️ **Orion Prosper** - LIMITED DATA IN INVOICES

**Source:** Republic Services invoice PDFs

**Service Details Found:**
- ✗ **Container Sizes:** NOT in invoices
- ✗ **Service Frequency:** NOT in invoices
- ✗ **Container Type:** NOT in invoices
- ⚠️ **Quantity field:** Present in some line items (64.2% populated)

**Invoice Format:**
- Republic Services invoices use generic line item descriptions
- No detailed service specifications in invoice body
- Service details likely in contract (not yet reviewed)

**Action Required:**
- 🔍 **REVIEW CONTRACT** - Service details should be in service agreement
- 📄 **LOCATE CONTRACT** - Check property folder or request from property manager
- 🔧 **EXTRACT FROM CONTRACT** once located

**Expected Data Source:** Service contract/agreement

---

### ⚠️ **Orion Prosper Lakes** - CONTRACT IS IMAGE-BASED

**Source:** `Little Elm 01-01-25 contract.pdf`

**Service Details Found:**
- ⚠️ **Contract exists** but is image-based (scanned PDF)
- ✗ **No extractable text** - PDF is images, not text
- 🔍 **Needs OCR or manual review**

**Action Required:**
- 🔧 **OCR PROCESSING** - Use OCR to extract text from scanned contract
- 📝 **MANUAL ENTRY** - Alternative: manually read and enter service details
- 🔍 **VISUAL REVIEW** - Open PDF and manually extract service specifications

**Expected Data Source:** Contract (after OCR or manual review)

---

### ⚠️ **McCord Park FL** - LIMITED DATA IN INVOICES

**Source:** Community Waste Disposal invoice PDFs

**Service Details Found:**
- ✗ **Container Sizes:** NOT in invoices
- ✗ **Service Frequency:** NOT in invoices
- ⚠️ **Container Type:** Partially populated (28.6% - 12/42 records)
- ✓ **Quantity field:** 100% populated (42/42 records)

**Invoice Format:**
- Community Waste invoices have basic line items
- Limited service specifications in invoice body
- Service details likely in contract

**Action Required:**
- 🔍 **LOCATE CONTRACT** - Service agreement should have full details
- 🔧 **EXTRACT FROM CONTRACT** once located
- ✅ **Container count already captured** (100% populated)

**Expected Data Source:** Service contract/agreement

---

### ✅ **Bella Mirage** - DATA ALREADY EXTRACTED

**Source:** `Bella Mirage - Trash Bills.xlsx`

**Service Details Found:**
- ✓ **Container Count:** 94/102 records (92.2%)
- ✓ **Container Size:** 102/102 records (100%)
- ✓ **Service Frequency:** 85/102 records (83.3%)
- ⚠️ **Container Type:** Column exists but 0% populated

**Excel File Status:**
- Data already extracted to master file
- Only missing: Container Type

**Action Required:**
- 🔍 **REVIEW CONTRACT** - `Bella Mirage Waste Mgmt Contract 4.20 for 3 yrs.pdf`
- 🔧 **EXTRACT CONTAINER TYPE** from contract
- ✅ **All other fields complete**

**Expected Update:** Container Type only

---

## SUMMARY OF ACTIONS REQUIRED

### Priority 1: Re-Extract from Existing Documents

**1. Orion McKinney** (Contract available)
- Source: `McKinney Frontier Trash Agreement.pdf`
- Extract: Container count (10), sizes (8 YD, 10 YD), frequency (3x/week), type (FEL)
- Status: ✅ Document available, ready to extract

**2. The Club at Millenia** (Invoices available)
- Source: Invoice PDFs (17 files)
- Extract: Container sizes (4/6/8 YD), frequency (4x/week), type (Dumpster), count (6)
- Status: ✅ Documents available, ready to extract

**3. Bella Mirage** (Contract available)
- Source: `Bella Mirage Waste Mgmt Contract 4.20 for 3 yrs.pdf`
- Extract: Container type only
- Status: ✅ Document available, ready to extract

### Priority 2: Locate and Extract from Contracts

**4. Orion Prosper** (Contract needed)
- Source: Service contract (not yet located)
- Extract: All service details (size, frequency, type, count)
- Status: ⚠️ Need to locate contract

**5. McCord Park FL** (Contract needed)
- Source: Service contract (not yet located)
- Extract: Container size and frequency (count already captured)
- Status: ⚠️ Need to locate contract

### Priority 3: OCR or Manual Entry

**6. Orion Prosper Lakes** (Image-based contract)
- Source: `Little Elm 01-01-25 contract.pdf` (scanned/image PDF)
- Extract: All service details
- Status: ⚠️ Needs OCR processing or manual review

---

## EXTRACTION METHODOLOGY

### For Text-Based PDFs (Orion McKinney, The Club at Millenia)

**Recommended Approach:**
1. Use `pdfplumber` to extract text
2. Parse with regex patterns:
   - Container sizes: `(\d+)\s*(?:YD|YARD)`
   - Frequencies: `(\d+)x?\s*(?:per|/)\s*week` or `(Weekly|Daily)`
   - Container types: Keywords (COMPACTOR, DUMPSTER, FEL, etc.)
   - Container count: Quantity fields or count from line items
3. Validate extracted data
4. Update master file

**Python Script Example:**
```python
import pdfplumber
import re

with pdfplumber.open('contract.pdf') as pdf:
    text = pdf.pages[0].extract_text()
    
    # Extract sizes
    sizes = re.findall(r'(\d+)\s*(?:YD|YARD)', text, re.IGNORECASE)
    
    # Extract frequencies
    freqs = re.findall(r'(\d+)x?\s*per\s*week', text, re.IGNORECASE)
```

### For Image-Based PDFs (Orion Prosper Lakes)

**Option 1: OCR Processing**
- Use Tesseract OCR or Adobe Acrobat OCR
- Convert to text-based PDF
- Then use standard extraction

**Option 2: Manual Review**
- Open PDF visually
- Manually read and record service details
- Enter directly into master file

### For Excel Files (Bella Mirage)

**Approach:**
- Already extracted
- Only need to add Container Type from contract
- Use pandas to read contract or manual entry

---

## IMPACT ANALYSIS

### Current State (Before Re-Extraction)

| Property | Count | Size | Freq | Type | Score |
|----------|-------|------|------|------|-------|
| Orion McKinney | ✓ | ✓ | ✓ | ✓ | 4/4 |
| Bella Mirage | ✓ | ✓ | ✓ | ✗ | 3/4 |
| The Club at Millenia | ✓ | ✗ | ✗ | ✓ | 2/4 |
| Orion Prosper | ✓ | ✗ | ✗ | ✗ | 1/4 |
| Orion Prosper Lakes | ✓ | ✗ | ✗ | ✗ | 1/4 |
| McCord Park FL | ✓ | ✗ | ✗ | ✓ | 2/4 |

### After Re-Extraction (Expected)

| Property | Count | Size | Freq | Type | Score |
|----------|-------|------|------|------|-------|
| Orion McKinney | ✓ | ✓ | ✓ | ✓ | 4/4 ✅ |
| Bella Mirage | ✓ | ✓ | ✓ | ✓ | 4/4 ✅ |
| The Club at Millenia | ✓ | ✓ | ✓ | ✓ | 4/4 ✅ |
| Orion Prosper | ✓ | ✓ | ✓ | ✓ | 4/4 ✅ (if contract found) |
| Orion Prosper Lakes | ✓ | ✓ | ✓ | ✓ | 4/4 ✅ (after OCR) |
| McCord Park FL | ✓ | ✓ | ✓ | ✓ | 4/4 ✅ (if contract found) |

**Improvement:** From 1/6 complete (17%) to potentially 6/6 complete (100%)

---

## NEXT STEPS

1. **Immediate Actions** (Can do now):
   - ✅ Extract Orion McKinney data from contract
   - ✅ Extract The Club at Millenia data from invoices
   - ✅ Extract Bella Mirage container type from contract

2. **Short-Term Actions** (Need to locate documents):
   - 🔍 Locate Orion Prosper service contract
   - 🔍 Locate McCord Park FL service contract

3. **Medium-Term Actions** (Requires OCR):
   - 🔧 OCR Orion Prosper Lakes contract
   - 📝 Or manually review and enter data

4. **Update Master File:**
   - Add extracted service details to property tabs
   - Recalculate YPD and efficiency metrics
   - Regenerate performance reports

---

## CONCLUSION

**Key Takeaway:** The data exists in source documents but was not fully extracted during the initial extraction process.

**Root Cause:** 
- Initial extraction focused on invoice amounts and dates
- Service details in contracts were not systematically extracted
- Some invoice formats (Republic Services, Community Waste) don't include service specs

**Solution:**
- Re-extract from contracts (primary source for service details)
- Parse invoice line items for properties with detailed invoices (The Club at Millenia)
- Use OCR for image-based contracts (Orion Prosper Lakes)

**Expected Outcome:**
- 6/6 TX/FL properties with complete service data (100%)
- Ability to calculate YPD for all 6 properties
- Comprehensive performance reporting across portfolio

---

**For questions or to run invoice checks again:**
```bash
python Code/check_invoice_service_details.py
```

