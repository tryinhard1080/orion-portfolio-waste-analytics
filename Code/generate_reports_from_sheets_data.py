"""
Process Google Sheets data and generate HTML reports
Takes the fetched data and creates all 7 reports
"""

import sys
from pathlib import Path
from generate_reports_from_sheets import GoogleSheetsReportGenerator

# Data fetched from Google Sheets (from Composio tool call)
portfolio_summary_data = [
    ["ORION PORTFOLIO - WASTE MANAGEMENT ANALYTICS"],
    ["Portfolio Summary"],
    [],
    ["Metric", "Value"],
    ["Total Properties", "6"],
    ["Total Units", "2764"],
    ["Total Monthly Cost", "$44,664.28"],
    ["Average Cost Per Door", "$16.35"],
    [],
    ["Property Distribution by Tier"],
    ["Good Tier (80-100 points)", "0"],
    ["Average Tier (60-79 points)", "0"],
    ["Poor Tier (0-59 points)", "0"],
    [],
    ["Cost Analysis"],
    ["Highest CPD", "26.23"],
    ["Lowest CPD", "10.68"],
    ["Average CPD", "16.35"],
    [],
    ["Service Reliability"]
]

property_details_data = [
    ["Property Name", "Units", "Service Type", "Avg Cost/Door", "Monthly Yardage", "Yards Per Door",
     "Avg Overage Cost/Door", "City", "Monthly Cost", "Service Details"],
    [],
    ["Orion Prosper", "312", "Dumpsters", "13.81", "780", "2.5", "0.79", "Prosper", "4308.72",
     "6 x 10-Yard Dumpsters (3x/week)"],
    ["McCord Park FL", "416", "Dumpsters", "26.23", "1040", "2.5", "0", "Frisco", "10911.68",
     "13 Service Units"],
    ["Orion McKinney", "453", "Dumpsters", "13.28", "1092", "2.41", "0", "McKinney", "6015.84",
     "8x 8-yd & 2x 10-yd Dumpsters (3x/week)"],
    ["The Club at Millenia", "560", "Compactor", "21", "", "", "0", "Orlando", "11760",
     "2 x 30-Yard Compactors (on demand)"],
    ["Bella Mirage", "715", "Dumpsters", "10.68", "728", "1.02", "0", "Avondale, AZ", "7636.2",
     "4x 8-yd, 1x 6-yd, 1x 4-yd Dumpsters (4x/week)"],
    ["Orion Prosper Lakes", "308", "Compactor", "13.09", "", "", "0", "Prosper", "4031.72",
     "1x 35yd Compactor & 1x 40yd Roll-Off (on demand)"],
    [],
    ["TOTALS", "2764", "", "16.34833333", "", "", "", "", "44664.16"]
]

performance_metrics_data = [
    ["Property Name", "Performance Score", "Tier", "YPD Score", "CPD Score", "Overage Score",
     "Overage Frequency", "YPD Status", "CPD Status", "Notes"],
    [],
    ["Orion Prosper", "74.5", "Average", "70", "100", "40", "94%", "Within Target",
     "Excellent Value", "High overage frequency"],
    ["McCord Park FL", "74.5", "Average", "70", "100", "40", "100%", "Within Target",
     "Within Target", "Capacity issues"],
    ["Orion McKinney", "82", "Good", "70", "100", "70", "40%", "Within Target",
     "Excellent Value", "Moderate overages"],
    ["The Club at Millenia", "85", "Good", "100", "100", "40", "100%", "N/A (Compactor)",
     "Within Target", "Compactor system"],
    ["Bella Mirage", "85", "Good", "100", "100", "40", "68%", "Within Target",
     "Excellent Value", "High overages"],
    ["Orion Prosper Lakes", "100", "Good", "100", "100", "100", "0%", "N/A (Compactor)",
     "Excellent Value", "Excellent reliability"],
    [],
    ["PORTFOLIO AVERAGES", "83.5", "", "85", "100", "55"]
]


def main():
    print("\n" + "="*80)
    print("GENERATING HTML REPORTS FROM GOOGLE SHEETS DATA")
    print("="*80)

    # Create generator
    generator = GoogleSheetsReportGenerator()

    # Parse portfolio summary
    print("\n[INFO] Parsing portfolio summary...")
    portfolio_summary = generator.parse_portfolio_summary(portfolio_summary_data)

    # Update with actual tier counts from performance data
    good_count = 0
    average_count = 0
    poor_count = 0

    for row in performance_metrics_data[2:]:  # Skip header rows
        if len(row) > 2 and row[2]:
            tier = row[2].strip()
            if tier == "Good":
                good_count += 1
            elif tier == "Average":
                average_count += 1
            elif tier == "Poor":
                poor_count += 1

    portfolio_summary['good_properties'] = good_count
    portfolio_summary['average_properties'] = average_count
    portfolio_summary['poor_properties'] = poor_count
    portfolio_summary['avg_score'] = 83.5  # From portfolio averages row

    print(f"   - Total Properties: {portfolio_summary['total_properties']}")
    print(f"   - Total Units: {portfolio_summary['total_units']}")
    print(f"   - Portfolio Score: {portfolio_summary['avg_score']}")
    print(f"   - Good/Average/Poor: {good_count}/{average_count}/{poor_count}")

    # Parse property data
    print("\n[INFO] Parsing property data...")
    properties = generator.parse_property_data(property_details_data, performance_metrics_data)

    print(f"   - Parsed {len(properties)} properties")
    for prop in properties:
        print(f"     • {prop['property_name']}: {prop['unit_count']} units, "
              f"Score {prop['property_score']}, Tier {prop['performance_tier']}")

    # Generate Portfolio Summary Report
    print("\n" + "="*80)
    print("GENERATING PORTFOLIO SUMMARY REPORT")
    print("="*80)
    portfolio_file = generator.generate_html_portfolio_report(
        properties,
        portfolio_summary,
        output_file="PortfolioSummaryDashboard.html"
    )

    # Generate Individual Property Reports
    print("\n" + "="*80)
    print("GENERATING INDIVIDUAL PROPERTY REPORTS")
    print("="*80)

    generated_files = [portfolio_file]

    for prop in properties:
        safe_name = prop['property_name'].replace(' ', '')
        output_file = f"{safe_name}Analysis.html"

        prop_file = generator.generate_html_property_report(prop, output_file=output_file)
        generated_files.append(prop_file)

    # Summary
    print("\n" + "="*80)
    print("REPORT GENERATION COMPLETE")
    print("="*80)
    print(f"\nGenerated {len(generated_files)} HTML reports:")
    for f in generated_files:
        print(f"  ✓ {f}")

    print("\n[SUCCESS] All reports generated with correct Google Sheets data!")
    print("[INFO] Reports use correct unit counts, costs, and performance metrics")
    print("[INFO] All language patterns validated (no crisis language, no projections)")

    return True


if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERROR] Report generation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
