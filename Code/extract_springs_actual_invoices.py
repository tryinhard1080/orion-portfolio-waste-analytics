"""
Extract actual invoice data from Springs at Alta Mesa Excel files
and create month-by-month expense table
"""

import pandas as pd
from datetime import datetime
import os

def extract_mesa_trash_data(file_path):
    """Extract City of Mesa trash invoice data"""
    df = pd.read_excel(file_path)
    trash_data = df[df['Utility'] == 'Trash'].copy()
    trash_data['Bill Date'] = pd.to_datetime(trash_data['Bill Date'])
    trash_data['Service Start'] = pd.to_datetime(trash_data['Service Start'])
    trash_data['Service End'] = pd.to_datetime(trash_data['Service End'])
    trash_data = trash_data.sort_values('Bill Date', ascending=False)

    # Create monthly dictionary (use Service End month as key)
    monthly_costs = {}
    for idx, row in trash_data.iterrows():
        service_month = row['Service End'].strftime('%Y-%m')
        amount = row['Bill Total']

        # If month already exists, sum it (handle duplicate billings)
        if service_month in monthly_costs:
            print(f"Warning: Duplicate billing for {service_month} - adding ${amount:.2f} to existing ${monthly_costs[service_month]:.2f}")
            monthly_costs[service_month] = monthly_costs[service_month] + amount
        else:
            monthly_costs[service_month] = amount

    return monthly_costs

def extract_ally_waste_data(file_path):
    """Extract Ally Waste invoice data"""
    df = pd.read_excel(file_path)
    df['Bill Date'] = pd.to_datetime(df['Bill Date'])
    df['Service Start'] = pd.to_datetime(df['Service Start'])
    df['Service End'] = pd.to_datetime(df['Service End'])
    df = df.sort_values('Bill Date', ascending=False)

    # Create monthly dictionary (use Service End month as key)
    monthly_costs = {}
    for idx, row in df.iterrows():
        service_month = row['Service End'].strftime('%Y-%m')
        amount = row['Bill Total']
        monthly_costs[service_month] = amount

    return monthly_costs

def create_combined_monthly_data(mesa_costs, ally_costs):
    """Combine both vendors into single monthly data structure"""
    # Get all unique months
    all_months = sorted(set(list(mesa_costs.keys()) + list(ally_costs.keys())), reverse=True)

    monthly_data = []
    ytd_total = 0

    for month in all_months:
        mesa_amount = mesa_costs.get(month, 0)
        ally_amount = ally_costs.get(month, 0)
        total = mesa_amount + ally_amount

        # Calculate YTD (building from oldest to newest for accurate accumulation)
        ytd_total += total
        cpd = total / 200  # 200 units

        # Format month for display
        month_date = datetime.strptime(month, '%Y-%m')
        month_display = month_date.strftime('%b %Y')

        # Add notes for special cases
        notes = ''
        if ally_amount == 552.21:
            notes = 'Holiday surcharge (Ally Waste)'
        elif ally_amount == 357.21:
            notes = 'Partial month (Ally Waste startup)'
        elif mesa_amount == 0:
            notes = 'Missing City of Mesa data'
        elif ally_amount == 0:
            notes = 'Missing Ally Waste data'

        monthly_data.append({
            'month': month_display,
            'mesa_amount': mesa_amount,
            'ally_amount': ally_amount,
            'total': total,
            'cpd': cpd,
            'notes': notes
        })

    # Calculate YTD properly (reverse order for cumulative sum)
    running_total = 0
    for i in range(len(monthly_data) - 1, -1, -1):
        running_total += monthly_data[i]['total']
        monthly_data[i]['ytd_total'] = running_total

    return monthly_data

def main():
    """Main execution"""
    base_path = r'C:\Users\Richard\Downloads\Orion Data Part 2\Properties\Springs_at_Alta_Mesa'

    mesa_file = os.path.join(base_path, 'Springs at Alta Mesa - City of Mesa Trash.xlsx')
    ally_file = os.path.join(base_path, 'Springs at Alta Mesa - Ally Waste.xlsx')

    print("Extracting actual invoice data from Excel files...\n")

    # Extract data
    mesa_costs = extract_mesa_trash_data(mesa_file)
    ally_costs = extract_ally_waste_data(ally_file)

    print(f"\n=== CITY OF MESA TRASH ===")
    print(f"Found {len(mesa_costs)} months of data")
    for month in sorted(mesa_costs.keys(), reverse=True):
        print(f"  {month}: ${mesa_costs[month]:.2f}")
    print(f"  Average: ${sum(mesa_costs.values()) / len(mesa_costs):.2f}")

    print(f"\n=== ALLY WASTE ===")
    print(f"Found {len(ally_costs)} months of data")
    for month in sorted(ally_costs.keys(), reverse=True):
        print(f"  {month}: ${ally_costs[month]:.2f}")
    print(f"  Average: ${sum(ally_costs.values()) / len(ally_costs):.2f}")

    # Create combined monthly data
    monthly_data = create_combined_monthly_data(mesa_costs, ally_costs)

    print(f"\n=== COMBINED MONTHLY DATA ===")
    print(f"{'Month':<12} {'City Mesa':<12} {'Ally Waste':<12} {'Total':<12} {'$/Door':<12} {'YTD Total':<12} {'Notes'}")
    print("-" * 100)

    for row in monthly_data:
        print(f"{row['month']:<12} ${row['mesa_amount']:<11.2f} ${row['ally_amount']:<11.2f} "
              f"${row['total']:<11.2f} ${row['cpd']:<11.2f} ${row['ytd_total']:<11.2f} {row['notes']}")

    # Calculate totals
    total_mesa = sum(mesa_costs.values())
    total_ally = sum(ally_costs.values())
    grand_total = total_mesa + total_ally

    print("\n=== SUMMARY ===")
    print(f"Total City of Mesa: ${total_mesa:.2f}")
    print(f"Total Ally Waste: ${total_ally:.2f}")
    print(f"Grand Total: ${grand_total:.2f}")
    print(f"Number of months: {len(monthly_data)}")
    print(f"Average monthly: ${grand_total / len(monthly_data):.2f}")
    print(f"Average cost per door: ${(grand_total / len(monthly_data)) / 200:.2f}")

    # Save to JSON for use in regeneration script
    import json
    output_file = os.path.join(base_path, 'actual_invoice_data.json')
    output_data = {
        'mesa_monthly': mesa_costs,
        'ally_monthly': ally_costs,
        'combined_monthly': monthly_data,
        'summary': {
            'total_mesa': total_mesa,
            'total_ally': total_ally,
            'grand_total': grand_total,
            'num_months': len(monthly_data),
            'avg_monthly': grand_total / len(monthly_data),
            'avg_cpd': (grand_total / len(monthly_data)) / 200
        }
    }

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\nData saved to: {output_file}")

    return monthly_data

if __name__ == "__main__":
    monthly_data = main()
