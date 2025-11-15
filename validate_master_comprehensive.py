import pandas as pd
import sys

excel_file = 'Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx'

# Read all critical sheets
df_overview = pd.read_excel(excel_file, sheet_name='Property Overview')
df_service = pd.read_excel(excel_file, sheet_name='Service Details')
df_ypd = pd.read_excel(excel_file, sheet_name='Yards Per Door')
df_contract = pd.read_excel(excel_file, sheet_name='Contract Terms')

# Remove totals row
df_overview_clean = df_overview[df_overview['Property Name'] != 'PORTFOLIO TOTAL'].copy()

print('='*80)
print('COMPREHENSIVE MASTER FILE VALIDATION REPORT')
print('='*80)

# 1. Property Name Consistency
print('\n\n1. PROPERTY NAME CONSISTENCY CHECK')
print('-'*80)

overview_props = set(df_overview_clean['Property Name'].dropna())
service_props = set(df_service['Property'].dropna())
ypd_props = set(df_ypd['Property'].dropna())
contract_props = set(df_contract['Property'].dropna())

all_props = overview_props | service_props | ypd_props | contract_props

print(f'\nTotal Unique Properties: {len(all_props)}')
print(f'  Property Overview: {len(overview_props)}')
print(f'  Service Details: {len(service_props)}')
print(f'  Yards Per Door: {len(ypd_props)}')
print(f'  Contract Terms: {len(contract_props)}')

missing_in_sheets = {}
for prop in all_props:
    missing = []
    if prop not in overview_props: missing.append('Property Overview')
    if prop not in service_props: missing.append('Service Details')
    if prop not in ypd_props: missing.append('Yards Per Door')
    if prop not in contract_props: missing.append('Contract Terms')
    if missing:
        missing_in_sheets[prop] = missing

if missing_in_sheets:
    print('\nWARNING - Properties missing from sheets:')
    for prop, sheets in missing_in_sheets.items():
        print(f'  {prop}: Missing from {", ".join(sheets)}')
else:
    print('\nOK - All properties present in all sheets')

# 2. Unit Count Consistency
print('\n\n2. UNIT COUNT CONSISTENCY CHECK')
print('-'*80)

for prop in sorted(all_props):
    units_overview = df_overview_clean[df_overview_clean['Property Name'] == prop]['Unit Count'].values
    units_ypd = df_ypd[df_ypd['Property'] == prop]['Units'].values if 'Units' in df_ypd.columns else None
    
    if len(units_overview) > 0 and units_ypd is not None and len(units_ypd) > 0:
        if units_overview[0] != units_ypd[0]:
            print(f'MISMATCH - {prop}:')
            print(f'  Property Overview: {units_overview[0]}')
            print(f'  Yards Per Door: {units_ypd[0]}')

# 3. Service Details vs Property Overview
print('\n\n3. SERVICE DETAILS VALIDATION')
print('-'*80)

for prop in sorted(service_props):
    prop_services = df_service[df_service['Property'] == prop]
    total_yards = prop_services['Total Yards'].sum()
    container_count = len(prop_services)
    
    overview_data = df_overview_clean[df_overview_clean['Property Name'] == prop]
    if len(overview_data) > 0:
        overview_container_count = overview_data['Container Count'].values[0]
        
        print(f'\n{prop}:')
        print(f'  Service Details: {len(prop_services)} rows, {total_yards} total yards')
        print(f'  Property Overview Container Count: {overview_container_count}')

# 4. Contract Terms Completeness
print('\n\n4. CONTRACT TERMS COMPLETENESS')
print('-'*80)

critical_fields = ['Vendor', 'Contract Start', 'Contract Term', 'Contract End', 'Auto Renewal', 'Notice Period']

for idx, row in df_contract.iterrows():
    prop = row['Property']
    missing_fields = []
    
    for field in critical_fields:
        value = str(row[field])
        if pd.isna(row[field]) or 'TBD' in value or 'Unknown' in value or 'Review' in value:
            missing_fields.append(field)
    
    if missing_fields:
        print(f'\n{prop}:')
        for field in missing_fields:
            print(f'  - {field}: {row[field]}')

print('\n\n' + '='*80)
print('END OF VALIDATION REPORT')
print('='*80)
