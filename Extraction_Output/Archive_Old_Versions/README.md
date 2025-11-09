# Archive - Old Extraction File Versions

**Archive Date:** November 6, 2025
**Reason:** Consolidation and data quality cleanup

---

## Why These Files Were Archived

These files represent earlier versions of the portfolio extraction with various issues:

1. **Incomplete Data** - Missing invoice amounts for Orion Prosper and Orion Prosper Lakes
2. **Duplicate Versions** - Multiple iterations of the same extraction
3. **Superseded** - Replaced by corrected and consolidated master file

---

## Archived Files

### ❌ INCOMPLETE DATA (Do Not Use)

**COMPLETE_All_Properties_UPDATED_20251103_101053.xlsx**
- **Issue:** Missing 91% of Orion Prosper data (only 4 rows vs. 95 rows)
- **Issue:** Missing 84% of Orion Prosper Lakes data (only 17 rows vs. 104 rows)
- **Status:** INCOMPLETE - Do not use

**BACKUP_COMPLETE_All_Properties_UPDATED_20251103_101053.xlsx**
- **Issue:** Backup of incomplete file above
- **Status:** INCOMPLETE - Do not use

### 📦 EARLIER VERSIONS (Superseded)

**Orion_Invoice_Extraction_20251103_074451.xlsx**
- Early extraction (Oct 26, 7:44 AM)
- Superseded by later consolidations

**Complete_Extraction_20251103_083215.xlsx**
- Mid-process extraction (Oct 26, 8:32 AM)
- Partial data, superseded by later versions

**MASTER_All_Properties_20251103_084251.xlsx**
- Early "master" version (Oct 26, 8:42 AM)
- Only 4 properties (missing 6 properties)
- Superseded by complete 11-property version

**COMPLETE_All_Properties_20251103_094938.xlsx**
- Pre-update version (Oct 26, 9:49 AM)
- Superseded by corrected version

**COMPLETE_All_Properties_UPDATED_20251103_100529.xlsx**
- First update attempt (Oct 26, 10:05 AM)
- Had data quality issues, superseded

---

## Current Active Files (Not Archived)

✅ **MASTER_Orion_Portfolio_Complete_Extraction.xlsx**
- **Official master extraction table**
- 11 properties, 894 invoice line items
- Created from COMPLETE_All_Properties_FIXED_20251104_044641.xlsx
- **USE THIS FILE FOR ANALYSIS**

✅ **COMPLETE_All_Properties_FIXED_20251104_044641.xlsx**
- Source file for master (kept as backup)
- Complete and verified data
- 11 properties, all data present

✅ **Individual Property Files:**
- BellaMirage_WasteAnalysis_Validated.xlsx
- McCordParkFL_WasteAnalysis_Validated.xlsx
- OrionMcKinney_WasteAnalysis_Validated.xlsx
- OrionProsper_WasteAnalysis_Validated.xlsx
- OrionProsperLakes_WasteAnalysis_Validated.xlsx
- TheClubAtMillenia_WasteAnalysis_Validated.xlsx
- Mandarina_WasteAnalysis_Validated.xlsx
- PavilionsAtArrowhead_WasteAnalysis_Validated.xlsx
- SpringsAtAltaMesa_WasteAnalysis_Validated.xlsx
- TempeVista_WasteAnalysis_Validated.xlsx

---

## Recovery Information

If you need to restore any archived file:
1. Copy from `Archive_Old_Versions/` folder
2. Note: These files have known data quality issues
3. Recommend using current master file instead

---

**Do Not Delete:** Keep for historical reference and audit trail
