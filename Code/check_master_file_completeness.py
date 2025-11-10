"""
Check master file for missing service details and YPD calculations
"""

import pandas as pd
from pathlib import Path

print('=' * 80)
print('MASTER FILE DATA QUALITY CHECK')
print('=' * 80)
print()

master_file = 'Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx'

# Check all property sheets
properties = [
    'Orion Prosper',
    'Orion Prosper Lakes',
    'McCord Park FL',
    'Orion McKinney',
    'The Club at Millenia',
    'Bella Mirage',
    'Mandarina',
    'Pavilions at Arrowhead',
    'Springs at Alta Mesa',
    'Tempe Vista'
]

missing_data = []

for prop in properties:
    print(f'{prop}:')
    print('-' * 80)
    
    try:
        df = pd.read_excel(master_file, sheet_name=prop)
        
        print(f'  Total Rows: {len(df)}')
        print(f'  Columns: {len(df.columns)}')
        print()
        
        # Check for service detail columns
        service_columns = [
            'Container Count',
            'Container Size',
            'Container Type',
            'Service Frequency',
            'Service Days',
            'Total Yards',
            'YPD',
            'Service Notes'
        ]
        
        print('  Service Detail Columns:')
        has_issues = False
        
        for col in service_columns:
            if col in df.columns:
                # Check if populated
                non_null = df[col].notna().sum()
                if non_null > 0:
                    sample_value = df[col].iloc[0]
                    print(f'    ✅ {col}: {non_null}/{len(df)} rows ({sample_value})')
                else:
                    print(f'    ⚠️ {col}: EMPTY')
                    has_issues = True
            else:
                print(f'    ❌ {col}: MISSING')
                has_issues = True
        
        if has_issues:
            missing_data.append(prop)
        
        print()
        
    except Exception as e:
        print(f'  ❌ ERROR: {e}')
        print()
        missing_data.append(prop)

print()
print('=' * 80)
print('SUMMARY')
print('=' * 80)
print()

if missing_data:
    print(f'⚠️ Properties with Missing/Incomplete Data: {len(missing_data)}/10')
    for prop in missing_data:
        print(f'  - {prop}')
else:
    print('✅ All 10 properties have complete service details!')

print()

