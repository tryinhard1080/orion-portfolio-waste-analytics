"""
Check Service Details - Identify properties missing container/service information

This script checks for:
- Container count
- Container size
- Service frequency
- Container type
"""

import pandas as pd
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
MASTER_FILE = BASE_DIR / "Portfolio_Reports" / "MASTER_Portfolio_Complete_Data.xlsx"

def check_service_details():
    """Check which properties have complete service details"""
    
    print('=' * 80)
    print('SERVICE DETAILS COMPLETENESS CHECK')
    print('=' * 80)
    print()
    
    xl = pd.ExcelFile(MASTER_FILE)
    property_tabs = xl.sheet_names[7:]  # Skip summary tabs
    
    # Fields to check
    service_fields = {
        'Container Count': ['Container Count', 'Containers', 'Number of Containers', 'Qty', 'Quantity'],
        'Container Size': ['Container Size', 'Size', 'Yard Size', 'Yards', 'Container Yards'],
        'Service Frequency': ['Frequency', 'Service Frequency', 'Pickups Per Week', 'Frequency/Week', 'Weekly Frequency'],
        'Container Type': ['Container Type', 'Type', 'Service Type', 'Equipment Type']
    }
    
    results = []
    
    for prop in property_tabs:
        df = pd.read_excel(xl, prop)
        
        print(f'{prop}:')
        print(f'  Total records: {len(df)}')
        print(f'  Columns: {list(df.columns)}')
        print()
        
        # Check each service field
        field_status = {}
        
        for field_name, possible_columns in service_fields.items():
            found = False
            found_col = None
            populated_count = 0
            
            # Check if any of the possible column names exist
            for col in possible_columns:
                if col in df.columns:
                    found = True
                    found_col = col
                    populated_count = df[col].notna().sum()
                    break
            
            if found:
                pct = (populated_count / len(df) * 100) if len(df) > 0 else 0
                status = '✓' if populated_count > 0 else '⚠'
                print(f'  {status} {field_name}: {populated_count}/{len(df)} ({pct:.1f}%) - Column: "{found_col}"')
                field_status[field_name] = {
                    'found': True,
                    'column': found_col,
                    'populated': populated_count,
                    'total': len(df),
                    'percentage': pct
                }
            else:
                print(f'  ✗ {field_name}: MISSING')
                field_status[field_name] = {
                    'found': False,
                    'column': None,
                    'populated': 0,
                    'total': len(df),
                    'percentage': 0
                }
        
        print()
        
        # Calculate completeness score
        fields_found = sum(1 for f in field_status.values() if f['found'])
        fields_populated = sum(1 for f in field_status.values() if f['populated'] > 0)
        
        results.append({
            'Property': prop,
            'Records': len(df),
            'Container Count': field_status['Container Count'],
            'Container Size': field_status['Container Size'],
            'Service Frequency': field_status['Service Frequency'],
            'Container Type': field_status['Container Type'],
            'Fields Found': fields_found,
            'Fields Populated': fields_populated
        })
    
    # Summary
    print('=' * 80)
    print('SUMMARY: SERVICE DETAILS COMPLETENESS')
    print('=' * 80)
    print()
    
    print(f'{"Property":<30} {"Records":<10} {"Count":<8} {"Size":<8} {"Freq":<8} {"Type":<8} {"Score":<10}')
    print('-' * 80)
    
    for r in results:
        count_status = '✓' if r['Container Count']['populated'] > 0 else '✗'
        size_status = '✓' if r['Container Size']['populated'] > 0 else '✗'
        freq_status = '✓' if r['Service Frequency']['populated'] > 0 else '✗'
        type_status = '✓' if r['Container Type']['populated'] > 0 else '✗'
        score = f"{r['Fields Populated']}/4"
        
        print(f'{r["Property"]:<30} {r["Records"]:<10} {count_status:<8} {size_status:<8} {freq_status:<8} {type_status:<8} {score:<10}')
    
    print()
    print('=' * 80)
    print('PROPERTIES MISSING KEY SERVICE DATA')
    print('=' * 80)
    print()
    
    # Properties missing critical data
    missing_count = [r for r in results if r['Container Count']['populated'] == 0]
    missing_size = [r for r in results if r['Container Size']['populated'] == 0]
    missing_freq = [r for r in results if r['Service Frequency']['populated'] == 0]
    missing_type = [r for r in results if r['Container Type']['populated'] == 0]
    
    print(f'Properties missing CONTAINER COUNT: {len(missing_count)}/10')
    if missing_count:
        for r in missing_count:
            print(f'  - {r["Property"]}')
    print()
    
    print(f'Properties missing CONTAINER SIZE: {len(missing_size)}/10')
    if missing_size:
        for r in missing_size:
            print(f'  - {r["Property"]}')
    print()
    
    print(f'Properties missing SERVICE FREQUENCY: {len(missing_freq)}/10')
    if missing_freq:
        for r in missing_freq:
            print(f'  - {r["Property"]}')
    print()
    
    print(f'Properties missing CONTAINER TYPE: {len(missing_type)}/10')
    if missing_type:
        for r in missing_type:
            print(f'  - {r["Property"]}')
    print()
    
    # Overall summary
    complete_properties = [r for r in results if r['Fields Populated'] == 4]
    partial_properties = [r for r in results if 0 < r['Fields Populated'] < 4]
    missing_all_properties = [r for r in results if r['Fields Populated'] == 0]
    
    print('=' * 80)
    print('OVERALL SUMMARY')
    print('=' * 80)
    print()
    print(f'✓ Complete service data (4/4 fields): {len(complete_properties)}/10 properties')
    if complete_properties:
        for r in complete_properties:
            print(f'  - {r["Property"]}')
    print()
    
    print(f'⚠ Partial service data (1-3/4 fields): {len(partial_properties)}/10 properties')
    if partial_properties:
        for r in partial_properties:
            print(f'  - {r["Property"]} ({r["Fields Populated"]}/4 fields)')
    print()
    
    print(f'✗ Missing all service data (0/4 fields): {len(missing_all_properties)}/10 properties')
    if missing_all_properties:
        for r in missing_all_properties:
            print(f'  - {r["Property"]}')
    print()
    
    # Recommendations
    print('=' * 80)
    print('RECOMMENDATIONS')
    print('=' * 80)
    print()
    
    if missing_all_properties or partial_properties:
        print('Properties needing service data extraction:')
        print()
        
        needs_attention = missing_all_properties + partial_properties
        for r in sorted(needs_attention, key=lambda x: x['Fields Populated']):
            print(f'{r["Property"]}:')
            
            missing_fields = []
            if r['Container Count']['populated'] == 0:
                missing_fields.append('Container Count')
            if r['Container Size']['populated'] == 0:
                missing_fields.append('Container Size')
            if r['Service Frequency']['populated'] == 0:
                missing_fields.append('Service Frequency')
            if r['Container Type']['populated'] == 0:
                missing_fields.append('Container Type')
            
            print(f'  Missing: {", ".join(missing_fields)}')
            print(f'  Action: Review contracts and invoices to extract service details')
            print()
    else:
        print('✓ All properties have complete service data!')
        print('  No action needed.')
    print()

if __name__ == "__main__":
    check_service_details()

