"""
Master File Audit Script for Expense Report Generation
Validates data quality across all 10 properties before extraction

PURPOSE: Ensure data integrity and identify issues before processing
OUTPUT: audit_report.json with validation results
"""

import pandas as pd
import openpyxl
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Property configuration from Property Reference Sheet
PROPERTY_CONFIG = {
    'Bella Mirage': {'units': 715, 'state': 'AZ', 'type': 'Garden Style', 'service': 'Compactor'},
    'Pavilions at Arrowhead': {'units': 248, 'state': 'AZ', 'type': 'Garden Style', 'service': 'Dumpster'},
    'Springs at Alta Mesa': {'units': 200, 'state': 'AZ', 'type': 'Garden Style', 'service': 'Mixed'},
    'Mandarina': {'units': 180, 'state': 'AZ', 'type': 'Garden Style', 'service': 'Dumpster'},
    'Tempe Vista': {'units': 186, 'state': 'AZ', 'type': 'Garden Style', 'service': 'Dumpster'},
    'The Club at Millenia': {'units': 560, 'state': 'FL', 'type': 'Garden Style', 'service': 'Compactor'},
    'Orion Prosper Lakes': {'units': 308, 'state': 'TX', 'type': 'Garden Style', 'service': 'Compactor'},
    'McCord Park FL': {'units': 416, 'state': 'TX', 'type': 'Garden Style', 'service': 'Dumpster'},
    'Orion McKinney': {'units': 453, 'state': 'TX', 'type': 'Garden Style', 'service': 'Mixed'},
    'Orion Prosper': {'units': 312, 'state': 'TX', 'type': 'Garden Style', 'service': 'Compactor'}
}

class MasterFileAuditor:
    """Audit master file data quality and structure"""

    def __init__(self, master_file_path):
        self.master_file_path = master_file_path
        self.audit_results = {
            'audit_date': datetime.now().isoformat(),
            'master_file': str(master_file_path),
            'properties': {},
            'overall_status': 'PENDING',
            'critical_issues': [],
            'warnings': [],
            'summary': {}
        }

    def run_audit(self):
        """Execute complete audit workflow"""
        print("="*70)
        print("MASTER FILE AUDIT - EXPENSE REPORT DATA VALIDATION")
        print("="*70)
        print(f"File: {self.master_file_path}")
        print(f"Audit Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Load workbook
        try:
            wb = openpyxl.load_workbook(self.master_file_path, read_only=True, data_only=True)
            print(f"[OK] Successfully loaded workbook with {len(wb.sheetnames)} sheets\n")
        except Exception as e:
            self.audit_results['critical_issues'].append(f"Failed to load workbook: {str(e)}")
            self.audit_results['overall_status'] = 'FAILED'
            return self.audit_results

        # Audit each property
        for property_name in PROPERTY_CONFIG.keys():
            print(f"\n{'='*70}")
            print(f"AUDITING: {property_name}")
            print(f"{'='*70}")

            result = self.audit_property(property_name)
            self.audit_results['properties'][property_name] = result

        # Generate summary
        self.generate_summary()

        # Determine overall status
        critical_count = len(self.audit_results['critical_issues'])
        if critical_count > 0:
            self.audit_results['overall_status'] = 'FAILED'
            print(f"\n[FAIL] AUDIT FAILED: {critical_count} critical issues found")
        else:
            self.audit_results['overall_status'] = 'PASSED'
            print(f"\n[OK] AUDIT PASSED: All validation checks passed")

        return self.audit_results

    def audit_property(self, property_name):
        """Audit a single property tab"""
        result = {
            'property_name': property_name,
            'units': PROPERTY_CONFIG[property_name]['units'],
            'service_type': PROPERTY_CONFIG[property_name]['service'],
            'status': 'PENDING',
            'issues': [],
            'warnings': [],
            'metrics': {}
        }

        try:
            # Load property data
            df = pd.read_excel(self.master_file_path, sheet_name=property_name)

            if df.empty:
                result['issues'].append("Property tab is empty - no data found")
                result['status'] = 'FAILED'
                self.audit_results['critical_issues'].append(f"{property_name}: Empty tab")
                return result

            # Store metrics
            result['metrics']['total_records'] = len(df)
            result['metrics']['columns'] = list(df.columns)

            print(f"  Total Records: {len(df)}")
            print(f"  Columns: {len(df.columns)}")

            # Check 1: Detect data pattern
            pattern = self.detect_data_pattern(df, property_name)
            result['data_pattern'] = pattern
            print(f"  Data Pattern: {pattern}")

            # Check 2: Validate required columns
            required_cols = ['Invoice Date', 'Vendor']
            missing_required = [col for col in required_cols if col not in df.columns]
            if missing_required:
                result['issues'].append(f"Missing required columns: {missing_required}")
                self.audit_results['critical_issues'].append(f"{property_name}: Missing columns {missing_required}")

            # Check 3: Identify amount field
            amount_field = self.identify_amount_field(df, property_name)
            result['amount_field'] = amount_field
            print(f"  Amount Field: {amount_field}")

            if not amount_field:
                result['issues'].append("No amount field found (Extended Amount, Invoice Amount, Total Amount)")
                self.audit_results['critical_issues'].append(f"{property_name}: No amount field")

            # Check 4: Check for missing invoice numbers
            if 'Invoice Number' in df.columns:
                missing_invoice_nums = df['Invoice Number'].isna().sum()
                result['metrics']['missing_invoice_numbers'] = int(missing_invoice_nums)

                if missing_invoice_nums > 0:
                    pct = (missing_invoice_nums / len(df)) * 100
                    result['warnings'].append(f"{missing_invoice_nums} records ({pct:.1f}%) missing invoice numbers")
                    self.audit_results['warnings'].append(f"{property_name}: {missing_invoice_nums} missing invoice numbers")
                    print(f"  [WARNING] Missing Invoice Numbers: {missing_invoice_nums} ({pct:.1f}%)")
            else:
                result['warnings'].append("No 'Invoice Number' column found")

            # Check 5: Vendor analysis
            if 'Vendor' in df.columns:
                vendors = df['Vendor'].dropna().unique()
                result['metrics']['unique_vendors'] = list(vendors)
                result['metrics']['vendor_count'] = len(vendors)
                print(f"  Unique Vendors: {len(vendors)}")
                for vendor in vendors:
                    vendor_count = (df['Vendor'] == vendor).sum()
                    print(f"    - {vendor}: {vendor_count} records")

                # Check for vendor name variations
                vendor_variations = self.detect_vendor_variations(vendors)
                if vendor_variations:
                    result['warnings'].append(f"Vendor name variations detected: {vendor_variations}")
                    print(f"  [WARNING] Vendor Variations: {vendor_variations}")

            # Check 6: Date range analysis
            if 'Invoice Date' in df.columns:
                df['Invoice Date'] = pd.to_datetime(df['Invoice Date'], errors='coerce')
                valid_dates = df['Invoice Date'].dropna()

                if len(valid_dates) > 0:
                    min_date = valid_dates.min()
                    max_date = valid_dates.max()
                    result['metrics']['date_range'] = {
                        'start': min_date.strftime('%Y-%m-%d'),
                        'end': max_date.strftime('%Y-%m-%d'),
                        'months_covered': (max_date.year - min_date.year) * 12 + (max_date.month - min_date.month) + 1
                    }
                    print(f"  Date Range: {min_date.strftime('%Y-%m')} to {max_date.strftime('%Y-%m')}")
                    print(f"  Months Covered: {result['metrics']['date_range']['months_covered']}")

                    # Check for monthly gaps
                    monthly_counts = df.groupby(df['Invoice Date'].dt.to_period('M')).size()
                    if len(monthly_counts) < result['metrics']['date_range']['months_covered']:
                        missing_months = result['metrics']['date_range']['months_covered'] - len(monthly_counts)
                        result['warnings'].append(f"Potential {missing_months} month gaps in data")
                        print(f"  [WARNING] Potential Gaps: {missing_months} months")

            # Check 7: Calculate total spend
            if amount_field:
                total_spend = df[amount_field].sum()
                result['metrics']['total_spend'] = float(total_spend)
                result['metrics']['avg_monthly_spend'] = float(total_spend / result['metrics']['date_range']['months_covered']) if 'date_range' in result['metrics'] else None
                print(f"  Total Spend: ${total_spend:,.2f}")
                if result['metrics']['avg_monthly_spend']:
                    print(f"  Avg Monthly: ${result['metrics']['avg_monthly_spend']:,.2f}")

            # Check 8: Duplicate detection
            if 'Invoice Number' in df.columns and 'Invoice Date' in df.columns:
                df_clean = df.dropna(subset=['Invoice Number', 'Invoice Date'])
                duplicates = df_clean[df_clean.duplicated(subset=['Invoice Number', 'Invoice Date'], keep=False)]
                if len(duplicates) > 0:
                    result['warnings'].append(f"{len(duplicates)} potential duplicate invoice records")
                    print(f"  [WARNING] Potential Duplicates: {len(duplicates)} records")

            # Check 9: Compactor validation
            if PROPERTY_CONFIG[property_name]['service'] == 'Compactor':
                result['requires_compactor_handling'] = True
                print(f"  [NOTE] Compactor Property: Requires tons-to-yards conversion (138 lbs/yd³)")
            else:
                result['requires_compactor_handling'] = False

            # Determine property status
            if len(result['issues']) == 0:
                result['status'] = 'PASSED'
                print(f"  [OK] Status: PASSED")
            else:
                result['status'] = 'FAILED'
                print(f"  [FAIL] Status: FAILED ({len(result['issues'])} issues)")

        except Exception as e:
            result['issues'].append(f"Audit error: {str(e)}")
            result['status'] = 'ERROR'
            self.audit_results['critical_issues'].append(f"{property_name}: Audit error - {str(e)}")
            print(f"  [FAIL] ERROR: {str(e)}")

        return result

    def detect_data_pattern(self, df, property_name):
        """Detect which data pattern (A/B/C) this property uses"""

        # Pattern A: Has 'Extended Amount' field (most common)
        if 'Extended Amount' in df.columns:
            return 'A - Full Invoice Breakdown (Extended Amount)'

        # Pattern B: Has 'Total Amount' and 'Line Item Amount'
        if 'Total Amount' in df.columns and 'Line Item Amount' in df.columns:
            return 'B - Total Amount with Line Items'

        # Pattern C: Has 'Invoice Amount' only
        if 'Invoice Amount' in df.columns:
            return 'C - Invoice Amount Only'

        return 'UNKNOWN - Manual review required'

    def identify_amount_field(self, df, property_name):
        """Identify which column contains invoice amounts"""

        # Priority order for amount fields
        amount_fields = ['Extended Amount', 'Invoice Amount', 'Total Amount', 'Line Item Amount']

        for field in amount_fields:
            if field in df.columns:
                # Verify it contains numeric data
                if pd.api.types.is_numeric_dtype(df[field]):
                    return field

        return None

    def detect_vendor_variations(self, vendors):
        """Detect potential vendor name variations"""
        variations = []

        # Common patterns
        vendor_lower = [v.lower() if isinstance(v, str) else '' for v in vendors]

        # Check for "WM" variations
        wm_variants = [v for v in vendors if isinstance(v, str) and ('wm' in v.lower() or 'waste management' in v.lower())]
        if len(wm_variants) > 1:
            variations.append(f"WM/Waste Management: {wm_variants}")

        # Check for "Frontier" variations
        frontier_variants = [v for v in vendors if isinstance(v, str) and 'frontier' in v.lower()]
        if len(frontier_variants) > 1:
            variations.append(f"Frontier: {frontier_variants}")

        # Check for "Republic" variations
        republic_variants = [v for v in vendors if isinstance(v, str) and 'republic' in v.lower()]
        if len(republic_variants) > 1:
            variations.append(f"Republic: {republic_variants}")

        return variations if variations else None

    def generate_summary(self):
        """Generate audit summary statistics"""
        summary = {
            'total_properties': len(PROPERTY_CONFIG),
            'properties_passed': 0,
            'properties_failed': 0,
            'properties_error': 0,
            'total_records': 0,
            'total_spend': 0,
            'compactor_properties': [],
            'missing_invoice_numbers_total': 0,
            'data_patterns': defaultdict(list)
        }

        for prop_name, prop_result in self.audit_results['properties'].items():
            # Count statuses
            if prop_result['status'] == 'PASSED':
                summary['properties_passed'] += 1
            elif prop_result['status'] == 'FAILED':
                summary['properties_failed'] += 1
            elif prop_result['status'] == 'ERROR':
                summary['properties_error'] += 1

            # Aggregate metrics
            if 'metrics' in prop_result:
                summary['total_records'] += prop_result['metrics'].get('total_records', 0)
                summary['total_spend'] += prop_result['metrics'].get('total_spend', 0)
                summary['missing_invoice_numbers_total'] += prop_result['metrics'].get('missing_invoice_numbers', 0)

            # Track compactor properties
            if prop_result.get('requires_compactor_handling'):
                summary['compactor_properties'].append(prop_name)

            # Track data patterns
            if 'data_pattern' in prop_result:
                summary['data_patterns'][prop_result['data_pattern']].append(prop_name)

        self.audit_results['summary'] = summary

        # Print summary
        print("\n" + "="*70)
        print("AUDIT SUMMARY")
        print("="*70)
        print(f"Total Properties: {summary['total_properties']}")
        print(f"  [OK] Passed: {summary['properties_passed']}")
        print(f"  [FAIL] Failed: {summary['properties_failed']}")
        print(f"  [WARNING] Errors: {summary['properties_error']}")
        print(f"\nTotal Records: {summary['total_records']:,}")
        print(f"Total Portfolio Spend: ${summary['total_spend']:,.2f}")
        print(f"Missing Invoice Numbers: {summary['missing_invoice_numbers_total']}")
        print(f"Compactor Properties: {len(summary['compactor_properties'])} - {summary['compactor_properties']}")

        print(f"\nData Patterns:")
        for pattern, properties in summary['data_patterns'].items():
            print(f"  {pattern}: {len(properties)} properties")
            for prop in properties:
                print(f"    - {prop}")

        print(f"\nCritical Issues: {len(self.audit_results['critical_issues'])}")
        for issue in self.audit_results['critical_issues']:
            print(f"  [FAIL] {issue}")

        print(f"\nWarnings: {len(self.audit_results['warnings'])}")
        for warning in self.audit_results['warnings'][:10]:  # Show first 10
            print(f"  [WARNING] {warning}")
        if len(self.audit_results['warnings']) > 10:
            print(f"  ... and {len(self.audit_results['warnings']) - 10} more warnings")

    def save_report(self, output_path):
        """Save audit report to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(self.audit_results, f, indent=2)
        print(f"\n[OK] Audit report saved to: {output_path}")


def main():
    """Execute audit"""
    base_dir = Path(r'C:\Users\Richard\Downloads\Orion Data Part 2')
    master_file = base_dir / 'Portfolio_Reports' / 'MASTER_Portfolio_Complete_Data.xlsx'
    output_file = base_dir / 'Portfolio_Reports' / 'audit_report.json'

    # Run audit
    auditor = MasterFileAuditor(master_file)
    results = auditor.run_audit()

    # Save report
    auditor.save_report(output_file)

    # Return status code
    return 0 if results['overall_status'] == 'PASSED' else 1


if __name__ == "__main__":
    exit(main())
