"""Verify Arizona properties update"""

import pandas as pd

print('=' * 80)
print('ARIZONA PROPERTIES - VERIFICATION')
print('=' * 80)
print()

properties = ['Tempe Vista', 'Mandarina', 'Springs at Alta Mesa', 'Pavilions at Arrowhead']

for prop in properties:
    df = pd.read_excel('Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx', sheet_name=prop)
    
    print(f'{prop}:')
    
    row = df.iloc[0]
    
    print(f'  Container Count: {row["Container Count"]}')
    print(f'  Container Size: {row["Container Size"]}')
    print(f'  Container Type: {row["Container Type"]}')
    print(f'  Service Frequency: {row["Service Frequency"]}')
    print(f'  Total Yards: {row["Total Yards"]}')
    print(f'  YPD: {row["YPD"]}')
    print(f'  Service Notes: {row["Service Notes"]}')
    print(f'  Rows: {len(df)}')
    print()

print('=' * 80)
print('PORTFOLIO SUMMARY - ALL 8 PROPERTIES')
print('=' * 80)
print()

all_props = [
    'McCord Park FL', 'Orion McKinney', 'The Club at Millenia', 'Bella Mirage',
    'Tempe Vista', 'Mandarina', 'Springs at Alta Mesa', 'Pavilions at Arrowhead'
]

print('| Property | Containers | YPD | Status |')
print('|----------|------------|-----|--------|')

for prop in all_props:
    df = pd.read_excel('Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx', sheet_name=prop)
    
    if 'Container Count' in df.columns and 'YPD' in df.columns:
        count = df['Container Count'].iloc[0]
        ypd = df['YPD'].iloc[0]
        
        if isinstance(ypd, (int, float)):
            if ypd <= 2.0:
                status = '✅ Excellent'
            elif ypd <= 2.25:
                status = '✅ Good'
            else:
                status = '⚠️ High'
            print(f'| {prop} | {count} | {ypd:.2f} | {status} |')
        else:
            print(f'| {prop} | {count} | {ypd} | ⚠️ TBD |')

print()

