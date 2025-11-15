"""
Investigate Bella Mirage Category Math Error

User reported: Categories sum to $121K but total shows $67K
"""

import pandas as pd

def main():
    print("="*80)
    print("BELLA MIRAGE CATEGORY MATH INVESTIGATION")
    print("="*80)

    master_path = 'Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx'

    # Read Bella Mirage property tab
    df_bella = pd.read_excel(master_path, sheet_name='Bella Mirage')

    print(f"\nBella Mirage Property Tab:")
    print(f"  Total invoice line items: {len(df_bella)}")

    # Calculate grand total
    grand_total = df_bella['Extended Amount'].sum()
    print(f"  Grand Total (all line items): ${grand_total:,.2f}")

    # Category breakdown
    print("\nCategory Breakdown:")
    print("-"*80)

    category_totals = {}
    for cat in df_bella['Category'].unique():
        if pd.notna(cat):
            cat_data = df_bella[df_bella['Category'] == cat]
            cat_total = cat_data['Extended Amount'].sum()
            count = len(cat_data)
            category_totals[cat] = cat_total

            print(f"  {cat:15}: ${cat_total:>12,.2f}  ({count} items)")

    # Sum of categories
    cat_sum = sum(category_totals.values())
    print("-"*80)
    print(f"  {'SUM OF CATEGORIES':15}: ${cat_sum:>12,.2f}")

    # Compare
    print("\n" + "="*80)
    print("COMPARISON")
    print("="*80)
    print(f"Grand Total (all line items):  ${grand_total:,.2f}")
    print(f"Sum of Categories:             ${cat_sum:,.2f}")
    print(f"Difference:                    ${abs(grand_total - cat_sum):,.2f}")

    if abs(grand_total - cat_sum) > 1.00:
        print("\nDISCREPANCY FOUND!")
        print("Categories do not sum to Grand Total.")
    else:
        print("\nNo discrepancy found - categories sum correctly.")

    # Check Spend by Category sheet
    print("\n" + "="*80)
    print("SPEND BY CATEGORY SHEET (after regeneration)")
    print("="*80)

    df_spend = pd.read_excel(master_path, sheet_name='Spend by Category')
    bella_spend = df_spend[df_spend['Property'] == 'Bella Mirage']

    print("\nBella Mirage in Spend by Category:")
    for _, row in bella_spend.iterrows():
        print(f"  {row['Category']:15}: ${row['Total Spend']:>12,.2f}")

    bella_total = bella_spend['Total Spend'].sum()
    print("-"*80)
    print(f"  {'TOTAL':15}: ${bella_total:>12,.2f}")

    # Old report data (if user mentioned $121K vs $67K)
    print("\n" + "="*80)
    print("USER'S REPORTED ISSUE")
    print("="*80)
    print("User reported: Categories sum to $121K but total shows $67K")
    print(f"\nActual current data:")
    print(f"  Category sum from property tab: ${cat_sum:,.2f}")
    print(f"  Grand total from property tab:  ${grand_total:,.2f}")

    if abs(cat_sum - 121000) < 5000:
        print(f"\n  -> Category sum (~$121K) matches user's report")
    if abs(grand_total - 67000) < 5000:
        print(f"  -> Grand total (~$67K) matches user's report")

    if abs(grand_total - cat_sum) > 1000:
        print("\n  CONFIRMED: Discrepancy exists between category sum and grand total")
        print("\n  Likely cause: Some line items may not have a category assigned")

        # Check for uncategorized items
        uncategorized = df_bella[df_bella['Category'].isna()]
        if len(uncategorized) > 0:
            uncategorized_total = uncategorized['Extended Amount'].sum()
            print(f"\n  Found {len(uncategorized)} uncategorized line items")
            print(f"  Uncategorized total: ${uncategorized_total:,.2f}")

            print("\n  Sample uncategorized items:")
            print(uncategorized[['Invoice Date', 'Description', 'Extended Amount']].head(10).to_string(index=False))
    else:
        print("\n  No significant discrepancy in current data.")

if __name__ == '__main__':
    main()
