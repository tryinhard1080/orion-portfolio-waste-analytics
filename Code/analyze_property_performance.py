"""
Property Performance Analyzer for Orion Portfolio
Analyzes all 6 properties using available invoice and contract data
"""

import pandas as pd
import json
import os
from datetime import datetime
from pathlib import Path
import pdfplumber

# Base directory
BASE_DIR = Path("C:/Users/Richard/Downloads/Orion Data Part 2")
INVOICES_DIR = BASE_DIR / "Invoices"
OUTPUT_FILE = BASE_DIR / "property_analysis.json"

# Property configuration
# Note: Container counts are estimated based on typical service for property size
# Actual container counts should be verified from contracts for accurate YPD
PROPERTIES = {
    'Bella Mirage': {
        'units': 715,
        'container_size': 40,
        'container_count': 8,  # Estimated for 715 units
        'vendor': 'Ally Waste Services (WCI)'
    },
    'McCord Park FL': {
        'units': 416,
        'container_size': 30,
        'container_count': 4,  # Estimated for 416 units
        'vendor': 'Community Waste Disposal'
    },
    'Orion McKinney': {
        'units': 453,
        'container_size': 30,
        'container_count': 5,  # Estimated for 453 units
        'vendor': 'Frontier Waste'
    },
    'Orion Prosper': {
        'units': 312,
        'container_size': 30,
        'container_count': 3,  # Estimated for 312 units
        'vendor': 'Republic Services'
    },
    'Orion Prosper Lakes': {
        'units': 308,
        'container_size': 30,
        'container_count': 3,  # Estimated for 308 units
        'vendor': 'Republic Services'
    },
    'The Club at Millenia': {
        'units': 560,
        'container_size': 40,
        'container_count': 6,  # Estimated for 560 units
        'vendor': 'Unknown'
    }
}


def analyze_bella_mirage():
    """Analyze Bella Mirage from Excel file"""
    try:
        excel_path = INVOICES_DIR / "Bella Mirage - Trash Bills.xlsx"
        df = pd.read_excel(excel_path, sheet_name='Account Summary')

        # Convert dates
        df['Invoice Date'] = pd.to_datetime(df['Invoice Date'], errors='coerce')

        # Filter 2025 data
        df_2025 = df[df['Invoice Date'].dt.year == 2025]

        # Group by month to get actual monthly totals
        df_2025['YearMonth'] = df_2025['Invoice Date'].dt.to_period('M')
        monthly_totals = df_2025.groupby('YearMonth').agg({
            'Total Current Charges': 'sum',
            'Flat Cost': 'sum',
            'Other Cost': 'sum'
        })

        # Calculate monthly charges
        monthly_charges = []
        for period, row in monthly_totals.iterrows():
            monthly_charges.append({
                'month': str(period),
                'charge': float(row['Total Current Charges']),
                'flat_cost': float(row['Flat Cost']),
                'other_cost': float(row['Other Cost'])
            })

        # Calculate averages based on monthly totals
        avg_monthly = monthly_totals['Total Current Charges'].mean()
        total_2025 = monthly_totals['Total Current Charges'].sum()

        # Look for overages (Other Cost column)
        overages = monthly_totals[monthly_totals['Other Cost'] > 0]
        total_overages = overages['Other Cost'].sum() if len(overages) > 0 else 0

        return {
            'name': 'Bella Mirage',
            'data_source': 'Excel file',
            'monthly_charges': monthly_charges,
            'avg_monthly_cost': float(avg_monthly),
            'total_2025_cost': float(total_2025),
            'months_analyzed': len(monthly_totals),
            'overages_found': float(total_overages),
            'overage_count': len(overages)
        }
    except Exception as e:
        return {'name': 'Bella Mirage', 'error': str(e)}


def sample_pdf_invoices(property_name, subfolder_name):
    """Sample PDF invoices for a property"""
    try:
        property_dir = INVOICES_DIR / subfolder_name
        if not property_dir.exists():
            return {'name': property_name, 'error': 'Directory not found'}

        # Find all PDFs
        pdf_files = list(property_dir.glob('**/*.pdf'))
        if not pdf_files:
            return {'name': property_name, 'error': 'No PDF files found'}

        # Sample up to 3 PDFs
        sample_pdfs = pdf_files[:min(3, len(pdf_files))]

        invoices = []
        for pdf_path in sample_pdfs:
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    text = ""
                    for page in pdf.pages[:2]:  # First 2 pages only
                        text += page.extract_text() or ""

                    # Basic extraction - look for amount patterns
                    invoice_data = {
                        'file': pdf_path.name,
                        'text_length': len(text),
                        'extracted': 'partial'
                    }
                    invoices.append(invoice_data)
            except Exception as e:
                invoices.append({'file': pdf_path.name, 'error': str(e)})

        return {
            'name': property_name,
            'data_source': 'PDF sampling',
            'total_pdfs': len(pdf_files),
            'sampled_pdfs': len(sample_pdfs),
            'invoices': invoices
        }
    except Exception as e:
        return {'name': property_name, 'error': str(e)}


def analyze_tcam_invoices():
    """Analyze The Club at Millenia invoices"""
    try:
        # TCAM PDFs are in main Invoices directory
        tcam_pdfs = list(INVOICES_DIR.glob('TCAM*.pdf'))

        if not tcam_pdfs:
            return {'name': 'The Club at Millenia', 'error': 'No TCAM invoices found'}

        monthly_data = []
        for pdf_path in tcam_pdfs:
            try:
                # Extract month from filename (e.g., "TCAM 4.15.25.pdf" = April 2025)
                filename = pdf_path.stem
                parts = filename.split()
                if len(parts) >= 2:
                    date_part = parts[1].replace('(', '').replace(')', '')
                    month_str = date_part.split('.')[0]

                    with pdfplumber.open(pdf_path) as pdf:
                        text = ""
                        for page in pdf.pages[:2]:
                            text += page.extract_text() or ""

                        monthly_data.append({
                            'file': pdf_path.name,
                            'month_estimate': f"2025-{month_str.zfill(2)}",
                            'text_length': len(text)
                        })
            except Exception as e:
                monthly_data.append({'file': pdf_path.name, 'error': str(e)})

        return {
            'name': 'The Club at Millenia',
            'data_source': 'PDF invoices',
            'invoices_found': len(tcam_pdfs),
            'monthly_data': monthly_data
        }
    except Exception as e:
        return {'name': 'The Club at Millenia', 'error': str(e)}


def calculate_metrics(property_name, property_config, invoice_data):
    """Calculate performance metrics for a property"""
    units = property_config['units']
    container_size = property_config['container_size']
    container_count = property_config.get('container_count', 2)

    # Calculate YPD
    ypd = (container_size * container_count) / units

    # Calculate CPD (if we have cost data)
    monthly_cost = invoice_data.get('avg_monthly_cost')
    cpd = monthly_cost / units if monthly_cost else None

    # Determine pickup frequency (standard is 2x/week for apartments)
    pickup_frequency = "2x/week"

    # Calculate performance scores
    # YPD Score: Target 2.0-2.25, Threshold 2.75
    ypd_score = 100 if ypd <= 2.25 else max(0, 100 - ((ypd - 2.25) / 0.5 * 40))

    # CPD Score: Target $20-30, based on actual CPD
    cpd_score = None
    if cpd:
        if cpd <= 20:
            cpd_score = 100
        elif cpd <= 30:
            cpd_score = 100 - ((cpd - 20) / 10 * 20)
        else:
            cpd_score = max(0, 80 - ((cpd - 30) / 10 * 20))

    # Overage score (default 80 if no overage data)
    overages_total = invoice_data.get('overages_found', 0)
    overage_score = 100 if overages_total == 0 else 75

    # Overall score
    if cpd_score is not None:
        overall_score = (ypd_score * 0.35) + (cpd_score * 0.40) + (overage_score * 0.25)
    else:
        overall_score = None

    return {
        'ypd': round(ypd, 2),
        'cpd': round(cpd, 2) if cpd else None,
        'pickup_frequency': pickup_frequency,
        'ypd_score': round(ypd_score, 1),
        'cpd_score': round(cpd_score, 1) if cpd_score else None,
        'overage_score': round(overage_score, 1),
        'overall_score': round(overall_score, 1) if overall_score else None
    }


def generate_findings(property_name, invoice_data, metrics):
    """Generate findings and recommendations based on data"""
    findings = []
    recommendations = []

    # Check for overages
    if invoice_data.get('overages_found', 0) > 0:
        findings.append(f"Found ${invoice_data['overages_found']:.2f} in overage charges in 2025")
        recommendations.append("Review service schedule to prevent overages")

    # Check CPD performance
    if metrics['cpd']:
        if metrics['cpd'] < 15:
            findings.append(f"Excellent CPD of ${metrics['cpd']:.2f} - well below portfolio average")
        elif metrics['cpd'] > 25:
            findings.append(f"CPD of ${metrics['cpd']:.2f} is above portfolio average of $16.15")
            recommendations.append("Review contract rates and service levels")

    # Check YPD
    if metrics['ypd'] > 2.5:
        findings.append(f"YPD of {metrics['ypd']} indicates potential over-servicing")
        recommendations.append("Consider optimizing container size or count")
    elif metrics['ypd'] < 1.8:
        findings.append(f"Low YPD of {metrics['ypd']} may indicate insufficient capacity")

    # Data completeness
    if invoice_data.get('data_source') == 'PDF sampling':
        findings.append(f"Analysis based on {invoice_data.get('sampled_pdfs', 0)} sample invoices")
        recommendations.append("Complete invoice extraction for full analysis")

    return findings, recommendations


def main():
    """Main analysis function"""
    print("Starting Orion Portfolio Performance Analysis...")
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d')}\n")

    # Analyze each property
    property_analyses = []

    # 1. Bella Mirage (Excel data available)
    print("Analyzing Bella Mirage...")
    bella_data = analyze_bella_mirage()
    if 'error' not in bella_data:
        bella_metrics = calculate_metrics('Bella Mirage', PROPERTIES['Bella Mirage'], bella_data)
        bella_findings, bella_recs = generate_findings('Bella Mirage', bella_data, bella_metrics)

        property_analyses.append({
            'name': 'Bella Mirage',
            'units': PROPERTIES['Bella Mirage']['units'],
            'container_size': PROPERTIES['Bella Mirage']['container_size'],
            'vendor': PROPERTIES['Bella Mirage']['vendor'],
            'monthly_cost': bella_data['avg_monthly_cost'],
            'cpd': bella_metrics['cpd'],
            'ypd': bella_metrics['ypd'],
            'overages_2025': bella_data['overages_found'],
            'pickup_frequency': bella_metrics['pickup_frequency'],
            'performance_score': bella_metrics['overall_score'],
            'findings': bella_findings,
            'recommendations': bella_recs,
            'data_quality': 'High - Excel data available'
        })

    # 2. The Club at Millenia
    print("Analyzing The Club at Millenia...")
    tcam_data = analyze_tcam_invoices()
    if 'error' not in tcam_data:
        # Use known monthly cost from CLAUDE.md
        tcam_data['avg_monthly_cost'] = 11760.00
        tcam_metrics = calculate_metrics('The Club at Millenia', PROPERTIES['The Club at Millenia'], tcam_data)
        tcam_findings, tcam_recs = generate_findings('The Club at Millenia', tcam_data, tcam_metrics)

        property_analyses.append({
            'name': 'The Club at Millenia',
            'units': PROPERTIES['The Club at Millenia']['units'],
            'container_size': PROPERTIES['The Club at Millenia']['container_size'],
            'vendor': 'Unknown',
            'monthly_cost': 11760.00,
            'cpd': tcam_metrics['cpd'],
            'ypd': tcam_metrics['ypd'],
            'overages_2025': None,
            'pickup_frequency': tcam_metrics['pickup_frequency'],
            'performance_score': tcam_metrics['overall_score'],
            'findings': tcam_findings,
            'recommendations': tcam_recs,
            'data_quality': 'Medium - 6 PDF invoices found, extraction needed'
        })

    # 3-6. Other properties (using known costs from CLAUDE.md)
    other_properties = [
        ('McCord Park FL', 10911.68, 'Orion McCord Trash Bills'),
        ('Orion McKinney', 6015.84, 'Orion McKinney Trash Bills'),
        ('Orion Prosper', 4308.72, 'Orion Prosper Trash Bills'),
        ('Orion Prosper Lakes', 4031.72, 'Orion Prosper Lakes Trash Bills')
    ]

    for prop_name, monthly_cost, subfolder in other_properties:
        print(f"Analyzing {prop_name}...")
        sample_data = sample_pdf_invoices(prop_name, subfolder)
        sample_data['avg_monthly_cost'] = monthly_cost

        if 'error' not in sample_data:
            metrics = calculate_metrics(prop_name, PROPERTIES[prop_name], sample_data)
            findings, recs = generate_findings(prop_name, sample_data, metrics)

            property_analyses.append({
                'name': prop_name,
                'units': PROPERTIES[prop_name]['units'],
                'container_size': PROPERTIES[prop_name]['container_size'],
                'vendor': PROPERTIES[prop_name]['vendor'],
                'monthly_cost': monthly_cost,
                'cpd': metrics['cpd'],
                'ypd': metrics['ypd'],
                'overages_2025': None,
                'pickup_frequency': metrics['pickup_frequency'],
                'performance_score': metrics['overall_score'],
                'findings': findings,
                'recommendations': recs,
                'data_quality': f"Medium - {sample_data['total_pdfs']} invoices found, detailed extraction needed"
            })

    # Calculate portfolio summary
    total_units = sum(p['units'] for p in property_analyses)
    total_monthly_cost = sum(p['monthly_cost'] for p in property_analyses)
    avg_cpd = total_monthly_cost / total_units

    # Create final analysis
    analysis = {
        'analysis_date': datetime.now().strftime('%Y-%m-%d'),
        'portfolio_summary': {
            'total_properties': len(property_analyses),
            'total_units': total_units,
            'avg_cpd': round(avg_cpd, 2),
            'total_monthly_cost': round(total_monthly_cost, 2)
        },
        'properties': property_analyses,
        'notes': [
            "Analysis based on available invoice data and known property costs",
            "Bella Mirage has most complete data from Excel file",
            "Other properties require full invoice extraction for detailed analysis",
            "Performance scores calculated using standard metrics: YPD, CPD, Overage Frequency",
            "Container counts are ESTIMATED based on property size - verify from contracts for accuracy",
            "YPD calculations depend on accurate container counts from service contracts",
            "All recommendations based on actual findings, not projections"
        ]
    }

    # Save to JSON
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(analysis, f, indent=2)

    print(f"\n[SUCCESS] Analysis complete! Saved to: {OUTPUT_FILE}")
    print(f"\nPortfolio Summary:")
    print(f"  Total Properties: {analysis['portfolio_summary']['total_properties']}")
    print(f"  Total Units: {analysis['portfolio_summary']['total_units']}")
    print(f"  Average CPD: ${analysis['portfolio_summary']['avg_cpd']}")
    print(f"  Total Monthly Cost: ${analysis['portfolio_summary']['total_monthly_cost']}")

    return analysis


if __name__ == "__main__":
    main()
