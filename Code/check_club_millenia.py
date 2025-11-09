import pandas as pd

xl = pd.ExcelFile('Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx')
df = pd.read_excel(xl, 'The Club at Millenia')

print('THE CLUB AT MILLENIA - DETAILED CHECK')
print('=' * 80)
print()
print(f'Total records: {len(df)}')
print()
print('Columns:')
for i, col in enumerate(df.columns, 1):
    print(f'  {i}. {col}')
print()

# Check if Total Amount exists
if 'Total Amount' in df.columns:
    amounts = df['Total Amount'].dropna()
    print(f'Total Amount column:')
    print(f'  Records with amount: {len(amounts)}/{len(df)}')
    min_amt = amounts.min()
    max_amt = amounts.max()
    total_amt = amounts.sum()
    print(f'  Amount range: ${min_amt:,.2f} to ${max_amt:,.2f}')
    print(f'  Total spend: ${total_amt:,.2f}')
    print()
    
    # Show sample
    print('Sample records:')
    sample = df[['Invoice Date', 'Total Amount', 'Description']].head(5)
    for idx, row in sample.iterrows():
        desc = str(row['Description'])[:50] if pd.notna(row['Description']) else 'N/A'
        print(f'  - {row["Invoice Date"]}: ${row["Total Amount"]:,.2f} - {desc}')

