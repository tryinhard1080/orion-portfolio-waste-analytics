"""
Analyze Tax Treatment Across All Properties

Identify properties where tax equals base spend, which indicates either:
1. Tax-inclusive pricing (tax already included in base price)
2. Data extraction error (tax mistakenly set equal to base)
"""

import pandas as pd

def main():
    print("="*80)
    print("TAX TREATMENT ANALYSIS - ALL PROPERTIES")
    print("="*80)

    master_path = 'Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx'
    df = pd.read_excel(master_path, sheet_name='Spend by Category')

    # Get unique properties
    properties = sorted(df['Property'].unique())

    issues_found = []

    print("\nProperty-by-Property Analysis:")
    print("-"*80)

    for prop in properties:
        prop_data = df[df['Property'] == prop]

        # Get base and tax values
        base = prop_data[prop_data['Category'] == 'base']['Total Spend'].values
        tax = prop_data[prop_data['Category'] == 'tax']['Total Spend'].values

        if len(base) > 0 and len(tax) > 0:
            base_val = base[0]
            tax_val = tax[0]

            # Check if they're equal (within $0.01)
            if abs(base_val - tax_val) < 0.01:
                print(f"\n{prop}:")
                print(f"  Base Spend:  ${base_val:,.2f}")
                print(f"  Tax Spend:   ${tax_val:,.2f}")
                print(f"  Status: *** BASE = TAX *** (Issue Found)")
                issues_found.append(prop)
            else:
                print(f"\n{prop}:")
                print(f"  Base Spend:  ${base_val:,.2f}")
                print(f"  Tax Spend:   ${tax_val:,.2f}")
                tax_pct = (tax_val / base_val * 100) if base_val > 0 else 0
                print(f"  Tax Rate:    {tax_pct:.2f}% (Normal)")

        elif len(base) > 0:
            print(f"\n{prop}:")
            print(f"  Base Spend:  ${base[0]:,.2f}")
            print(f"  Tax Spend:   Not found")
            print(f"  Status: No tax category")
        else:
            print(f"\n{prop}:")
            print(f"  Status: No base or tax categories found")

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total Properties Analyzed: {len(properties)}")
    print(f"Properties with BASE = TAX Issue: {len(issues_found)}")

    if issues_found:
        print("\nProperties Requiring Investigation:")
        for i, prop in enumerate(issues_found, 1):
            print(f"  {i}. {prop}")

        print("\nNext Steps:")
        print("  1. Review invoices for these properties")
        print("  2. Determine if tax is included in base price or separate")
        print("  3. Update category classification if needed")
        print("  4. Document tax treatment for each property")

if __name__ == '__main__':
    main()
