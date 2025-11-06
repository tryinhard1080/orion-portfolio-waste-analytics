"""
Final Comprehensive Extraction - Complete Excel Output
Combines all data sources into one perfect Excel file
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# Paths
OUTPUT_FOLDER = Path("../Extraction_Output")
ARIZONA_JSON = OUTPUT_FOLDER / "arizona_invoices_consolidated.json"

print("=" * 80)
print("FINAL COMPREHENSIVE EXTRACTION")
print("=" * 80)

# Property name standardization
def normalize_property_name(name):
    """Standardize all property name variations"""
    if not name:
        return "Unknown Property"

    name = str(name).strip()

    mapping = {
        'ORION PROSPER': 'Orion Prosper',
        'Orion Prosper': 'Orion Prosper',
        'orion prosper': 'Orion Prosper',
        'ORION PROSPER LAKES': 'Orion Prosper Lakes',
        'Orion Prosper Lakes': 'Orion Prosper Lakes',
        'orion prosper lakes': 'Orion Prosper Lakes',
        'ORION MCKINNEY': 'Orion McKinney',
        'Orion McKinney': 'Orion McKinney',
        'MCCORD PARK FL': 'McCord Park FL',
        'McCord Park FL': 'McCord Park FL',
        'THE CLUB @ MILLENIA': 'The Club at Millenia',
        'The Club at Millenia': 'The Club at Millenia',
        'BELLA MIRAGE': 'Bella Mirage',
        'Bella Mirage': 'Bella Mirage',
        'MANDARINA': 'Mandarina',
        'Mandarina': 'Mandarina',
        'PAVILIONS AT ARROWHEAD': 'Pavilions at Arrowhead',
        'Pavilions at Arrowhead': 'Pavilions at Arrowhead',
        'SPRINGS AT ALTA MESA': 'Springs at Alta Mesa',
        'Springs at Alta Mesa': 'Springs at Alta Mesa',
        'TEMPE VISTA': 'Tempe Vista',
        'Tempe Vista': 'Tempe Vista'
    }

    return mapping.get(name, name)

# Load Texas PDF invoice data
print("\n1. Loading Texas PDF invoice data...")
texas_excel = OUTPUT_FOLDER / "Orion_Invoice_Extraction_20251103_074451.xlsx"
texas_properties = {}

if texas_excel.exists():
    xls = pd.ExcelFile(texas_excel)

    for sheet in xls.sheet_names:
        if sheet not in ['Summary', 'Validation']:
            df = pd.read_excel(texas_excel, sheet_name=sheet)
            if not df.empty and 'Property' in df.columns:
                prop_name = normalize_property_name(df['Property'].iloc[0])
                texas_properties[prop_name] = df

    print(f"   Loaded {len(texas_properties)} Texas properties")
    for prop in sorted(texas_properties.keys()):
        print(f"     - {prop}: {len(texas_properties[prop])} rows")
else:
    print("   No Texas data found")

# Load Arizona invoice data
print("\n2. Loading Arizona invoice data...")
arizona_invoices = []

if ARIZONA_JSON.exists():
    with open(ARIZONA_JSON, 'r') as f:
        arizona_data = json.load(f)
    arizona_invoices = arizona_data.get('invoices', [])

    # Normalize property names
    for inv in arizona_invoices:
        inv['property_name'] = normalize_property_name(inv.get('property_name'))

    print(f"   Loaded {len(arizona_invoices)} Arizona invoices")
else:
    print("   No Arizona data found")

# Organize Arizona by property
arizona_by_property = {}
for inv in arizona_invoices:
    prop = inv.get('property_name', 'Unknown Property')
    if prop not in arizona_by_property:
        arizona_by_property[prop] = []
    arizona_by_property[prop].append(inv)

if arizona_by_property:
    print(f"   Organized into {len(arizona_by_property)} properties:")
    for prop in sorted(arizona_by_property.keys()):
        print(f"     - {prop}: {len(arizona_by_property[prop])} invoices")

# Get all unique properties
all_properties = set(texas_properties.keys()) | set(arizona_by_property.keys())
print(f"\n3. Total unique properties: {len(all_properties)}")

# Create comprehensive Excel
print("\n4. Creating comprehensive Excel file...")
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
excel_output = OUTPUT_FOLDER / f"COMPLETE_All_Properties_{timestamp}.xlsx"

with pd.ExcelWriter(excel_output, engine='xlsxwriter') as writer:
    workbook = writer.book

    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4472C4',
        'font_color': 'white',
        'border': 1
    })

    # Portfolio Summary
    print("   Creating Portfolio Summary...")
    summary_data = []

    for prop in sorted(all_properties):
        texas_count = len(texas_properties.get(prop, pd.DataFrame())) if prop in texas_properties else 0
        arizona_count = len(arizona_by_property.get(prop, []))

        summary_data.append({
            'Property Name': prop,
            'Texas PDF Invoices': texas_count if texas_count > 0 else 0,
            'Arizona Invoices': arizona_count,
            'Total Invoice Records': texas_count + arizona_count,
            'Data Source': 'PDF' if texas_count > 0 else 'Excel' if arizona_count > 0 else 'None'
        })

    df_summary = pd.DataFrame(summary_data)
    df_summary.to_excel(writer, sheet_name='Portfolio Summary', index=False)

    ws = writer.sheets['Portfolio Summary']
    for col_num, value in enumerate(df_summary.columns.values):
        ws.write(0, col_num, value, header_format)
        ws.set_column(col_num, col_num, 20)

    # Individual property sheets
    for prop in sorted(all_properties):
        print(f"   Creating sheet for {prop}...")

        # Create safe sheet name
        sheet_name = prop[:30] if len(prop) <= 31 else prop[:27] + "..."
        sheet_name = sheet_name.replace("/", "-").replace("\\", "-").replace("[", "").replace("]", "").replace("*", "").replace("?", "")

        all_rows = []

        # Add Texas PDF data
        if prop in texas_properties:
            df_texas = texas_properties[prop].copy()
            df_texas['Data Source'] = 'Texas PDF'
            all_rows.append(df_texas)

        # Add Arizona data
        if prop in arizona_by_property:
            az_records = []
            for inv in arizona_by_property[prop]:
                az_records.append({
                    'Data Source': 'Arizona Excel',
                    'Source File': inv.get('source_file'),
                    'Property': inv.get('property_name'),
                    'Vendor': inv.get('vendor_name'),
                    'Invoice #': inv.get('invoice_number'),
                    'Invoice Date': inv.get('invoice_date'),
                    'Amount': inv.get('total_amount'),
                    'Billing Period': inv.get('billing_period'),
                    'Description': inv.get('description'),
                    'Service Type': inv.get('service_type'),
                    'Account #': inv.get('account_number')
                })

            if az_records:
                df_arizona = pd.DataFrame(az_records)
                all_rows.append(df_arizona)

        # Combine and export
        if all_rows:
            df_combined = pd.concat(all_rows, ignore_index=True, sort=False)
            df_combined.to_excel(writer, sheet_name=sheet_name, index=False)

            ws = writer.sheets[sheet_name]
            for col_num, value in enumerate(df_combined.columns.values):
                ws.write(0, col_num, value, header_format)
                max_width = min(max(df_combined[value].astype(str).apply(len).max(), len(str(value))) + 2, 50)
                ws.set_column(col_num, col_num, max_width)

print(f"\n5. Excel file created: {excel_output.name}")

# Generate summary report
print("\n6. Generating summary statistics...")

total_texas = sum(len(texas_properties.get(p, pd.DataFrame())) for p in all_properties if p in texas_properties)
total_arizona = len(arizona_invoices)

print("\n" + "=" * 80)
print("EXTRACTION COMPLETE!")
print("=" * 80)
print(f"\nFile: {excel_output}")
print(f"\nStatistics:")
print(f"  - Total Properties: {len(all_properties)}")
print(f"  - Total Texas Invoice Records: {total_texas}")
print(f"  - Total Arizona Invoices: {total_arizona}")
print(f"  - Grand Total: {total_texas + total_arizona}")
print(f"\nProperties by State:")

texas_props = ['Bella Mirage', 'McCord Park FL', 'Orion McKinney',
               'Orion Prosper', 'Orion Prosper Lakes', 'The Club at Millenia']
arizona_props = ['Mandarina', 'Pavilions at Arrowhead',
                 'Springs at Alta Mesa', 'Tempe Vista']

print(f"\n  Texas ({len([p for p in texas_props if p in all_properties])} properties):")
for prop in sorted(texas_props):
    if prop in all_properties:
        t_count = len(texas_properties.get(prop, pd.DataFrame())) if prop in texas_properties else 0
        print(f"    - {prop}: {t_count} records")

print(f"\n  Arizona ({len([p for p in arizona_props if p in all_properties])} properties):")
for prop in sorted(arizona_props):
    if prop in all_properties:
        a_count = len(arizona_by_property.get(prop, []))
        print(f"    - {prop}: {a_count} invoices")

other_props = [p for p in all_properties if p not in texas_props and p not in arizona_props]
if other_props:
    print(f"\n  Other/Unknown ({len(other_props)} properties):")
    for prop in sorted(other_props):
        t_count = len(texas_properties.get(prop, pd.DataFrame())) if prop in texas_properties else 0
        a_count = len(arizona_by_property.get(prop, []))
        print(f"    - {prop}: {t_count + a_count} records")

print("\nAll data successfully consolidated into one Excel file!")
