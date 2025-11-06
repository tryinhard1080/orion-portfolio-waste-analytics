#!/usr/bin/env python3
"""
Update consolidated Excel file with re-extracted invoice data
for Orion Prosper and Orion Prosper Lakes
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import shutil

# Configuration
EXTRACTION_OUTPUT = Path("C:/Users/Richard/Downloads/Orion Data Part 2/Extraction_Output")
CURRENT_EXCEL = EXTRACTION_OUTPUT / "COMPLETE_All_Properties_UPDATED_20251103_101053.xlsx"
ORION_PROSPER_JSON = EXTRACTION_OUTPUT / "OrionProsper_ReExtraction_20251104_044254.json"
ORION_PROSPER_LAKES_JSON = EXTRACTION_OUTPUT / "OrionProsperLakes_ReExtraction_20251104_044525.json"

# Output file
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
OUTPUT_EXCEL = EXTRACTION_OUTPUT / f"COMPLETE_All_Properties_FIXED_{timestamp}.xlsx"

print("="*80)
print("UPDATING CONSOLIDATED EXCEL WITH RE-EXTRACTED INVOICES")
print("="*80)
print(f"Input Excel: {CURRENT_EXCEL.name}")
print(f"Output Excel: {OUTPUT_EXCEL.name}\n")

# Create backup
backup_file = EXTRACTION_OUTPUT / f"BACKUP_{CURRENT_EXCEL.name}"
shutil.copy2(CURRENT_EXCEL, backup_file)
print(f"Backup created: {backup_file.name}")

def parse_invoice_to_dataframe(invoice_data, property_name):
    """Convert JSON invoice data to DataFrame rows (one row per line item)"""
    rows = []

    for invoice in invoice_data.get("invoices", []):
        source_file = invoice.get("source_file", "")
        vendor_name = invoice.get("vendor_name", "")
        vendor_account = invoice.get("vendor_account_number", "")
        billing_period = invoice.get("billing_period", {}).get("month_year", "")

        invoice_info = invoice.get("invoice", {})
        invoice_number = invoice_info.get("invoice_number", "")
        invoice_date = invoice_info.get("invoice_date", "")
        total_amount = invoice_info.get("amount_due", "")

        line_items = invoice_info.get("line_items", [])

        if not line_items:
            # If no line items, create one row with invoice total
            rows.append({
                "Property": property_name,
                "Source File": source_file,
                "Vendor": vendor_name,
                "Account Number": vendor_account,
                "Billing Period": billing_period,
                "Invoice Number": invoice_number,
                "Invoice Date": invoice_date,
                "Invoice Total": total_amount,
                "Service Date": invoice_date,
                "Description": "Total Invoice Amount",
                "Category": "total",
                "Quantity": "",
                "Unit Rate": "",
                "Extended Amount": total_amount
            })
        else:
            # Create one row per line item
            for item in line_items:
                rows.append({
                    "Property": property_name,
                    "Source File": source_file,
                    "Vendor": vendor_name,
                    "Account Number": vendor_account,
                    "Billing Period": billing_period,
                    "Invoice Number": invoice_number,
                    "Invoice Date": invoice_date,
                    "Invoice Total": total_amount,
                    "Service Date": item.get("date", ""),
                    "Description": item.get("description", ""),
                    "Category": item.get("category", ""),
                    "Quantity": item.get("quantity", ""),
                    "Unit Rate": item.get("unit_rate", ""),
                    "Extended Amount": item.get("extended_amount", "")
                })

    return pd.DataFrame(rows)

# Load JSON files
print("\nLoading re-extracted invoice data...")
with open(ORION_PROSPER_JSON, 'r', encoding='utf-8') as f:
    orion_prosper_data = json.load(f)

with open(ORION_PROSPER_LAKES_JSON, 'r', encoding='utf-8') as f:
    orion_prosper_lakes_data = json.load(f)

# Convert to DataFrames
print("Converting Orion Prosper invoices to DataFrame...")
df_orion_prosper = parse_invoice_to_dataframe(orion_prosper_data, "Orion Prosper")
print(f"  Created {len(df_orion_prosper)} rows from {orion_prosper_data['extraction_metadata']['successful_extractions']} invoices")

print("Converting Orion Prosper Lakes invoices to DataFrame...")
df_orion_prosper_lakes = parse_invoice_to_dataframe(orion_prosper_lakes_data, "Orion Prosper Lakes")
print(f"  Created {len(df_orion_prosper_lakes)} rows from {orion_prosper_lakes_data['extraction_metadata']['successful_extractions']} invoices")

# Load existing Excel file
print("\nLoading existing Excel file...")
excel_file = pd.ExcelFile(CURRENT_EXCEL)
print(f"Existing sheets: {excel_file.sheet_names}")

# Create a copy of all sheets
all_sheets = {}
for sheet_name in excel_file.sheet_names:
    if sheet_name not in ["Orion Prosper", "Orion Prosper Lakes"]:
        # Keep other sheets as-is
        all_sheets[sheet_name] = pd.read_excel(excel_file, sheet_name=sheet_name)
        print(f"  Preserved: {sheet_name} ({len(all_sheets[sheet_name])} rows)")

# Add/replace the re-extracted sheets
all_sheets["Orion Prosper"] = df_orion_prosper
all_sheets["Orion Prosper Lakes"] = df_orion_prosper_lakes

print("\n" + "="*80)
print("SHEET UPDATES:")
print("="*80)
print(f"Orion Prosper: REPLACED with {len(df_orion_prosper)} rows (16 invoices)")
print(f"Orion Prosper Lakes: REPLACED with {len(df_orion_prosper_lakes)} rows (10 invoices)")

# Write to new Excel file
print(f"\nWriting updated Excel file: {OUTPUT_EXCEL.name}")
with pd.ExcelWriter(OUTPUT_EXCEL, engine='openpyxl') as writer:
    for sheet_name, df in all_sheets.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"  Written: {sheet_name} ({len(df)} rows)")

print("\n" + "="*80)
print("EXCEL UPDATE COMPLETE")
print("="*80)
print(f"New file: {OUTPUT_EXCEL}")
print(f"Backup: {backup_file}")
print("="*80)

# Summary statistics
print("\nEXTRACTION SUMMARY:")
print(f"  Orion Prosper:")
print(f"    - Invoices: {orion_prosper_data['extraction_metadata']['successful_extractions']}")
print(f"    - Date range: {df_orion_prosper['Billing Period'].min()} to {df_orion_prosper['Billing Period'].max()}")
print(f"    - Total amount: ${df_orion_prosper['Invoice Total'].astype(str).str.replace(',','').astype(float).sum():,.2f}")
print(f"    - Excel rows: {len(df_orion_prosper)}")
print()
print(f"  Orion Prosper Lakes:")
print(f"    - Invoices: {orion_prosper_lakes_data['extraction_metadata']['successful_extractions']}")
print(f"    - Date range: {df_orion_prosper_lakes['Billing Period'].min()} to {df_orion_prosper_lakes['Billing Period'].max()}")
print(f"    - Total amount: ${df_orion_prosper_lakes['Invoice Total'].astype(str).str.replace(',','').astype(float).sum():,.2f}")
print(f"    - Excel rows: {len(df_orion_prosper_lakes)}")
