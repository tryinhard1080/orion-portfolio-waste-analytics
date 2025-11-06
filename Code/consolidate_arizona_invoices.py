"""
Arizona Invoice Consolidation Script
Reads all 9 Excel invoice files from rearizona4packtrashanalysis folder
and consolidates them into a structured JSON format.

Author: Claude Code
Date: 2025-11-03
"""

import pandas as pd
import json
import os
from datetime import datetime
from pathlib import Path
import sys

# File mappings: (filename, property_name, vendor_name)
INVOICE_FILES = [
    ("Mandarina - Ally Waste.xlsx", "Mandarina", "Ally Waste"),
    ("Mandarina - Waste Management Compactor.xlsx", "Mandarina", "Waste Management - Compactor"),
    ("Mandarina - Waste Management Hauling.xlsx", "Mandarina", "Waste Management - Hauling"),
    ("Pavilions - Ally Waste.xlsx", "Pavilions at Arrowhead", "Ally Waste"),
    ("Pavilions - City of Glendale Trash.xlsx", "Pavilions at Arrowhead", "City of Glendale"),
    ("Springs at Alta Mesa - Ally Waste.xlsx", "Springs at Alta Mesa", "Ally Waste"),
    ("Springs at Alta Mesa - City of Mesa Trash.xlsx", "Springs at Alta Mesa", "City of Mesa"),
    ("Tempe Vista - Ally Waste.xlsx", "Tempe Vista", "Ally Waste"),
    ("Tempe Vista - Waste Management Hauling.xlsx", "Tempe Vista", "Waste Management - Hauling"),
]

def parse_date(date_value):
    """Parse date value to string format YYYY-MM-DD"""
    if pd.isna(date_value):
        return None

    if isinstance(date_value, str):
        try:
            # Try parsing common formats
            dt = pd.to_datetime(date_value)
            return dt.strftime('%Y-%m-%d')
        except:
            return date_value
    elif isinstance(date_value, (pd.Timestamp, datetime)):
        return date_value.strftime('%Y-%m-%d')
    else:
        return str(date_value)

def extract_invoice_data(file_path, property_name, vendor_name):
    """Extract invoice data from a single Excel file"""
    print(f"\n[*] Processing: {os.path.basename(file_path)}")

    try:
        # Read Excel file
        df = pd.read_excel(file_path, sheet_name='Invoice')

        print(f"   [+] Found {len(df)} invoice records")

        invoices = []

        for idx, row in df.iterrows():
            invoice = {
                "property_name": property_name,
                "vendor_name": vendor_name,
                "invoice_number": str(row.get('Invoice Number', '')),
                "invoice_date": parse_date(row.get('Bill Date')),
                "service_start": parse_date(row.get('Service Start')),
                "service_end": parse_date(row.get('Service End')),
                "amount": float(row.get('Bill Total', 0.0)) if pd.notna(row.get('Bill Total')) else 0.0,
                "due_date": parse_date(row.get('Due Date')),
                "paid_date": parse_date(row.get('Paid')),
                "account_number": str(row.get('Account Number', '')),
                "control_number": str(row.get('Control Number', '')),
                "service_address": str(row.get('Service Address', '')),
                "utility_type": str(row.get('Utility', '')),
                "gl_code": str(row.get('GLCode', '')),
                "provider": str(row.get('Provider', vendor_name)),
                "funding_requested": parse_date(row.get('Funding Requested')),
                "funding_received": parse_date(row.get('Funding Received')),
                "processed_date": parse_date(row.get('Processed Date')),
                "dna_link": str(row.get('Dna Link', '')),
                "meter_number": str(row.get('Meter Number', '')),

                # Metadata
                "source_file": os.path.basename(file_path),
                "extraction_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }

            invoices.append(invoice)

        print(f"   [+] Extracted {len(invoices)} invoices")
        return invoices

    except Exception as e:
        print(f"   [!] ERROR: {str(e)}")
        return []

def validate_data(consolidated_data):
    """Validate extracted data completeness and accuracy"""
    print("\n" + "="*80)
    print("VALIDATION REPORT")
    print("="*80)

    total_invoices = len(consolidated_data['invoices'])
    print(f"\nTotal Invoices Extracted: {total_invoices}")

    # Group by property
    properties = {}
    vendors = {}
    total_amount = 0.0

    for invoice in consolidated_data['invoices']:
        prop = invoice['property_name']
        vendor = invoice['vendor_name']

        if prop not in properties:
            properties[prop] = {'count': 0, 'total': 0.0}
        if vendor not in vendors:
            vendors[vendor] = {'count': 0, 'total': 0.0}

        properties[prop]['count'] += 1
        properties[prop]['total'] += invoice['amount']

        vendors[vendor]['count'] += 1
        vendors[vendor]['total'] += invoice['amount']

        total_amount += invoice['amount']

    # Property breakdown
    print("\nBY PROPERTY:")
    print("-" * 80)
    for prop, data in sorted(properties.items()):
        print(f"   {prop:30} | {data['count']:3} invoices | ${data['total']:>12,.2f}")

    # Vendor breakdown
    print("\nBY VENDOR:")
    print("-" * 80)
    for vendor, data in sorted(vendors.items()):
        print(f"   {vendor:35} | {data['count']:3} invoices | ${data['total']:>12,.2f}")

    # Financial summary
    print("\nFINANCIAL SUMMARY:")
    print("-" * 80)
    print(f"   Total Amount: ${total_amount:,.2f}")
    print(f"   Average Invoice: ${total_amount/total_invoices:,.2f}")

    # Data quality checks
    print("\nDATA QUALITY CHECKS:")
    print("-" * 80)

    missing_invoice_num = sum(1 for inv in consolidated_data['invoices'] if not inv['invoice_number'])
    missing_dates = sum(1 for inv in consolidated_data['invoices'] if not inv['invoice_date'])
    missing_amounts = sum(1 for inv in consolidated_data['invoices'] if inv['amount'] == 0.0)

    print(f"   Missing Invoice Numbers: {missing_invoice_num} ({missing_invoice_num/total_invoices*100:.1f}%)")
    print(f"   Missing Invoice Dates: {missing_dates} ({missing_dates/total_invoices*100:.1f}%)")
    print(f"   Zero/Missing Amounts: {missing_amounts} ({missing_amounts/total_invoices*100:.1f}%)")

    # Date range
    dates = [inv['invoice_date'] for inv in consolidated_data['invoices'] if inv['invoice_date']]
    if dates:
        print(f"\nDATE RANGE:")
        print(f"   Earliest Invoice: {min(dates)}")
        print(f"   Latest Invoice: {max(dates)}")

    print("\n" + "="*80)

    return {
        'total_invoices': total_invoices,
        'properties': len(properties),
        'vendors': len(vendors),
        'total_amount': total_amount,
        'data_quality': {
            'missing_invoice_numbers': missing_invoice_num,
            'missing_dates': missing_dates,
            'missing_amounts': missing_amounts
        }
    }

def main():
    """Main consolidation workflow"""
    print("="*80)
    print("ARIZONA INVOICE CONSOLIDATION")
    print("="*80)

    # Set paths
    base_dir = Path(r"C:\Users\Richard\Downloads\Orion Data Part 2")
    input_dir = base_dir / "rearizona4packtrashanalysis"
    output_dir = base_dir / "Extraction_Output"

    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)

    print(f"\nInput Directory: {input_dir}")
    print(f"Output Directory: {output_dir}")

    # Consolidated data structure
    consolidated_data = {
        "metadata": {
            "extraction_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "source_directory": str(input_dir),
            "file_count": len(INVOICE_FILES),
            "extractor": "consolidate_arizona_invoices.py"
        },
        "invoices": []
    }

    # Process each file
    for filename, property_name, vendor_name in INVOICE_FILES:
        file_path = input_dir / filename

        if not file_path.exists():
            print(f"\n[!] WARNING: File not found: {filename}")
            continue

        invoices = extract_invoice_data(file_path, property_name, vendor_name)
        consolidated_data['invoices'].extend(invoices)

    # Validate data
    validation_summary = validate_data(consolidated_data)
    consolidated_data['metadata']['validation_summary'] = validation_summary

    # Save to JSON
    output_file = output_dir / "arizona_invoices_consolidated.json"
    print(f"\n[*] Saving consolidated data to: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(consolidated_data, f, indent=2, ensure_ascii=False)

    print(f"[+] SUCCESS! Saved {len(consolidated_data['invoices'])} invoices")

    # Also create a summary CSV for quick viewing
    summary_file = output_dir / "arizona_invoices_summary.csv"
    print(f"\n[*] Creating summary CSV: {summary_file}")

    df_summary = pd.DataFrame(consolidated_data['invoices'])
    df_summary.to_csv(summary_file, index=False)

    print(f"[+] Summary CSV saved")

    print("\n" + "="*80)
    print("CONSOLIDATION COMPLETE")
    print("="*80)
    print(f"\nOutput Files:")
    print(f"  1. {output_file}")
    print(f"  2. {summary_file}")
    print()

if __name__ == "__main__":
    main()
