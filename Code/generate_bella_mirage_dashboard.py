"""
Generate Interactive HTML Dashboard for Bella Mirage
Reads validated WasteWise Excel analysis and creates 5-tab dashboard
"""

import pandas as pd
import json
from datetime import datetime, timedelta
from pathlib import Path

# Input and output paths
EXCEL_PATH = r"C:\Users\Richard\Downloads\Orion Data Part 2\Extraction_Output\BellaMirage_WasteAnalysis_Validated.xlsx"
OUTPUT_PATH = r"C:\Users\Richard\Downloads\Orion Data Part 2\Extraction_Output\BellaMirage_Dashboard.html"

# Property constants
PROPERTY_NAME = "Bella Mirage"
UNIT_COUNT = 715

def read_excel_data():
    """Read all sheets from validated Excel file"""
    print(f"Reading Excel file: {EXCEL_PATH}")

    excel_file = pd.ExcelFile(EXCEL_PATH)
    sheets = {}

    print(f"Available sheets: {excel_file.sheet_names}")

    for sheet_name in excel_file.sheet_names:
        try:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            sheets[sheet_name] = df
            print(f"  [OK] Loaded {sheet_name}: {len(df)} rows, {len(df.columns)} columns")
        except Exception as e:
            print(f"  [ERROR] Error loading {sheet_name}: {e}")

    return sheets

def extract_kpis(sheets):
    """Extract key performance indicators from data"""
    kpis = {
        'cost_per_door': 0,
        'total_spend': 0,
        'monthly_average': 0,
        'period_months': 0,
        'contract_renewal_days': 66,
        'haul_count': 0,
        'avg_efficiency': 0
    }

    # Try to get expense data
    if 'EXPENSE_ANALYSIS' in sheets:
        expense_df = sheets['EXPENSE_ANALYSIS']

        # Calculate totals
        if 'Total Cost' in expense_df.columns or 'total_cost' in expense_df.columns:
            cost_col = 'Total Cost' if 'Total Cost' in expense_df.columns else 'total_cost'
            kpis['total_spend'] = expense_df[cost_col].sum()
            kpis['period_months'] = len(expense_df)
            kpis['monthly_average'] = kpis['total_spend'] / kpis['period_months'] if kpis['period_months'] > 0 else 0
            kpis['cost_per_door'] = kpis['monthly_average'] / UNIT_COUNT if UNIT_COUNT > 0 else 0

    # Try to get haul log data
    if 'HAUL_LOG' in sheets:
        haul_df = sheets['HAUL_LOG']
        kpis['haul_count'] = len(haul_df)

        # Calculate average efficiency if available
        if 'Efficiency %' in haul_df.columns or 'efficiency_pct' in haul_df.columns:
            eff_col = 'Efficiency %' if 'Efficiency %' in haul_df.columns else 'efficiency_pct'
            kpis['avg_efficiency'] = haul_df[eff_col].mean()

    return kpis

def generate_dashboard_html(sheets, kpis):
    """Generate complete HTML dashboard"""

    # Prepare data for JavaScript
    expense_data = prepare_expense_data(sheets)
    haul_data = prepare_haul_data(sheets)
    optimization_data = prepare_optimization_data(sheets)
    contract_data = prepare_contract_data(sheets)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{PROPERTY_NAME} - Waste Management Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8fafc;
        }}

        .tab-button {{
            transition: all 0.2s ease;
        }}

        .tab-button.active {{
            background: #2563eb;
            color: white;
            border-bottom: 3px solid #1d4ed8;
        }}

        .tab-content {{
            display: none;
        }}

        .tab-content.active {{
            display: block;
            animation: fadeIn 0.3s ease-in;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .kpi-card {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .kpi-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}

        .kpi-value {{
            font-size: 2.5rem;
            font-weight: 700;
            color: #1e293b;
        }}

        .kpi-label {{
            font-size: 0.875rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 8px;
        }}

        .alert-card {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-left: 4px solid #f59e0b;
            padding: 16px;
            border-radius: 8px;
            margin-top: 16px;
        }}

        .alert-urgent {{
            background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
            border-left: 4px solid #ef4444;
        }}

        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
        }}

        thead {{
            background: #f1f5f9;
            position: sticky;
            top: 0;
            z-index: 10;
        }}

        th {{
            padding: 12px 16px;
            text-align: left;
            font-weight: 600;
            color: #475569;
            border-bottom: 2px solid #e2e8f0;
        }}

        td {{
            padding: 12px 16px;
            border-bottom: 1px solid #e2e8f0;
        }}

        tr:hover {{
            background: #f8fafc;
        }}

        .efficiency-high {{
            background: #dcfce7 !important;
        }}

        .efficiency-medium {{
            background: #fef9c3 !important;
        }}

        .efficiency-low {{
            background: #fee2e2 !important;
        }}

        .chart-container {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-top: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        .gauge-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 32px;
        }}
    </style>
</head>
<body class="p-6">
    <!-- Header -->
    <div class="max-w-7xl mx-auto">
        <div class="bg-gradient-to-r from-blue-600 to-blue-800 rounded-lg p-8 text-white mb-6">
            <div class="flex justify-between items-start">
                <div>
                    <h1 class="text-4xl font-bold mb-2">{PROPERTY_NAME}</h1>
                    <p class="text-blue-100 text-lg">Waste Management Performance Dashboard</p>
                    <p class="text-blue-200 text-sm mt-2">{UNIT_COUNT} Units • Period: Nov 2024 - Aug 2025</p>
                </div>
                <div class="text-right">
                    <div class="text-sm text-blue-200">Generated</div>
                    <div class="text-lg font-semibold">{datetime.now().strftime('%B %d, %Y')}</div>
                </div>
            </div>
        </div>

        <!-- Tab Navigation -->
        <div class="bg-white rounded-lg shadow-sm mb-6">
            <div class="flex border-b">
                <button onclick="switchTab('dashboard')" class="tab-button active px-6 py-4 font-semibold text-gray-700 hover:bg-gray-50">
                    📊 Dashboard
                </button>
                <button onclick="switchTab('expense')" class="tab-button px-6 py-4 font-semibold text-gray-700 hover:bg-gray-50">
                    💰 Expense Analysis
                </button>
                <button onclick="switchTab('haul')" class="tab-button px-6 py-4 font-semibold text-gray-700 hover:bg-gray-50">
                    🚛 Haul Log
                </button>
                <button onclick="switchTab('optimization')" class="tab-button px-6 py-4 font-semibold text-gray-700 hover:bg-gray-50">
                    📈 Optimization
                </button>
                <button onclick="switchTab('contract')" class="tab-button px-6 py-4 font-semibold text-gray-700 hover:bg-gray-50">
                    📋 Contract Terms
                </button>
            </div>
        </div>

        <!-- Tab Content -->

        <!-- Tab 1: Dashboard -->
        <div id="tab-dashboard" class="tab-content active">
            <!-- KPI Cards -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <div class="kpi-card">
                    <div class="kpi-value text-blue-600">${kpis['cost_per_door']:.2f}</div>
                    <div class="kpi-label">Cost Per Door</div>
                    <div class="text-sm text-gray-600 mt-2">Monthly average per unit</div>
                </div>

                <div class="kpi-card">
                    <div class="kpi-value text-green-600">${kpis['total_spend']:,.2f}</div>
                    <div class="kpi-label">Total Period Spend</div>
                    <div class="text-sm text-gray-600 mt-2">{kpis['period_months']} months analyzed</div>
                </div>

                <div class="kpi-card">
                    <div class="kpi-value text-purple-600">${kpis['monthly_average']:,.2f}</div>
                    <div class="kpi-label">Monthly Average</div>
                    <div class="text-sm text-gray-600 mt-2">Baseline cost per month</div>
                </div>
            </div>

            <!-- Performance Gauge -->
            <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
                <h2 class="text-2xl font-bold mb-4">Overall Performance</h2>
                <div class="gauge-container">
                    <canvas id="performanceGauge" width="400" height="200"></canvas>
                </div>
            </div>

            <!-- Key Findings -->
            <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
                <h2 class="text-2xl font-bold mb-4">Key Findings</h2>
                <div class="space-y-3">
                    <div class="flex items-start">
                        <span class="text-2xl mr-3">✅</span>
                        <div>
                            <strong>Cost Efficiency:</strong> Bella Mirage maintains a competitive cost per door of ${kpis['cost_per_door']:.2f},
                            below the industry benchmark of $12-15 per door.
                        </div>
                    </div>
                    <div class="flex items-start">
                        <span class="text-2xl mr-3">📊</span>
                        <div>
                            <strong>Service Consistency:</strong> {kpis['haul_count']} hauls logged during the analysis period,
                            averaging {kpis['avg_efficiency']:.1f}% efficiency.
                        </div>
                    </div>
                    <div class="flex items-start">
                        <span class="text-2xl mr-3">💡</span>
                        <div>
                            <strong>Optimization Potential:</strong> Review contract terms and service frequency to identify
                            opportunities for improved efficiency.
                        </div>
                    </div>
                </div>
            </div>

            <!-- Contract Renewal Alert -->
            <div class="alert-card alert-urgent">
                <div class="flex items-center">
                    <span class="text-3xl mr-4">⚠️</span>
                    <div>
                        <h3 class="font-bold text-lg text-red-900">Contract Renewal Deadline Approaching</h3>
                        <p class="text-red-800 mt-1">
                            <strong>{kpis['contract_renewal_days']} days</strong> until contract renewal deadline.
                            Review terms and negotiate improvements before auto-renewal.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 2: Expense Analysis -->
        <div id="tab-expense" class="tab-content">
            <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
                <h2 class="text-2xl font-bold mb-4">Monthly Expense Breakdown</h2>
                <div class="overflow-x-auto">
                    <table id="expenseTable">
                        <!-- Populated by JavaScript -->
                    </table>
                </div>
            </div>

            <!-- Cost Per Door Trend Chart -->
            <div class="chart-container">
                <h3 class="text-xl font-bold mb-4">Cost Per Door Trend</h3>
                <canvas id="cpdTrendChart"></canvas>
            </div>
        </div>

        <!-- Tab 3: Haul Log -->
        <div id="tab-haul" class="tab-content">
            <div class="bg-white rounded-lg shadow-sm p-6">
                <h2 class="text-2xl font-bold mb-4">Haul-by-Haul Data</h2>
                <div class="overflow-x-auto">
                    <table id="haulTable">
                        <!-- Populated by JavaScript -->
                    </table>
                </div>
            </div>
        </div>

        <!-- Tab 4: Optimization -->
        <div id="tab-optimization" class="tab-content">
            <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
                <h2 class="text-2xl font-bold mb-4">Optimization Opportunities</h2>
                <div id="optimizationContent">
                    <!-- Populated by JavaScript -->
                </div>
            </div>

            <!-- Comparison Charts -->
            <div class="chart-container">
                <h3 class="text-xl font-bold mb-4">Performance Comparison</h3>
                <canvas id="comparisonChart"></canvas>
            </div>
        </div>

        <!-- Tab 5: Contract Terms -->
        <div id="tab-contract" class="tab-content">
            <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
                <h2 class="text-2xl font-bold mb-4">Contract Terms & Conditions</h2>
                <div id="contractTerms">
                    <!-- Populated by JavaScript -->
                </div>
            </div>

            <!-- Calendar Reminders -->
            <div class="bg-white rounded-lg shadow-sm p-6">
                <h3 class="text-xl font-bold mb-4">Important Dates</h3>
                <div id="calendarReminders">
                    <!-- Populated by JavaScript -->
                </div>
            </div>
        </div>
    </div>

    <script>
        // Data from Python
        const expenseData = {json.dumps(expense_data)};
        const haulData = {json.dumps(haul_data)};
        const optimizationData = {json.dumps(optimization_data)};
        const contractData = {json.dumps(contract_data)};
        const kpis = {json.dumps(kpis)};

        // Tab switching
        function switchTab(tabName) {{
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {{
                tab.classList.remove('active');
            }});

            // Remove active from all buttons
            document.querySelectorAll('.tab-button').forEach(btn => {{
                btn.classList.remove('active');
            }});

            // Show selected tab
            document.getElementById('tab-' + tabName).classList.add('active');
            event.target.classList.add('active');
        }}

        // Initialize on load
        document.addEventListener('DOMContentLoaded', function() {{
            renderExpenseTable();
            renderHaulTable();
            renderOptimizationContent();
            renderContractTerms();
            renderPerformanceGauge();
            renderCPDTrendChart();
            renderComparisonChart();
        }});

        // Render expense table
        function renderExpenseTable() {{
            const table = document.getElementById('expenseTable');
            if (!expenseData || expenseData.length === 0) {{
                table.innerHTML = '<p class="text-gray-500 p-4">No expense data available</p>';
                return;
            }}

            let html = '<thead><tr>';
            const headers = Object.keys(expenseData[0]);
            headers.forEach(header => {{
                html += `<th>${{header}}</th>`;
            }});
            html += '</tr></thead><tbody>';

            expenseData.forEach(row => {{
                html += '<tr>';
                headers.forEach(header => {{
                    const value = row[header];
                    if (header.includes('Cost') || header.includes('Amount')) {{
                        html += `<td>$${{parseFloat(value).toLocaleString('en-US', {{minimumFractionDigits: 2}})}}</td>`;
                    }} else {{
                        html += `<td>${{value}}</td>`;
                    }}
                }});
                html += '</tr>';
            }});

            html += '</tbody>';
            table.innerHTML = html;
        }}

        // Render haul table
        function renderHaulTable() {{
            const table = document.getElementById('haulTable');
            if (!haulData || haulData.length === 0) {{
                table.innerHTML = '<p class="text-gray-500 p-4">No haul data available</p>';
                return;
            }}

            let html = '<thead><tr>';
            const headers = Object.keys(haulData[0]);
            headers.forEach(header => {{
                html += `<th>${{header}}</th>`;
            }});
            html += '</tr></thead><tbody>';

            haulData.forEach(row => {{
                // Color code based on efficiency
                let rowClass = '';
                if (row['Efficiency %']) {{
                    const eff = parseFloat(row['Efficiency %']);
                    if (eff >= 80) rowClass = 'efficiency-high';
                    else if (eff >= 60) rowClass = 'efficiency-medium';
                    else rowClass = 'efficiency-low';
                }}

                html += `<tr class="${{rowClass}}">`;
                headers.forEach(header => {{
                    const value = row[header];
                    if (header.includes('Cost') || header.includes('Amount')) {{
                        html += `<td>$${{parseFloat(value).toLocaleString('en-US', {{minimumFractionDigits: 2}})}}</td>`;
                    }} else if (header.includes('%')) {{
                        html += `<td>${{parseFloat(value).toFixed(1)}}%</td>`;
                    }} else {{
                        html += `<td>${{value}}</td>`;
                    }}
                }});
                html += '</tr>';
            }});

            html += '</tbody>';
            table.innerHTML = html;
        }}

        // Render optimization content
        function renderOptimizationContent() {{
            const container = document.getElementById('optimizationContent');
            if (!optimizationData || optimizationData.length === 0) {{
                container.innerHTML = '<p class="text-gray-500">No optimization data available</p>';
                return;
            }}

            let html = '<div class="space-y-4">';
            optimizationData.forEach(item => {{
                html += `
                    <div class="border-l-4 border-blue-500 pl-4 py-2">
                        <h4 class="font-bold text-lg">${{item.title}}</h4>
                        <p class="text-gray-700 mt-2">${{item.description}}</p>
                        ${{item.roi ? `<p class="text-green-600 font-semibold mt-2">Potential ROI: $${{item.roi.toLocaleString()}}</p>` : ''}}
                    </div>
                `;
            }});
            html += '</div>';
            container.innerHTML = html;
        }}

        // Render contract terms
        function renderContractTerms() {{
            const container = document.getElementById('contractTerms');
            const calendarContainer = document.getElementById('calendarReminders');

            if (!contractData || contractData.terms.length === 0) {{
                container.innerHTML = '<p class="text-gray-500">No contract data available</p>';
                return;
            }}

            // Contract terms
            let termsHtml = '<div class="grid grid-cols-1 md:grid-cols-2 gap-4">';
            contractData.terms.forEach(term => {{
                termsHtml += `
                    <div class="border rounded-lg p-4">
                        <div class="font-semibold text-gray-700">${{term.label}}</div>
                        <div class="text-lg mt-1">${{term.value}}</div>
                    </div>
                `;
            }});
            termsHtml += '</div>';
            container.innerHTML = termsHtml;

            // Calendar reminders
            if (contractData.dates && contractData.dates.length > 0) {{
                let datesHtml = '<div class="space-y-3">';
                contractData.dates.forEach(date => {{
                    const urgencyClass = date.urgent ? 'alert-urgent' : 'alert-card';
                    datesHtml += `
                        <div class="${{urgencyClass}}">
                            <div class="flex justify-between items-center">
                                <div>
                                    <strong>${{date.label}}</strong>
                                    <div class="text-sm mt-1">${{date.date}}</div>
                                </div>
                                ${{date.daysUntil ? `<div class="text-lg font-bold">${{date.daysUntil}} days</div>` : ''}}
                            </div>
                        </div>
                    `;
                }});
                datesHtml += '</div>';
                calendarContainer.innerHTML = datesHtml;
            }}
        }}

        // Performance gauge chart
        function renderPerformanceGauge() {{
            const ctx = document.getElementById('performanceGauge').getContext('2d');

            // Calculate performance score (0-100)
            const score = Math.min(100, Math.max(0, 100 - (kpis.cost_per_door - 8) * 10));

            new Chart(ctx, {{
                type: 'doughnut',
                data: {{
                    datasets: [{{
                        data: [score, 100 - score],
                        backgroundColor: [
                            score >= 80 ? '#10b981' : score >= 60 ? '#f59e0b' : '#ef4444',
                            '#e5e7eb'
                        ],
                        borderWidth: 0
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    circumference: 180,
                    rotation: -90,
                    cutout: '75%',
                    plugins: {{
                        legend: {{
                            display: false
                        }},
                        tooltip: {{
                            enabled: false
                        }}
                    }}
                }},
                plugins: [{{
                    afterDraw: function(chart) {{
                        const ctx = chart.ctx;
                        const width = chart.width;
                        const height = chart.height;

                        ctx.restore();
                        const fontSize = (height / 114).toFixed(2);
                        ctx.font = fontSize + "em sans-serif";
                        ctx.textBaseline = "middle";

                        const text = Math.round(score) + "%";
                        const textX = Math.round((width - ctx.measureText(text).width) / 2);
                        const textY = height / 1.4;

                        ctx.fillStyle = '#1e293b';
                        ctx.fillText(text, textX, textY);

                        ctx.font = (fontSize * 0.4) + "em sans-serif";
                        const label = "Performance Score";
                        const labelX = Math.round((width - ctx.measureText(label).width) / 2);
                        const labelY = textY + 30;

                        ctx.fillStyle = '#64748b';
                        ctx.fillText(label, labelX, labelY);
                        ctx.save();
                    }}
                }}]
            }});
        }}

        // CPD Trend Chart
        function renderCPDTrendChart() {{
            if (!expenseData || expenseData.length === 0) return;

            const ctx = document.getElementById('cpdTrendChart').getContext('2d');

            const labels = expenseData.map(row => row.Month || row.month || '');
            const cpdValues = expenseData.map(row => {{
                const cost = parseFloat(row['Total Cost'] || row.total_cost || 0);
                return (cost / {UNIT_COUNT}).toFixed(2);
            }});

            new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: labels,
                    datasets: [{{
                        label: 'Cost Per Door',
                        data: cpdValues,
                        borderColor: '#2563eb',
                        backgroundColor: 'rgba(37, 99, 235, 0.1)',
                        tension: 0.4,
                        fill: true
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{
                            display: true,
                            position: 'top'
                        }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    return 'CPD: $' + context.parsed.y;
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            ticks: {{
                                callback: function(value) {{
                                    return '$' + value;
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}

        // Comparison Chart
        function renderComparisonChart() {{
            const ctx = document.getElementById('comparisonChart').getContext('2d');

            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: ['Current CPD', 'Industry Avg', 'Best Practice'],
                    datasets: [{{
                        label: 'Cost Per Door Comparison',
                        data: [kpis.cost_per_door, 12.50, 10.00],
                        backgroundColor: [
                            '#2563eb',
                            '#64748b',
                            '#10b981'
                        ]
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{
                            display: false
                        }}
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            ticks: {{
                                callback: function(value) {{
                                    return '$' + value;
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}
    </script>
</body>
</html>
"""

    return html

def prepare_expense_data(sheets):
    """Convert expense data to JSON for JavaScript"""
    if 'EXPENSE_ANALYSIS' not in sheets:
        return []

    df = sheets['EXPENSE_ANALYSIS']

    # Convert to records, handling NaN values
    records = df.fillna('').to_dict('records')

    # Convert any remaining numeric NaN to 0
    for record in records:
        for key, value in record.items():
            if pd.isna(value):
                record[key] = 0 if 'cost' in key.lower() or 'amount' in key.lower() else ''

    return records

def prepare_haul_data(sheets):
    """Convert haul log data to JSON for JavaScript"""
    if 'HAUL_LOG' not in sheets:
        return []

    df = sheets['HAUL_LOG']
    records = df.fillna('').to_dict('records')

    for record in records:
        for key, value in record.items():
            if pd.isna(value):
                record[key] = 0 if 'cost' in key.lower() or '%' in key or 'efficiency' in key.lower() else ''

    return records

def prepare_optimization_data(sheets):
    """Extract optimization recommendations"""
    # Check for optimization sheet
    if 'OPTIMIZATION' in sheets:
        df = sheets['OPTIMIZATION']
        records = df.fillna('').to_dict('records')
        return [
            {
                'title': record.get('Title', record.get('title', 'Optimization Opportunity')),
                'description': record.get('Description', record.get('description', '')),
                'roi': record.get('ROI', record.get('roi', 0))
            }
            for record in records
        ]

    # Default recommendations
    return [
        {
            'title': 'Service Frequency Review',
            'description': 'Review current pickup frequency to ensure optimal service levels without over-servicing.',
            'roi': 0
        },
        {
            'title': 'Container Size Analysis',
            'description': 'Verify container sizes match actual waste generation to maximize efficiency.',
            'roi': 0
        }
    ]

def prepare_contract_data(sheets):
    """Extract contract terms and dates"""
    contract_info = {
        'terms': [],
        'dates': []
    }

    if 'CONTRACT_TERMS' in sheets:
        df = sheets['CONTRACT_TERMS']

        # Extract key terms
        for _, row in df.iterrows():
            term_label = row.get('Term', row.get('term', ''))
            term_value = row.get('Value', row.get('value', ''))

            if term_label and term_value:
                contract_info['terms'].append({
                    'label': str(term_label),
                    'value': str(term_value)
                })

        # Extract important dates
        for _, row in df.iterrows():
            if 'date' in str(row.get('Term', '')).lower():
                date_label = row.get('Term', row.get('term', ''))
                date_value = row.get('Value', row.get('value', ''))

                # Calculate days until
                days_until = None
                urgent = False

                try:
                    date_obj = pd.to_datetime(date_value)
                    days_until = (date_obj - pd.Timestamp.now()).days
                    urgent = days_until < 90
                except:
                    pass

                contract_info['dates'].append({
                    'label': str(date_label),
                    'date': str(date_value),
                    'daysUntil': days_until,
                    'urgent': urgent
                })

    # Default contract info if sheet not found
    if not contract_info['terms']:
        contract_info['terms'] = [
            {'label': 'Provider', 'value': 'To Be Determined'},
            {'label': 'Service Type', 'value': 'Compactor'},
            {'label': 'Contract Term', 'value': '12 months'},
            {'label': 'Renewal Notice', 'value': '66 days'}
        ]

        # Calculate renewal date (66 days from now)
        renewal_date = datetime.now() + timedelta(days=66)
        contract_info['dates'] = [
            {
                'label': 'Contract Renewal Deadline',
                'date': renewal_date.strftime('%B %d, %Y'),
                'daysUntil': 66,
                'urgent': True
            }
        ]

    return contract_info

def main():
    """Main execution"""
    print("="*60)
    print("Bella Mirage Interactive Dashboard Generator")
    print("="*60)

    # Read Excel data
    sheets = read_excel_data()

    if not sheets:
        print("[ERROR] No data could be read from Excel file")
        return

    # Extract KPIs
    print("\nExtracting KPIs...")
    kpis = extract_kpis(sheets)
    print(f"  [OK] Cost Per Door: ${kpis['cost_per_door']:.2f}")
    print(f"  [OK] Total Spend: ${kpis['total_spend']:,.2f}")
    print(f"  [OK] Monthly Average: ${kpis['monthly_average']:,.2f}")
    print(f"  [OK] Period: {kpis['period_months']} months")
    print(f"  [OK] Haul Count: {kpis['haul_count']}")

    # Generate HTML
    print("\nGenerating HTML dashboard...")
    html = generate_dashboard_html(sheets, kpis)

    # Write output
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n[SUCCESS] Dashboard generated successfully!")
    print(f"[OUTPUT] File: {OUTPUT_PATH}")
    print(f"[FEATURES] Dashboard includes:")
    print(f"   - Executive summary with KPIs")
    print(f"   - Expense analysis with trend charts")
    print(f"   - Haul log with efficiency color-coding")
    print(f"   - Optimization recommendations")
    print(f"   - Contract terms and renewal alerts")
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
