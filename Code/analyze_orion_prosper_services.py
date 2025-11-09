"""
Analyze Orion Prosper and Orion Prosper Lakes service details from invoices
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
MASTER_FILE = BASE_DIR / "Portfolio_Reports" / "MASTER_Portfolio_Complete_Data.xlsx"

print('=' * 80)
print('SERVICE DETAILS EXTRACTED FROM INVOICES')
print('=' * 80)
print()

print('ORION PROSPER:')
print('-' * 80)
print('From Invoice Description:')
print('  "2 Front Load 10 Yd, 6 Lifts Per Week"')
print()
print('Extracted Details:')
print('  Container Count: 2')
print('  Container Size: 10 YD')
print('  Container Type: Front Loader (FEL)')
print('  Service Frequency: 6 lifts per week')
print('  Units: 312')
print()
print('YPD Calculation:')
print('  Formula: (Size × Count × Pickups/Week × 4.33) / Units')
print('  YPD = (10 × 2 × 6 × 4.33) / 312')
print('  YPD = (519.6) / 312')
ypd_prosper = (10 * 2 * 6 * 4.33) / 312
print(f'  YPD = {ypd_prosper:.2f}')
print()

target = 2.0
if ypd_prosper <= target:
    pct_below = ((target - ypd_prosper) / target) * 100
    print(f'Performance: ✅ {pct_below:.1f}% BELOW target (2.0) - EXCELLENT!')
else:
    pct_above = ((ypd_prosper - target) / target) * 100
    print(f'Performance: ⚠️ {pct_above:.1f}% ABOVE target (2.0)')

print()
print()

print('ORION PROSPER LAKES:')
print('-' * 80)
print('From Invoice Descriptions:')
print('  "1 Waste Compactor 35 Cu Yd, On Call Service"')
print('  "1 Waste Container 40 Cu Yd, On Call Service"')
print()
print('Analysis:')
print('  - Multiple compactor sizes mentioned (35 CY and 40 CY)')
print('  - On Call Service = as-needed pickups')
print('  - Need to count actual pickups per month')
print()

# Load data
df = pd.read_excel(MASTER_FILE, sheet_name='Orion Prosper Lakes')

# Count disposal/pickup lines
pickup_count = 0
disposal_count = 0

for idx, row in df.iterrows():
    desc = str(row.get('Description', ''))
    if 'Pickup Service' in desc and 'Disposal' not in desc:
        pickup_count += 1
    elif 'Disposal/Recycling' in desc:
        disposal_count += 1

print(f'Pickup Service lines: {pickup_count}')
print(f'Disposal/Recycling lines: {disposal_count}')
print()

# Count by month
monthly_pickups = {}
for idx, row in df.iterrows():
    desc = str(row.get('Description', ''))
    invoice_date = row.get('Invoice Date', '')
    
    if pd.notna(invoice_date) and ('Disposal/Recycling' in desc or 'Pickup Service' in desc):
        if isinstance(invoice_date, str):
            month = invoice_date[:7]
        else:
            month = invoice_date.strftime('%Y-%m')
        monthly_pickups[month] = monthly_pickups.get(month, 0) + 1

print('Pickups by Month:')
for month, count in sorted(monthly_pickups.items()):
    print(f'  {month}: {count} pickups')

if monthly_pickups:
    avg_pickups = sum(monthly_pickups.values()) / len(monthly_pickups)
    print()
    print(f'  Average: {avg_pickups:.1f} pickups per month')
    
    # Estimate weekly frequency
    weekly_freq = avg_pickups / 4.33
    print(f'  Estimated Weekly Frequency: {weekly_freq:.1f}x per week')
    print()
    
    # For compactor, we need tonnage data
    print('Compactor Service Details:')
    print('  Container Count: 1')
    print('  Container Type: Compactor')
    print('  Container Size: 35-40 CY (variable)')
    print(f'  Service Frequency: {weekly_freq:.1f}x per week (on-call)')
    print('  Units: 308')
    print()
    
    # Try to calculate YPD using container size approach
    # Use 40 CY as the standard size
    container_size = 40
    monthly_yards = container_size * avg_pickups
    ypd_lakes = monthly_yards / 308
    
    print('YPD Calculation (Container Volume Method):')
    print(f'  Monthly Yards = {container_size} CY × {avg_pickups:.1f} pickups')
    print(f'  Monthly Yards = {monthly_yards:.2f}')
    print(f'  YPD = {monthly_yards:.2f} / 308 units')
    print(f'  YPD = {ypd_lakes:.2f}')
    print()
    
    if ypd_lakes <= target:
        pct_below = ((target - ypd_lakes) / target) * 100
        print(f'Performance: ✅ {pct_below:.1f}% BELOW target (2.0) - EXCELLENT!')
    else:
        pct_above = ((ypd_lakes - target) / target) * 100
        print(f'Performance: ⚠️ {pct_above:.1f}% ABOVE target (2.0)')

print()
print()

print('=' * 80)
print('SUMMARY - BOTH PROPERTIES')
print('=' * 80)
print()

print('| Property | Units | Containers | Size | Type | Frequency | YPD | Performance |')
print('|----------|-------|------------|------|------|-----------|-----|-------------|')
print(f'| Orion Prosper | 312 | 2 | 10 YD | FEL | 6x/week | {ypd_prosper:.2f} | ✅ Excellent |')

if monthly_pickups:
    print(f'| Orion Prosper Lakes | 308 | 1 | 40 CY | Compactor | {weekly_freq:.1f}x/week | {ypd_lakes:.2f} | ✅ Excellent |')
else:
    print('| Orion Prosper Lakes | 308 | 1 | 40 CY | Compactor | On-call | TBD | TBD |')

print()

