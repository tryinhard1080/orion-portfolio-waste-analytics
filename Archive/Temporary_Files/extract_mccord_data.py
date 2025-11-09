import pandas as pd
import sys

# Load the Excel file
file_path = r'C:\Users\Richard\Downloads\Orion Data Part 2\Extraction_Output\COMPLETE_All_Properties_UPDATED_20251103_101053.xlsx'

# Read McCord Park FL sheet
try:
    df = pd.read_excel(file_path, sheet_name='McCord Park FL')
    print('=== McCORD PARK FL DATA ===')
    print(f'\nTotal Rows: {len(df)}')
    print(f'\nColumns: {list(df.columns)}')
    print('\n=== FIRST 10 ROWS ===')
    print(df.head(10).to_string())
    print('\n=== DATA SUMMARY ===')
    print(f'Date Range: {df["Invoice Date"].min()} to {df["Invoice Date"].max()}')
    print(f'Total Amount Due: ${df["Amount Due"].sum():,.2f}')
    print(f'Number of Invoices: {df["Invoice Number"].nunique()}')
    print(f'Average Monthly Cost: ${df["Amount Due"].sum() / df["Invoice Date"].dt.to_period("M").nunique():,.2f}')
    print('\n=== UNIQUE VENDORS ===')
    print(df['Vendor Name'].unique())
    print('\n=== SERVICE TYPE ANALYSIS ===')
    print(df['Service Type'].value_counts())
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)
    sys.exit(1)
