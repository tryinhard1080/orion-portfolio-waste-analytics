import pandas as pd

df = pd.read_excel('Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx', sheet_name='Service Details')

print("=" * 80)
print("FINAL SERVICE CONFIGURATION - ALL 10 PROPERTIES")
print("=" * 80)
print()

for prop in sorted(df['Property'].unique()):
    prop_data = df[df['Property'] == prop]
    print(f"{prop}: {int(prop_data['Quantity'].sum())} containers")
    for _, row in prop_data.iterrows():
        print(f"  {int(row['Quantity'])}x {row['Container Size']} {row['Container Type']} @ {row['Frequency']}")
    print()

print("=" * 80)
print(f"TOTAL PORTFOLIO CONTAINERS: {int(df['Quantity'].sum())}")
print(f"TOTAL SERVICE LINE ITEMS: {len(df)}")
print(f"PROPERTIES: {len(df['Property'].unique())}/10")
print("=" * 80)
