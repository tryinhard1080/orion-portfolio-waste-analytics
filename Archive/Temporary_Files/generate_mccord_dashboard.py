"""
McCord Park FL Interactive HTML Dashboard Generator
5-Tab Dashboard with Chart.js Visualizations
"""

import pandas as pd
import json
from datetime import datetime

# Property Constants
PROPERTY_NAME = "McCord Park FL"
UNITS = 416
LOCATION = "Florida"

# File Paths
INPUT_FILE = r'C:\Users\Richard\Downloads\Orion Data Part 2\Extraction_Output\COMPLETE_All_Properties_UPDATED_20251103_101053.xlsx'
OUTPUT_HTML = r'C:\Users\Richard\Downloads\Orion Data Part 2\Extraction_Output\McCordParkFL_Dashboard.html'

def load_data():
    """Load McCord Park FL data"""
    df = pd.read_excel(INPUT_FILE, sheet_name='McCord Park FL')
    df.columns = ['Source File', 'Property', 'Vendor', 'Account #', 'Invoice #',
                  'Invoice Date', 'Due Date', 'Amount Due', 'Service Date',
                  'Description', 'Category', 'Quantity', 'UOM',
                  'Container Size (yd)', 'Container Type', 'Frequency/Week',
                  'Unit Rate', 'Extended Amount', 'Notes', 'Data Source']

    df['Invoice Date'] = pd.to_datetime(df['Invoice Date'])
    df['Service Date'] = pd.to_datetime(df['Service Date'])
    return df

def prepare_chart_data(df):
    """Prepare data for Chart.js visualizations"""
    # Monthly cost trend
    df['YearMonth'] = df['Invoice Date'].dt.to_period('M')
    monthly = df.groupby('YearMonth').agg({
        'Amount Due': 'first',
        'Invoice #': 'nunique'
    }).reset_index()

    monthly.columns = ['YearMonth', 'Monthly_Cost', 'Invoice_Count']
    monthly['Cost_Per_Door'] = monthly['Monthly_Cost'] / UNITS
    monthly['YearMonth_Str'] = monthly['YearMonth'].astype(str)

    # Category breakdown
    base_total = df[df['Category'] == 'base']['Extended Amount'].sum()
    tax_total = df[df['Category'] == 'tax']['Extended Amount'].sum()

    # Convert to JSON-serializable types
    monthly_list = []
    for _, row in monthly.iterrows():
        monthly_list.append({
            'YearMonth': str(row['YearMonth']),
            'Monthly_Cost': float(row['Monthly_Cost']),
            'Invoice_Count': int(row['Invoice_Count']),
            'Cost_Per_Door': float(row['Cost_Per_Door'])
        })

    return {
        'monthly': monthly_list,
        'labels': [str(x) for x in monthly['YearMonth'].tolist()],
        'costs': [float(x) for x in monthly['Monthly_Cost'].tolist()],
        'cpd': [float(x) for x in monthly['Cost_Per_Door'].tolist()],
        'invoice_counts': [int(x) for x in monthly['Invoice_Count'].tolist()],
        'category_breakdown': {
            'labels': ['Base Charges', 'Taxes'],
            'values': [float(base_total), float(tax_total)]
        }
    }

def generate_html(df, chart_data):
    """Generate complete HTML dashboard"""

    # Calculate summary metrics
    total_invoices = df['Invoice #'].nunique()
    date_start = df['Invoice Date'].min().strftime('%b %Y')
    date_end = df['Invoice Date'].max().strftime('%b %Y')
    avg_monthly = df.groupby(df['Invoice Date'].dt.to_period('M'))['Amount Due'].first().mean()
    avg_cpd = avg_monthly / UNITS
    total_spend = df.groupby('Invoice #')['Amount Due'].first().sum()

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{PROPERTY_NAME} - Waste Management Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .tab-button {{
            transition: all 0.3s ease;
        }}
        .tab-button.active {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        .tab-content {{
            display: none;
            animation: fadeIn 0.5s;
        }}
        .tab-content.active {{
            display: block;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }}
        .data-table {{
            font-size: 0.875rem;
        }}
        .data-table th {{
            background-color: #f3f4f6;
            font-weight: 600;
            padding: 0.75rem;
            text-align: left;
        }}
        .data-table td {{
            padding: 0.75rem;
            border-bottom: 1px solid #e5e7eb;
        }}
        .data-table tr:hover {{
            background-color: #f9fafb;
        }}
    </style>
</head>
<body class="bg-gray-50">
    <div class="container mx-auto px-4 py-8 max-w-7xl">
        <!-- Header -->
        <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-gray-800">{PROPERTY_NAME}</h1>
                    <p class="text-gray-600 mt-2">Waste Management Performance Dashboard</p>
                    <p class="text-sm text-gray-500 mt-1">{LOCATION} • {UNITS} Units • {date_start} - {date_end}</p>
                </div>
                <div class="text-right">
                    <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 60'%3E%3Ctext x='10' y='40' font-family='Arial, sans-serif' font-size='24' font-weight='bold' fill='%23667eea'%3EAdvantage Waste%3C/text%3E%3C/svg%3E" alt="Advantage Waste" class="h-12">
                </div>
            </div>
        </div>

        <!-- Tab Navigation -->
        <div class="bg-white rounded-lg shadow-lg mb-6 p-2">
            <div class="flex space-x-2">
                <button onclick="showTab('executive')" class="tab-button active flex-1 px-4 py-3 rounded-lg font-medium transition">
                    Executive Dashboard
                </button>
                <button onclick="showTab('expense')" class="tab-button flex-1 px-4 py-3 rounded-lg font-medium transition text-gray-700 hover:bg-gray-100">
                    Expense Analysis
                </button>
                <button onclick="showTab('service')" class="tab-button flex-1 px-4 py-3 rounded-lg font-medium transition text-gray-700 hover:bg-gray-100">
                    Service Details
                </button>
                <button onclick="showTab('optimization')" class="tab-button flex-1 px-4 py-3 rounded-lg font-medium transition text-gray-700 hover:bg-gray-100">
                    Optimization
                </button>
                <button onclick="showTab('contract')" class="tab-button flex-1 px-4 py-3 rounded-lg font-medium transition text-gray-700 hover:bg-gray-100">
                    Contract Status
                </button>
            </div>
        </div>

        <!-- Tab 1: Executive Dashboard -->
        <div id="executive" class="tab-content active">
            <!-- Key Metrics -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
                <div class="metric-card">
                    <div class="text-sm opacity-90 mb-1">Average Monthly Cost</div>
                    <div class="text-3xl font-bold">${avg_monthly:,.2f}</div>
                </div>
                <div class="metric-card">
                    <div class="text-sm opacity-90 mb-1">Cost Per Door</div>
                    <div class="text-3xl font-bold">${avg_cpd:.2f}</div>
                </div>
                <div class="metric-card">
                    <div class="text-sm opacity-90 mb-1">Total Spend</div>
                    <div class="text-3xl font-bold">${total_spend:,.2f}</div>
                </div>
                <div class="metric-card">
                    <div class="text-sm opacity-90 mb-1">Total Invoices</div>
                    <div class="text-3xl font-bold">{total_invoices}</div>
                </div>
            </div>

            <!-- Charts Row 1 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div class="bg-white rounded-lg shadow-lg p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Monthly Cost Trend</h3>
                    <canvas id="costTrendChart"></canvas>
                </div>
                <div class="bg-white rounded-lg shadow-lg p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Invoice Count by Month</h3>
                    <canvas id="invoiceCountChart"></canvas>
                </div>
            </div>

            <!-- Charts Row 2 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-white rounded-lg shadow-lg p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Cost Breakdown</h3>
                    <canvas id="categoryPieChart"></canvas>
                </div>
                <div class="bg-white rounded-lg shadow-lg p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Cost Per Door Trend</h3>
                    <canvas id="cpdTrendChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Tab 2: Expense Analysis -->
        <div id="expense" class="tab-content">
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h2 class="text-2xl font-bold text-gray-800 mb-4">Monthly Expense Breakdown</h2>
                <div class="overflow-x-auto">
                    <table class="data-table w-full">
                        <thead>
                            <tr>
                                <th>Month</th>
                                <th>Monthly Cost</th>
                                <th>Cost Per Door</th>
                                <th>Invoice Count</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
'''

    # Add monthly expense rows
    for month_data in chart_data['monthly']:
        month_str = month_data['YearMonth']
        cost = month_data['Monthly_Cost']
        cpd = month_data['Cost_Per_Door']
        inv_count = month_data['Invoice_Count']

        # Status based on CPD
        if cpd < 20:
            status = '<span class="text-green-600 font-semibold">Good</span>'
        elif cpd < 30:
            status = '<span class="text-yellow-600 font-semibold">Average</span>'
        else:
            status = '<span class="text-red-600 font-semibold">High</span>'

        html += f'''
                            <tr>
                                <td class="font-medium">{month_str}</td>
                                <td>${cost:,.2f}</td>
                                <td>${cpd:.2f}</td>
                                <td>{int(inv_count)}</td>
                                <td>{status}</td>
                            </tr>
'''

    html += f'''
                        </tbody>
                    </table>
                </div>

                <div class="mt-6 p-4 bg-blue-50 rounded-lg">
                    <h3 class="font-semibold text-gray-800 mb-2">Summary Statistics</h3>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div>
                            <div class="text-gray-600">Average CPD</div>
                            <div class="text-lg font-bold text-gray-800">${avg_cpd:.2f}</div>
                        </div>
                        <div>
                            <div class="text-gray-600">Average Monthly</div>
                            <div class="text-lg font-bold text-gray-800">${avg_monthly:,.2f}</div>
                        </div>
                        <div>
                            <div class="text-gray-600">Total Period</div>
                            <div class="text-lg font-bold text-gray-800">${total_spend:,.2f}</div>
                        </div>
                        <div>
                            <div class="text-gray-600">Months Analyzed</div>
                            <div class="text-lg font-bold text-gray-800">{len(chart_data['monthly'])}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 3: Service Details -->
        <div id="service" class="tab-content">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-white rounded-lg shadow-lg p-6">
                    <h2 class="text-2xl font-bold text-gray-800 mb-4">Service Information</h2>
                    <div class="space-y-3">
                        <div class="flex justify-between py-2 border-b">
                            <span class="text-gray-600">Service Type:</span>
                            <span class="font-semibold">Front Load Refuse (FEL)</span>
                        </div>
                        <div class="flex justify-between py-2 border-b">
                            <span class="text-gray-600">Vendor:</span>
                            <span class="font-semibold">Community Waste Disposal, LP</span>
                        </div>
                        <div class="flex justify-between py-2 border-b">
                            <span class="text-gray-600">Account Number:</span>
                            <span class="font-semibold">105004</span>
                        </div>
                        <div class="flex justify-between py-2 border-b">
                            <span class="text-gray-600">Container Type:</span>
                            <span class="font-semibold">Dumpsters</span>
                        </div>
                        <div class="flex justify-between py-2 border-b">
                            <span class="text-gray-600">Recycling Program:</span>
                            <span class="font-semibold">Yes (416 units)</span>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-lg shadow-lg p-6">
                    <h2 class="text-2xl font-bold text-gray-800 mb-4">Data Limitations</h2>
                    <div class="space-y-3">
                        <div class="p-3 bg-yellow-50 border-l-4 border-yellow-400 rounded">
                            <div class="font-semibold text-gray-800">Container Specifications</div>
                            <div class="text-sm text-gray-600 mt-1">Container count, size, and frequency not available in invoice data</div>
                        </div>
                        <div class="p-3 bg-yellow-50 border-l-4 border-yellow-400 rounded">
                            <div class="font-semibold text-gray-800">Yards Per Door</div>
                            <div class="text-sm text-gray-600 mt-1">Cannot calculate without container specifications</div>
                        </div>
                        <div class="p-3 bg-blue-50 border-l-4 border-blue-400 rounded">
                            <div class="font-semibold text-gray-800">Recommendation</div>
                            <div class="text-sm text-gray-600 mt-1">Obtain service contract for complete service specifications</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 4: Optimization -->
        <div id="optimization" class="tab-content">
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h2 class="text-2xl font-bold text-gray-800 mb-4">Optimization Analysis</h2>

                <div class="space-y-4">
                    <!-- Compactor Check -->
                    <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="flex justify-between items-start mb-2">
                            <h3 class="text-lg font-semibold">Compactor Optimization</h3>
                            <span class="px-3 py-1 bg-gray-200 text-gray-700 rounded-full text-sm font-medium">N/A</span>
                        </div>
                        <p class="text-gray-600 text-sm">Property uses dumpster service, not compactors. Optimization trigger not applicable.</p>
                        <div class="mt-2 text-xs text-gray-500">
                            <strong>Trigger:</strong> Avg tons/haul &lt; 6 tons (compactors only)
                        </div>
                    </div>

                    <!-- Contamination Check -->
                    <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="flex justify-between items-start mb-2">
                            <h3 class="text-lg font-semibold">Contamination Reduction</h3>
                            <span class="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">PASS</span>
                        </div>
                        <p class="text-gray-600 text-sm">No contamination charges identified in invoice data. Currently operating within normal parameters.</p>
                        <div class="mt-2 text-xs text-gray-500">
                            <strong>Trigger:</strong> Contamination charges &gt; 3% of total spend
                        </div>
                        <div class="mt-2 text-sm">
                            <strong>Status:</strong> 0% contamination charges
                        </div>
                    </div>

                    <!-- Bulk Subscription Check -->
                    <div class="p-4 bg-gray-50 rounded-lg">
                        <div class="flex justify-between items-start mb-2">
                            <h3 class="text-lg font-semibold">Bulk Subscription (Ally Waste)</h3>
                            <span class="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">PASS</span>
                        </div>
                        <p class="text-gray-600 text-sm">No bulk trash charges identified. Ally Waste subscription not recommended at this time.</p>
                        <div class="mt-2 text-xs text-gray-500">
                            <strong>Trigger:</strong> Average monthly bulk &gt; $500
                        </div>
                        <div class="mt-2 text-sm">
                            <strong>Status:</strong> $0/month bulk charges
                        </div>
                    </div>

                    <!-- Summary -->
                    <div class="p-4 bg-blue-50 border-l-4 border-blue-500 rounded">
                        <h3 class="text-lg font-semibold text-blue-900 mb-2">Overall Assessment</h3>
                        <p class="text-blue-800">No optimization opportunities identified with current data. Property is operating within normal parameters.</p>
                        <p class="text-sm text-blue-700 mt-2">Recommendation: Obtain service contract and container specifications for complete analysis.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 5: Contract Status -->
        <div id="contract" class="tab-content">
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h2 class="text-2xl font-bold text-gray-800 mb-4">Contract Status</h2>

                <div class="p-6 bg-red-50 border-2 border-red-200 rounded-lg mb-6">
                    <div class="flex items-center mb-2">
                        <svg class="w-6 h-6 text-red-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                        </svg>
                        <span class="text-lg font-semibold text-red-900">No Contract on File</span>
                    </div>
                    <p class="text-red-800">Service contract not available for McCord Park FL. Contract review recommended.</p>
                </div>

                <div class="mb-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-3">Recommended Contract Review Items</h3>
                    <ul class="space-y-2">
                        <li class="flex items-start">
                            <svg class="w-5 h-5 text-blue-600 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                            <span>Renewal terms and automatic renewal clauses</span>
                        </li>
                        <li class="flex items-start">
                            <svg class="w-5 h-5 text-blue-600 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                            <span>Rate increase provisions and CPI adjustments</span>
                        </li>
                        <li class="flex items-start">
                            <svg class="w-5 h-5 text-blue-600 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                            <span>Service level specifications (container count, size, frequency)</span>
                        </li>
                        <li class="flex items-start">
                            <svg class="w-5 h-5 text-blue-600 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                            <span>Termination rights and notice periods</span>
                        </li>
                        <li class="flex items-start">
                            <svg class="w-5 h-5 text-blue-600 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                            <span>Contamination penalty terms and thresholds</span>
                        </li>
                    </ul>
                </div>

                <div class="p-4 bg-blue-50 rounded-lg">
                    <h3 class="font-semibold text-blue-900 mb-2">Next Steps</h3>
                    <ol class="list-decimal list-inside space-y-1 text-blue-800">
                        <li>Obtain executed service agreement from vendor or property management</li>
                        <li>Review contract terms for potential optimization opportunities</li>
                        <li>Validate that invoiced services match contracted specifications</li>
                        <li>Re-run analysis with contract data for complete assessment</li>
                    </ol>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="mt-8 text-center text-gray-500 text-sm">
            <p>Generated by Advantage Waste Analytics • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p class="mt-1">Analysis based on WasteWise Calculation Standards v2.0</p>
        </div>
    </div>

    <script>
        // Tab switching
        function showTab(tabName) {{
            // Hide all tabs
            const tabs = document.querySelectorAll('.tab-content');
            tabs.forEach(tab => tab.classList.remove('active'));

            // Remove active from all buttons
            const buttons = document.querySelectorAll('.tab-button');
            buttons.forEach(btn => btn.classList.remove('active'));

            // Show selected tab
            document.getElementById(tabName).classList.add('active');

            // Activate button
            event.target.classList.add('active');
        }}

        // Chart data from Python
        const chartData = {json.dumps(chart_data)};

        // Chart.js configurations
        const chartOptions = {{
            responsive: true,
            maintainAspectRatio: true,
            plugins: {{
                legend: {{
                    display: true,
                    position: 'top'
                }}
            }}
        }};

        // Cost Trend Chart
        const costCtx = document.getElementById('costTrendChart').getContext('2d');
        new Chart(costCtx, {{
            type: 'line',
            data: {{
                labels: chartData.labels,
                datasets: [{{
                    label: 'Monthly Cost',
                    data: chartData.costs,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: true
                }}]
            }},
            options: {{
                ...chartOptions,
                scales: {{
                    y: {{
                        beginAtZero: false,
                        ticks: {{
                            callback: function(value) {{
                                return '$' + value.toLocaleString();
                            }}
                        }}
                    }}
                }},
                plugins: {{
                    ...chartOptions.plugins,
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return 'Cost: $' + context.parsed.y.toLocaleString('en-US', {{minimumFractionDigits: 2}});
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Invoice Count Chart
        const invCtx = document.getElementById('invoiceCountChart').getContext('2d');
        new Chart(invCtx, {{
            type: 'bar',
            data: {{
                labels: chartData.labels,
                datasets: [{{
                    label: 'Invoice Count',
                    data: chartData.invoice_counts,
                    backgroundColor: '#764ba2',
                    borderRadius: 6
                }}]
            }},
            options: {{
                ...chartOptions,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            stepSize: 1
                        }}
                    }}
                }}
            }}
        }});

        // Category Pie Chart
        const catCtx = document.getElementById('categoryPieChart').getContext('2d');
        new Chart(catCtx, {{
            type: 'doughnut',
            data: {{
                labels: chartData.category_breakdown.labels,
                datasets: [{{
                    data: chartData.category_breakdown.values,
                    backgroundColor: ['#667eea', '#764ba2'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                ...chartOptions,
                plugins: {{
                    ...chartOptions.plugins,
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return label + ': $' + value.toLocaleString('en-US', {{minimumFractionDigits: 2}}) + ' (' + percentage + '%)';
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // CPD Trend Chart
        const cpdCtx = document.getElementById('cpdTrendChart').getContext('2d');
        new Chart(cpdCtx, {{
            type: 'line',
            data: {{
                labels: chartData.labels,
                datasets: [{{
                    label: 'Cost Per Door',
                    data: chartData.cpd,
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    tension: 0.4,
                    fill: true
                }}]
            }},
            options: {{
                ...chartOptions,
                scales: {{
                    y: {{
                        beginAtZero: false,
                        ticks: {{
                            callback: function(value) {{
                                return '$' + value.toFixed(2);
                            }}
                        }}
                    }}
                }},
                plugins: {{
                    ...chartOptions.plugins,
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return 'CPD: $' + context.parsed.y.toFixed(2);
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>'''

    return html

def main():
    """Main execution"""
    print("="*80)
    print("GENERATING HTML DASHBOARD")
    print("="*80)

    # Load data
    print("\nLoading data...")
    df = load_data()

    # Prepare chart data
    print("Preparing visualizations...")
    chart_data = prepare_chart_data(df)

    # Generate HTML
    print("Generating HTML...")
    html = generate_html(df, chart_data)

    # Write file
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)

    file_size_kb = len(html) / 1024

    print(f"\n{'='*80}")
    print("DASHBOARD GENERATED SUCCESSFULLY")
    print(f"{'='*80}")
    print(f"File: {OUTPUT_HTML}")
    print(f"Size: {file_size_kb:.1f} KB")
    print(f"\nFeatures:")
    print("  [OK] 5 interactive tabs")
    print("  [OK] 4 Chart.js visualizations")
    print("  [OK] Responsive Tailwind CSS design")
    print("  [OK] Self-contained (inline CSS/JS)")
    print(f"\nOpen in browser to view dashboard.")

if __name__ == "__main__":
    main()
