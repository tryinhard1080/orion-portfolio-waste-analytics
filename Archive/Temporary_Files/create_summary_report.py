#!/usr/bin/env python3
"""
Generate detailed summary report from extraction results
"""

import json
from collections import defaultdict
from datetime import datetime

def load_results(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def analyze_results(results):
    report = []
    report.append("=" * 100)
    report.append("ORION PORTFOLIO INVOICE EXTRACTION - DETAILED SUMMARY REPORT")
    report.append("=" * 100)
    report.append(f"Extraction Date: {results['extraction_date']}")
    report.append(f"Total Invoices Processed: {results['total_invoices']}")
    report.append("")

    # Property breakdown
    report.append("-" * 100)
    report.append("PROPERTY BREAKDOWN")
    report.append("-" * 100)

    property_counts = defaultdict(int)
    property_totals = defaultdict(float)
    vendor_by_property = defaultdict(set)

    for inv in results['invoices']:
        prop = inv.get('property_name', 'UNKNOWN')
        property_counts[prop] += 1
        if inv.get('total_amount'):
            property_totals[prop] += inv['total_amount']
        if inv.get('vendor'):
            vendor_by_property[prop].add(inv['vendor'])

    for prop in sorted(property_counts.keys(), key=lambda x: (x is None, x)):
        prop_name = prop if prop else "UNKNOWN"
        report.append(f"\n{prop_name}:")
        report.append(f"  Invoice Count: {property_counts[prop]}")
        report.append(f"  Total Amount: ${property_totals[prop]:,.2f}")
        report.append(f"  Vendors: {', '.join(sorted(vendor_by_property[prop]))}")

    # Vendor breakdown
    report.append("")
    report.append("-" * 100)
    report.append("VENDOR BREAKDOWN")
    report.append("-" * 100)

    vendor_counts = defaultdict(int)
    vendor_totals = defaultdict(float)

    for inv in results['invoices']:
        vendor = inv.get('vendor', 'UNKNOWN')
        vendor_counts[vendor] += 1
        if inv.get('total_amount'):
            vendor_totals[vendor] += inv['total_amount']

    for vendor in sorted(vendor_counts.keys()):
        report.append(f"\n{vendor}:")
        report.append(f"  Invoice Count: {vendor_counts[vendor]}")
        report.append(f"  Total Amount: ${vendor_totals[vendor]:,.2f}")

    # Date range analysis
    report.append("")
    report.append("-" * 100)
    report.append("DATE RANGE ANALYSIS")
    report.append("-" * 100)

    dates = [inv.get('invoice_date') for inv in results['invoices'] if inv.get('invoice_date')]
    if dates:
        dates.sort()
        report.append(f"Earliest Invoice: {dates[0]}")
        report.append(f"Latest Invoice: {dates[-1]}")

        # Count by month
        month_counts = defaultdict(int)
        for date in dates:
            month = date[:7]  # YYYY-MM
            month_counts[month] += 1

        report.append(f"\nInvoices by Month:")
        for month in sorted(month_counts.keys()):
            report.append(f"  {month}: {month_counts[month]} invoices")

    # Data quality analysis
    report.append("")
    report.append("-" * 100)
    report.append("DATA QUALITY ANALYSIS")
    report.append("-" * 100)
    report.append(f"Total Flags: {results['summary']['red_flags'] + results['summary']['yellow_flags'] + results['summary']['green_flags']}")
    report.append(f"  [RED] Critical Issues:       {results['summary']['red_flags']}")
    report.append(f"  [YELLOW] Needs Review:       {results['summary']['yellow_flags']}")
    report.append(f"  [GREEN] Validate:            {results['summary']['green_flags']}")
    report.append(f"  [OK] Clean Extractions:      {results['summary']['clean_extractions']}")

    # Field completion rates
    report.append("")
    report.append("Field Completion Rates:")

    field_counts = {
        'invoice_number': 0,
        'invoice_date': 0,
        'property_name': 0,
        'total_amount': 0,
        'vendor': 0,
        'service_period': 0
    }

    for inv in results['invoices']:
        for field in field_counts.keys():
            if inv.get(field):
                field_counts[field] += 1

    total_invoices = len(results['invoices'])
    for field, count in sorted(field_counts.items()):
        pct = (count / total_invoices * 100) if total_invoices > 0 else 0
        report.append(f"  {field:20s}: {count:3d}/{total_invoices} ({pct:5.1f}%)")

    # Confidence score distribution
    report.append("")
    report.append("Confidence Score Distribution:")
    confidence_ranges = {
        '90-100%': 0,
        '75-89%': 0,
        '50-74%': 0,
        'Below 50%': 0
    }

    for inv in results['invoices']:
        conf = inv.get('confidence', 0)
        if conf >= 90:
            confidence_ranges['90-100%'] += 1
        elif conf >= 75:
            confidence_ranges['75-89%'] += 1
        elif conf >= 50:
            confidence_ranges['50-74%'] += 1
        else:
            confidence_ranges['Below 50%'] += 1

    for range_name, count in confidence_ranges.items():
        pct = (count / total_invoices * 100) if total_invoices > 0 else 0
        report.append(f"  {range_name:12s}: {count:3d} invoices ({pct:5.1f}%)")

    # Critical issues requiring immediate attention
    report.append("")
    report.append("-" * 100)
    report.append("CRITICAL ISSUES REQUIRING IMMEDIATE ATTENTION")
    report.append("-" * 100)

    critical_issues = []
    for inv in results['invoices']:
        for flag in inv.get('flags', []):
            if flag['level'] == 'RED_FLAG':
                critical_issues.append({
                    'filename': inv['filename'],
                    'field': flag['field'],
                    'message': flag['message'],
                    'property': inv.get('property_name', 'UNKNOWN'),
                    'vendor': inv.get('vendor', 'UNKNOWN')
                })

    # Group by issue type
    issue_types = defaultdict(list)
    for issue in critical_issues:
        key = f"{issue['field']}: {issue['message']}"
        issue_types[key].append(issue['filename'])

    report.append(f"\nTotal Critical Issues: {len(critical_issues)}")
    report.append(f"\nGrouped by Issue Type:")

    for idx, (issue_type, filenames) in enumerate(sorted(issue_types.items()), 1):
        report.append(f"\n{idx}. {issue_type}")
        report.append(f"   Affected Invoices ({len(filenames)}):")
        for fn in sorted(filenames)[:10]:  # Show first 10
            report.append(f"     - {fn}")
        if len(filenames) > 10:
            report.append(f"     ... and {len(filenames) - 10} more")

    # Missing data summary
    report.append("")
    report.append("-" * 100)
    report.append("MISSING CRITICAL DATA SUMMARY")
    report.append("-" * 100)

    missing_fields = defaultdict(list)
    for inv in results['invoices']:
        if not inv.get('property_name'):
            missing_fields['property_name'].append(inv['filename'])
        if not inv.get('invoice_date'):
            missing_fields['invoice_date'].append(inv['filename'])
        if not inv.get('total_amount'):
            missing_fields['total_amount'].append(inv['filename'])
        if not inv.get('vendor') or inv.get('vendor') == 'UNKNOWN':
            missing_fields['vendor'].append(inv['filename'])

    for field, filenames in sorted(missing_fields.items()):
        if filenames:
            report.append(f"\nMissing {field} ({len(filenames)} invoices):")
            for fn in sorted(filenames)[:15]:
                report.append(f"  - {fn}")
            if len(filenames) > 15:
                report.append(f"  ... and {len(filenames) - 15} more")

    # Recommendations
    report.append("")
    report.append("-" * 100)
    report.append("RECOMMENDATIONS")
    report.append("-" * 100)

    recommendations = []

    if missing_fields['total_amount']:
        recommendations.append(f"1. PRIORITY: {len(missing_fields['total_amount'])} invoices missing total amount - manual review required")

    if missing_fields['property_name']:
        recommendations.append(f"2. HIGH: {len(missing_fields['property_name'])} invoices need property identification")

    if missing_fields['invoice_date']:
        recommendations.append(f"3. HIGH: {len(missing_fields['invoice_date'])} invoices missing invoice date")

    yellow_flags = results['summary']['yellow_flags']
    if yellow_flags > 0:
        recommendations.append(f"4. MEDIUM: {yellow_flags} items flagged for review (container details, frequencies)")

    green_flags = results['summary']['green_flags']
    if green_flags > 0:
        recommendations.append(f"5. LOW: {green_flags} items flagged for validation (excess charges, service types)")

    for rec in recommendations:
        report.append(rec)

    if not recommendations:
        report.append("All invoices extracted cleanly with no issues!")

    # Property-specific recommendations
    report.append("")
    report.append("Property-Specific Actions:")

    for prop in sorted(property_counts.keys(), key=lambda x: (x is None, x)):
        prop_name = prop if prop else "UNKNOWN"
        prop_invoices = [inv for inv in results['invoices'] if inv.get('property_name') == prop]
        prop_issues = sum(1 for inv in prop_invoices for flag in inv.get('flags', []) if flag['level'] == 'RED_FLAG')

        if prop_issues > 0:
            report.append(f"  - {prop_name}: Review {prop_issues} critical issues")

    report.append("")
    report.append("=" * 100)
    report.append("END OF REPORT")
    report.append("=" * 100)

    return "\n".join(report)

def main():
    results = load_results("extraction_results.json")
    report = analyze_results(results)

    # Save report
    report_filename = f"EXTRACTION_SUMMARY_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_filename, 'w') as f:
        f.write(report)

    print(report)
    print(f"\nReport saved to: {report_filename}")

if __name__ == "__main__":
    main()
