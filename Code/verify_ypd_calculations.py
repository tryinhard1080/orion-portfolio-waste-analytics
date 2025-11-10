"""
Verify all YPD calculations match the standard formulas
"""

import pandas as pd
from pathlib import Path

print('=' * 80)
print('YPD CALCULATION VERIFICATION')
print('=' * 80)
print()

print('STANDARD FORMULAS:')
print('-' * 80)
print()
print('DUMPSTER/FRONT LOADER SERVICE:')
print('  YPD = (Container Size × Containers × Pickups/Week × 4.33) / Units')
print()
print('COMPACTOR SERVICE (with tonnage):')
print('  Step 1: Yards = (Tons × 2000) / 138')
print('  Step 2: YPD = (Total Monthly Tonnage × 2000 / 138) / Units')
print()
print('COMPACTOR SERVICE (without tonnage - volume method):')
print('  Monthly Yards = Container Size (CY) × Pickups Per Month')
print('  YPD = Monthly Yards / Units')
print()
print('=' * 80)
print()

master_file = 'Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx'

# Property data with service details
properties = {
    'Orion Prosper': {
        'units': 312,
        'service_type': 'Front Loader',
        'containers': 2,
        'container_size': 10,  # YD
        'frequency': 6,  # per week
        'expected_ypd': (10 * 2 * 6 * 4.33) / 312
    },
    'Orion Prosper Lakes': {
        'units': 308,
        'service_type': 'Compactor (on-call)',
        'containers': 1,
        'container_size': 40,  # CY
        'avg_pickups_per_month': 10.3,
        'expected_ypd': (40 * 10.3) / 308
    },
    'McCord Park FL': {
        'units': 416,
        'service_type': 'Front Loader',
        'containers': 15,  # 1×4YD + 12×8YD (trash @ 3x/wk) + 2×8YD (recycling @ 2x/wk)
        'container_size': 'Mixed',
        'frequency': 'Mixed',
        'expected_ypd': ((4 * 1 * 3 * 4.33) + (8 * 12 * 3 * 4.33) + (8 * 2 * 2 * 4.33)) / 416
    },
    'Orion McKinney': {
        'units': 453,
        'service_type': 'Front Loader',
        'containers': 10,  # 8×8YD + 2×10YD
        'container_size': 8,  # weighted average
        'frequency': 3,
        'expected_ypd': ((8 * 8 * 3 * 4.33) + (10 * 2 * 3 * 4.33)) / 453
    },
    'The Club at Millenia': {
        'units': 560,
        'service_type': 'Dumpster',
        'containers': 6,  # 4×8YD + 1×6YD + 1×4YD
        'container_size': 8,  # weighted average
        'frequency': 4,
        'expected_ypd': ((8 * 4 * 4 * 4.33) + (6 * 1 * 4 * 4.33) + (4 * 1 * 4 * 4.33)) / 560
    },
    'Bella Mirage': {
        'units': 715,
        'service_type': 'Front End Loader',
        'containers': 6,
        'container_size': 8,
        'frequency': 3,
        'expected_ypd': (8 * 6 * 3 * 4.33) / 715
    },
    'Mandarina': {
        'units': 180,
        'service_type': 'Compactor',
        'containers': 2,
        'container_size': 6,
        'frequency': 3,
        'expected_ypd': (6 * 2 * 3 * 4.33) / 180
    },
    'Pavilions at Arrowhead': {
        'units': 248,
        'service_type': 'Dumpster',
        'containers': 4,
        'container_size': 4,
        'frequency': 2,
        'expected_ypd': (4 * 4 * 2 * 4.33) / 248
    },
    'Springs at Alta Mesa': {
        'units': 200,
        'service_type': 'Mixed',
        'containers': 16,  # 5×6YD + 4×4YD + 7×90gal
        'container_size': 'Mixed',
        'frequency': 3,
        'expected_ypd': ((6 * 5 * 3 * 4.33) + (4 * 4 * 3 * 4.33) + (0.034 * 7 * 3 * 4.33)) / 200
    },
    'Tempe Vista': {
        'units': 186,
        'service_type': 'Mixed',
        'containers': 8,  # 6×4YD + 1×6YD + 1×8YD
        'container_size': 'Mixed',
        'frequency': 3,
        'expected_ypd': ((4 * 6 * 3 * 4.33) + (6 * 1 * 3 * 4.33) + (8 * 1 * 3 * 4.33)) / 186
    }
}

print('PROPERTY-BY-PROPERTY VERIFICATION:')
print('=' * 80)
print()

issues_found = []

for prop_name, expected_data in properties.items():
    print(f'{prop_name}:')
    print('-' * 80)
    
    # Read from master file
    df = pd.read_excel(master_file, sheet_name=prop_name)
    
    if 'YPD' in df.columns:
        actual_ypd = df['YPD'].iloc[0]
        expected_ypd = expected_data['expected_ypd']
        
        print(f'  Service Type: {expected_data["service_type"]}')
        print(f'  Units: {expected_data["units"]}')
        print(f'  Containers: {expected_data["containers"]}')
        
        if expected_data['service_type'] == 'Compactor (on-call)':
            print(f'  Container Size: {expected_data["container_size"]} CY')
            print(f'  Avg Pickups/Month: {expected_data["avg_pickups_per_month"]}')
            print()
            print(f'  Calculation:')
            print(f'    Monthly Yards = {expected_data["container_size"]} CY × {expected_data["avg_pickups_per_month"]} pickups')
            print(f'    Monthly Yards = {expected_data["container_size"] * expected_data["avg_pickups_per_month"]:.2f}')
            print(f'    YPD = {expected_data["container_size"] * expected_data["avg_pickups_per_month"]:.2f} / {expected_data["units"]}')
        else:
            if 'frequency' in expected_data:
                print(f'  Frequency: {expected_data["frequency"]}x/week')
        
        print()
        print(f'  Expected YPD: {expected_ypd:.2f}')
        print(f'  Actual YPD:   {actual_ypd:.2f}')
        
        # Check if they match (within 0.01 tolerance)
        if abs(actual_ypd - expected_ypd) < 0.01:
            print(f'  ✅ CORRECT')
        else:
            print(f'  ❌ MISMATCH - Difference: {abs(actual_ypd - expected_ypd):.2f}')
            issues_found.append({
                'property': prop_name,
                'expected': expected_ypd,
                'actual': actual_ypd,
                'difference': abs(actual_ypd - expected_ypd)
            })
    else:
        print(f'  ❌ YPD column not found')
        issues_found.append({
            'property': prop_name,
            'expected': expected_data['expected_ypd'],
            'actual': None,
            'difference': None
        })
    
    print()

print()
print('=' * 80)
print('SUMMARY')
print('=' * 80)
print()

if issues_found:
    print(f'⚠️ Found {len(issues_found)} calculation issues:')
    print()
    for issue in issues_found:
        print(f'  {issue["property"]}:')
        print(f'    Expected: {issue["expected"]:.2f}')
        if issue["actual"] is not None:
            print(f'    Actual: {issue["actual"]:.2f}')
        else:
            print(f'    Actual: N/A')
        if issue["difference"]:
            print(f'    Difference: {issue["difference"]:.2f}')
        print()
else:
    print('✅ All YPD calculations are CORRECT!')
    print()
    print('All properties using standard formulas:')
    print('  - Dumpster/Front Loader: (Size × Containers × Freq × 4.33) / Units')
    print('  - Compactor (on-call): (Container Size × Pickups/Month) / Units')
    print()

