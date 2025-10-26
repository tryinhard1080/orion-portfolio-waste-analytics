"""
Orion Portfolio - HTML Report Generator (Google Sheets Data Source)
Version: 2.1

Generates HTML reports from Google Sheets data (our single source of truth).
Uses correct language patterns: data-focused analysis, no crisis language, no projections.

Key Principles:
- Factual presentation of actual costs from invoices
- Benchmark variances stated objectively
- Opportunity identification (not prescriptive solutions)
- Professional, neutral documentation tone
- All dollar amounts from verified invoice data (NO projections)
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import json

# Import Jinja2 for HTML templating
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Composio Google Sheets integration
from dotenv import load_dotenv

load_dotenv()

# Spreadsheet ID from our created sheet
SPREADSHEET_ID = "1oy-F3p_CPpJaGGmGUMcjQMubRIRi7p4IID7mfpNLZJQ"


class GoogleSheetsReportGenerator:
    """Report generator using Google Sheets as data source"""

    def __init__(self, spreadsheet_id: str = SPREADSHEET_ID):
        self.spreadsheet_id = spreadsheet_id

        # Set up Jinja2 template environment
        template_dir = Path(__file__).parent / "templates"
        template_dir.mkdir(exist_ok=True)

        self.jinja_env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )

        # Add custom filters for formatting
        self.jinja_env.filters['currency'] = self._format_currency
        self.jinja_env.filters['percent'] = self._format_percent
        self.jinja_env.filters['tier_badge'] = self._get_tier_badge

    def _format_currency(self, value):
        """Format number as currency"""
        if value is None or value == "":
            return "N/A"
        try:
            # Remove any existing currency symbols or commas
            if isinstance(value, str):
                value = value.replace('$', '').replace(',', '').strip()
            return f"${float(value):,.2f}"
        except:
            return str(value)

    def _format_percent(self, value):
        """Format number as percentage"""
        if value is None or value == "":
            return "N/A"
        try:
            # If already in percentage form (e.g., "94%"), extract number
            if isinstance(value, str) and '%' in value:
                value = float(value.replace('%', '').strip()) / 100
            return f"{float(value) * 100:.0f}%"
        except:
            return str(value)

    def _get_tier_badge(self, score):
        """Get performance tier classification from score"""
        if score is None or score == "":
            return {"color": "gray", "label": "N/A", "range": "No data"}

        try:
            score = float(score)
        except:
            return {"color": "gray", "label": "N/A", "range": "No data"}

        if score >= 80:
            return {"color": "green", "label": "Good", "range": "80-100 points"}
        elif score >= 60:
            return {"color": "yellow", "label": "Average", "range": "60-79 points"}
        else:
            return {"color": "red", "label": "Poor", "range": "0-59 points"}

    def _get_benchmark_status(self, metric_type: str, value) -> Dict:
        """Get benchmark comparison status for a metric"""
        if value is None or value == "":
            return {"status": "unknown", "message": "No data"}

        try:
            # Handle percentage strings like "94%"
            if isinstance(value, str):
                if '%' in value:
                    value = float(value.replace('%', '').strip()) / 100
                else:
                    value = float(value.replace('$', '').replace(',', '').strip())
            else:
                value = float(value)
        except:
            return {"status": "unknown", "message": "Invalid data"}

        # Define benchmarks (from CLAUDE.md lines 353-356)
        benchmarks = {
            'ypd': {'target': (2.0, 2.25), 'threshold': 2.75},
            'cpd': {'target': (20, 30), 'threshold': 30},
            'overage': {'target': 0.15, 'threshold': 0.50}  # as decimal
        }

        bench = benchmarks.get(metric_type.lower())
        if not bench:
            return {"status": "unknown", "message": ""}

        if metric_type.lower() == 'ypd':
            if value <= bench['target'][1]:
                return {"status": "good", "message": f"Within target range {bench['target'][0]}-{bench['target'][1]}"}
            elif value <= bench['threshold']:
                return {"status": "warning", "message": f"Above target, below threshold ({bench['threshold']})"}
            else:
                return {"status": "poor", "message": f"Exceeds threshold ({bench['threshold']})"}

        elif metric_type.lower() == 'cpd':
            if bench['target'][0] <= value <= bench['target'][1]:
                return {"status": "good", "message": f"Within target range ${bench['target'][0]}-${bench['target'][1]}"}
            elif value < bench['target'][0]:
                return {"status": "good", "message": f"Below target range (excellent value)"}
            elif value <= bench['threshold']:
                return {"status": "warning", "message": f"Above target, near threshold"}
            else:
                return {"status": "poor", "message": f"Exceeds threshold (${bench['threshold']})"}

        elif metric_type.lower() == 'overage':
            if value <= bench['target']:
                return {"status": "good", "message": f"At or below target ({bench['target']*100:.0f}%)"}
            elif value <= bench['threshold']:
                return {"status": "warning", "message": f"Above target, below threshold ({bench['threshold']*100:.0f}%)"}
            else:
                return {"status": "poor", "message": f"Exceeds threshold ({bench['threshold']*100:.0f}%)"}

        return {"status": "unknown", "message": ""}

    def get_sheet_data_via_composio(self, sheet_name: str) -> List[List[str]]:
        """Get data from a specific sheet using Composio tools"""
        # This will be called using the Composio tools from the main function
        # For now, return empty - will be populated by tool calls
        return []

    def parse_property_data(self, property_details_rows: List[List], performance_metrics_rows: List[List]) -> List[Dict]:
        """Parse property data from Google Sheets rows"""
        properties = []

        # Property Details sheet has headers in row 2 (index 1)
        # Data starts at row 3 (index 2)
        if len(property_details_rows) < 3:
            return properties

        # Performance Metrics sheet also has headers in row 2
        # Data starts at row 3 (index 2)
        if len(performance_metrics_rows) < 3:
            return properties

        # Parse each property (rows 3-8 in sheets, indices 2-7 in arrays)
        for i in range(2, min(len(property_details_rows), len(performance_metrics_rows))):
            details_row = property_details_rows[i]
            metrics_row = performance_metrics_rows[i]

            # Skip empty rows or summary rows (TOTALS, PORTFOLIO AVERAGES, etc.)
            if not details_row or len(details_row) == 0 or not details_row[0]:
                continue
            if details_row[0].upper() in ['TOTALS', 'PORTFOLIO AVERAGES', 'AVERAGES']:
                continue

            try:
                property_data = {
                    # From Property Details sheet (columns A-J)
                    'property_name': details_row[0] if len(details_row) > 0 else '',
                    'unit_count': int(details_row[1]) if len(details_row) > 1 and details_row[1] else 0,
                    'service_type': details_row[2] if len(details_row) > 2 else '',
                    'avg_cpd': float(details_row[3]) if len(details_row) > 3 and details_row[3] else 0,
                    'monthly_yardage': float(details_row[4]) if len(details_row) > 4 and details_row[4] else 0,
                    'avg_ypd': float(details_row[5]) if len(details_row) > 5 and details_row[5] else 0,
                    'avg_overage_cpd': float(details_row[6]) if len(details_row) > 6 and details_row[6] else 0,
                    'city': details_row[7] if len(details_row) > 7 else '',
                    'monthly_cost': float(str(details_row[8]).replace('$', '').replace(',', '')) if len(details_row) > 8 and details_row[8] else 0,
                    'service_details': details_row[9] if len(details_row) > 9 else '',

                    # From Performance Metrics sheet (columns A-J)
                    'property_score': float(metrics_row[1]) if len(metrics_row) > 1 and metrics_row[1] else 0,
                    'performance_tier': metrics_row[2] if len(metrics_row) > 2 else 'N/A',
                    'avg_ypd_score': float(metrics_row[3]) if len(metrics_row) > 3 and metrics_row[3] else 0,
                    'avg_cpd_score': float(metrics_row[4]) if len(metrics_row) > 4 and metrics_row[4] else 0,
                    'overage_score': float(metrics_row[5]) if len(metrics_row) > 5 and metrics_row[5] else 0,
                    'overage_frequency': metrics_row[6] if len(metrics_row) > 6 else '0%',
                    'ypd_status_text': metrics_row[7] if len(metrics_row) > 7 else '',
                    'cpd_status_text': metrics_row[8] if len(metrics_row) > 8 else '',
                    'notes': metrics_row[9] if len(metrics_row) > 9 else '',
                }

                properties.append(property_data)
            except Exception as e:
                print(f"[WARNING] Failed to parse property row {i}: {e}")
                continue

        return properties

    def parse_portfolio_summary(self, portfolio_rows: List[List]) -> Dict:
        """Parse portfolio summary data from Google Sheets"""
        summary = {
            'total_properties': 0,
            'total_units': 0,
            'total_monthly_cost': 0,
            'avg_cpd': 0,
            'good_properties': 0,
            'average_properties': 0,
            'poor_properties': 0,
            'avg_score': 0
        }

        try:
            # Portfolio Summary sheet structure:
            # Row 5: Total Properties | value
            # Row 6: Total Units | value
            # Row 7: Total Monthly Cost | value
            # Row 8: Average Cost Per Door | value
            # Row 11: Good Tier | value
            # Row 12: Average Tier | value
            # Row 13: Poor Tier | value

            if len(portfolio_rows) >= 5:
                summary['total_properties'] = int(portfolio_rows[4][1]) if len(portfolio_rows[4]) > 1 else 0
            if len(portfolio_rows) >= 6:
                summary['total_units'] = int(portfolio_rows[5][1]) if len(portfolio_rows[5]) > 1 else 0
            if len(portfolio_rows) >= 7:
                cost_str = str(portfolio_rows[6][1]).replace('$', '').replace(',', '')
                summary['total_monthly_cost'] = float(cost_str) if cost_str else 0
            if len(portfolio_rows) >= 8:
                cpd_str = str(portfolio_rows[7][1]).replace('$', '').replace(',', '')
                summary['avg_cpd'] = float(cpd_str) if cpd_str else 0
            if len(portfolio_rows) >= 11:
                summary['good_properties'] = int(portfolio_rows[10][1]) if len(portfolio_rows[10]) > 1 else 0
            if len(portfolio_rows) >= 12:
                summary['average_properties'] = int(portfolio_rows[11][1]) if len(portfolio_rows[11]) > 1 else 0
            if len(portfolio_rows) >= 13:
                summary['poor_properties'] = int(portfolio_rows[12][1]) if len(portfolio_rows[12]) > 1 else 0
            if len(portfolio_rows) >= 14:
                score_str = str(portfolio_rows[13][1]).replace(',', '')
                summary['avg_score'] = float(score_str) if score_str else 0

        except Exception as e:
            print(f"[WARNING] Failed to parse portfolio summary: {e}")

        return summary

    def generate_html_portfolio_report(self, property_data: List[Dict], portfolio_summary: Dict,
                                      output_file: str = None) -> str:
        """Generate portfolio summary HTML report"""
        print("\n[INFO] Generating HTML portfolio report from Google Sheets data...")

        # Prepare template data
        # Prepare empty focus areas structure that matches template expectations
        empty_focus_areas = {
            'by_controllability': {
                'Fully Controllable': [],
                'Partially Controllable': [],
                'Contract-Dependent': [],
                'Market-Constrained': []
            },
            'by_timeline': {
                'Immediate Action': [],
                'Contract Renewal': [],
                'Long-term Strategy': [],
                'Monitor Only': []
            },
            'by_type': {
                'Cost Control': [],
                'Service Right-Sizing': [],
                'Contract Strategy': [],
                'Performance Monitoring': []
            },
            'by_priority': {
                'Critical': [],
                'High': [],
                'Medium': [],
                'Low': []
            }
        }

        template_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'portfolio': {
                'total_properties': portfolio_summary['total_properties'],
                'total_units': portfolio_summary['total_units'],
                'total_monthly_cost': portfolio_summary['total_monthly_cost'],
                'avg_cpd': portfolio_summary['avg_cpd'],
                'good_properties': portfolio_summary['good_properties'],
                'average_properties': portfolio_summary['average_properties'],
                'poor_properties': portfolio_summary['poor_properties'],
                'avg_score': portfolio_summary['avg_score']
            },
            'data_coverage': {
                'properties_with_data': portfolio_summary['total_properties'],
                'total_invoices': 'Multiple months',
                'data_coverage': '100% (all properties)'
            },
            'focus_areas_summary': {
                'total_active': 0,  # We'll add focus areas later
                'critical': 0,
                'high_priority': 0,
                'immediate_action': 0,
                'controllable': 0
            },
            'properties': property_data,
            'focus_areas': empty_focus_areas,  # Proper structure for template
            'benchmarks': {
                'ypd_target': '2.0-2.25',
                'ypd_threshold': '2.75',
                'cpd_target': '$20-30',
                'cpd_threshold': '$30',
                'overage_target': '≤15%',
                'overage_threshold': '≤50%'
            }
        }

        # Add benchmark status for each property
        for prop in template_data['properties']:
            prop['ypd_status'] = self._get_benchmark_status('ypd', prop.get('avg_ypd'))
            prop['cpd_status'] = self._get_benchmark_status('cpd', prop.get('avg_cpd'))
            prop['overage_status'] = self._get_benchmark_status('overage', prop.get('overage_frequency'))
            prop['performance_indicator'] = f"{prop.get('performance_tier', 'N/A')} tier"

        # Render template
        template = self.jinja_env.get_template('portfolio_summary.html')
        html_content = template.render(**template_data)

        # Save HTML file
        if output_file is None:
            output_file = "PortfolioSummaryDashboard.html"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"[OK] HTML report saved to: {output_file}")
        return output_file

    def generate_html_property_report(self, property_data: Dict, output_file: str = None) -> str:
        """Generate individual property HTML report"""
        property_name = property_data.get('property_name', 'Unknown')
        print(f"\n[INFO] Generating HTML report for {property_name}...")

        # Create a property object that matches template expectations
        class PropertyData:
            def __init__(self, data_dict):
                for key, value in data_dict.items():
                    setattr(self, key, value)

        property_obj = PropertyData(property_data)

        # Prepare template data
        template_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'property_name': property_name,
            'property': property_obj,
            'invoice_count': 'Multiple months',  # We'll get this from invoice sheet later
            'focus_areas': [],  # We'll add focus areas later
            'benchmarks': {
                'ypd_target': '2.0-2.25',
                'cpd_target': '$20-30',
                'overage_target': '≤15%'
            }
        }

        # Add benchmark status
        template_data['ypd_status'] = self._get_benchmark_status('ypd', property_data.get('avg_ypd'))
        template_data['cpd_status'] = self._get_benchmark_status('cpd', property_data.get('avg_cpd'))
        template_data['overage_status'] = self._get_benchmark_status('overage', property_data.get('overage_frequency'))

        # Render template
        template = self.jinja_env.get_template('property_detail.html')
        html_content = template.render(**template_data)

        # Save HTML file
        if output_file is None:
            safe_name = property_name.replace(' ', '')
            output_file = f"{safe_name}Analysis.html"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"[OK] HTML report saved to: {output_file}")
        return output_file


def main():
    """Main function - will be called with Composio tool data"""
    print("\n" + "="*80)
    print("ORION PORTFOLIO - HTML REPORT GENERATOR (GOOGLE SHEETS)")
    print("="*80)
    print(f"Version: 2.1")
    print(f"Data Source: Google Sheets (Single Source of Truth)")
    print(f"Spreadsheet ID: {SPREADSHEET_ID}")
    print("="*80)

    generator = GoogleSheetsReportGenerator(SPREADSHEET_ID)

    print("\n[INFO] Generator initialized and ready")
    print("[INFO] This script will be called from the Composio workflow")
    print("[INFO] to generate reports after fetching Google Sheets data")

    return generator


if __name__ == '__main__':
    main()
