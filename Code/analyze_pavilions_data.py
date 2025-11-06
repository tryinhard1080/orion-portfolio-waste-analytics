import pandas as pd
import sys

try:
    # Load the most recent consolidated file
    file_path = r'C:\Users\Richard\Downloads\Orion Data Part 2\Extraction_Output\COMPLETE_All_Properties_UPDATED_20251103_101053.xlsx'

    # Read all sheet names first
    excel_file = pd.ExcelFile(file_path)
    print('Available sheets:')
    for sheet in excel_file.sheet_names:
        print(f'  - {sheet}')

    # Try to find Pavilions at Arrowhead sheet
    pavilions_sheet = None
    for sheet in excel_file.sheet_names:
        if 'pavilions' in sheet.lower() and 'arrowhead' in sheet.lower():
            pavilions_sheet = sheet
            break

    if not pavilions_sheet:
        print('\nERROR: Pavilions at Arrowhead sheet not found')
        sys.exit(1)

    print(f'\nFound sheet: {pavilions_sheet}')

    # Load the data
    df = pd.read_excel(file_path, sheet_name=pavilions_sheet)

    print(f'\nData Shape: {df.shape[0]} rows × {df.shape[1]} columns')
    print(f'\nColumn Names:')
    for col in df.columns:
        print(f'  - {col}')

    print(f'\nFirst 5 rows:')
    print(df.head().to_string())

    print(f'\nData Summary:')
    print(f'  - Total rows: {len(df)}')
    print(f'  - Non-null counts by column:')
    for col in df.columns:
        non_null = df[col].notna().sum()
        print(f'    {col}: {non_null}/{len(df)}')

    # Check for critical fields
    print(f'\nCritical Field Assessment:')

    if 'Invoice Amount' in df.columns:
        amounts = df['Invoice Amount'].dropna()
        print(f'  - Invoice amounts available: {len(amounts)}/{len(df)} rows')
        if len(amounts) > 0:
            print(f'  - Total spend: ${amounts.sum():,.2f}')
            print(f'  - Average invoice: ${amounts.mean():,.2f}')
    else:
        print('  - Invoice Amount column: NOT FOUND')

    if 'Units' in df.columns:
        units = df['Units'].dropna().unique()
        print(f'  - Unit count values: {units}')
    else:
        print('  - Units column: NOT FOUND')

    if 'Invoice Date' in df.columns or 'Date' in df.columns:
        date_col = 'Invoice Date' if 'Invoice Date' in df.columns else 'Date'
        dates = df[date_col].dropna()
        print(f'  - Dates available: {len(dates)}/{len(df)} rows')
        if len(dates) > 0:
            print(f'  - Date range: {dates.min()} to {dates.max()}')
    else:
        print('  - Date column: NOT FOUND')

    if 'Vendor' in df.columns:
        vendors = df['Vendor'].dropna().unique()
        print(f'  - Vendors: {vendors}')
    else:
        print('  - Vendor column: NOT FOUND')

except Exception as e:
    print(f'ERROR: {str(e)}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
