"""
Inspect Bella Mirage Excel structure to understand data layout
"""

import pandas as pd

EXCEL_PATH = r"C:\Users\Richard\Downloads\Orion Data Part 2\Extraction_Output\BellaMirage_WasteAnalysis_Validated.xlsx"

excel_file = pd.ExcelFile(EXCEL_PATH)

for sheet_name in excel_file.sheet_names:
    print(f"\n{'='*60}")
    print(f"Sheet: {sheet_name}")
    print(f"{'='*60}")

    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    print(f"\nColumns: {list(df.columns)}")
    print(f"Rows: {len(df)}")
    print(f"\nFirst 5 rows:")
    print(df.head())

    if len(df) > 0:
        print(f"\nSample data types:")
        print(df.dtypes)
