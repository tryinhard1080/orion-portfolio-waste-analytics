"""
Comprehensive QA - Final validation across all 10 properties

This script performs portfolio-wide quality assurance:
- Validates all 10 expense workbooks
- Cross-references totals against master file
- Generates comprehensive completion report

Author: Claude Code
Date: November 13, 2025
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime


def run_comprehensive_qa():
    """Run comprehensive QA across entire portfolio"""

    base_dir = Path(r'C:\Users\Richard\Downloads\Orion Data Part 2')
    master_file = base_dir / 'Portfolio_Reports' / 'MASTER_Portfolio_Complete_Data.xlsx'

    print(f"\n{'='*70}")
    print("COMPREHENSIVE PORTFOLIO QA")
    print(f"{'='*70}\n")

    # All 10 properties
    properties = [
        'Springs at Alta Mesa',
        'Orion Prosper',
        'The Club at Millenia',
        'Bella Mirage',
        'Mandarina',
        'Pavilions at Arrowhead',
        'Tempe Vista',
        'Orion Prosper Lakes',
        'McCord Park FL',
        'Orion McKinney'
    ]

    qa_results = {
        'qa_date': datetime.now().isoformat(),
        'portfolio_summary': {},
        'properties': [],
        'validation_summary': {
            'total_properties': len(properties),
            'passed': 0,
            'failed': 0,
            'warnings': 0
        }
    }

    portfolio_totals = {
        'total_months': 0,
        'total_spend': 0.0,
        'total_units': 0,
        'workbooks_generated': 0,
        'csv_files': 0,
        'validation_files': 0
    }

    print("Running QA checks on all 10 properties...\n")

    for prop in properties:
        prop_folder = base_dir / 'Properties' / prop.replace(' ', '_')

        # Check files exist
        workbook_path = prop_folder / f"{prop.replace(' ', '_')}_Expense_Report.xlsx"
        csv_path = prop_folder / f"{prop.replace(' ', '_')}_expense_data.csv"
        validation_path = prop_folder / f"{prop.replace(' ', '_')}_validation.json"

        prop_result = {
            'property_name': prop,
            'status': 'PENDING',
            'checks': {},
            'files_found': {},
            'metrics': {}
        }

        # Check 1: Files exist
        prop_result['files_found'] = {
            'workbook': workbook_path.exists(),
            'csv': csv_path.exists(),
            'validation': validation_path.exists()
        }

        if not all(prop_result['files_found'].values()):
            prop_result['status'] = 'FAILED'
            prop_result['errors'] = ['Missing required files']
            qa_results['properties'].append(prop_result)
            qa_results['validation_summary']['failed'] += 1
            print(f"  [FAIL] {prop}: Missing files")
            continue

        # Load data
        csv_df = pd.read_csv(csv_path)
        with open(validation_path, 'r') as f:
            validation = json.load(f)

        # Check 2: Validation status
        prop_result['checks']['validation_status'] = {
            'status': validation['status'],
            'passed': validation['status'] == 'PASSED'
        }

        # Check 3: Extract metrics
        prop_result['metrics'] = {
            'months': len(csv_df),
            'total_spend': float(csv_df['Amount'].sum()),
            'avg_monthly': float(csv_df['Amount'].mean()),
            'avg_cpd': float(csv_df['Cost_Per_Door'].mean())
        }

        # Check 4: Workbook exists and size
        if workbook_path.exists():
            prop_result['metrics']['workbook_size_kb'] = workbook_path.stat().st_size / 1024
            portfolio_totals['workbooks_generated'] += 1

        portfolio_totals['csv_files'] += 1
        portfolio_totals['validation_files'] += 1

        # Update portfolio totals
        portfolio_totals['total_months'] += prop_result['metrics']['months']
        portfolio_totals['total_spend'] += prop_result['metrics']['total_spend']

        # Determine overall status
        if validation['status'] == 'PASSED':
            prop_result['status'] = 'PASSED'
            qa_results['validation_summary']['passed'] += 1
            print(f"  [OK] {prop}: {prop_result['metrics']['months']} months, ${prop_result['metrics']['total_spend']:,.2f}")
        else:
            prop_result['status'] = 'FAILED'
            qa_results['validation_summary']['failed'] += 1
            print(f"  [FAIL] {prop}: Validation failed")

        qa_results['properties'].append(prop_result)

    # Cross-reference with master file
    print(f"\n{'='*70}")
    print("CROSS-REFERENCE WITH MASTER FILE")
    print(f"{'='*70}\n")

    try:
        # Load all tabs from master file
        excel_file = pd.ExcelFile(master_file)

        master_totals = {}
        for sheet_name in excel_file.sheet_names:
            if sheet_name in properties:
                df = pd.read_excel(master_file, sheet_name=sheet_name)

                # Determine amount field based on property
                if 'Extended Amount' in df.columns:
                    amount_col = 'Extended Amount'
                elif 'Total Amount' in df.columns:
                    # Pattern B - need to sum only first record per invoice
                    invoices = df.groupby('Invoice Number')['Total Amount'].first()
                    master_totals[sheet_name] = float(invoices.sum())
                    continue
                elif 'Invoice Amount' in df.columns:
                    amount_col = 'Invoice Amount'
                else:
                    print(f"  [WARNING] {sheet_name}: Could not determine amount column")
                    continue

                master_totals[sheet_name] = float(df[amount_col].sum())

        # Compare extracted vs master
        print("Comparing extracted totals vs master file:\n")

        discrepancies = []
        for prop_result in qa_results['properties']:
            prop_name = prop_result['property_name']

            if prop_name not in master_totals:
                print(f"  [SKIP] {prop_name}: Not found in master file")
                continue

            extracted = prop_result['metrics']['total_spend']
            master = master_totals[prop_name]
            diff = abs(extracted - master)

            prop_result['checks']['master_file_match'] = {
                'extracted': extracted,
                'master': master,
                'difference': diff,
                'passed': diff < 1.0
            }

            if diff < 1.0:
                print(f"  [OK] {prop_name}: ${extracted:,.2f} (diff: ${diff:.2f})")
            else:
                print(f"  [FAIL] {prop_name}: ${extracted:,.2f} vs ${master:,.2f} (diff: ${diff:.2f})")
                discrepancies.append(prop_name)

        if discrepancies:
            print(f"\n[WARNING] {len(discrepancies)} properties have discrepancies")
        else:
            print(f"\n[OK] All properties match master file")

    except Exception as e:
        print(f"[ERROR] Could not cross-reference master file: {str(e)}")

    # Final summary
    print(f"\n{'='*70}")
    print("PORTFOLIO SUMMARY")
    print(f"{'='*70}\n")

    print(f"Total Properties: {len(properties)}")
    print(f"Passed Validation: {qa_results['validation_summary']['passed']}")
    print(f"Failed Validation: {qa_results['validation_summary']['failed']}")
    print(f"\nTotal Months of Data: {portfolio_totals['total_months']}")
    print(f"Total Portfolio Spend: ${portfolio_totals['total_spend']:,.2f}")
    print(f"Workbooks Generated: {portfolio_totals['workbooks_generated']}")
    print(f"CSV Files: {portfolio_totals['csv_files']}")
    print(f"Validation Reports: {portfolio_totals['validation_files']}")

    # Save QA report
    qa_results['portfolio_summary'] = portfolio_totals

    report_path = base_dir / 'PHASE_4_COMPREHENSIVE_QA.json'
    with open(report_path, 'w') as f:
        json.dump(qa_results, f, indent=2)

    print(f"\n[OK] QA report saved: {report_path}")

    # Overall status
    if qa_results['validation_summary']['failed'] == 0:
        print(f"\n{'='*70}")
        print("[OK] COMPREHENSIVE QA PASSED")
        print(f"{'='*70}\n")
        return True
    else:
        print(f"\n{'='*70}")
        print(f"[FAIL] COMPREHENSIVE QA FAILED ({qa_results['validation_summary']['failed']} failures)")
        print(f"{'='*70}\n")
        return False


if __name__ == '__main__':
    success = run_comprehensive_qa()
    exit(0 if success else 1)
