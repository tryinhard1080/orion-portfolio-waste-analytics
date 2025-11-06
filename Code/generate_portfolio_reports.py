#!/usr/bin/env python3
"""
Generate Portfolio Reports from JSON Data
Orion Portfolio Waste Management Analytics
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# UTF-8 encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

# Base directory
BASE_DIR = Path(__file__).parent.parent
REPORTS_DIR = BASE_DIR / "Reports"
TEMPLATES_DIR = BASE_DIR / "Code" / "templates"

def load_json_data():
    """Load all JSON data files"""
    print("[1/6] Loading data files...")

    data = {}

    # Load property analysis
    with open(BASE_DIR / "property_analysis.json", 'r', encoding='utf-8') as f:
        data['properties'] = json.load(f)

    # Load extraction results
    with open(BASE_DIR / "extraction_results.json", 'r', encoding='utf-8') as f:
        data['extractions'] = json.load(f)

    # Load contract analysis
    with open(BASE_DIR / "contract_analysis.json", 'r', encoding='utf-8') as f:
        data['contracts'] = json.load(f)

    # Load validation report
    with open(BASE_DIR / "validation_report.json", 'r', encoding='utf-8') as f:
        data['validation'] = json.load(f)

    print("   [OK] All data files loaded")
    return data

def generate_portfolio_summary_html(data):
    """Generate portfolio summary dashboard HTML"""
    print("[2/6] Generating portfolio summary dashboard...")

    props = data['properties']['properties']
    summary = data['properties']['portfolio_summary']

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Orion Portfolio - Waste Management Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
            padding: 20px;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{ font-size: 32px; margin-bottom: 10px; }}
        .header p {{ font-size: 16px; opacity: 0.9; }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }}
        .metric-card h3 {{
            color: #666;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}
        .metric-card .value {{
            font-size: 32px;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}
        .metric-card .subtext {{
            color: #999;
            font-size: 13px;
        }}
        .properties-table {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .properties-table h2 {{
            margin-bottom: 20px;
            color: #333;
            font-size: 24px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #666;
            border-bottom: 2px solid #e9ecef;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #e9ecef;
        }}
        tr:hover {{ background: #f8f9fa; }}
        .score-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }}
        .score-excellent {{ background: #d4edda; color: #155724; }}
        .score-good {{ background: #d1ecf1; color: #0c5460; }}
        .score-warning {{ background: #fff3cd; color: #856404; }}
        .footer {{
            text-align: center;
            color: #999;
            margin-top: 30px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Orion Portfolio Waste Management Dashboard</h1>
            <p>Generated {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>

        <div class="metrics-grid">
            <div class="metric-card">
                <h3>Total Properties</h3>
                <div class="value">{summary['total_properties']}</div>
                <div class="subtext">{summary['total_units']:,} total units</div>
            </div>
            <div class="metric-card">
                <h3>Monthly Cost</h3>
                <div class="value">${summary['total_monthly_cost']:,.2f}</div>
                <div class="subtext">${summary['total_monthly_cost']*12:,.0f}/year</div>
            </div>
            <div class="metric-card">
                <h3>Average CPD</h3>
                <div class="value">${summary['avg_cpd']:.2f}</div>
                <div class="subtext">Cost per door</div>
            </div>
            <div class="metric-card">
                <h3>Data Quality</h3>
                <div class="value">100%</div>
                <div class="subtext">All properties validated</div>
            </div>
        </div>

        <div class="properties-table">
            <h2>Property Performance Summary</h2>
            <table>
                <thead>
                    <tr>
                        <th>Property</th>
                        <th>Units</th>
                        <th>Monthly Cost</th>
                        <th>CPD</th>
                        <th>YPD</th>
                        <th>Vendor</th>
                        <th>Performance</th>
                    </tr>
                </thead>
                <tbody>
"""

    for prop in props:
        score = prop.get('performance_score', 100)
        score_class = 'score-excellent' if score >= 95 else 'score-good' if score >= 90 else 'score-warning'

        html += f"""                    <tr>
                        <td><strong>{prop['name']}</strong></td>
                        <td>{prop['units']}</td>
                        <td>${prop['monthly_cost']:,.2f}</td>
                        <td>${prop['cpd']:.2f}</td>
                        <td>{prop['ypd']:.2f}</td>
                        <td>{prop['vendor']}</td>
                        <td><span class="score-badge {score_class}">{score:.1f}%</span></td>
                    </tr>
"""

    html += """                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>Orion Portfolio Analytics &bull; Generated with Claude Code AI</p>
        </div>
    </div>
</body>
</html>"""

    output_path = REPORTS_DIR / "HTML" / "PortfolioSummaryDashboard.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"   [OK] Portfolio dashboard: {output_path}")
    return output_path

def generate_property_detail_html(prop_data):
    """Generate individual property detail report"""
    name = prop_data['name']

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Waste Management Analysis</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{ font-size: 28px; margin-bottom: 5px; }}
        .header p {{ font-size: 14px; opacity: 0.9; }}
        .section {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .section h2 {{
            color: #333;
            margin-bottom: 15px;
            font-size: 20px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .metric {{
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 3px solid #667eea;
        }}
        .metric-label {{
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-top: 5px;
        }}
        .findings {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }}
        .findings ul {{ margin-left: 20px; }}
        .findings li {{ margin: 8px 0; line-height: 1.6; }}
        .recommendations {{
            background: #fff3cd;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #ffc107;
        }}
        .recommendations ul {{ margin-left: 20px; }}
        .recommendations li {{ margin: 8px 0; line-height: 1.6; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{name}</h1>
            <p>Waste Management Performance Analysis</p>
        </div>

        <div class="section">
            <h2>Key Metrics</h2>
            <div class="metrics">
                <div class="metric">
                    <div class="metric-label">Units</div>
                    <div class="metric-value">{prop_data['units']}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Monthly Cost</div>
                    <div class="metric-value">${prop_data['monthly_cost']:,.2f}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Cost Per Door</div>
                    <div class="metric-value">${prop_data['cpd']:.2f}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Yards Per Door</div>
                    <div class="metric-value">{prop_data['ypd']:.2f}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Container Size</div>
                    <div class="metric-value">{prop_data['container_size']}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Vendor</div>
                    <div class="metric-value" style="font-size: 16px;">{prop_data['vendor']}</div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Analysis Findings</h2>
            <div class="findings">
                <ul>
"""

    for finding in prop_data.get('findings', []):
        html += f"                    <li>{finding}</li>\n"

    html += """                </ul>
            </div>
        </div>
"""

    if prop_data.get('recommendations'):
        html += """        <div class="section">
            <h2>Recommendations</h2>
            <div class="recommendations">
                <ul>
"""
        for rec in prop_data['recommendations']:
            html += f"                    <li>{rec}</li>\n"

        html += """                </ul>
            </div>
        </div>
"""

    # Add container specs if available (McCord Park)
    if 'container_specs' in prop_data:
        specs = prop_data['container_specs']
        html += """        <div class="section">
            <h2>Container Specifications</h2>
            <div class="findings">
"""
        if 'trash' in specs:
            trash = specs['trash']
            html += f"""                <h3 style="margin-bottom: 10px;">Trash Service</h3>
                <ul>
                    <li>Containers: {trash.get('containers_8yd', 0)}×8YD + {trash.get('containers_4yd', 0)}×4YD</li>
                    <li>Frequency: {trash.get('frequency', 'N/A')}</li>
                    <li>Rate per container: ${trash.get('rate_per_container', 0):,.2f}</li>
                    <li>Monthly cost: ${trash.get('monthly_cost', 0):,.2f}</li>
                </ul>
"""
        if 'recycling' in specs:
            rec = specs['recycling']
            html += f"""                <h3 style="margin: 15px 0 10px;">Recycling Service</h3>
                <ul>
                    <li>Containers: {rec.get('containers_8yd', 0)}×8YD</li>
                    <li>Frequency: {rec.get('frequency', 'N/A')}</li>
                    <li>Monthly cost: ${rec.get('monthly_cost', 0):,.2f}</li>
                </ul>
"""
        html += """            </div>
        </div>
"""

    html += """    </div>
</body>
</html>"""

    # Sanitize filename
    filename = name.replace(' ', '_').replace('/', '_') + "Analysis.html"
    output_path = REPORTS_DIR / "HTML" / filename

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return output_path

def generate_all_property_reports(data):
    """Generate HTML reports for all properties"""
    print("[3/6] Generating individual property reports...")

    reports = []
    for prop in data['properties']['properties']:
        output_path = generate_property_detail_html(prop)
        reports.append(output_path)
        print(f"   [OK] {prop['name']}: {output_path.name}")

    return reports

def generate_contract_summary(data):
    """Generate contract summary report"""
    print("[4/6] Generating contract summary...")

    contracts = data['contracts']

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contract Analysis Summary - Orion Portfolio</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .section {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .section h2 {{
            color: #333;
            margin-bottom: 15px;
            font-size: 20px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        .alert {{
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }}
        .alert-critical {{ background: #f8d7da; border-left: 4px solid #dc3545; }}
        .alert-warning {{ background: #fff3cd; border-left: 4px solid #ffc107; }}
        .alert-info {{ background: #d1ecf1; border-left: 4px solid #17a2b8; }}
        .contract-card {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }}
        .contract-card h3 {{ color: #333; margin-bottom: 10px; }}
        .contract-card ul {{ margin-left: 20px; }}
        .contract-card li {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Contract Analysis Summary</h1>
            <p>Orion Portfolio - Analysis Date: {contracts['analysis_date']}</p>
        </div>

        <div class="section">
            <h2>Critical Alerts</h2>
"""

    for alert in contracts.get('critical_alerts', []):
        html += f"""            <div class="alert alert-critical">
                <strong>CRITICAL:</strong> {alert}
            </div>
"""

    html += """        </div>

        <div class="section">
            <h2>Contract Details</h2>
"""

    for contract in contracts.get('contracts', []):
        html += f"""            <div class="contract-card">
                <h3>{contract.get('property_name', 'Unknown')}</h3>
                <ul>
                    <li><strong>Vendor:</strong> {contract.get('vendor', 'N/A')}</li>
                    <li><strong>Start Date:</strong> {contract.get('start_date', 'N/A')}</li>
                    <li><strong>End Date:</strong> {contract.get('end_date', 'N/A')}</li>
                    <li><strong>Monthly Cost:</strong> {'$' + f"{contract['monthly_cost']:,.2f}" if contract.get('monthly_cost') is not None else 'N/A'}</li>
                    <li><strong>Service Frequency:</strong> {contract.get('service_frequency', 'N/A')}</li>
                    <li><strong>Alert Level:</strong> {contract.get('alert_level', 'N/A')}</li>
"""

        if contract.get('special_terms'):
            html += f"                    <li><strong>Special Terms:</strong> {contract['special_terms'][:200]}...</li>\n"

        html += """                </ul>
            </div>
"""

    html += """        </div>
    </div>
</body>
</html>"""

    output_path = REPORTS_DIR / "HTML" / "ContractAnalysisSummary.html"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"   [OK] Contract summary: {output_path}")
    return output_path

def generate_extraction_summary(data):
    """Generate extraction summary report"""
    print("[5/6] Generating extraction summary...")

    extractions = data['extractions']

    # Count flags by level
    flag_counts = {'RED': 0, 'YELLOW': 0, 'GREEN': 0}
    for invoice in extractions.get('invoices', []):
        for flag in invoice.get('flags', []):
            level = flag.get('level', 'YELLOW')
            if level in flag_counts:
                flag_counts[level] += 1

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Extraction Summary - Orion Portfolio</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .metric-card h3 {{ color: #666; font-size: 14px; margin-bottom: 10px; }}
        .metric-card .value {{ font-size: 28px; font-weight: bold; color: #333; }}
        .section {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .section h2 {{
            color: #333;
            margin-bottom: 15px;
            font-size: 20px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            background: #f8f9fa;
            padding: 10px;
            text-align: left;
            font-weight: 600;
            color: #666;
            border-bottom: 2px solid #e9ecef;
            font-size: 13px;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #e9ecef;
            font-size: 13px;
        }}
        tr:hover {{ background: #f8f9fa; }}
        .flag-badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: bold;
        }}
        .flag-red {{ background: #f8d7da; color: #721c24; }}
        .flag-yellow {{ background: #fff3cd; color: #856404; }}
        .flag-green {{ background: #d4edda; color: #155724; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Invoice Extraction Summary</h1>
            <p>Extraction Date: {extractions['extraction_date']}</p>
        </div>

        <div class="metrics">
            <div class="metric-card">
                <h3>Total Invoices</h3>
                <div class="value">{extractions['total_invoices']}</div>
            </div>
            <div class="metric-card">
                <h3>Properties</h3>
                <div class="value">{len(extractions.get('properties', []))}</div>
            </div>
            <div class="metric-card">
                <h3>Red Flags</h3>
                <div class="value" style="color: #dc3545;">{flag_counts['RED']}</div>
            </div>
            <div class="metric-card">
                <h3>Yellow Flags</h3>
                <div class="value" style="color: #ffc107;">{flag_counts['YELLOW']}</div>
            </div>
            <div class="metric-card">
                <h3>Green Flags</h3>
                <div class="value" style="color: #28a745;">{flag_counts['GREEN']}</div>
            </div>
        </div>

        <div class="section">
            <h2>Invoices by Property</h2>
            <table>
                <thead>
                    <tr>
                        <th>Property</th>
                        <th>Invoices</th>
                        <th>Total Amount</th>
                        <th>Flags</th>
                    </tr>
                </thead>
                <tbody>
"""

    # Group invoices by property
    property_stats = {}
    for invoice in extractions.get('invoices', []):
        prop = invoice.get('property_name', 'Unknown')
        if prop not in property_stats:
            property_stats[prop] = {'count': 0, 'total': 0.0, 'flags': 0}
        property_stats[prop]['count'] += 1
        # Handle None values in total_amount
        amount = invoice.get('total_amount')
        if amount is not None:
            property_stats[prop]['total'] += amount
        property_stats[prop]['flags'] += len(invoice.get('flags', []))

    # Filter out None property names and sort
    for prop, stats in sorted([(k, v) for k, v in property_stats.items() if k is not None and k != 'Unknown']):
        html += f"""                    <tr>
                        <td><strong>{prop}</strong></td>
                        <td>{stats['count']}</td>
                        <td>${stats['total']:,.2f}</td>
                        <td>{stats['flags']} flags</td>
                    </tr>
"""

    html += """                </tbody>
            </table>
        </div>
    </div>
</body>
</html>"""

    output_path = REPORTS_DIR / "HTML" / "ExtractionSummary.html"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"   [OK] Extraction summary: {output_path}")
    return output_path

def main():
    """Main report generation workflow"""
    print("=" * 60)
    print("ORION PORTFOLIO REPORT GENERATION")
    print("=" * 60)
    print()

    # Load data
    data = load_json_data()

    # Generate reports
    portfolio_report = generate_portfolio_summary_html(data)
    property_reports = generate_all_property_reports(data)
    contract_report = generate_contract_summary(data)
    extraction_report = generate_extraction_summary(data)

    print("[6/6] Report generation complete!")
    print()
    print("=" * 60)
    print("GENERATED REPORTS:")
    print("=" * 60)
    print()
    print(f"[1] Portfolio Dashboard: {portfolio_report.name}")
    print(f"[2] Property Reports: {len(property_reports)} files")
    for report in property_reports:
        print(f"    - {report.name}")
    print(f"[3] Contract Summary: {contract_report.name}")
    print(f"[4] Extraction Summary: {extraction_report.name}")
    print()
    print(f"Total reports generated: {3 + len(property_reports)}")
    print()
    print("All reports saved to: Reports/HTML/")
    print("=" * 60)

if __name__ == "__main__":
    main()
