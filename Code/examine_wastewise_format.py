import pandas as pd
import openpyxl
from pathlib import Path

file_path = r'C:\Users\Richard\Downloads\Mandarina_WasteWise_Verified_Analysis (1).xlsx'
wb = openpyxl.load_workbook(file_path)

print("="*70)
print("MANDARINA WASTEWISE FORMAT ANALYSIS")
print("="*70)

for sheet_name in wb.sheetnames:
    print(f"\n{'='*70}")
    print(f"SHEET: {sheet_name}")
    print(f"{'='*70}\n")

    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

        print(f"Total rows: {len(df)}")
        print(f"Total columns: {len(df.columns)}")

        print("\nFirst 15 rows:")
        for idx, row in df.head(15).iterrows():
            # Show first few non-null values
            non_null = [(i, val) for i, val in enumerate(row) if pd.notna(val)]
            if non_null:
                print(f"  Row {idx}: {non_null[:5]}")

        print("\n")
    except Exception as e:
        print(f"Error reading sheet: {e}\n")
