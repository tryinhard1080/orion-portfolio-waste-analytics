Generate performance analysis for a single property (fast, focused).

# Usage

Provide property name as argument:

```bash
/quick-report "Orion Prosper"
/quick-report "Bella Mirage"
/quick-report "The Club at Millenia"
```

# What This Command Does

1. Reads property data from Google Sheets
2. Generates single property analysis report
3. Skips portfolio summary
4. Faster than /generate-reports (1 property vs 7 reports)

# Execution

```bash
cd "C:\Users\Richard\Downloads\Orion Data Part 2"

PROPERTY="$1"

if [ -z "$PROPERTY" ]; then
  echo "Error: Property name required"
  echo ""
  echo "Usage: /quick-report \"Property Name\""
  echo ""
  echo "Available properties:"
  echo "  - Orion Prosper"
  echo "  - McCord Park FL"
  echo "  - Orion McKinney"
  echo "  - The Club at Millenia"
  echo "  - Bella Mirage"
  echo "  - Orion Prosper Lakes"
  exit 1
fi

echo "=========================================="
echo "QUICK REPORT: $PROPERTY"
echo "=========================================="
echo ""

# Generate single property report using Python
python -c "
import sys
sys.path.insert(0, 'Code')

from generate_reports_from_sheets import generate_single_property_report

property_name = '${PROPERTY}'
print(f'Generating report for {property_name}...')

try:
    generate_single_property_report(property_name)
    print(f'[OK] Report generated successfully')
except Exception as e:
    print(f'[ERROR] {e}')
    sys.exit(1)
"

echo ""
echo "=========================================="
echo "REPORT GENERATED"
echo "=========================================="
echo ""

# Normalize filename (remove spaces, etc.)
FILENAME=$(echo "$PROPERTY" | sed 's/ //g')
echo "Report: Reports/${FILENAME}Analysis.html"
echo ""
echo "Open in browser to review"
```

# Property Names (Exact Match Required)

- **Orion Prosper**
- **McCord Park FL**
- **Orion McKinney**
- **The Club at Millenia**
- **Bella Mirage**
- **Orion Prosper Lakes**

# Example Usage

```bash
# Generate report for Orion Prosper
/quick-report "Orion Prosper"

# Output:
# ==========================================
# QUICK REPORT: Orion Prosper
# ==========================================
#
# Generating report for Orion Prosper...
# [OK] Report generated successfully
#
# ==========================================
# REPORT GENERATED
# ==========================================
#
# Report: Reports/OrionProsperAnalysis.html
```

# When to Use

- On-demand property analysis
- Responding to specific property questions
- Quick data verification
- Before property meetings
- Testing after data updates
- Ad-hoc stakeholder requests

# Performance

- Time: ~30-60 seconds (vs 3-5 minutes for all reports)
- Output: Single HTML file
- Data source: Google Sheets (real-time)

# See Also

- /generate-reports - Generate all properties
- /validate-all - Validate the generated report
- /monthly-workflow - Complete workflow including all properties
