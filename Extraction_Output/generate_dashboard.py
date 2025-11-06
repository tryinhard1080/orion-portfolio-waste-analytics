import pandas as pd
import json
from datetime import datetime

# Load data
with open(r'C:\Users\Richard\Downloads\Orion Data Part 2\Extraction_Output\orion_prosper_lakes_summary.json', 'r') as f:
    summary = json.load(f)

df = pd.read_excel(r'C:\Users\Richard\Downloads\Orion Data Part 2\Extraction_Output\COMPLETE_All_Properties_UPDATED_20251103_101053.xlsx', sheet_name='Orion Prosper Lakes')

print("=" * 80)
print("PHASE 3: INTERACTIVE DASHBOARD GENERATION")
print("=" * 80)

# Prepare data for charts
invoice_summary = df.groupby('Invoice #').agg({
    'Invoice Date': 'first',
    'Amount Due': 'first'
}).reset_index().sort_values('Invoice Date')

category_summary = df.groupby('Category')['Extended Amount'].sum().reset_index()
category_summary = category_summary[category_summary['Extended Amount'] > 0]

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Orion Prosper Lakes - Waste Management Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        .tab-button {{ cursor: pointer; }}
        .tab-button.active {{
            background-color: #1e40af;
            color: white;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .status-below {{ color: #ef4444; }}
        .status-within {{ color: #10b981; }}
        .status-above {{ color: #f59e0b; }}
    </style>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-8">
        <!-- Header -->
        <div class="bg-white shadow-lg rounded-lg p-6 mb-6">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-gray-800">Orion Prosper Lakes</h1>
                    <p class="text-gray-600">Waste Management Performance Dashboard</p>
                    <p class="text-sm text-gray-500 mt-2">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                <div class="text-right">
                    <p class="text-sm text-gray-600">308 Units</p>
                    <p class="text-sm text-gray-600">Prosper, Texas</p>
                    <p class="text-sm text-gray-600">Republic Services</p>
                </div>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="bg-white shadow-lg rounded-lg mb-6">
            <div class="flex border-b">
                <button class="tab-button active px-6 py-3 font-semibold text-sm" onclick="switchTab('executive')">
                    Executive Dashboard
                </button>
                <button class="tab-button px-6 py-3 font-semibold text-sm" onclick="switchTab('expense')">
                    Expense Analysis
                </button>
                <button class="tab-button px-6 py-3 font-semibold text-sm" onclick="switchTab('service')">
                    Service Details
                </button>
                <button class="tab-button px-6 py-3 font-semibold text-sm" onclick="switchTab('optimization')">
                    Optimization Insights
                </button>
                <button class="tab-button px-6 py-3 font-semibold text-sm" onclick="switchTab('contract')">
                    Contract Status
                </button>
            </div>
        </div>

        <!-- Tab 1: Executive Dashboard -->
        <div id="executive" class="tab-content active">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <!-- Cost Per Door -->
                <div class="metric-card rounded-lg p-6 shadow-lg">
                    <h3 class="text-sm font-semibold opacity-80">Cost Per Door</h3>
                    <p class="text-4xl font-bold mt-2">${summary['cost_per_door']:.2f}</p>
                    <p class="text-sm mt-2 opacity-90">Average per unit per month</p>
                </div>

                <!-- Yards Per Door -->
                <div class="metric-card rounded-lg p-6 shadow-lg">
                    <h3 class="text-sm font-semibold opacity-80">Yards Per Door</h3>
                    <p class="text-4xl font-bold mt-2">{summary['yards_per_door']:.2f}</p>
                    <p class="text-sm mt-2 opacity-90 status-below">Below Benchmark (2.0-2.5)</p>
                </div>

                <!-- Monthly Cost -->
                <div class="metric-card rounded-lg p-6 shadow-lg">
                    <h3 class="text-sm font-semibold opacity-80">Avg Monthly Cost</h3>
                    <p class="text-4xl font-bold mt-2">${summary['avg_monthly_cost']:,.2f}</p>
                    <p class="text-sm mt-2 opacity-90">Based on 2 invoices</p>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <!-- Monthly Cost Trend -->
                <div class="bg-white rounded-lg shadow-lg p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Monthly Cost Trend</h3>
                    <canvas id="costTrendChart"></canvas>
                </div>

                <!-- Expense Breakdown -->
                <div class="bg-white rounded-lg shadow-lg p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Expense Categories</h3>
                    <canvas id="categoryChart"></canvas>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-lg p-6">
                <h3 class="text-lg font-semibold text-gray-800 mb-4">Key Metrics Summary</h3>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div class="border-l-4 border-blue-500 pl-4">
                        <p class="text-sm text-gray-600">Total Invoices</p>
                        <p class="text-2xl font-bold">{summary['invoice_count']}</p>
                    </div>
                    <div class="border-l-4 border-green-500 pl-4">
                        <p class="text-sm text-gray-600">Total Hauls</p>
                        <p class="text-2xl font-bold">{summary['num_hauls']}</p>
                    </div>
                    <div class="border-l-4 border-yellow-500 pl-4">
                        <p class="text-sm text-gray-600">Avg Tons/Haul</p>
                        <p class="text-2xl font-bold">{summary['avg_tons_per_haul']:.2f}</p>
                    </div>
                    <div class="border-l-4 border-red-500 pl-4">
                        <p class="text-sm text-gray-600">Total Tonnage</p>
                        <p class="text-2xl font-bold">{summary['total_tons']:.2f}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 2: Expense Analysis -->
        <div id="expense" class="tab-content">
            <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
                <h3 class="text-lg font-semibold text-gray-800 mb-4">Invoice History</h3>
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Invoice #</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cost/Door</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
'''

for idx, row in invoice_summary.iterrows():
    cpd = row['Amount Due'] / 308
    html_content += f'''
                            <tr>
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{row['Invoice #']}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{row['Invoice Date'].strftime('%Y-%m-%d')}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row['Amount Due']:,.2f}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${cpd:.2f}</td>
                            </tr>
'''

html_content += f'''
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-white rounded-lg shadow-lg p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Cost Breakdown</h3>
                    <div class="space-y-4">
                        <div class="flex justify-between items-center">
                            <span class="text-gray-700">Base Charges</span>
                            <span class="font-bold text-gray-900">${df[df['Category']=='base']['Extended Amount'].sum():,.2f}</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-gray-700">Extra Pickups</span>
                            <span class="font-bold text-gray-900">${df[df['Category']=='extra_pickup']['Extended Amount'].sum():,.2f}</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-gray-700">Taxes</span>
                            <span class="font-bold text-gray-900">${df[df['Category']=='tax']['Extended Amount'].sum():,.2f}</span>
                        </div>
                        <div class="border-t pt-4 flex justify-between items-center">
                            <span class="text-gray-900 font-bold">Total</span>
                            <span class="font-bold text-gray-900">${summary['total_spend']:,.2f}</span>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-lg shadow-lg p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Data Sufficiency</h3>
                    <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4">
                        <div class="flex">
                            <div class="flex-shrink-0">
                                <svg class="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                                </svg>
                            </div>
                            <div class="ml-3">
                                <p class="text-sm text-yellow-700">
                                    <strong>Limited Data Period</strong><br>
                                    Only 2 invoices available (Jan & Apr 2025). Minimum 6 months of data recommended for confident trend analysis and optimization recommendations.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 3: Service Details -->
        <div id="service" class="tab-content">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-white rounded-lg shadow-lg p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Service Configuration</h3>
                    <div class="space-y-3">
                        <div class="flex justify-between">
                            <span class="text-gray-600">Service Type:</span>
                            <span class="font-semibold">Compactor (35-40 yd)</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Vendor:</span>
                            <span class="font-semibold">{summary['vendor']}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Account #:</span>
                            <span class="font-semibold">{summary['account']}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Total Hauls:</span>
                            <span class="font-semibold">{summary['num_hauls']} hauls</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Avg Pickup Cost:</span>
                            <span class="font-semibold">${summary['avg_pickup_cost']:.2f}</span>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-lg shadow-lg p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Tonnage Analysis</h3>
                    <div class="space-y-3">
                        <div class="flex justify-between">
                            <span class="text-gray-600">Total Tonnage:</span>
                            <span class="font-semibold">{summary['total_tons']:.2f} tons</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Avg Tons/Haul:</span>
                            <span class="font-semibold status-below">{summary['avg_tons_per_haul']:.2f} tons</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Benchmark:</span>
                            <span class="font-semibold">6.0+ tons/haul</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Status:</span>
                            <span class="font-semibold status-below">Below Optimal</span>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-lg shadow-lg p-6 md:col-span-2">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Yards Per Door vs Benchmark</h3>
                    <canvas id="benchmarkChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Tab 4: Optimization Insights -->
        <div id="optimization" class="tab-content">
            <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
                <h3 class="text-lg font-semibold text-gray-800 mb-4">Optimization Opportunities</h3>

                <!-- Compactor Optimization -->
                <div class="border-l-4 border-green-500 bg-green-50 p-6 mb-6">
                    <h4 class="font-bold text-green-800 text-lg mb-3">✓ COMPACTOR OPTIMIZATION - TRIGGERED</h4>
                    <p class="text-green-700 mb-4">Average tons per haul (3.18) is below the 6.0 threshold, indicating optimization opportunity.</p>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                        <div class="bg-white rounded p-4">
                            <h5 class="font-semibold text-gray-800 mb-2">Current State</h5>
                            <ul class="text-sm text-gray-700 space-y-1">
                                <li>• {summary['num_hauls']} hauls at {summary['avg_tons_per_haul']:.2f} tons/haul</li>
                                <li>• ~6 days between pickups</li>
                                <li>• Monthly pickup cost: $2,644.65</li>
                            </ul>
                        </div>
                        <div class="bg-white rounded p-4">
                            <h5 class="font-semibold text-gray-800 mb-2">Optimized State (14-day max)</h5>
                            <ul class="text-sm text-gray-700 space-y-1">
                                <li>• 2.14 hauls at 7.43 tons/haul</li>
                                <li>• 14 days between pickups</li>
                                <li>• Monthly pickup cost: $1,132.28</li>
                            </ul>
                        </div>
                    </div>

                    <div class="bg-white rounded p-4">
                        <h5 class="font-semibold text-gray-800 mb-2">Potential Savings (Calculation-Based)</h5>
                        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                            <div>
                                <p class="text-xs text-gray-600">Monthly Savings</p>
                                <p class="text-lg font-bold text-green-600">$1,512.37</p>
                            </div>
                            <div>
                                <p class="text-xs text-gray-600">Annual Savings</p>
                                <p class="text-lg font-bold text-green-600">$18,148.44</p>
                            </div>
                            <div>
                                <p class="text-xs text-gray-600">Monitor Cost (Annual)</p>
                                <p class="text-lg font-bold text-gray-600">$2,400.00</p>
                            </div>
                            <div>
                                <p class="text-xs text-gray-600">Net Savings (Year 1)</p>
                                <p class="text-lg font-bold text-green-600">$15,448.44</p>
                            </div>
                        </div>
                    </div>

                    <div class="mt-4 bg-yellow-50 rounded p-4">
                        <p class="text-sm text-yellow-800">
                            <strong>Note:</strong> Savings calculations are extrapolated from 2-invoice data. Additional invoice history recommended for confident projections.
                        </p>
                    </div>
                </div>

                <!-- Contamination -->
                <div class="border-l-4 border-gray-300 bg-gray-50 p-6 mb-6">
                    <h4 class="font-bold text-gray-800 text-lg mb-3">✗ CONTAMINATION REDUCTION - NOT TRIGGERED</h4>
                    <p class="text-gray-700">No contamination charges detected in available invoices. Threshold: >3% of total spend.</p>
                </div>

                <!-- Bulk Subscription -->
                <div class="border-l-4 border-gray-300 bg-gray-50 p-6">
                    <h4 class="font-bold text-gray-800 text-lg mb-3">✗ BULK SUBSCRIPTION - NOT TRIGGERED</h4>
                    <p class="text-gray-700">No bulk pickup charges detected in available invoices. Threshold: >$500/month average.</p>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-lg p-6">
                <h3 class="text-lg font-semibold text-gray-800 mb-4">Data Limitations</h3>
                <div class="bg-blue-50 border-l-4 border-blue-400 p-4">
                    <div class="flex">
                        <div class="flex-shrink-0">
                            <svg class="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <div class="ml-3">
                            <p class="text-sm text-blue-700">
                                <strong>Limited Data Period:</strong> Analysis based on 2 invoices (Jan & Apr 2025). For confident optimization recommendations, 6-12 months of invoice history is recommended. Current savings projections are calculation-based but should be validated with additional data.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 5: Contract Status -->
        <div id="contract" class="tab-content">
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h3 class="text-lg font-semibold text-gray-800 mb-4">Contract Information</h3>

                <div class="bg-red-50 border-l-4 border-red-400 p-6 mb-6">
                    <div class="flex">
                        <div class="flex-shrink-0">
                            <svg class="h-6 w-6 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <div class="ml-3">
                            <h4 class="text-lg font-bold text-red-800">NO CONTRACT FILE AVAILABLE</h4>
                            <p class="mt-2 text-sm text-red-700">
                                No contract file was found for Orion Prosper Lakes in the Contracts/ folder. This limits the ability to analyze renewal dates, rate increase terms, and contractual obligations.
                            </p>
                        </div>
                    </div>
                </div>

                <div class="mb-6">
                    <h4 class="font-semibold text-gray-800 mb-3">Impact of Missing Contract</h4>
                    <ul class="list-disc list-inside text-gray-700 space-y-2">
                        <li>Cannot determine contract renewal date or notification deadline</li>
                        <li>Unable to analyze rate increase terms and escalation clauses</li>
                        <li>Cannot verify contracted service levels vs actual service</li>
                        <li>Missing visibility into termination notice requirements</li>
                        <li>Unable to identify concerning contractual obligations</li>
                    </ul>
                </div>

                <div class="bg-green-50 border-l-4 border-green-400 p-6">
                    <div class="flex">
                        <div class="flex-shrink-0">
                            <svg class="h-6 w-6 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <div class="ml-3">
                            <h4 class="text-lg font-bold text-green-800">Recommended Action</h4>
                            <p class="mt-2 text-sm text-green-700">
                                <strong>Request contract file from property management or procurement team.</strong> Once available, update the CONTRACT_TERMS tab in the Excel workbook with key contract details including:
                            </p>
                            <ul class="mt-2 list-disc list-inside text-sm text-green-700 space-y-1">
                                <li>Contract start and end dates</li>
                                <li>Renewal notification deadline</li>
                                <li>Base rates and service inclusions</li>
                                <li>Rate increase terms</li>
                                <li>Special terms or concerning clauses</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Tab switching
        function switchTab(tabName) {{
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {{
                tab.classList.remove('active');
            }});

            // Remove active class from all buttons
            document.querySelectorAll('.tab-button').forEach(btn => {{
                btn.classList.remove('active');
            }});

            // Show selected tab
            document.getElementById(tabName).classList.add('active');

            // Add active class to clicked button
            event.target.classList.add('active');
        }}

        // Cost Trend Chart
        const costTrendCtx = document.getElementById('costTrendChart').getContext('2d');
        new Chart(costTrendCtx, {{
            type: 'line',
            data: {{
                labels: ['Jan 2025', 'Apr 2025'],
                datasets: [{{
                    label: 'Invoice Amount',
                    data: [774.50, 2950.50],
                    borderColor: 'rgb(59, 130, 246)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.1
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    title: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return '$' + value.toFixed(2);
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Category Pie Chart
        const categoryCtx = document.getElementById('categoryChart').getContext('2d');
        new Chart(categoryCtx, {{
            type: 'pie',
            data: {{
                labels: ['Base Charges', 'Extra Pickups', 'Taxes'],
                datasets: [{{
                    data: [3237.05, 530.25, 283.92],
                    backgroundColor: [
                        'rgb(59, 130, 246)',
                        'rgb(251, 191, 36)',
                        'rgb(239, 68, 68)'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});

        // Benchmark Comparison Chart
        const benchmarkCtx = document.getElementById('benchmarkChart').getContext('2d');
        new Chart(benchmarkCtx, {{
            type: 'bar',
            data: {{
                labels: ['Actual', 'Minimum', 'Maximum'],
                datasets: [{{
                    label: 'Yards/Door/Month',
                    data: [{summary['yards_per_door']:.2f}, 2.0, 2.5],
                    backgroundColor: [
                        'rgb(239, 68, 68)',
                        'rgb(34, 197, 94)',
                        'rgb(34, 197, 94)'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    title: {{
                        display: true,
                        text: 'Garden-Style Benchmark: 2.0-2.5 yards/door/month'
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 3.0
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
'''

# Write the HTML file
output_file = r'C:\Users\Richard\Downloads\Orion Data Part 2\Extraction_Output\OrionProsperLakes_Dashboard.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

file_size = len(html_content)
print(f"\n[1/1] Interactive HTML Dashboard Generated")
print(f"      File: {output_file}")
print(f"      Size: {file_size:,} bytes (~{file_size/1024:.1f} KB)")
print(f"\n5 TABS CREATED:")
print("  1. Executive Dashboard - Key metrics and charts")
print("  2. Expense Analysis - Invoice breakdown and trends")
print("  3. Service Details - Tonnage and configuration")
print("  4. Optimization Insights - Triggered opportunities")
print("  5. Contract Status - Missing contract notification")
print("\n" + "=" * 80)
print("INTERACTIVE DASHBOARD GENERATION COMPLETE")
print("=" * 80)
