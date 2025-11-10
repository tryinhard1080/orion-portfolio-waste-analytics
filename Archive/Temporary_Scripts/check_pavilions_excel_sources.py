import pandas as pd
import numpy as np

print("="*80)
print("PAVILIONS AT ARROWHEAD - SOURCE EXCEL FILE ANALYSIS")
print("="*80)

files = [
    r'C:\Users\Richard\Downloads\Orion Data Part 2\rearizona4packtrashanalysis\Pavilions - Ally Waste.xlsx',
    r'C:\Users\Richard\Downloads\Orion Data Part 2\rearizona4packtrashanalysis\Pavilions - City of Glendale Trash.xlsx'
]

all_data = []

for file_path in files:
    print(f"\n{'='*80}")
    print(f"FILE: {file_path.split('\\')[-1]}")
    print(f"{'='*80}")

    try:
        # Read Excel file
        excel_file = pd.ExcelFile(file_path)
        print(f"\nSheets: {excel_file.sheet_names}")

        for sheet_name in excel_file.sheet_names:
            print(f"\n--- Sheet: {sheet_name} ---")
            df = pd.read_excel(file_path, sheet_name=sheet_name)

            print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
            print(f"\nColumns: {list(df.columns)}")

            print(f"\nFirst 3 rows:")
            print(df.head(3).to_string())

            # Look for amount/cost columns
            amount_cols = [col for col in df.columns if any(keyword in str(col).lower() for keyword in ['amount', 'total', 'cost', 'charge', 'price'])]
            if amount_cols:
                print(f"\nAmount columns found: {amount_cols}")
                for col in amount_cols:
                    non_null = df[col].notna().sum()
                    if non_null > 0:
                        values = df[col].dropna()
                        print(f"  {col}: {non_null} values, Sum: ${values.sum() if values.dtype in [np.float64, np.int64] else 'N/A'}")

            # Look for unit count
            unit_keywords = ['unit', 'apartment', 'dwelling']
            for col in df.columns:
                if any(keyword in str(col).lower() for keyword in unit_keywords):
                    print(f"\nPotential unit column: {col}")
                    print(f"  Values: {df[col].unique()}")

            # Store data
            df['Source File'] = file_path.split('\\')[-1]
            df['Sheet Name'] = sheet_name
            all_data.append(df)

    except Exception as e:
        print(f"ERROR reading file: {e}")

print(f"\n{'='*80}")
print("SUMMARY")
print(f"{'='*80}")
print(f"Total records collected: {sum(len(df) for df in all_data)}")
