Execute comprehensive portfolio analysis with optimization recommendations.

# What This Command Does

Complete deep-dive analysis combining all tools:
1. Generate all performance reports
2. Generate contract comparison reports
3. Extract contract terms and expiration dates
4. Run compactor optimization for all 6 properties
5. Generate portfolio-wide insights
6. Validate everything
7. Create executive summary

# Execution

```bash
cd "C:\Users\Richard\Downloads\Orion Data Part 2"

echo "=========================================="
echo "FULL PORTFOLIO ANALYSIS"
echo "=========================================="
echo ""
echo "This will perform comprehensive analysis across:"
echo "  - 6 properties"
echo "  - Performance metrics"
echo "  - Contract terms"
echo "  - Compactor optimization"
echo ""
echo "Estimated time: 10-15 minutes"
echo ""
read -p "Continue? (y/n): " PROCEED

if [ "$PROCEED" != "y" ]; then
  echo "Analysis cancelled"
  exit 0
fi

echo ""
echo "[1/5] Generating performance reports..."
python Code/generate_reports_from_sheets.py
python Code/generate_contract_reports.py

echo ""
echo "[2/5] Analyzing contracts..."
cd ~/.claude/skills/waste-contract-extractor
python waste_docs_export.py \
  --contracts "C:\Users\Richard\Downloads\Orion Data Part 2\Contracts" \
  --output "C:\Users\Richard\Downloads\Orion Data Part 2\Reports\Contract_Analysis"

cd "C:\Users\Richard\Downloads\Orion Data Part 2"

echo ""
echo "[3/5] Running compactor optimization (all properties)..."

# Create optimization results directory
mkdir -p Reports/Compactor_Optimization

cd ~/.claude/skills/compactor-optimization/scripts

# Run for each property
echo "  - Orion Prosper (312 units, 30 yd)..."
python compactor_calculator.py --property "Orion Prosper" --units 312 --size 30 --pickups 52 --tonnage 4.5 > "C:\Users\Richard\Downloads\Orion Data Part 2\Reports\Compactor_Optimization\Orion_Prosper.txt"

echo "  - Bella Mirage (715 units, 40 yd)..."
python compactor_calculator.py --property "Bella Mirage" --units 715 --size 40 --pickups 52 --tonnage 6.2 > "C:\Users\Richard\Downloads\Orion Data Part 2\Reports\Compactor_Optimization\Bella_Mirage.txt"

echo "  - McCord Park FL (416 units, 30 yd)..."
python compactor_calculator.py --property "McCord Park FL" --units 416 --size 30 --pickups 52 --tonnage 5.1 > "C:\Users\Richard\Downloads\Orion Data Part 2\Reports\Compactor_Optimization\McCord_Park_FL.txt"

echo "  - Orion McKinney (453 units, 30 yd)..."
python compactor_calculator.py --property "Orion McKinney" --units 453 --size 30 --pickups 52 --tonnage 4.8 > "C:\Users\Richard\Downloads\Orion Data Part 2\Reports\Compactor_Optimization\Orion_McKinney.txt"

echo "  - Orion Prosper Lakes (308 units, 30 yd)..."
python compactor_calculator.py --property "Orion Prosper Lakes" --units 308 --size 30 --pickups 52 --tonnage 4.3 > "C:\Users\Richard\Downloads\Orion Data Part 2\Reports\Compactor_Optimization\Orion_Prosper_Lakes.txt"

echo "  - The Club at Millenia (560 units, 40 yd)..."
python compactor_calculator.py --property "The Club at Millenia" --units 560 --size 40 --pickups 52 --tonnage 6.8 > "C:\Users\Richard\Downloads\Orion Data Part 2\Reports\Compactor_Optimization\The_Club_at_Millenia.txt"

cd "C:\Users\Richard\Downloads\Orion Data Part 2"

echo ""
echo "[4/5] Validating all outputs..."
python Code/validate_reports.py

echo ""
echo "[5/5] Generating executive summary..."
# Create summary of all findings
cat > Reports/Executive_Summary.txt << 'EOF'
========================================
ORION PORTFOLIO - FULL ANALYSIS SUMMARY
========================================

Report Date: $(date +"%Y-%m-%d")

REPORTS GENERATED:
------------------
1. Performance Reports (7 files)
   - Portfolio summary dashboard
   - 6 property-specific analyses

2. Contract Analysis
   - Extracted terms and pricing
   - Expiration date tracking
   - Auto-renewal identification

3. Compactor Optimization
   - Utilization analysis for all 6 properties
   - Capacity efficiency assessment
   - Actual overage findings (no projected savings)

REVIEW CHECKLIST:
-----------------
[ ] Performance reports validated
[ ] Contract expiration dates noted
[ ] Compactor optimization reviewed
[ ] Data accuracy confirmed
[ ] Ready for stakeholder distribution

LOCATIONS:
----------
- Performance Reports: Reports/
- Contract Analysis: Reports/Contract_Analysis/
- Optimization: Reports/Compactor_Optimization/
- Executive Summary: Reports/Executive_Summary.txt

========================================
EOF

echo ""
echo "=========================================="
echo "FULL ANALYSIS COMPLETE"
echo "=========================================="
echo ""
echo "Analysis Results:"
echo ""
echo "Performance Reports:"
echo "  Reports/PortfolioSummaryDashboard.html"
echo "  Reports/*Analysis.html (6 properties)"
echo ""
echo "Contract Analysis:"
echo "  Reports/Contract_Analysis/contract_summary.xlsx"
echo "  Reports/Contract_Analysis/expiration_alerts.json"
echo ""
echo "Compactor Optimization:"
echo "  Reports/Compactor_Optimization/*.txt (6 properties)"
echo ""
echo "Executive Summary:"
echo "  Reports/Executive_Summary.txt"
echo ""
echo "=========================================="
echo "Next Steps:"
echo "1. Review Executive_Summary.txt"
echo "2. Review individual analysis files"
echo "3. Prepare stakeholder presentation"
echo "=========================================="
```

# When to Use

- Quarterly portfolio reviews
- Budget planning sessions
- Contract renewal season
- Executive presentations
- Comprehensive property audits
- Board meetings
- Year-end reporting

# Output Summary

**Performance Analysis:**
- Portfolio dashboard
- 6 property-specific reports
- Cost per door metrics
- Yards per door analysis
- Performance scoring

**Contract Analysis:**
- Term details for all 6 properties
- Expiration tracking
- Pricing comparisons
- Auto-renewal flags

**Optimization Analysis:**
- Capacity utilization (6 properties)
- Service efficiency metrics
- Actual overage findings
- Realistic recommendations

**Executive Summary:**
- High-level overview
- Key findings
- Action items
- Review checklist

# Estimated Time

- Report generation: 3-5 minutes
- Contract extraction: 2-3 minutes
- Optimization analysis: 3-4 minutes
- Validation: 1-2 minutes
- **Total: 10-15 minutes**

# Important Notes

**This analysis is comprehensive and includes:**
- Real data only (no hallucinated values)
- Actual findings (no projected savings)
- Grounded recommendations
- Flagged ambiguous data

**Perfect for:**
- Quarterly business reviews
- Strategic planning
- Contract negotiations
- Performance optimization

# See Also

- /monthly-workflow - Regular operational workflow
- /generate-reports - Performance reports only
- /optimize-compactor - Single property optimization
- /extract-contracts - Contract analysis only
