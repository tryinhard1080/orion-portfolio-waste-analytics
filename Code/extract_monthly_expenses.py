"""
Universal Expense Extraction Engine for Waste Management Invoice Data
Handles 3 data patterns (A/B/C) across 10 properties with comprehensive validation

CRITICAL: This generates budget data for property teams - accuracy is paramount
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import numpy as np

class ExpenseExtractor:
    """Universal expense extraction engine with pattern detection and validation"""

    def __init__(self, master_file_path, property_config_path, vendor_mapping_path):
        self.master_file_path = Path(master_file_path)
        self.property_config_path = Path(property_config_path)
        self.vendor_mapping_path = Path(vendor_mapping_path)

        # Load configuration
        with open(property_config_path, 'r') as f:
            self.config = json.load(f)

        with open(vendor_mapping_path, 'r') as f:
            self.vendor_mapping = json.load(f)['mapping']

        self.extraction_log = []

    def extract_property(self, property_name):
        """
        Extract monthly expense data for a single property
        Returns: DataFrame with monthly breakdown + validation report
        """
        print(f"\n{'='*70}")
        print(f"EXTRACTING: {property_name}")
        print(f"{'='*70}")

        # Get property configuration
        if property_name not in self.config['properties']:
            raise ValueError(f"Property '{property_name}' not found in configuration")

        prop_config = self.config['properties'][property_name]

        # Load property data from master file
        try:
            df = pd.read_excel(self.master_file_path, sheet_name=property_name)
            print(f"Loaded {len(df)} records from master file")
        except Exception as e:
            raise Exception(f"Failed to load property data: {str(e)}")

        # Detect and validate data pattern
        detected_pattern = self._detect_pattern(df, prop_config)
        print(f"Data Pattern: {detected_pattern}")

        # Extract based on pattern
        if detected_pattern == 'A':
            monthly_df = self._extract_pattern_a(df, property_name, prop_config)
        elif detected_pattern == 'B':
            monthly_df = self._extract_pattern_b(df, property_name, prop_config)
        elif detected_pattern == 'C':
            monthly_df = self._extract_pattern_c(df, property_name, prop_config)
        else:
            raise ValueError(f"Unknown data pattern: {detected_pattern}")

        # Post-processing
        monthly_df = self._standardize_vendor_names(monthly_df, property_name)
        monthly_df = self._calculate_cost_per_door(monthly_df, prop_config['units'])
        monthly_df = self._add_ytd_totals(monthly_df)
        monthly_df = self._detect_anomalies(monthly_df, property_name)

        # Validation
        validation_result = self._validate_extraction(monthly_df, df, prop_config)

        print(f"\n[OK] Extraction complete: {len(monthly_df)} months extracted")
        print(f"Total spend: ${monthly_df['Amount'].sum():,.2f}")
        print(f"Validation: {validation_result['status']}")

        return monthly_df, validation_result

    def _detect_pattern(self, df, prop_config):
        """Detect data pattern and validate against config"""
        # Check for amount fields in priority order
        if 'Extended Amount' in df.columns:
            detected = 'A'
        elif 'Total Amount' in df.columns and 'Line Item Amount' in df.columns:
            detected = 'B'
        elif 'Invoice Amount' in df.columns:
            detected = 'C'
        else:
            raise ValueError("No recognized amount field found")

        # Validate against config
        expected = prop_config['data_pattern']
        if detected != expected:
            print(f"[WARNING] Pattern mismatch: detected {detected}, expected {expected}")

        return detected

    def _extract_pattern_a(self, df, property_name, prop_config):
        """
        Pattern A: Full Invoice Breakdown (Extended Amount)
        Multiple line items per invoice - sum by invoice number
        """
        print(f"Using Pattern A extraction (Extended Amount aggregation)")

        # Ensure Invoice Date is datetime
        df['Invoice Date'] = pd.to_datetime(df['Invoice Date'], errors='coerce')

        # Drop rows with no amount
        df_clean = df[df['Extended Amount'].notna()].copy()
        print(f"  Records with amounts: {len(df_clean)}")

        # Handle missing invoice numbers
        missing_inv = df_clean['Invoice Number'].isna().sum()
        if missing_inv > 0:
            print(f"  [WARNING] {missing_inv} records missing invoice numbers - will aggregate by month")
            df_clean['Invoice Number'] = df_clean.apply(
                lambda row: f"MONTHLY-{row['Vendor']}-{row['Invoice Date'].strftime('%Y-%m')}"
                if pd.isna(row['Invoice Number'])
                else row['Invoice Number'],
                axis=1
            )

        # Group by invoice and sum amounts
        agg_dict = {
            'Extended Amount': 'sum'
        }
        if 'Category' in df_clean.columns:
            agg_dict['Category'] = lambda x: ', '.join(x.dropna().unique()) if len(x.dropna().unique()) > 0 else 'Service'

        invoice_groups = df_clean.groupby(['Invoice Number', 'Invoice Date', 'Vendor']).agg(agg_dict).reset_index()

        if 'Category' not in invoice_groups.columns:
            invoice_groups['Category'] = 'Service'

        print(f"  Unique invoices: {len(invoice_groups)}")

        # Create month column for grouping
        invoice_groups['Month'] = invoice_groups['Invoice Date'].dt.to_period('M')

        # Group by month
        agg_monthly = {
            'Invoice Number': lambda x: ', '.join(x.astype(str)),
            'Invoice Date': 'first',  # Use first invoice date in month
            'Vendor': lambda x: ', '.join(x.unique()),
            'Extended Amount': 'sum'
        }
        if 'Category' in invoice_groups.columns:
            agg_monthly['Category'] = lambda x: ', '.join(x.unique())

        monthly_df = invoice_groups.groupby('Month').agg(agg_monthly).reset_index()

        if 'Category' not in monthly_df.columns:
            monthly_df['Category'] = 'Service'

        # Rename columns to standard format
        monthly_df = monthly_df.rename(columns={'Extended Amount': 'Amount'})
        monthly_df['Month'] = monthly_df['Month'].astype(str)

        # Sort by date
        monthly_df = monthly_df.sort_values('Invoice Date')

        return monthly_df

    def _extract_pattern_b(self, df, property_name, prop_config):
        """
        Pattern B: Total Amount with Line Items
        Use Total Amount from first record per invoice to avoid duplication
        """
        print(f"Using Pattern B extraction (Total Amount - first record per invoice)")

        # Ensure Invoice Date is datetime
        df['Invoice Date'] = pd.to_datetime(df['Invoice Date'], errors='coerce')

        # Drop rows with no amount
        df_clean = df[df['Total Amount'].notna()].copy()
        print(f"  Records with amounts: {len(df_clean)}")

        # For each invoice, take first record's Total Amount
        invoice_groups = df_clean.groupby(['Invoice Number', 'Vendor']).first().reset_index()

        print(f"  Unique invoices: {len(invoice_groups)}")

        # Create month column
        invoice_groups['Month'] = pd.to_datetime(invoice_groups['Invoice Date']).dt.to_period('M')

        # Group by month
        agg_monthly = {
            'Invoice Number': lambda x: ', '.join(x.astype(str)),
            'Invoice Date': 'first',
            'Vendor': lambda x: ', '.join(x.unique()),
            'Total Amount': 'sum'
        }
        if 'Category' in invoice_groups.columns:
            agg_monthly['Category'] = lambda x: ', '.join(x.dropna().unique())

        monthly_df = invoice_groups.groupby('Month').agg(agg_monthly).reset_index()

        if 'Category' not in monthly_df.columns:
            monthly_df['Category'] = 'Service'

        # Rename columns
        monthly_df = monthly_df.rename(columns={'Total Amount': 'Amount'})
        monthly_df['Month'] = monthly_df['Month'].astype(str)

        # Sort by date
        monthly_df = monthly_df.sort_values('Invoice Date')

        return monthly_df

    def _extract_pattern_c(self, df, property_name, prop_config):
        """
        Pattern C: Invoice Amount Only
        CRITICAL: Handles MIXED scenarios (some records with invoice numbers, some without)
        Common for municipal services where City charges lack invoice numbers
        """
        print(f"Using Pattern C extraction (Invoice Amount - handles mixed invoice scenarios)")

        # Ensure Invoice Date is datetime
        df['Invoice Date'] = pd.to_datetime(df['Invoice Date'], errors='coerce')

        # Drop rows with no amount
        df_clean = df[df['Invoice Amount'].notna()].copy()
        print(f"  Records with amounts: {len(df_clean)}")

        # Create month column
        df_clean['Month'] = df_clean['Invoice Date'].dt.to_period('M')

        # Split into records WITH and WITHOUT invoice numbers
        df_with_inv = df_clean[df_clean['Invoice Number'].notna()].copy()
        df_without_inv = df_clean[df_clean['Invoice Number'].isna()].copy()

        print(f"  With invoice numbers: {len(df_with_inv)} records ({len(df_with_inv)/len(df_clean)*100:.1f}%)")
        print(f"  Without invoice numbers: {len(df_without_inv)} records ({len(df_without_inv)/len(df_clean)*100:.1f}%)")

        all_monthly_data = []

        # Process records WITH invoice numbers
        if len(df_with_inv) > 0:
            print(f"  Processing records with invoice numbers...")

            # Group by invoice number first
            agg_dict = {'Invoice Amount': 'sum'}
            if 'Category' in df_with_inv.columns:
                agg_dict['Category'] = lambda x: ', '.join(x.dropna().unique())

            invoice_groups = df_with_inv.groupby(['Invoice Number', 'Invoice Date', 'Vendor', 'Month']).agg(agg_dict).reset_index()

            if 'Category' not in invoice_groups.columns:
                invoice_groups['Category'] = 'Service'

            # Then group by month and vendor
            agg_monthly = {
                'Invoice Number': lambda x: ', '.join(x.astype(str)),
                'Invoice Date': 'first',
                'Invoice Amount': 'sum',
                'Category': lambda x: ', '.join(x.unique())
            }

            monthly_with_inv = invoice_groups.groupby(['Month', 'Vendor']).agg(agg_monthly).reset_index()
            all_monthly_data.append(monthly_with_inv)
            print(f"    Extracted {len(monthly_with_inv)} month-vendor combinations")

        # Process records WITHOUT invoice numbers (municipal charges, etc.)
        if len(df_without_inv) > 0:
            print(f"  Processing records without invoice numbers...")

            agg_no_inv = {
                'Invoice Date': 'first',
                'Invoice Amount': 'sum'
            }
            if 'Category' in df_without_inv.columns:
                agg_no_inv['Category'] = lambda x: ', '.join(x.dropna().unique())

            monthly_no_inv = df_without_inv.groupby(['Month', 'Vendor']).agg(agg_no_inv).reset_index()

            if 'Category' not in monthly_no_inv.columns:
                monthly_no_inv['Category'] = 'Service'

            # Create synthetic invoice numbers
            monthly_no_inv['Invoice Number'] = monthly_no_inv.apply(
                lambda row: f"MONTHLY-{row['Vendor'].replace(' ', '-')}-{row['Month']}",
                axis=1
            )

            all_monthly_data.append(monthly_no_inv)
            print(f"    Extracted {len(monthly_no_inv)} month-vendor combinations")

        # Combine both groups
        if len(all_monthly_data) == 0:
            raise ValueError("No data extracted - check amount field")

        monthly_df = pd.concat(all_monthly_data, ignore_index=True)

        # Combine all vendors within each month into single row
        print(f"  Aggregating all vendors by month...")

        agg_by_month = {
            'Invoice Number': lambda x: ', '.join(sorted(set(x.astype(str)))),
            'Invoice Date': 'first',
            'Vendor': lambda x: ', '.join(sorted(set(x))),
            'Invoice Amount': 'sum',
            'Category': lambda x: ', '.join(sorted(set(x)))
        }

        monthly_df = monthly_df.groupby('Month').agg(agg_by_month).reset_index()

        # Rename columns
        monthly_df = monthly_df.rename(columns={'Invoice Amount': 'Amount'})
        monthly_df['Month'] = monthly_df['Month'].astype(str)

        # Sort by date
        monthly_df = monthly_df.sort_values('Invoice Date')

        total_extracted = monthly_df['Amount'].sum()
        print(f"  Months extracted: {len(monthly_df)}")
        print(f"  Total amount: ${total_extracted:,.2f}")

        return monthly_df

    def _standardize_vendor_names(self, df, property_name):
        """Apply vendor name standardization mapping"""
        if property_name not in self.vendor_mapping:
            return df

        mapping = self.vendor_mapping[property_name]

        def standardize(vendor_str):
            if pd.isna(vendor_str):
                return vendor_str

            # Handle multiple vendors (comma-separated)
            vendors = [v.strip() for v in str(vendor_str).split(',')]
            standardized = [mapping.get(v, v) for v in vendors]
            return ', '.join(standardized)

        df['Vendor'] = df['Vendor'].apply(standardize)

        print(f"  Vendor names standardized using mapping")
        return df

    def _calculate_cost_per_door(self, df, units):
        """Calculate cost per door for each month"""
        df['Cost_Per_Door'] = df['Amount'] / units
        print(f"  Cost per door calculated ({units} units)")
        return df

    def _add_ytd_totals(self, df):
        """Add year-to-date running totals"""
        # Ensure sorted by date
        df = df.sort_values('Invoice Date')

        # Calculate cumulative sum
        df['YTD_Total'] = df['Amount'].cumsum()

        # Calculate YTD average cost per door
        df['Months_Elapsed'] = range(1, len(df) + 1)
        df['YTD_Avg_CPD'] = df['YTD_Total'] / df['Months_Elapsed'] / df['Cost_Per_Door'].iloc[0] * df['Cost_Per_Door'].iloc[0]

        # Drop temp column
        df = df.drop('Months_Elapsed', axis=1)

        print(f"  YTD totals calculated")
        return df

    def _detect_anomalies(self, df, property_name):
        """Detect and flag cost anomalies"""
        df['Notes'] = ''

        # Calculate month-over-month percentage change
        df['MoM_Change'] = df['Amount'].pct_change() * 100

        for idx in df.index[1:]:  # Skip first month
            notes = []

            # Flag significant increases
            if df.loc[idx, 'MoM_Change'] > 20:
                notes.append(f"Cost increased {df.loc[idx, 'MoM_Change']:.1f}% from prior month")

            # Flag significant decreases
            elif df.loc[idx, 'MoM_Change'] < -20:
                notes.append(f"Cost decreased {abs(df.loc[idx, 'MoM_Change']):.1f}% from prior month")

            # Check for specific keywords in category
            if 'overage' in str(df.loc[idx, 'Category']).lower():
                notes.append("Overage charges present")

            if 'payment' in str(df.loc[idx, 'Category']).lower() or df.loc[idx, 'Amount'] < 0:
                notes.append("Payment or credit applied")

            df.loc[idx, 'Notes'] = '; '.join(notes) if notes else ''

        # Drop temp column
        df = df.drop('MoM_Change', axis=1)

        anomaly_count = (df['Notes'] != '').sum()
        if anomaly_count > 0:
            print(f"  [NOTE] {anomaly_count} anomalies detected and flagged")

        return df

    def _validate_extraction(self, monthly_df, raw_df, prop_config):
        """
        Validate extracted data against master file
        CRITICAL: Totals must match within $1.00
        """
        validation = {
            'property': prop_config['property_type'],
            'status': 'PENDING',
            'checks': {}
        }

        # Check 1: Total spend match
        extracted_total = monthly_df['Amount'].sum()
        expected_total = prop_config['total_spend']
        difference = abs(extracted_total - expected_total)

        validation['checks']['total_spend'] = {
            'extracted': float(extracted_total),
            'expected': float(expected_total),
            'difference': float(difference),
            'tolerance': 1.00,
            'passed': bool(difference <= 1.00)
        }

        # Check 2: Month count
        extracted_months = len(monthly_df)
        expected_months = prop_config['date_range']['months_covered']

        validation['checks']['month_count'] = {
            'extracted': int(extracted_months),
            'expected': int(expected_months),
            'passed': bool(extracted_months == expected_months)
        }

        # Check 3: Date range
        min_date = monthly_df['Invoice Date'].min()
        max_date = monthly_df['Invoice Date'].max()
        expected_start = pd.to_datetime(prop_config['date_range']['start'])
        expected_end = pd.to_datetime(prop_config['date_range']['end'])

        validation['checks']['date_range'] = {
            'extracted_start': min_date.strftime('%Y-%m'),
            'extracted_end': max_date.strftime('%Y-%m'),
            'expected_start': expected_start.strftime('%Y-%m'),
            'expected_end': expected_end.strftime('%Y-%m'),
            'passed': bool(min_date.strftime('%Y-%m') == expected_start.strftime('%Y-%m') and
                          max_date.strftime('%Y-%m') == expected_end.strftime('%Y-%m'))
        }

        # Overall status
        all_passed = all(check.get('passed', False) for check in validation['checks'].values())
        validation['status'] = 'PASSED' if all_passed else 'FAILED'

        # Print validation summary
        print(f"\n  VALIDATION RESULTS:")
        print(f"    Total Spend: ${extracted_total:,.2f} vs ${expected_total:,.2f} (diff: ${difference:.2f}) - {'[OK]' if validation['checks']['total_spend']['passed'] else '[FAIL]'}")
        print(f"    Month Count: {extracted_months} vs {expected_months} - {'[OK]' if validation['checks']['month_count']['passed'] else '[FAIL]'}")
        print(f"    Date Range: {min_date.strftime('%Y-%m')} to {max_date.strftime('%Y-%m')} - {'[OK]' if validation['checks']['date_range']['passed'] else '[FAIL]'}")

        if validation['status'] == 'FAILED':
            print(f"    [WARNING] Validation failed - review extraction logic")

        return validation

    def save_extraction(self, monthly_df, validation_result, property_name, output_dir):
        """Save extracted data and validation report"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save monthly data to CSV
        csv_path = output_dir / f'{property_name.replace(" ", "_")}_expense_data.csv'
        monthly_df.to_csv(csv_path, index=False)
        print(f"\n[OK] Data saved to: {csv_path}")

        # Save validation report to JSON
        json_path = output_dir / f'{property_name.replace(" ", "_")}_validation.json'
        validation_result['extraction_date'] = datetime.now().isoformat()
        validation_result['property_name'] = property_name
        validation_result['record_count'] = len(monthly_df)

        with open(json_path, 'w') as f:
            json.dump(validation_result, f, indent=2)
        print(f"[OK] Validation saved to: {json_path}")

        return csv_path, json_path


def main():
    """Extract monthly expenses for specified property"""
    import sys

    base_dir = Path(r'C:\Users\Richard\Downloads\Orion Data Part 2')
    master_file = base_dir / 'Portfolio_Reports' / 'MASTER_Portfolio_Complete_Data.xlsx'
    config_file = base_dir / 'Code' / 'property_config.json'
    vendor_mapping = base_dir / 'Code' / 'vendor_name_mapping.json'

    # Get property name from command line argument
    if len(sys.argv) < 2:
        property_name = 'Springs at Alta Mesa'  # Default for backward compatibility
        print(f"[NOTE] No property specified, using default: {property_name}")
    else:
        property_name = sys.argv[1]

    output_dir = base_dir / 'Properties' / property_name.replace(' ', '_')

    # Initialize extractor
    extractor = ExpenseExtractor(master_file, config_file, vendor_mapping)

    # Extract specified property
    monthly_df, validation = extractor.extract_property(property_name)

    # Save results
    extractor.save_extraction(monthly_df, validation, property_name, output_dir)

    # Display sample
    print(f"\n{'='*70}")
    print("SAMPLE OUTPUT (First 5 months):")
    print(f"{'='*70}")
    print(monthly_df.head().to_string())

    return 0 if validation['status'] == 'PASSED' else 1


if __name__ == "__main__":
    exit(main())
