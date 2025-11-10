"""Verify that master file has all service details including McCord Park FL info"""

import pandas as pd
import openpyxl
from pathlib import Path

file_path = Path('Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx')

print('=' * 80)
print('MASTER FILE - SERVICE DETAILS VERIFICATION')
print('=' * 80)
print()

# Check McCord Park FL specifically
print('McCord Park FL - Detailed Check:')
print('-' * 80)

df = pd.read_excel(file_path, sheet_name='McCord Park FL')

# Show all columns
print(f'Total Columns: {len(df.columns)}')
print()
print('All Columns:')
for i, col in enumerate(df.columns, 1):
    print(f'  {i}. {col}')

print()
print('-' * 80)
print('Sample Data (First Row):')
print('-' * 80)

# Show first row of key service columns
service_cols = ['Property', 'Container Count', 'Container Size', 'Container Type', 
                'Service Frequency', 'Service Days', 'Total Yards', 'YPD', 'Service Notes']

available_cols = [col for col in service_cols if col in df.columns]

if available_cols:
    first_row = df[available_cols].iloc[0]
    for col in available_cols:
        val = first_row[col]
        print(f'{col}: {val}')
else:
    print('⚠️ Service columns not found!')

print()
print('=' * 80)
print()

# Check all 4 properties
properties = ['McCord Park FL', 'Orion McKinney', 'The Club at Millenia', 'Bella Mirage']

print('ALL PROPERTIES - SERVICE DETAILS SUMMARY:')
print('=' * 80)
print()

for prop in properties:
    df = pd.read_excel(file_path, sheet_name=prop)
    
    print(f'{prop}:')
    
    # Check for service columns
    service_cols_check = {
        'Container Count': 'Container Count' in df.columns,
        'Container Size': 'Container Size' in df.columns,
        'Container Type': 'Container Type' in df.columns,
        'Service Frequency': 'Service Frequency' in df.columns,
        'Service Days': 'Service Days' in df.columns,
        'Total Yards': 'Total Yards' in df.columns,
        'YPD': 'YPD' in df.columns,
        'Service Notes': 'Service Notes' in df.columns
    }
    
    missing = [col for col, exists in service_cols_check.items() if not exists]
    
    if missing:
        print(f'  ⚠️ Missing columns: {", ".join(missing)}')
    else:
        print(f'  ✅ All service columns present')
    
    # Show values if columns exist
    if all(service_cols_check.values()):
        row = df.iloc[0]
        print(f'  Container Count: {row["Container Count"]}')
        print(f'  Container Size: {row["Container Size"]}')
        print(f'  Container Type: {row["Container Type"]}')
        print(f'  Service Frequency: {row["Service Frequency"]}')
        
        service_days = row["Service Days"]
        print(f'  Service Days: {service_days if pd.notna(service_days) else "Not specified"}')
        
        print(f'  Total Yards: {row["Total Yards"]}')
        print(f'  YPD: {row["YPD"]}')
        
        notes = row["Service Notes"]
        print(f'  Service Notes: {notes if pd.notna(notes) else "None"}')
    
    print()

print('=' * 80)
print('CHECKING FOR MISSING INFORMATION')
print('=' * 80)
print()

# Check what McCord Park FL should have based on user's input
print('McCord Park FL - Expected Service Details:')
print('  Account: Acct# 105004')
print('  Service 1: Trash - 1×4yd FL @ 3x/WK on M/W/F')
print('  Service 2: Trash - 12×8yd FL @ 3x/WK on M/W/F')
print('  Service 3: Recycling - 2×8yd SS @ 2x/WK on M/F')
print()

df_mccord = pd.read_excel(file_path, sheet_name='McCord Park FL')

print('McCord Park FL - Current Values in Master File:')
if 'Account Number' in df_mccord.columns:
    print(f'  Account Number: {df_mccord["Account Number"].iloc[0]}')
else:
    print('  ⚠️ Account Number column not found')

if 'Service Notes' in df_mccord.columns:
    notes = df_mccord["Service Notes"].iloc[0]
    print(f'  Service Notes: {notes if pd.notna(notes) else "⚠️ MISSING - Should include breakdown of services"}')
else:
    print('  ⚠️ Service Notes column not found')

if 'Service Days' in df_mccord.columns:
    days = df_mccord["Service Days"].iloc[0]
    print(f'  Service Days: {days if pd.notna(days) else "⚠️ MISSING - Should be M/W/F"}')
else:
    print('  ⚠️ Service Days column not found')

print()

