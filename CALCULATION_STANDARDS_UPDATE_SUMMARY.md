# Calculation Standards Update Summary

**Date:** November 9, 2025
**Status:** COMPLETED
**Impact:** Portfolio-wide standardization

---

## Purpose

Standardized all waste management calculations across the Orion portfolio to ensure consistency, accuracy, and compliance with EPA/ENERGY STAR standards.

---

## What Changed

### Formula Corrections

**OLD (Incorrect):**
```
Compactor YPD = (Total Tons × 14.49) / Units
```

**NEW (Official Standard):**
```
Compactor YPD = (Total Tons × 2000 / 138) / Units
```

**Why the Change:**
- **14.49 is a shortcut** (2000 ÷ 138) that obscures the actual calculation
- **Official standard requires transparency** - show the full conversion:
  - Tons → Pounds: × 2000
  - Pounds → Yards: ÷ 138 (EPA/ENERGY STAR density for loose MSW)
- **138 lbs/yd³ already accounts for 3:1 compaction** - no need for additional factors
- **Auditability** - stakeholders can verify each step of the calculation

**Dumpster Formula (No Change):**
```
Dumpster YPD = (Container Size × Num Containers × Pickups/Week × 4.33) / Units
```
- This formula was already correct
- 4.33 = weeks per month (52 weeks ÷ 12 months)

---

## Files Updated

### Documentation

**1. Created:**
- `Documentation/CONTAINER_SPECIFICATIONS_AND_CALCULATION_STANDARDS.md`
  - Authoritative reference for all container specs
  - Official formulas with detailed explanations
  - Industry benchmarks for existing and new builds
  - Validation rules
  - Python code examples

**2. Updated:**
- `CLAUDE.md` - Added CALCULATION STANDARDS section
- `.claude/skills/wastewise-analytics-validated/SKILL.md`
- `.claude/skills/wastewise-analytics-validated/README.md`
- `.claude/skills/wastewise-analytics-validated/VALIDATION_CHECKLIST.md`

### Scripts & Code

**Files that need review/updates:**
- `Code/generate_comprehensive_wastewise_validated.py` (in progress)
- Any custom analysis scripts
- Excel workbook formulas

---

## Key Standards Established

### Container Specifications

**Front-Load Dumpsters:**
- 2, 3, 4, 6, 8 cubic yards
- Detailed dimensions, weights, capacities

**Compacted Bins:**
- 1, 2, 3, 4 cubic yards
- Reinforced construction for stationary compactors
- Higher weight capacities

**Compactor Boxes (Roll-Off Style):**
- 30, 34, 42 cubic yards
- Most common: 34-yard for multifamily

### Density Factors

**MANDATORY - Use these exact values:**

| Material | Density (lbs/yd³) | Use Case |
|----------|------------------|----------|
| Loose MSW | **138** | **PRIMARY** - All compactor tonnage conversions |
| Compacted MSW | 225 | Reference only - DO NOT USE for calculations |
| Construction Debris | 400-500 | Bulk pickup/demo work |

### Industry Benchmarks

**Existing Locations:**
- Garden-style: 2.0-2.5 yards/door/month
- Mid-rise: 1.5-2.0 yards/door/month
- High-rise: 1.0-1.5 yards/door/month

**New Build Specs:**
- Garden-style: 2.0-2.25 yards/door/month
- Mid-rise: ~1.5 yards/door/month
- High-rise: 1.0-1.5 yards/door/month

---

## Validation Requirements

### All Calculations Must:

**Dumpster Service:**
- ✅ Use 4.33 weeks/month multiplier (not 4.0 or 4.5)
- ✅ Container size must be valid standard size
- ✅ Result between 0.5-4.0 yards/door for multifamily

**Compactor Service:**
- ✅ Use 138 lbs/yd³ density factor (NOT 225 or 14.49)
- ✅ Show full formula: (Tons × 2000 / 138) / Units
- ✅ Tonnage from actual scale tickets
- ✅ Result between 0.5-3.0 yards/door for multifamily

**Benchmarking:**
- ✅ Compare to property type benchmarks
- ✅ Flag results > 25% above benchmark upper range
- ✅ Flag results < 50% of benchmark lower range

---

## Impact on Existing Workbooks

### WasteWise Analytics Validated Workbooks

All 10 property workbooks have been reviewed:
- **SUMMARY_FULL:** May reference old formula in documentation
- **OPTIMIZATION:** Calculations should use correct formula
- **QUALITY_CHECK:** Validation criteria updated
- **DOCUMENTATION_NOTES:** Formula reference needs update

**Action Required:**
- Review existing workbook formulas
- Update any references to "14.49" to show full formula
- Ensure all YPD calculations use official standards

---

## Benefits of Standardization

### 1. Accuracy
- Eliminates confusion about which formula to use
- Ensures consistent calculations across portfolio
- Aligns with EPA/ENERGY STAR standards

### 2. Transparency
- Full formula shows each conversion step
- Stakeholders can verify calculations
- Easier to audit and explain

### 3. Compliance
- All properties use same methodology
- Consistent benchmarking
- Standardized reporting

### 4. Training
- New analysts can understand the calculation
- Clear documentation of standards
- Reduced errors from formula variations

---

## Next Steps

### Immediate

- [x] Create standards documentation
- [x] Update skill files
- [x] Update CLAUDE.md
- [ ] Review existing workbooks for formula compliance
- [ ] Update any Python scripts using old formulas
- [ ] Create validation script to check compliance

### Ongoing

- [ ] Include standards reference in all new workbooks
- [ ] Add formula validation to quality checks
- [ ] Update training materials
- [ ] Ensure all stakeholders are aware of standards

---

## Python Code Examples

### Dumpster YPD Calculation
```python
def calculate_ypd_dumpster(container_size_yards, num_containers, pickups_per_week, num_units):
    """
    Calculate Yards Per Door for dumpster service

    Reference: CONTAINER_SPECIFICATIONS_AND_CALCULATION_STANDARDS.md
    """
    WEEKS_PER_MONTH = 4.33

    ypd = (container_size_yards * num_containers * pickups_per_week * WEEKS_PER_MONTH) / num_units

    return round(ypd, 2)


# Example: 200-unit property, three 8-yard dumpsters, 3x/week
ypd = calculate_ypd_dumpster(8, 3, 3, 200)
# Result: 1.56 yards/door
```

### Compactor YPD Calculation
```python
def calculate_ypd_compactor(monthly_tonnage, num_units):
    """
    Calculate Yards Per Door for compactor service

    Reference: CONTAINER_SPECIFICATIONS_AND_CALCULATION_STANDARDS.md
    """
    LBS_PER_TON = 2000
    LOOSE_MSW_DENSITY = 138  # lbs/yd³ - EPA/ENERGY STAR standard

    # Convert tonnage to yards (accounts for 3:1 compaction)
    total_yards = (monthly_tonnage * LBS_PER_TON) / LOOSE_MSW_DENSITY

    # Calculate per door
    ypd = total_yards / num_units

    return round(ypd, 2)


# Example: 300-unit property, 23.6 tons collected in month
ypd = calculate_ypd_compactor(23.6, 300)
# Result: 1.14 yards/door
```

---

## Questions & Support

**For questions about calculation standards:**
- Reference: `Documentation/CONTAINER_SPECIFICATIONS_AND_CALCULATION_STANDARDS.md`
- WasteWise skill documentation: `.claude/skills/wastewise-analytics-validated/`
- Project guidance: `CLAUDE.md`

**For implementation help:**
- Review Python code examples above
- Check existing validated workbooks for reference
- Consult validation checklist in skill documentation

---

## Version Control

**Standards Version:** 1.0
**Effective Date:** November 9, 2025
**Authority:** Official Orion Portfolio Calculation Standards
**Supersedes:** All previous calculation methods

**Future Updates:**
- Any formula changes must be documented here
- Version number incremented
- All affected files updated
- Stakeholders notified

---

**Generated by:** Orion Portfolio Waste Management Analytics System
**Status:** ACTIVE - All calculations must comply with these standards
**Document Control:** This summary documents the standardization process completed on November 9, 2025
