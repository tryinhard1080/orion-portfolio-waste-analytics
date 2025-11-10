# Container Specifications & Calculation Standards

**Official Reference for Orion Portfolio Waste Management Analytics**
**Last Updated:** November 9, 2025
**Status:** MANDATORY - All calculations must use these standards

---

## Purpose

This document establishes the authoritative container specifications and calculation formulas for all waste management analysis across the Orion portfolio. All scripts, skills, and workbooks must reference these standards.

---

## Container Specifications Reference

### Residential Totes

| **Container Type** | **Capacity** | **Dimensions (H × W × D)** | **Dry Weight** | **Max Fill Weight** |
|-------------------|--------------|---------------------------|----------------|---------------------|
| Residential Cart | 64 gallons | 43" × 23.5" × 27" | 35-40 lbs | 200-250 lbs |
| Residential Cart | 96 gallons | 46" × 28" × 34" | 45-55 lbs | 300-350 lbs |

**Note:** Tote dimensions may vary slightly by manufacturer (Toter, Cascade Cart Solutions, Otto Environmental, etc.)

---

### Front-Load Dumpsters

| **Container Size** | **Cubic Yards** | **Dimensions (L × W × H)** | **Dry Weight** | **Max Fill Weight** |
|-------------------|----------------|---------------------------|----------------|---------------------|
| 2-Yard | 2 yd³ | 6' × 3'6" × 3' | 350-450 lbs | 800-1,000 lbs |
| 3-Yard | 3 yd³ | 6' × 4' × 4' | 400-500 lbs | 1,200-1,500 lbs |
| 4-Yard | 4 yd³ | 6' × 5'6" × 4'6" | 450-600 lbs | 1,600-2,000 lbs |
| 6-Yard | 6 yd³ | 6' × 5'6" × 6' | 600-800 lbs | 2,400-3,000 lbs |
| 8-Yard | 8 yd³ | 6' × 6' × 7' | 700-1,000 lbs | 3,200-4,000 lbs |

**Common configurations:**
- Standard front-load containers use a universal fork pocket system
- Height measurements are to top of container (not including lids)
- Max fill weights assume MSW at ~225 lbs/yd³ density

---

### Compacted Bins (for Stationary Compactors)

**These are reinforced front-load containers designed to withstand compaction forces from stationary compactor units**

| **Container Size** | **Cubic Yards** | **Dimensions (L × W × H)** | **Dry Weight** | **Max Fill Weight** |
|-------------------|----------------|---------------------------|----------------|---------------------|
| 1-Yard Compacted | 1 yd³ | 4' × 3' × 3' | 450-550 lbs | 1,500-2,000 lbs |
| 2-Yard Compacted | 2 yd³ | 6' × 3'6" × 3' | 500-650 lbs | 2,500-3,500 lbs |
| 3-Yard Compacted | 3 yd³ | 6' × 4' × 4' | 600-750 lbs | 3,500-4,500 lbs |
| 4-Yard Compacted | 4 yd³ | 6' × 5'6" × 4'6" | 700-900 lbs | 4,500-6,000 lbs |

**Key differences from standard dumpsters:**
- Heavier gauge steel (10-12 gauge vs. 12-14 gauge) to handle compaction forces
- Reinforced frame and structural supports
- Higher dry weight (150-300 lbs heavier than equivalent standard dumpster)
- Higher fill capacity due to compacted waste density (3:1 to 4:1 compaction typical)
- Compatible with stationary compactor ram/chute systems
- Often feature reinforced bottom and side panels

**Typical applications:**
- Small apartment buildings (50-150 units) with limited space
- Properties with stationary compactors in trash rooms
- Urban locations requiring smaller footprint with higher capacity
- Buildings transitioning from chute systems to compaction

---

### Roll-Off Containers

| **Container Size** | **Cubic Yards** | **Dimensions (L × W × H)** | **Dry Weight** | **Max Fill Weight** |
|-------------------|----------------|---------------------------|----------------|---------------------|
| 10-Yard | 10 yd³ | 14' × 8' × 3'6" | 2,000-2,500 lbs | 4,000-6,000 lbs |
| 15-Yard | 15 yd³ | 16' × 8' × 4' | 2,200-2,800 lbs | 6,000-8,000 lbs |
| 20-Yard | 20 yd³ | 22' × 8' × 4' | 2,500-3,200 lbs | 8,000-10,000 lbs |
| 30-Yard | 30 yd³ | 22' × 8' × 6' | 3,000-3,800 lbs | 12,000-15,000 lbs |
| 40-Yard | 40 yd³ | 22' × 8' × 8' | 3,500-4,500 lbs | 16,000-20,000 lbs |

**Note:** Roll-off containers are typically used for temporary projects, construction debris, or in multifamily as compactor boxes

---

### Compactor Boxes (Roll-Off Style)

| **Container Size** | **Cubic Yards** | **Dimensions (L × W × H)** | **Dry Weight** | **Notes** |
|-------------------|----------------|---------------------------|--------------|-----------|
| 30-Yard Compactor | 30 yd³ | 22' × 8' × 6' | 3,500-4,000 lbs | Reinforced for compaction loads |
| 34-Yard Compactor | 34 yd³ | 22' × 8' × 6'10" | 3,800-4,500 lbs | Most common multifamily size |
| 42-Yard Compactor | 42 yd³ | 22' × 8' × 8'6" | 4,200-5,000 lbs | High-volume properties only |

**Compactor box specifications:**
- Heavier construction than standard roll-offs due to compaction forces
- Most multifamily properties use 30 or 34-yard compactor boxes
- Weight capacity includes compacted MSW (typically 3:1 to 4:1 ratio)

---

## OFFICIAL CALCULATION FORMULAS

### Formula 1: Yards Per Door (Dumpster Service)

**MANDATORY FORMULA:**
```
Yards per Door = (Container Size × Number of Containers × Pickups per Week × 4.33) / Number of Units
```

**Components:**
- **Container Size:** Cubic yards of a single container
- **Number of Containers:** Total count of containers at the property
- **Pickups per Week:** Service frequency (how many times per week containers are emptied)
- **4.33:** Weeks per month multiplier (52 weeks ÷ 12 months)
- **Number of Units:** Total residential units at the property

**Example 1: Garden-style apartment**
- 200-unit property
- Three 8-yard dumpsters
- Serviced 3 times per week

```
(8 yd³ × 3 containers × 3 pickups/week × 4.33) / 200 units = 1.56 yards per door
```

**Example 2: Mid-rise property**
- 150-unit property
- Two 6-yard dumpsters
- Serviced 4 times per week

```
(6 yd³ × 2 containers × 4 pickups/week × 4.33) / 150 units = 1.38 yards per door
```

---

### Formula 2: Yards Per Door (Compactor Service)

**MANDATORY FORMULA (Two Steps):**

**Step 1: Convert Tons to Yards (per haul)**
```
Yards = (Tons × 2000) / 138
```

**Components:**
- **Tons:** Weight of compacted waste from scale ticket
- **2000:** Pounds per ton conversion factor
- **138:** Standard density factor (lbs/yd³) for loose MSW

**Example: Single compactor haul**
- Compactor picked up 5.4 tons of material

```
(5.4 tons × 2000) / 138 = 78.3 yards of service
```

---

**Step 2: Calculate Monthly Yards Per Door**
```
Yards per Door = (Total Monthly Tonnage × 2000 / 138) / Number of Units
```

**Process:**
1. Add all tonnage from each haul for the month
2. Convert total monthly tonnage to yards using formula
3. Divide by number of units at property

**Example: Monthly calculation**
- 300-unit property
- Four compactor hauls during the month:
  - Haul 1: 5.4 tons
  - Haul 2: 6.1 tons
  - Haul 3: 5.8 tons
  - Haul 4: 6.3 tons
- **Total monthly tonnage:** 23.6 tons

```
Step 1: Convert to yards
(23.6 tons × 2000) / 138 = 342.0 yards

Step 2: Calculate per door
342.0 yards / 300 units = 1.14 yards per door
```

**CRITICAL:** The 138 lbs/yd³ density factor represents loose MSW and already accounts for typical 3:1 compaction ratios. The formula converts compacted tonnage directly to loose cubic yards, which is the standard measurement for consumption rates.

---

## INDUSTRY BENCHMARKS

**These benchmarks apply universally to property performance analysis, regardless of service type (dumpster or compactor).**

### Existing Locations

| Property Type | Yards/Door/Month Range |
|--------------|------------------------|
| Garden-style apartments | 2.0 to 2.5 |
| Mid-rise/Mixed-use | 1.5 to 2.0 |
| High-rise | 1.0 to 1.5 |

**Usage:** Range-based benchmarks for evaluating existing property performance. Properties significantly above the upper range may have optimization opportunities through frequency adjustments or container right-sizing. These ranges apply to both dumpster and compactor properties since both are measured in yards per door per month.

### New Build Specs

| Property Type | Yards/Door/Month Target |
|--------------|-------------------------|
| Garden-style apartments | 2.0–2.25 |
| Mid-rise/Mixed-use | ~1.5 |
| High-rise | 1.0–1.5 |

**Usage:** Precision targets for new development planning. Use these specifications when designing waste service levels and equipment capacity for properties in pre-construction or development phases, regardless of whether dumpster or compactor service is planned.

---

## Volume Conversion Quick Reference

**Gallons to Cubic Yards:**
- 1 cubic yard = 201.97 gallons
- 64-gallon tote ≈ 0.32 cubic yards
- 96-gallon tote ≈ 0.48 cubic yards

**Common multifamily equivalents:**
- One 2-yard dumpster ≈ thirty-one 64-gallon totes
- One 8-yard dumpster ≈ 125 64-gallon totes

---

## Key Considerations

### Weight Limits

- Always confirm local regulations and hauler weight restrictions
- Exceeding max fill weight may result in overage charges or safety violations
- Compacted waste in compactor boxes can approach 10-12 tons per haul

### Dimensional Clearances

- Front-load: Minimum 14' overhead clearance for truck arms
- Roll-off: Minimum 20' overhead clearance for cable hoist system
- Side clearances: 3-4 feet on service side, 2 feet on non-service sides

### Material Variations

- Steel thickness: 12-14 gauge for front-load, 10-12 gauge for roll-offs
- Lid options add 50-100 lbs to dry weight
- Specialized containers (e.g., food waste, recycling) may have modified specs

---

## Density Factors (Official)

**CRITICAL - Use these exact values in all calculations:**

| Material Type | Density (lbs/yd³) | Use Case |
|--------------|------------------|----------|
| Loose MSW | 138 | **PRIMARY** - Use for all compactor tonnage conversions |
| Compacted MSW | 225 | Reference only - already factored into 138 conversion |
| Construction Debris | 400-500 | Bulk pickup/demo work |
| Cardboard (loose) | 100 | Recycling calculations |
| Mixed Recyclables | 150 | Recycling calculations |

**The 138 lbs/yd³ factor is EPA/ENERGY STAR standard and accounts for 3:1 compaction. Do NOT use 225 or other density factors for compactor YPD calculations.**

---

## Python Code Reference

**For dumpster service:**
```python
def calculate_ypd_dumpster(container_size_yards, num_containers, pickups_per_week, num_units):
    """
    Calculate Yards Per Door for dumpster service

    Args:
        container_size_yards: Size of container in cubic yards
        num_containers: Number of containers at property
        pickups_per_week: Service frequency per week
        num_units: Total residential units

    Returns:
        float: Yards per door per month
    """
    WEEKS_PER_MONTH = 4.33

    ypd = (container_size_yards * num_containers * pickups_per_week * WEEKS_PER_MONTH) / num_units

    return round(ypd, 2)
```

**For compactor service:**
```python
def calculate_ypd_compactor(monthly_tonnage, num_units):
    """
    Calculate Yards Per Door for compactor service

    Args:
        monthly_tonnage: Total tons collected in month
        num_units: Total residential units

    Returns:
        float: Yards per door per month
    """
    LBS_PER_TON = 2000
    LOOSE_MSW_DENSITY = 138  # lbs/yd³ - EPA/ENERGY STAR standard

    # Convert tonnage to yards (accounts for 3:1 compaction)
    total_yards = (monthly_tonnage * LBS_PER_TON) / LOOSE_MSW_DENSITY

    # Calculate per door
    ypd = total_yards / num_units

    return round(ypd, 2)
```

---

## Validation Rules

All calculations must be validated against these rules:

**Dumpster Service:**
1. ✅ Container size must be a valid standard size (2, 3, 4, 6, or 8 yards)
2. ✅ Number of containers must be ≥ 1
3. ✅ Pickups per week must be ≥ 1 and ≤ 7
4. ✅ 4.33 weeks/month multiplier must be used (not 4.0 or 4.5)
5. ✅ Result should be between 0.5 and 4.0 yards/door for multifamily

**Compactor Service:**
1. ✅ Tonnage must be from actual scale tickets
2. ✅ 138 lbs/yd³ density factor must be used (NOT 225 or other values)
3. ✅ 2000 lbs/ton conversion must be used
4. ✅ Result should be between 0.5 and 3.0 yards/door for multifamily
5. ✅ Monthly totals must sum all hauls in the billing period

**Benchmarking:**
1. ✅ Compare calculated YPD to property type benchmarks
2. ✅ Flag results > 25% above benchmark upper range
3. ✅ Flag results < 50% of benchmark lower range (potential data issue)

---

## Document Control

**Authority:** This document supersedes all previous calculation methods and formulas
**Updates:** Any changes to formulas or specifications must be approved and documented
**Reference:** All WasteWise skills, Python scripts, and Excel workbooks must cite this document

**Version History:**
- v1.0 (2025-11-09): Initial standardization document

---

**For questions or clarifications on these standards, refer to:**
- WasteWise Analytics - Validated Edition skill documentation
- CLAUDE.md project instructions
- This document (authoritative source)
