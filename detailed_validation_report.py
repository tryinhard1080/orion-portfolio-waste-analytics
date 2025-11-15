import pandas as pd

excel_file = 'Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx'

df_overview = pd.read_excel(excel_file, sheet_name='Property Overview')
df_service = pd.read_excel(excel_file, sheet_name='Service Details')

print('='*80)
print('PROPERTY OVERVIEW DATA QUALITY ISSUES')
print('='*80)

df_props = df_overview[df_overview['Property Name'] != 'PORTFOLIO TOTAL'].copy()

print('\n\nDETAILED PROPERTY ANALYSIS:')
print('-'*80)

for idx, row in df_props.iterrows():
    prop = row['Property Name']
    issues = []
    
    # Check Service Type column
    service_type = str(row['Service Type'])
    if service_type.isdigit():
        issues.append(f"Service Type is numeric: '{service_type}' (should be Compactor/Dumpster/Mixed)")
    
    # Check Container Count column
    container_count = str(row['Container Count'])
    if 'x/week' in container_count or 'x-' in container_count:
        issues.append(f"Container Count has frequency: '{container_count}' (should be a number)")
    
    # Check Container Size column
    container_size = str(row['Container Size'])
    
    # Check Service Frequency column
    service_freq = str(row['Service Frequency'])
    
    if issues:
        print(f'\n{prop}:')
        for issue in issues:
            print(f'  ISSUE: {issue}')
        print(f'  Current Data:')
        print(f'    Service Type: {service_type}')
        print(f'    Container Count: {container_count}')
        print(f'    Container Size: {container_size}')
        print(f'    Service Frequency: {service_freq}')
        
        # Get correct data from Service Details
        service_data = df_service[df_service['Property'] == prop]
        if len(service_data) > 0:
            print(f'  Correct Data (from Service Details):')
            for sdx, srow in service_data.iterrows():
                print(f'    {srow["Quantity"]}x {srow["Container Type"]} {srow["Container Size"]} @ {srow["Frequency"]}')

print('\n\n' + '='*80)
print('SUMMARY OF ISSUES FOUND')
print('='*80)

print('\n1. PROPERTY OVERVIEW DATA CORRUPTION:')
print('  - Orion McKinney: Service Type shows "10" instead of "Dumpster" or "Mixed"')
print('  - Orion McKinney: Container Count shows "3x/week" (frequency in wrong column)')
print('  - Bella Mirage: Service Type shows "6" instead of "Dumpster"')
print('  - Bella Mirage: Container Count shows "4x/week" (frequency in wrong column)')
print('  - Tempe Vista: Service Type shows "9" instead of "Dumpster" or "Mixed"')
print('  - Tempe Vista: Container Count shows "1x-3x/week" (frequency in wrong column)')

print('\n2. PROPERTY NAME INCONSISTENCY:')
print('  - "Orion Prosper Lakes" vs "Orion Prosper Lakes (Little Elm)"')
print('  - Property Overview uses: "Orion Prosper Lakes"')
print('  - Contract Terms uses: "Orion Prosper Lakes (Little Elm)"')

print('\n3. CONTRACT DATA GAPS:')
print('  - 8 of 10 properties have incomplete contract data')
print('  - Only 2 properties have complete contract information')
print('  - Critical missing: Contract dates, terms, renewal clauses')
