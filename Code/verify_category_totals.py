"""
Verify Category Totals for Properties with Tax Issues

Compare actual totals from property tabs vs. Spend by Category sheet
"""

import pandas as pd

def main():
    master_path = 'Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx'

    # Properties with BASE = TAX issue
    problem_properties = ['McCord Park FL', 'Orion Prosper', 'Orion Prosper Lakes']

    print("="*80)
    print("CATEGORY TOTAL VERIFICATION")
    print("="*80)

    # Read Spend by Category for comparison
    df_spend = pd.read_excel(master_path, sheet_name='Spend by Category')

    for prop in problem_properties:
        print(f"\n{prop}")
        print("-"*80)

        # Read property tab
        try:
            df_prop = pd.read_excel(master_path, sheet_name=prop)

            print("\nACTUAL TOTALS (from property tab):")
            for cat in ['base', 'tax', 'overage', 'extra_pickup', 'admin', 'other']:
                if cat in df_prop['Category'].values:
                    cat_total = df_prop[df_prop['Category'] == cat]['Extended Amount'].sum()
                    count = len(df_prop[df_prop['Category'] == cat])
                    print(f"  {cat:15}: ${cat_total:>12,.2f}  ({count} line items)")

            grand_total = df_prop['Extended Amount'].sum()
            print(f"  {'Grand Total':15}: ${grand_total:>12,.2f}")

            print("\nSPEND BY CATEGORY SHEET (what's recorded):")
            prop_spend = df_spend[df_spend['Property'] == prop]
            for _, row in prop_spend.iterrows():
                print(f"  {row['Category']:15}: ${row['Total Spend']:>12,.2f}")

            # Compare base vs tax
            base_actual = df_prop[df_prop['Category'] == 'base']['Extended Amount'].sum()
            tax_actual = df_prop[df_prop['Category'] == 'tax']['Extended Amount'].sum()

            print(f"\nDISCREPANCY CHECK:")
            if abs(base_actual - tax_actual) < 0.01:
                print(f"  WARNING: Base and Tax ARE actually equal in source data")
            else:
                print(f"  Base Actual:  ${base_actual:,.2f}")
                print(f"  Tax Actual:   ${tax_actual:,.2f}")
                print(f"  ISSUE: Spend by Category sheet shows BASE = TAX")
                print(f"         but property tab shows different values!")

        except Exception as e:
            print(f"  Error reading property tab: {e}")

    print("\n" + "="*80)
    print("CONCLUSION")
    print("="*80)
    print("If Spend by Category sheet shows BASE = TAX but property tabs show")
    print("different values, then the Spend by Category sheet needs to be recalculated")
    print("or regenerated from the property tab data.")

if __name__ == '__main__':
    main()
