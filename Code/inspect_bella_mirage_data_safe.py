"""
Inspect Bella Mirage Excel structure (safe for Windows console)
"""

import pandas as pd
import json

EXCEL_PATH = r"C:\Users\Richard\Downloads\Orion Data Part 2\Extraction_Output\BellaMirage_WasteAnalysis_Validated.xlsx"

excel_file = pd.ExcelFile(EXCEL_PATH)

# Save to JSON for review
data_structure = {}

for sheet_name in excel_file.sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    data_structure[sheet_name] = {
        'columns': list(df.columns),
        'rows': len(df),
        'sample_data': df.head(10).fillna('').to_dict('records')
    }

# Write to JSON file
output_path = r"C:\Users\Richard\Downloads\Orion Data Part 2\Extraction_Output\bella_mirage_structure.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data_structure, f, indent=2, ensure_ascii=False)

print(f"Data structure saved to: {output_path}")
print("\nSheet summary:")
for sheet_name, info in data_structure.items():
    print(f"  {sheet_name}: {info['rows']} rows, columns: {info['columns']}")
