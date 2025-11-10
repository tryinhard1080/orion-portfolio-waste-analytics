"""
Check property location data for regulatory research
"""

import pandas as pd
from pathlib import Path

print('=' * 80)
print('PROPERTY LOCATION DATA FOR REGULATORY RESEARCH')
print('=' * 80)
print()

# Load property data
master_file = 'Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx'

properties = {
    'Orion Prosper': {'state': 'TX', 'city': 'Prosper'},
    'Orion Prosper Lakes': {'state': 'TX', 'city': 'Prosper'},
    'Orion McKinney': {'state': 'TX', 'city': 'McKinney'},
    'McCord Park FL': {'state': 'FL', 'city': 'TBD'},
    'The Club at Millenia': {'state': 'FL', 'city': 'Orlando'},
    'Bella Mirage': {'state': 'AZ', 'city': 'Phoenix'},
    'Mandarina': {'state': 'AZ', 'city': 'Phoenix'},
    'Pavilions at Arrowhead': {'state': 'AZ', 'city': 'Glendale'},
    'Springs at Alta Mesa': {'state': 'AZ', 'city': 'Mesa'},
    'Tempe Vista': {'state': 'AZ', 'city': 'Tempe'}
}

units_map = {
    'Orion Prosper': 312,
    'Orion Prosper Lakes': 308,
    'McCord Park FL': 416,
    'Orion McKinney': 453,
    'The Club at Millenia': 560,
    'Bella Mirage': 715,
    'Mandarina': 180,
    'Pavilions at Arrowhead': 248,
    'Springs at Alta Mesa': 200,
    'Tempe Vista': 186
}

# Get units and service data
for prop_name, location in properties.items():
    df = pd.read_excel(master_file, sheet_name=prop_name)
    
    units = units_map.get(prop_name, 0)
    
    # Get service details
    if 'YPD' in df.columns:
        ypd = df['YPD'].iloc[0]
        container_type = df['Container Type'].iloc[0] if 'Container Type' in df.columns else 'Unknown'
        container_count = df['Container Count'].iloc[0] if 'Container Count' in df.columns else 0
    else:
        ypd = 'N/A'
        container_type = 'Unknown'
        container_count = 0
    
    city = location['city']
    state = location['state']
    
    print(f'{prop_name}:')
    print(f'  Location: {city}, {state}')
    print(f'  Units: {units}')
    print(f'  Service Type: {container_type}')
    print(f'  Containers: {container_count}')
    print(f'  YPD: {ypd}')
    print()

print()
print('=' * 80)
print('REGULATORY RESEARCH PLAN')
print('=' * 80)
print()
print('For each property, the wastewise-regulatory skill will research:')
print()
print('1. Local Waste/Recycling/Organics Ordinances')
print('   - Mandatory vs voluntary requirements')
print('   - Property size thresholds')
print('   - Capacity requirements')
print('   - Service frequency minimums')
print()
print('2. Penalties and Enforcement')
print('   - Fine structures')
print('   - Enforcement agencies')
print('   - Violation procedures')
print()
print('3. Licensed Haulers')
print('   - Minimum 3-5 haulers per location')
print('   - Contact information')
print('   - Service capabilities')
print()
print('4. Compliance Checklist')
print('   - Requirements met')
print('   - Requirements needing attention')
print('   - Upcoming deadlines')
print()

print('=' * 80)
print('UNIQUE LOCATIONS TO RESEARCH')
print('=' * 80)
print()

# Get unique city/state combinations
unique_locations = {}
for prop_name, location in properties.items():
    key = f"{location['city']}, {location['state']}"
    if key not in unique_locations:
        unique_locations[key] = []
    unique_locations[key].append(prop_name)

for location, props in unique_locations.items():
    print(f'{location}:')
    for prop in props:
        units = units_map.get(prop, 0)
        print(f'  - {prop} ({units} units)')
    print()

print(f'Total Unique Locations: {len(unique_locations)}')
print()

