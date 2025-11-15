"""
Check Current State of Master Portfolio File
Document baseline before making corrections
"""

import pandas as pd

def main():
    master_path = 'Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx'

    print("="*80)
    print("MASTER FILE BASELINE - CURRENT STATE")
    print("="*80)

    # Read Property Overview
    df_overview = pd.read_excel(master_path, sheet_name='Property Overview')

    print("\n1. PROPERTY OVERVIEW - ALL PROPERTIES")
    print("="*80)
    cols = ['Property Name', 'Unit Count', 'Service Type', 'Container Count', 'Container Size', 'Service Frequency']
    print(df_overview[cols].to_string(index=False))

    # Check for data corruption
    print("\n\n2. DATA CORRUPTION DETECTION")
    print("="*80)

    issues_found = []
    for idx, row in df_overview.iterrows():
        prop = row['Property Name']
        if pd.notna(prop) and 'PORTFOLIO' not in str(prop).upper():
            svc_type = str(row['Service Type'])
            cnt = str(row['Container Count'])
            freq = str(row['Service Frequency'])

            # Check if Service Type contains numbers (should be text like "Compactor", "Dumpster")
            if svc_type.replace('.0', '').replace('nan', '').isdigit():
                issues_found.append(f"CORRUPTION: {prop} - Service Type = '{svc_type}' (should be text)")

            # Check if Container Count contains frequency text (should be number)
            if any(x in cnt for x in ['x/week', 'x/wk', 'On-call', 'Weekly']):
                issues_found.append(f"CORRUPTION: {prop} - Container Count = '{cnt}' (should be number)")

            # Check if Frequency contains numbers only (should have text like "3x/week")
            if freq.replace('.0', '').replace('nan', '').isdigit() and len(freq) < 5:
                issues_found.append(f"CORRUPTION: {prop} - Frequency = '{freq}' (should have 'x/week')")

    if issues_found:
        print(f"Found {len(issues_found)} DATA CORRUPTION ISSUES:\n")
        for issue in issues_found:
            print(f"  {issue}")
    else:
        print("No data corruption detected.")

    # Read Service Details for comparison
    df_service = pd.read_excel(master_path, sheet_name='Service Details')

    print("\n\n3. SERVICE DETAILS - CROSS-REFERENCE")
    print("="*80)
    for prop in sorted(df_service['Property'].unique()):
        prop_data = df_service[df_service['Property'] == prop]
        total_containers = int(prop_data['Quantity'].sum())
        print(f"{prop}: {total_containers} containers")
        for _, row in prop_data.iterrows():
            print(f"  {int(row['Quantity'])}x {row['Container Size']} {row['Container Type']} @ {row['Frequency']}")

    # Check Contract Terms
    df_contract = pd.read_excel(master_path, sheet_name='Contract Terms')

    print("\n\n4. CONTRACT TERMS - PROPERTY NAME CONSISTENCY")
    print("="*80)
    overview_names = set(df_overview[df_overview['Property Name'].notna()]['Property Name'].tolist())
    overview_names = {n for n in overview_names if 'PORTFOLIO' not in str(n).upper()}

    contract_names = set(df_contract['Property'].tolist())

    print(f"Property Overview names: {len(overview_names)}")
    print(f"Contract Terms names: {len(contract_names)}")

    name_mismatches = []
    for name in contract_names:
        if name not in overview_names:
            # Check for close match
            for ov_name in overview_names:
                if ov_name in name or name in ov_name:
                    name_mismatches.append(f"MISMATCH: Contract='{name}' vs Overview='{ov_name}'")

    if name_mismatches:
        print("\nProperty name inconsistencies found:")
        for mm in name_mismatches:
            print(f"  {mm}")
    else:
        print("\nAll property names consistent.")

    # Summary
    print("\n\n5. SUMMARY")
    print("="*80)
    print(f"Total properties in Overview: {len(overview_names)}")
    print(f"Total properties in Service Details: {len(df_service['Property'].unique())}")
    print(f"Total properties in Contract Terms: {len(contract_names)}")
    print(f"Data corruption issues: {len(issues_found)}")
    print(f"Name inconsistencies: {len(name_mismatches)}")

if __name__ == '__main__':
    main()
