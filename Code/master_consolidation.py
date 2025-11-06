"""
Master Consolidation - All Data Sources
Combines PDF extractions + Arizona Excel data into one comprehensive workbook
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Paths
OUTPUT_FOLDER = Path("../Extraction_Output")
ARIZONA_JSON = OUTPUT_FOLDER / "arizona_invoices_consolidated.json"

print("=" * 80)
print("MASTER CONSOLIDATION - ALL DATA SOURCES")
print("=" * 80)

# Step 1: Load Arizona data
print("\nLoading Arizona invoice data...")
if ARIZONA_JSON.exists():
    with open(ARIZONA_JSON, 'r') as f:
        arizona_data = json.load(f)
    az_invoices = arizona_data.get('invoices', [])
    print(f"  Loaded {len(az_invoices)} Arizona invoices")
else:
    az_invoices = []
    print("  No Arizona data found")

# Step 2: Load latest PDF extraction JSON
print("\nLoading PDF extraction data...")
json_files = sorted(OUTPUT_FOLDER.glob("Complete_Data_*.json"), reverse=True)
if json_files:
    with open(json_files[0], 'r') as f:
        pdf_data = json.load(f)
    pdf_invoices = pdf_data.get('invoices', [])
    pdf_contracts = pdf_data.get('contracts', [])
    print(f"  Loaded {len(pdf_invoices)} PDF invoices")
    print(f"  Loaded {len(pdf_contracts)} PDF contracts")
else:
    pdf_invoices = []
    pdf_contracts = []
    print("  No PDF extraction data found")

# Step 3: Normalize property names
print("\nNormalizing property names...")
property_name_map = {
    # Standardize case and variations
    'ORION PROSPER': 'Orion Prosper',
    'Orion Prosper': 'Orion Prosper',
    'orion prosper': 'Orion Prosper',
    'ORION PROSPER LAKES': 'Orion Prosper Lakes',
    'Orion Prosper Lakes': 'Orion Prosper Lakes',
    'orion prosper lakes': 'Orion Prosper Lakes',
    'ORION MCKINNEY': 'Orion McKinney',
    'Orion McKinney': 'Orion McKinney',
    'ORION MCKINN': 'Orion McKinney',
    'MCCORD PARK FL': 'McCord Park FL',
    'McCord Park FL': 'McCord Park FL',
    'Mccord Park FL': 'McCord Park FL',
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

def normalize_property(name):
    if not name:
        return "Unknown Property"
    return property_name_map.get(name, name)

# Normalize all property names
for inv in pdf_invoices:
    if inv:
        inv['property_name'] = normalize_property(inv.get('property_name'))

for con in pdf_contracts:
    if con:
        con['property_name'] = normalize_property(con.get('property_name'))

for inv in az_invoices:
    inv['property_name'] = normalize_property(inv.get('property_name'))

# Step 4: Organize by property
print("\nOrganizing data by property...")
properties = defaultdict(lambda: {
    'invoices': [],
    'contracts': [],
    'arizona_invoices': []
})

for inv in pdf_invoices:
    if inv:
        prop = inv.get('property_name', 'Unknown Property')
        properties[prop]['invoices'].append(inv)

for con in pdf_contracts:
    if con:
        prop = con.get('property_name', 'Unknown Property')
        properties[prop]['contracts'].append(con)

for inv in az_invoices:
    prop = inv.get('property_name', 'Unknown Property')
    properties[prop]['arizona_invoices'].append(inv)

# Print summary
print(f"\n  Found {len(properties)} unique properties:")
for prop in sorted(properties.keys()):
    data = properties[prop]
    print(f"    {prop}:")
    print(f"      - PDF Invoices: {len(data['invoices'])}")
    print(f"      - Contracts: {len(data['contracts'])}")
    print(f"      - Arizona Invoices: {len(data['arizona_invoices'])}")

# Step 5: Create comprehensive Excel
print("\nCreating comprehensive Excel workbook...")
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
excel_output = OUTPUT_FOLDER / f"MASTER_All_Properties_{timestamp}.xlsx"

with pd.ExcelWriter(excel_output, engine='xlsxwriter') as writer:
    workbook = writer.book

    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4472C4',
        'font_color': 'white',
        'border': 1
    })

    # Summary tab
    summary_rows = []
    for prop in sorted(properties.keys()):
        data = properties[prop]
        summary_rows.append({
            'Property Name': prop,
            'PDF Invoices': len(data['invoices']),
            'Arizona Invoices': len(data['arizona_invoices']),
            'Total Invoices': len(data['invoices']) + len(data['arizona_invoices']),
            'Contracts': len(data['contracts']),
            'Has Complete Data': 'Yes' if (data['invoices'] or data['arizona_invoices']) and data['contracts'] else 'Partial'
        })

    df_summary = pd.DataFrame(summary_rows)
    df_summary.to_excel(writer, sheet_name='Portfolio Summary', index=False)

    worksheet = writer.sheets['Portfolio Summary']
    for col_num, value in enumerate(df_summary.columns.values):
        worksheet.write(0, col_num, value, header_format)
        worksheet.set_column(col_num, col_num, 18)

    # Property tabs
    for prop in sorted(properties.keys()):
        data = properties[prop]

        # Create unique sheet name
        sheet_name = prop[:30] if len(prop) <= 31 else prop[:27] + "..."
        sheet_name = sheet_name.replace("/", "-").replace("\\", "-").replace("[", "").replace("]", "")

        rows = []

        # Add PDF invoices
        for inv in data['invoices']:
            invoice = inv.get('invoice', {})
            base_row = {
                'Source': 'PDF Extraction',
                'Source File': inv.get('source_file'),
                'Property': inv.get('property_name'),
                'Vendor': inv.get('vendor_name'),
                'Account #': inv.get('vendor_account_number'),
                'Invoice #': invoice.get('invoice_number'),
                'Invoice Date': invoice.get('invoice_date'),
                'Due Date': invoice.get('due_date'),
                'Amount Due': invoice.get('amount_due'),
                'Billing Period': inv.get('billing_period', {}).get('month_year')
            }

            line_items = invoice.get('line_items', [])
            if line_items:
                for item in line_items:
                    row = base_row.copy()
                    row.update({
                        'Service Date': item.get('date'),
                        'Description': item.get('description'),
                        'Category': item.get('category'),
                        'Quantity': item.get('quantity'),
                        'UOM': item.get('uom'),
                        'Container Size': item.get('container_size_yd'),
                        'Container Type': item.get('container_type'),
                        'Unit Rate': item.get('unit_rate'),
                        'Extended Amount': item.get('extended_amount')
                    })
                    rows.append(row)
            else:
                rows.append(base_row)

        # Add Arizona invoices
        for az_inv in data['arizona_invoices']:
            rows.append({
                'Source': 'Arizona Excel',
                'Source File': az_inv.get('source_file'),
                'Property': az_inv.get('property_name'),
                'Vendor': az_inv.get('vendor_name'),
                'Invoice #': az_inv.get('invoice_number'),
                'Invoice Date': az_inv.get('invoice_date'),
                'Amount Due': az_inv.get('total_amount'),
                'Billing Period': az_inv.get('billing_period'),
                'Description': az_inv.get('description')
            })

        if rows:
            df_property = pd.DataFrame(rows)
            df_property.to_excel(writer, sheet_name=sheet_name, index=False)

            worksheet = writer.sheets[sheet_name]
            for col_num, value in enumerate(df_property.columns.values):
                worksheet.write(0, col_num, value, header_format)
                max_len = min(max(df_property[value].astype(str).apply(len).max(), len(str(value))) + 2, 50)
                worksheet.set_column(col_num, col_num, max_len)

    # Contract Summary tab
    contract_rows = []
    for prop in sorted(properties.keys()):
        for contract in properties[prop]['contracts']:
            contract_details = contract.get('contract_details', {})
            pricing = contract.get('pricing', {})
            contract_rows.append({
                'Source File': contract.get('source_file'),
                'Property': contract.get('property_name'),
                'Vendor': contract.get('vendor_name'),
                'Effective Date': contract_details.get('effective_date'),
                'Expiration Date': contract_details.get('expiration_date'),
                'Term (Years)': contract_details.get('initial_term_years'),
                'Auto Renew': contract_details.get('auto_renew'),
                'Notice Days': contract_details.get('notice_term_days'),
                'Monthly Total': pricing.get('monthly_total'),
                'Annual Total': pricing.get('annual_total')
            })

    if contract_rows:
        df_contracts = pd.DataFrame(contract_rows)
        df_contracts.to_excel(writer, sheet_name='All Contracts', index=False)

        worksheet = writer.sheets['All Contracts']
        for col_num, value in enumerate(df_contracts.columns.values):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, 15)

print(f"\n  Excel created: {excel_output}")

# Step 6: Generate property inventory report
print("\nGenerating property inventory report...")
report_output = OUTPUT_FOLDER / f"PROPERTY_INVENTORY_{timestamp}.md"

with open(report_output, 'w') as f:
    f.write("# COMPLETE PROPERTY INVENTORY\n\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    f.write("## SUMMARY\n\n")
    f.write(f"- **Total Properties:** {len(properties)}\n")
    f.write(f"- **Total PDF Invoices:** {len(pdf_invoices)}\n")
    f.write(f"- **Total Arizona Invoices:** {len(az_invoices)}\n")
    f.write(f"- **Total Contracts:** {len(pdf_contracts)}\n\n")

    # Texas properties
    texas_props = ['Orion Prosper', 'Orion Prosper Lakes', 'Orion McKinney',
                   'McCord Park FL', 'Bella Mirage', 'The Club at Millenia']
    f.write("## TEXAS PROPERTIES (6)\n\n")
    for prop in sorted(texas_props):
        if prop in properties:
            data = properties[prop]
            f.write(f"### {prop}\n\n")
            f.write(f"- **PDF Invoices:** {len(data['invoices'])}\n")
            f.write(f"- **Contracts:** {len(data['contracts'])}\n")
            status = "✅ Complete" if data['invoices'] and data['contracts'] else "⚠️ Incomplete"
            f.write(f"- **Status:** {status}\n\n")

    # Arizona properties
    az_props = ['Mandarina', 'Pavilions at Arrowhead', 'Springs at Alta Mesa', 'Tempe Vista']
    f.write("## ARIZONA PROPERTIES (4)\n\n")
    for prop in sorted(az_props):
        if prop in properties:
            data = properties[prop]
            f.write(f"### {prop}\n\n")
            f.write(f"- **Arizona Invoices (Excel):** {len(data['arizona_invoices'])}\n")
            f.write(f"- **Contracts:** {len(data['contracts'])}\n")
            status = "✅ Complete" if data['arizona_invoices'] and data['contracts'] else "⚠️ Incomplete"
            f.write(f"- **Status:** {status}\n\n")

    # Unknown properties
    unknown_props = [p for p in properties.keys() if p not in texas_props and p not in az_props]
    if unknown_props:
        f.write("## OTHER/UNKNOWN PROPERTIES\n\n")
        for prop in sorted(unknown_props):
            data = properties[prop]
            f.write(f"### {prop}\n\n")
            f.write(f"- **PDF Invoices:** {len(data['invoices'])}\n")
            f.write(f"- **Arizona Invoices:** {len(data['arizona_invoices'])}\n")
            f.write(f"- **Contracts:** {len(data['contracts'])}\n\n")

print(f"  Report created: {report_output}")

# Final summary
print("\n" + "=" * 80)
print("MASTER CONSOLIDATION COMPLETE!")
print("=" * 80)
print(f"\nOutput Files:")
print(f"  1. Excel: {excel_output}")
print(f"  2. Report: {report_output}")
print(f"\nData Included:")
print(f"  - {len(pdf_invoices)} PDF invoices")
print(f"  - {len(az_invoices)} Arizona invoices")
print(f"  - {len(pdf_contracts)} contracts")
print(f"  - {len(properties)} unique properties")
print(f"\nAll data sources successfully consolidated!")
