import pandas as pd

# Read The Club at Millenia data
master_file = r'C:\Users\Richard\Downloads\Orion Data Part 2\Portfolio_Reports\MASTER_Portfolio_Complete_Data.xlsx'
df = pd.read_excel(master_file, sheet_name='The Club at Millenia')

print(f'Total records: {len(df)}')
print(f'\nColumn names:')
for col in df.columns:
    print(f'  - {col}')

print(f'\nSample of first invoice (Invoice 1549125W460):')
invoice_sample = df[df['Invoice Number'] == '1549125W460'][['Invoice Date', 'Description', 'Line Item Amount', 'Total Amount', 'Service Type']].head(10)
print(invoice_sample.to_string())

print(f'\nUnique invoices: {df["Invoice Number"].nunique()}')
print(f'Invoice numbers: {sorted(df["Invoice Number"].unique())}')

print(f'\nTotal Amount sum (all records): ${df["Total Amount"].sum():,.2f}')
print(f'Line Item Amount sum (all records): ${df["Line Item Amount"].sum():,.2f}')

print(f'\nTotal Amount per invoice (first record):')
total_from_first_records = 0
for inv in sorted(df['Invoice Number'].unique()):
    inv_df = df[df['Invoice Number'] == inv]
    first_total = inv_df.iloc[0]['Total Amount']
    line_sum = inv_df['Line Item Amount'].sum()
    total_from_first_records += first_total
    print(f'  {inv}: First record Total = ${first_total:,.2f}, Line Items sum = ${line_sum:,.2f}, Records = {len(inv_df)}')

print(f'\nTotal from first records of each invoice: ${total_from_first_records:,.2f}')
