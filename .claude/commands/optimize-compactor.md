Run compactor optimization analysis for a specific property.

# What This Command Does

Uses compactor-optimization skill to:
1. Analyze yards per door ratio
2. Calculate capacity utilization
3. Identify over/under-servicing
4. Recommend optimal pickup frequency
5. Estimate potential cost efficiency improvements (based on real data)

# Execution

```bash
echo "=========================================="
echo "COMPACTOR OPTIMIZATION ANALYSIS"
echo "=========================================="
echo ""
echo "Enter property details:"
read -p "Property name: " PROPERTY
read -p "Units: " UNITS
read -p "Container Size (yards): " SIZE
read -p "Current Pickups/year: " PICKUPS
read -p "Average Tonnage/pull: " TONNAGE

echo ""
echo "Running optimization analysis for $PROPERTY..."
echo ""

cd ~/.claude/skills/compactor-optimization/scripts

python compactor_calculator.py \
  --property "$PROPERTY" \
  --units $UNITS \
  --size $SIZE \
  --pickups $PICKUPS \
  --tonnage $TONNAGE

echo ""
echo "=========================================="
echo "Analysis saved to optimization_report.txt"
echo "=========================================="
```

# Example Usage

```bash
# Orion Prosper
Property: Orion Prosper
Units: 312
Container Size: 30
Current Pickups: 52
Average Tonnage: 4.5

# Bella Mirage
Property: Bella Mirage
Units: 715
Container Size: 40
Current Pickups: 52
Average Tonnage: 6.2
```

# Example Output

```
============================================================
COMPACTOR OPTIMIZATION ANALYSIS - Orion Prosper
============================================================

PROPERTY INFORMATION
------------------------------------------------------------
Units: 312
Container Size: 30 yards
Current Pickups: 52/year (weekly)
Average Tonnage: 4.5 tons/pull

CAPACITY ANALYSIS
------------------------------------------------------------
Maximum Capacity: 8.7 tons
Current Utilization: 51.7%
Status: Under-utilized

YARDS PER DOOR ANALYSIS
------------------------------------------------------------
Available Capacity: 0.15 yards/door/week
Current YPD: 2.2
Target YPD Range: 1.8 - 2.1
Status: Slightly over target

RECOMMENDATIONS (Based on Actual Data)
------------------------------------------------------------
1. Service Frequency: Currently optimal at weekly
2. Capacity Utilization: Monitor for seasonal changes
3. Overages: Review actual invoices for extra pickup charges

ACTUAL FINDINGS FROM INVOICE DATA
------------------------------------------------------------
- Found $350 in overage charges (Q1 2025)
- 3 extra pickups beyond contract (Feb, Mar, Jun)
- Cost efficiency opportunity: Reduce overages through better forecasting

IMPORTANT NOTE
------------------------------------------------------------
Recommendations are based on actual invoice data and usage patterns.
No projected savings are included. Review contract terms before making changes.
```

# Data Integrity

**What This Analysis Provides:**
- Utilization metrics based on actual tonnage
- Comparisons to industry benchmarks
- Identification of overages (from real invoices)
- Service right-sizing recommendations

**What It Does NOT Provide:**
- Projected/estimated savings
- Recommendations to eliminate essential services
- Unrealistic cost reduction targets

# When to Use

- New property analysis
- Service contract negotiation
- Performance optimization review
- Quarterly efficiency assessments
- Investigating overage charges
- Budget planning

# Property-Specific Data

**Current Portfolio Parameters:**

| Property | Units | Container | Pickups/Year | Avg Tonnage |
|----------|-------|-----------|--------------|-------------|
| Orion Prosper | 312 | 30 yd | 52 | 4.5 |
| Bella Mirage | 715 | 40 yd | 52 | 6.2 |
| McCord Park FL | 416 | 30 yd | 52 | 5.1 |
| Orion McKinney | 453 | 30 yd | 52 | 4.8 |
| Orion Prosper Lakes | 308 | 30 yd | 52 | 4.3 |
| The Club at Millenia | 560 | 40 yd | 52 | 6.8 |

# See Also

- ~/.claude/skills/compactor-optimization/references/compactor_optimization_reference.md
- /extract-invoices - Get tonnage and pickup data
