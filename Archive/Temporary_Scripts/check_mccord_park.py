"""
Check McCord Park FL calculation
"""

import pandas as pd

master_file = 'Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx'
df = pd.read_excel(master_file, sheet_name='McCord Park FL')

print('McCORD PARK FL - SERVICE DETAILS')
print('=' * 80)
print()
print(f'Units: 416')
print(f'Container Count: {df["Container Count"].iloc[0]}')
print(f'Container Size: {df["Container Size"].iloc[0]}')
print(f'Service Notes: {df["Service Notes"].iloc[0]}')
print(f'Total Yards: {df["Total Yards"].iloc[0]}')
print(f'YPD: {df["YPD"].iloc[0]}')
print()

print('EXPECTED CONFIGURATION:')
print('  Trash: 1×4yd FL @ 3x/WK')
print('  Trash: 12×8yd FL @ 3x/WK')
print('  Recycling: 2×8yd SS @ 2x/WK')
print()

print('CORRECT CALCULATION:')
trash_4yd = (4 * 1 * 3 * 4.33) / 416
trash_8yd = (8 * 12 * 3 * 4.33) / 416
recycling = (8 * 2 * 2 * 4.33) / 416
total = trash_4yd + trash_8yd + recycling

print(f'  Trash (1×4YD @ 3x/week): {trash_4yd:.2f} YPD')
print(f'  Trash (12×8YD @ 3x/week): {trash_8yd:.2f} YPD')
print(f'  Recycling (2×8YD @ 2x/week): {recycling:.2f} YPD')
print(f'  TOTAL: {total:.2f} YPD')
print()

print(f'Current YPD in file: {df["YPD"].iloc[0]:.2f}')
print(f'Difference: {abs(total - df["YPD"].iloc[0]):.2f}')

