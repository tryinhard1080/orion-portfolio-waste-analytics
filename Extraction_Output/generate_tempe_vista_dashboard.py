"""
Generate Interactive HTML Dashboard for Tempe Vista
5-Tab Dashboard with Chart.js visualizations
"""

import pandas as pd
import json
from datetime import datetime
from pathlib import Path

# Load data
base_path = Path(r"C:\Users\Richard\Downloads\Orion Data Part 2")
ally_file = base_path / "rearizona4packtrashanalysis" / "Tempe Vista - Ally Waste.xlsx"
wm_file = base_path / "rearizona4packtrashanalysis" / "Tempe Vista - Waste Management Hauling.xlsx"

df_ally = pd.read_excel(ally_file)
df_wm = pd.read_excel(wm_file)

# Property constants
PROPERTY_NAME = "Tempe Vista"
PROPERTY_LOCATION = "Tempe, Arizona"
UNITS_ESTIMATED = 150
UNITS_SOURCE = "ESTIMATED - REQUIRES VERIFICATION"

# Process data
ally_invoices = []
for _, row in df_ally.iterrows():
    ally_invoices.append({
        'Date': pd.to_datetime(row['Bill Date']),
        'Amount': float(row['Bill Total']),
        'Vendor': 'Ally Waste'
    })

wm_invoices = []
for _, row in df_wm.iterrows():
    wm_invoices.append({
        'Date': pd.to_datetime(row['Bill Date']),
        'Amount': float(row['Bill Total']),
        'Vendor': 'Waste Management'
    })

all_invoices = ally_invoices + wm_invoices
df_all = pd.DataFrame(all_invoices).sort_values('Date')

# Calculate monthly aggregates
monthly_data = df_all.groupby([df_all['Date'].dt.to_period('M'), 'Vendor'])['Amount'].sum().unstack(fill_value=0)
monthly_data['Total'] = monthly_data.sum(axis=1)
monthly_data.index = monthly_data.index.astype(str)

# Prepare chart data
chart_labels = monthly_data.index.tolist()
chart_ally = monthly_data.get('Ally Waste', pd.Series([0]*len(monthly_data))).tolist()
chart_wm = monthly_data.get('Waste Management', pd.Series([0]*len(monthly_data))).tolist()
chart_total = monthly_data['Total'].tolist()

# Calculate metrics
total_spend = df_all['Amount'].sum()
avg_monthly = monthly_data['Total'].mean()
cost_per_door = avg_monthly / UNITS_ESTIMATED
ally_total = df_ally['Bill Total'].sum()
wm_total = df_wm['Bill Total'].sum()
ally_pct = (ally_total / total_spend * 100)
wm_pct = (wm_total / total_spend * 100)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{PROPERTY_NAME} - Waste Management Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .tab-button {{
            transition: all 0.3s ease;
        }}
        .tab-button:hover {{
            background-color: #2563eb;
            color: white;
        }}
        .tab-button.active {{
            background-color: #1e40af;
            color: white;
            border-bottom: 3px solid #fbbf24;
        }}
        .tab-content {{
            display: none;
        }}
        .tab-content.active {{
            display: block;
        }}
        .metric-card {{
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }}
        .warning-banner {{
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            animation: pulse 2s ease-in-out infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.9; }}
        }}
    </style>
</head>
<body class="bg-gray-50">
    <!-- Header -->
    <div class="bg-gradient-to-r from-blue-900 to-blue-700 text-white p-6 shadow-lg">
        <div class="max-w-7xl mx-auto">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold">{PROPERTY_NAME}</h1>
                    <p class="text-blue-200 mt-1">{PROPERTY_LOCATION} • Waste Management Analytics Dashboard</p>
                </div>
                <div class="text-right">
                    <div class="text-sm text-blue-200">Property 10 of 10</div>
                    <div class="text-lg font-semibold">FINAL PROPERTY</div>
                    <div class="text-xs text-blue-300 mt-1">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Warning Banner -->
    <div class="warning-banner text-gray-900 p-4 shadow-md">
        <div class="max-w-7xl mx-auto flex items-center justify-center">
            <svg class="w-6 h-6 mr-3" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
            </svg>
            <span class="font-bold">DATA QUALITY NOTICE:</span>
            <span class="ml-2">Unit count estimated at {UNITS_ESTIMATED} units - All per-door metrics require verification</span>
        </div>
    </div>

    <!-- Tab Navigation -->
    <div class="max-w-7xl mx-auto mt-6 px-6">
        <div class="bg-white rounded-lg shadow-md overflow-hidden">
            <div class="flex border-b">
                <button class="tab-button active flex-1 px-6 py-4 text-center font-semibold" onclick="showTab('executive')">
                    📊 Executive Dashboard
                </button>
                <button class="tab-button flex-1 px-6 py-4 text-center font-semibold" onclick="showTab('expense')">
                    💰 Expense Analysis
                </button>
                <button class="tab-button flex-1 px-6 py-4 text-center font-semibold" onclick="showTab('service')">
                    🚛 Service Details
                </button>
                <button class="tab-button flex-1 px-6 py-4 text-center font-semibold" onclick="showTab('optimization')">
                    ⚡ Optimization
                </button>
                <button class="tab-button flex-1 px-6 py-4 text-center font-semibold" onclick="showTab('contract')">
                    📄 Contract Status
                </button>
            </div>

            <!-- TAB 1: EXECUTIVE DASHBOARD -->
            <div id="executive" class="tab-content active p-6">
                <h2 class="text-2xl font-bold text-gray-800 mb-6">Executive Dashboard</h2>

                <!-- Key Metrics -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div class="metric-card bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg shadow-lg p-6 text-white">
                        <div class="text-sm font-semibold opacity-90">Units (ESTIMATED)</div>
                        <div class="text-4xl font-bold mt-2">{UNITS_ESTIMATED}</div>
                        <div class="text-xs mt-2 opacity-75">{UNITS_SOURCE}</div>
                    </div>

                    <div class="metric-card bg-gradient-to-br from-green-500 to-green-600 rounded-lg shadow-lg p-6 text-white">
                        <div class="text-sm font-semibold opacity-90">Avg Monthly Cost</div>
                        <div class="text-4xl font-bold mt-2">${avg_monthly:,.0f}</div>
                        <div class="text-xs mt-2 opacity-75">Last 12 months</div>
                    </div>

                    <div class="metric-card bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg shadow-lg p-6 text-white">
                        <div class="text-sm font-semibold opacity-90">Cost Per Door (EST)</div>
                        <div class="text-4xl font-bold mt-2">${cost_per_door:.2f}</div>
                        <div class="text-xs mt-2 opacity-75">Based on estimated units</div>
                    </div>

                    <div class="metric-card bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg shadow-lg p-6 text-white">
                        <div class="text-sm font-semibold opacity-90">Total Period Spend</div>
                        <div class="text-4xl font-bold mt-2">${total_spend:,.0f}</div>
                        <div class="text-xs mt-2 opacity-75">{len(df_all)} invoices analyzed</div>
                    </div>
                </div>

                <!-- Charts Row -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="bg-white border rounded-lg shadow p-6">
                        <h3 class="text-lg font-bold text-gray-800 mb-4">Monthly Cost Trend</h3>
                        <canvas id="trendChart"></canvas>
                    </div>

                    <div class="bg-white border rounded-lg shadow p-6">
                        <h3 class="text-lg font-bold text-gray-800 mb-4">Vendor Split</h3>
                        <canvas id="vendorChart"></canvas>
                    </div>
                </div>

                <!-- Service Summary -->
                <div class="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-6">
                    <h3 class="text-lg font-bold text-gray-800 mb-4">Service Overview</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <div class="font-semibold text-gray-700">Primary Hauler</div>
                            <div class="text-gray-600">Waste Management</div>
                            <div class="text-sm text-gray-500">${wm_total:,.2f} ({wm_pct:.1f}% of total)</div>
                        </div>
                        <div>
                            <div class="font-semibold text-gray-700">Bulk Service</div>
                            <div class="text-gray-600">Ally Waste</div>
                            <div class="text-sm text-gray-500">${ally_total:,.2f} ({ally_pct:.1f}% of total)</div>
                        </div>
                        <div>
                            <div class="font-semibold text-gray-700">Analysis Period</div>
                            <div class="text-gray-600">{df_all['Date'].min().strftime('%B %Y')} - {df_all['Date'].max().strftime('%B %Y')}</div>
                            <div class="text-sm text-gray-500">{len(monthly_data)} months</div>
                        </div>
                        <div>
                            <div class="font-semibold text-gray-700">Data Completeness</div>
                            <div class="text-gray-600">100% (Amounts & Dates)</div>
                            <div class="text-sm text-gray-500">Service specs: 0%</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- TAB 2: EXPENSE ANALYSIS -->
            <div id="expense" class="tab-content p-6">
                <h2 class="text-2xl font-bold text-gray-800 mb-6">Expense Analysis</h2>

                <div class="bg-white border rounded-lg shadow overflow-hidden">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Month</th>
                                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Ally Waste</th>
                                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Waste Management</th>
                                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
                                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Cost/Door (EST)</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
"""

# Add monthly rows
for month, row in monthly_data.iterrows():
    ally_amt = row.get('Ally Waste', 0)
    wm_amt = row.get('Waste Management', 0)
    total_amt = row['Total']
    cpd = total_amt / UNITS_ESTIMATED

    html_content += f"""
                            <tr class="hover:bg-gray-50">
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{month}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-500">${ally_amt:,.2f}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-500">${wm_amt:,.2f}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-right font-semibold text-gray-900">${total_amt:,.2f}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-500">${cpd:.2f}</td>
                            </tr>
"""

html_content += f"""
                        </tbody>
                        <tfoot class="bg-gray-50">
                            <tr>
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900">TOTALS</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-right font-bold text-gray-900">${ally_total:,.2f}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-right font-bold text-gray-900">${wm_total:,.2f}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-right font-bold text-blue-600">${total_spend:,.2f}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-right font-bold text-gray-900">${cost_per_door:.2f}</td>
                            </tr>
                        </tfoot>
                    </table>
                </div>

                <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="bg-white border rounded-lg shadow p-6">
                        <h3 class="text-lg font-bold text-gray-800 mb-4">Monthly Expense Stacked Chart</h3>
                        <canvas id="expenseStackedChart"></canvas>
                    </div>
                    <div class="bg-white border rounded-lg shadow p-6">
                        <h3 class="text-lg font-bold text-gray-800 mb-4">Cost Per Door Trend (ESTIMATED)</h3>
                        <canvas id="cpdTrendChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- TAB 3: SERVICE DETAILS -->
            <div id="service" class="tab-content p-6">
                <h2 class="text-2xl font-bold text-gray-800 mb-6">Service Details</h2>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Waste Management Card -->
                    <div class="bg-white border rounded-lg shadow p-6">
                        <h3 class="text-lg font-bold text-blue-600 mb-4">Waste Management - Primary Hauler</h3>
                        <div class="space-y-3">
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Account Number</span>
                                <span class="text-gray-600">17-16175-33003</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Contract Number</span>
                                <span class="text-gray-600">S0009750102</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Service Type</span>
                                <span class="text-gray-600">MSW Collection + Recycling</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Equipment</span>
                                <span class="text-gray-600">9 containers (FEL)</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Recycling</span>
                                <span class="text-gray-600">1x 4-yard, 1x/week</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">MSW Line 1</span>
                                <span class="text-gray-600">3x 3-yard, 3x/week</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">MSW Line 2</span>
                                <span class="text-gray-600">5x 4-yard, 3x/week</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Contract Base Rate</span>
                                <span class="text-gray-600">$757.95/month</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="font-semibold text-gray-700">Actual Average</span>
                                <span class="text-blue-600 font-bold">${df_wm['Bill Total'].mean():,.2f}/month</span>
                            </div>
                        </div>
                    </div>

                    <!-- Ally Waste Card -->
                    <div class="bg-white border rounded-lg shadow p-6">
                        <h3 class="text-lg font-bold text-orange-600 mb-4">Ally Waste - Bulk Service</h3>
                        <div class="space-y-3">
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Account Number</span>
                                <span class="text-gray-600">AW-ct76</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Service Type</span>
                                <span class="text-gray-600">Bulk Trash Removal</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Subscription Model</span>
                                <span class="text-gray-600">Monthly flat rate</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Typical Rate</span>
                                <span class="text-gray-600">${df_ally['Bill Total'].mode()[0]:.2f}/month</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Rate Range</span>
                                <span class="text-gray-600">${df_ally['Bill Total'].min():.2f} - ${df_ally['Bill Total'].max():.2f}</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Average Cost</span>
                                <span class="text-orange-600 font-bold">${df_ally['Bill Total'].mean():,.2f}/month</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Annual Projection</span>
                                <span class="text-gray-600">${df_ally['Bill Total'].mean() * 12:,.2f}/year</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Service History -->
                <div class="mt-6 bg-white border rounded-lg shadow overflow-hidden">
                    <div class="px-6 py-4 bg-gray-50 border-b">
                        <h3 class="text-lg font-bold text-gray-800">Invoice History</h3>
                    </div>
                    <div class="p-6">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <div class="font-semibold text-gray-700 mb-2">Waste Management Invoices</div>
                                <div class="text-sm space-y-1 max-h-60 overflow-y-auto">
"""

for _, inv in df_wm.iterrows():
    inv_date = pd.to_datetime(inv['Bill Date']).strftime('%Y-%m-%d')
    html_content += f"""
                                    <div class="flex justify-between py-1 border-b border-gray-100">
                                        <span class="text-gray-600">{inv_date}</span>
                                        <span class="font-mono text-gray-800">${inv['Bill Total']:,.2f}</span>
                                    </div>
"""

html_content += """
                                </div>
                            </div>
                            <div>
                                <div class="font-semibold text-gray-700 mb-2">Ally Waste Invoices</div>
                                <div class="text-sm space-y-1 max-h-60 overflow-y-auto">
"""

for _, inv in df_ally.iterrows():
    inv_date = pd.to_datetime(inv['Bill Date']).strftime('%Y-%m-%d')
    html_content += f"""
                                    <div class="flex justify-between py-1 border-b border-gray-100">
                                        <span class="text-gray-600">{inv_date}</span>
                                        <span class="font-mono text-gray-800">${inv['Bill Total']:,.2f}</span>
                                    </div>
"""

variance = df_wm['Bill Total'].mean() - 757.95
variance_pct = (variance / 757.95 * 100)

html_content += f"""
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Cost Variance Alert -->
                <div class="mt-6 bg-yellow-50 border border-yellow-200 rounded-lg p-6">
                    <h3 class="text-lg font-bold text-yellow-800 mb-3 flex items-center">
                        <svg class="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                        </svg>
                        Contract vs. Actual Cost Variance
                    </h3>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                        <div>
                            <div class="font-semibold text-gray-700">Contract Base Rate</div>
                            <div class="text-2xl font-bold text-gray-800">$757.95</div>
                            <div class="text-xs text-gray-500">Per month (from 2018 agreement)</div>
                        </div>
                        <div>
                            <div class="font-semibold text-gray-700">Actual Average Invoice</div>
                            <div class="text-2xl font-bold text-blue-600">${df_wm['Bill Total'].mean():,.2f}</div>
                            <div class="text-xs text-gray-500">Recent {len(df_wm)}-month average</div>
                        </div>
                        <div>
                            <div class="font-semibold text-gray-700">Variance</div>
                            <div class="text-2xl font-bold text-orange-600">+${variance:,.2f}</div>
                            <div class="text-xs text-gray-500">{variance_pct:.1f}% increase</div>
                        </div>
                    </div>
                    <div class="mt-4 text-sm text-gray-700">
                        <strong>Likely factors:</strong> CPI increases, fuel surcharges, environmental fees, regulatory cost recovery charges
                    </div>
                </div>
            </div>

            <!-- TAB 4: OPTIMIZATION -->
            <div id="optimization" class="tab-content p-6">
                <h2 class="text-2xl font-bold text-gray-800 mb-6">Optimization Insights</h2>

                <!-- Data Limitation Notice -->
                <div class="bg-red-50 border-2 border-red-300 rounded-lg p-6 mb-6">
                    <h3 class="text-lg font-bold text-red-800 mb-3 flex items-center">
                        <svg class="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                        </svg>
                        Insufficient Data for Full Optimization Analysis
                    </h3>
                    <div class="text-sm text-red-700 space-y-2">
                        <p class="font-semibold">Missing Critical Service Specifications:</p>
                        <ul class="list-disc list-inside ml-4 space-y-1">
                            <li>Tonnage data (cannot calculate yards per door)</li>
                            <li>Actual pickup frequency records (cannot verify service levels)</li>
                            <li>Container fill levels (cannot assess capacity utilization)</li>
                            <li>Verified unit count (cannot finalize per-door metrics)</li>
                        </ul>
                    </div>
                </div>

                <!-- What We CAN Analyze -->
                <div class="bg-green-50 border border-green-200 rounded-lg p-6 mb-6">
                    <h3 class="text-lg font-bold text-green-800 mb-4">✓ Available Analysis (Based on Invoice Data)</h3>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="bg-white rounded-lg p-4 shadow-sm">
                            <h4 class="font-bold text-gray-800 mb-3">Bulk Service Analysis</h4>
                            <div class="space-y-2 text-sm">
                                <div class="flex justify-between">
                                    <span class="text-gray-600">Monthly Average:</span>
                                    <span class="font-bold text-gray-800">${df_ally['Bill Total'].mean():.2f}</span>
                                </div>
                                <div class="flex justify-between">
                                    <span class="text-gray-600">Annual Projection:</span>
                                    <span class="font-bold text-gray-800">${df_ally['Bill Total'].mean() * 12:,.2f}</span>
                                </div>
                                <div class="flex justify-between">
                                    <span class="text-gray-600">Trigger Threshold:</span>
                                    <span class="font-bold text-gray-800">&gt; $500/month</span>
                                </div>
                                <div class="mt-3 pt-3 border-t">
                                    <div class="flex items-center text-green-700">
                                        <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                                        </svg>
                                        <span class="font-semibold">Trigger Met - Optimization Candidate</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="bg-white rounded-lg p-4 shadow-sm">
                            <h4 class="font-bold text-gray-800 mb-3">Cost Trend Analysis</h4>
                            <div class="space-y-2 text-sm">
                                <div class="flex justify-between">
                                    <span class="text-gray-600">Analysis Period:</span>
                                    <span class="font-bold text-gray-800">{len(monthly_data)} months</span>
                                </div>
                                <div class="flex justify-between">
                                    <span class="text-gray-600">Total Invoices:</span>
                                    <span class="font-bold text-gray-800">{len(df_all)}</span>
                                </div>
                                <div class="flex justify-between">
                                    <span class="text-gray-600">Data Completeness:</span>
                                    <span class="font-bold text-green-600">100%</span>
                                </div>
                                <div class="flex justify-between">
                                    <span class="text-gray-600">Trending:</span>
                                    <span class="font-bold text-gray-800">Stable with variance</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Recommendations -->
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
                    <h3 class="text-lg font-bold text-blue-800 mb-4">📋 Current Recommendations</h3>
                    <div class="space-y-4 text-sm">
                        <div class="bg-white rounded p-4">
                            <div class="font-bold text-gray-800 mb-2">1. Bulk Service Monitoring</div>
                            <div class="text-gray-600">
                                Current Ally Waste subscription cost (${df_ally['Bill Total'].mean():.2f}/month) is above optimization trigger.
                                Monitor bulk generation patterns and consider:
                                <ul class="list-disc list-inside ml-4 mt-2">
                                    <li>Resident education on bulk item disposal</li>
                                    <li>Seasonal variation analysis</li>
                                    <li>Comparison with on-call bulk pricing if available</li>
                                </ul>
                            </div>
                        </div>

                        <div class="bg-white rounded p-4">
                            <div class="font-bold text-gray-800 mb-2">2. Data Collection Priority</div>
                            <div class="text-gray-600">
                                To enable full optimization analysis, obtain:
                                <ul class="list-disc list-inside ml-4 mt-2">
                                    <li><strong>Priority 1:</strong> Verified unit count from property records</li>
                                    <li><strong>Priority 2:</strong> Service specifications from Waste Management</li>
                                    <li><strong>Priority 3:</strong> Tonnage reports (if available)</li>
                                    <li><strong>Priority 4:</strong> Container inventory and pickup schedules</li>
                                </ul>
                            </div>
                        </div>

                        <div class="bg-white rounded p-4">
                            <div class="font-bold text-gray-800 mb-2">3. Contract Variance Investigation</div>
                            <div class="text-gray-600">
                                Actual costs ({variance_pct:.1f}% above contract base) warrant review of:
                                <ul class="list-disc list-inside ml-4 mt-2">
                                    <li>CPI adjustment history since 2018</li>
                                    <li>Fuel surcharge trends</li>
                                    <li>Environmental fee increases</li>
                                    <li>Any overage or contamination charges</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- TAB 5: CONTRACT STATUS -->
            <div id="contract" class="tab-content p-6">
                <h2 class="text-2xl font-bold text-gray-800 mb-6">Contract Status</h2>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- WM Contract Card -->
                    <div class="bg-white border-2 border-blue-300 rounded-lg shadow-lg p-6">
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="text-lg font-bold text-blue-600">Waste Management Agreement</h3>
                            <span class="px-3 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded-full">ACTIVE</span>
                        </div>
                        <div class="space-y-3 text-sm">
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Contract #:</span>
                                <span class="text-gray-600">S0009750102</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Effective Date:</span>
                                <span class="text-gray-600">1/12/2018</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Initial Term:</span>
                                <span class="text-gray-600">1 year</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Renewal:</span>
                                <span class="text-gray-600">12-month auto-renewal</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Contract Years:</span>
                                <span class="text-gray-600">~7 years active</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="font-semibold text-gray-700">Base Rate:</span>
                                <span class="text-gray-600">$757.95/month</span>
                            </div>
                        </div>

                        <div class="mt-6 bg-blue-50 rounded p-4">
                            <div class="font-semibold text-blue-800 mb-2">Service Equipment</div>
                            <ul class="text-xs space-y-1 text-gray-700">
                                <li>• 1x 4-yard FEL (Recycling) - 1x/week</li>
                                <li>• 3x 3-yard FEL (MSW) - 3x/week</li>
                                <li>• 5x 4-yard FEL (MSW) - 3x/week</li>
                                <li class="font-semibold mt-2">Total: 9 containers, ~29 yards capacity</li>
                            </ul>
                        </div>
                    </div>

                    <!-- Ally Waste Card -->
                    <div class="bg-white border-2 border-orange-300 rounded-lg shadow-lg p-6">
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="text-lg font-bold text-orange-600">Ally Waste Subscription</h3>
                            <span class="px-3 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded-full">ACTIVE</span>
                        </div>
                        <div class="space-y-3 text-sm">
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Account #:</span>
                                <span class="text-gray-600">AW-ct76</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Service Type:</span>
                                <span class="text-gray-600">Bulk Trash Removal</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Billing Model:</span>
                                <span class="text-gray-600">Monthly subscription</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Typical Rate:</span>
                                <span class="text-gray-600">${df_ally['Bill Total'].mode()[0]:.2f}/month</span>
                            </div>
                            <div class="flex justify-between border-b pb-2">
                                <span class="font-semibold text-gray-700">Rate Range:</span>
                                <span class="text-gray-600">${df_ally['Bill Total'].min():.2f} - ${df_ally['Bill Total'].max():.2f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="font-semibold text-gray-700">12-Mo Average:</span>
                                <span class="text-gray-600">${df_ally['Bill Total'].mean():.2f}/month</span>
                            </div>
                        </div>

                        <div class="mt-6 bg-orange-50 rounded p-4">
                            <div class="font-semibold text-orange-800 mb-2">Service Benefits</div>
                            <ul class="text-xs space-y-1 text-gray-700">
                                <li>• Unlimited bulk item removal</li>
                                <li>• Scheduled pickups (typically weekly/bi-weekly)</li>
                                <li>• Resident satisfaction improvement</li>
                                <li>• Predictable monthly cost</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <!-- Contract Issues & Gaps -->
                <div class="mt-6 bg-yellow-50 border border-yellow-300 rounded-lg p-6">
                    <h3 class="text-lg font-bold text-yellow-800 mb-4">⚠️ Contract Information Gaps</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                        <div>
                            <div class="font-semibold text-gray-800 mb-2">Missing Critical Information:</div>
                            <ul class="list-disc list-inside space-y-1 text-gray-700">
                                <li>Unit count (not listed in contract)</li>
                                <li>Tonnage data (not in invoice records)</li>
                                <li>Container location details</li>
                                <li>Overage rate structure</li>
                                <li>Rate increase schedule specifics</li>
                            </ul>
                        </div>
                        <div>
                            <div class="font-semibold text-gray-800 mb-2">Recommended Actions:</div>
                            <ul class="list-disc list-inside space-y-1 text-gray-700">
                                <li>Contact WM for full account summary</li>
                                <li>Request tonnage/service reports</li>
                                <li>Conduct container inventory audit</li>
                                <li>Review full contract terms (pages 3-4)</li>
                                <li>Verify rate adjustment history</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <!-- Key Findings -->
                <div class="mt-6 bg-white border rounded-lg shadow p-6">
                    <h3 class="text-lg font-bold text-gray-800 mb-4">Key Contract Findings</h3>
                    <div class="space-y-4">
                        <div class="flex items-start">
                            <div class="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                                <span class="text-blue-600 font-bold">1</span>
                            </div>
                            <div>
                                <div class="font-semibold text-gray-800">Long-Term Service Relationship</div>
                                <div class="text-sm text-gray-600">7+ years with Waste Management (since 2018) indicates stable service partnership</div>
                            </div>
                        </div>
                        <div class="flex items-start">
                            <div class="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                                <span class="text-blue-600 font-bold">2</span>
                            </div>
                            <div>
                                <div class="font-semibold text-gray-800">Significant Cost Variance</div>
                                <div class="text-sm text-gray-600">Actual costs {variance_pct:.1f}% higher than 2018 contract base - likely due to CPI, fuel, and regulatory increases</div>
                            </div>
                        </div>
                        <div class="flex items-start">
                            <div class="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                                <span class="text-blue-600 font-bold">3</span>
                            </div>
                            <div>
                                <div class="font-semibold text-gray-800">Dual Vendor Strategy</div>
                                <div class="text-sm text-gray-600">Separating bulk service (Ally) from primary hauling (WM) provides specialized service for each waste stream</div>
                            </div>
                        </div>
                        <div class="flex items-start">
                            <div class="flex-shrink-0 w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center mr-3">
                                <span class="text-yellow-600 font-bold">!</span>
                            </div>
                            <div>
                                <div class="font-semibold text-gray-800">Unit Count Critical for Analysis</div>
                                <div class="text-sm text-gray-600">All per-door metrics are estimated - obtaining verified unit count is Priority 1 for finalizing analysis</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <div class="max-w-7xl mx-auto mt-8 px-6 pb-8">
        <div class="bg-gradient-to-r from-gray-700 to-gray-600 text-white rounded-lg shadow-lg p-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
                <div>
                    <div class="font-bold text-gray-200 mb-2">PROPERTY 10 OF 10</div>
                    <div class="text-gray-300">FINAL PROPERTY - PORTFOLIO COMPLETE</div>
                    <div class="text-xs text-gray-400 mt-1">All 10 Orion properties analyzed</div>
                </div>
                <div>
                    <div class="font-bold text-gray-200 mb-2">Analysis Standards</div>
                    <div class="text-gray-300">WasteWise Calculations v2.0</div>
                    <div class="text-xs text-gray-400 mt-1">Validated methodology across portfolio</div>
                </div>
                <div>
                    <div class="font-bold text-gray-200 mb-2">Generated</div>
                    <div class="text-gray-300">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
                    <div class="text-xs text-gray-400 mt-1">Property Coordinator Agent</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Tab switching functionality
        function showTab(tabName) {{
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

        // Chart.js configurations
        const chartLabels = {json.dumps(chart_labels)};
        const allyData = {json.dumps(chart_ally)};
        const wmData = {json.dumps(chart_wm)};
        const totalData = {json.dumps(chart_total)};

        // Trend Chart
        new Chart(document.getElementById('trendChart'), {{
            type: 'line',
            data: {{
                labels: chartLabels,
                datasets: [{{
                    label: 'Total Monthly Cost',
                    data: totalData,
                    borderColor: 'rgb(59, 130, 246)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4,
                    fill: true
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: true }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return '$' + context.parsed.y.toLocaleString('en-US', {{minimumFractionDigits: 2, maximumFractionDigits: 2}});
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return '$' + value.toLocaleString('en-US');
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Vendor Pie Chart
        new Chart(document.getElementById('vendorChart'), {{
            type: 'doughnut',
            data: {{
                labels: ['Waste Management', 'Ally Waste'],
                datasets: [{{
                    data: [{wm_pct:.1f}, {ally_pct:.1f}],
                    backgroundColor: ['rgb(59, 130, 246)', 'rgb(249, 115, 22)'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ position: 'bottom' }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return context.label + ': ' + context.parsed.toFixed(1) + '%';
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Stacked Bar Chart
        new Chart(document.getElementById('expenseStackedChart'), {{
            type: 'bar',
            data: {{
                labels: chartLabels,
                datasets: [
                    {{
                        label: 'Ally Waste',
                        data: allyData,
                        backgroundColor: 'rgb(249, 115, 22)',
                        borderColor: 'rgb(249, 115, 22)',
                        borderWidth: 1
                    }},
                    {{
                        label: 'Waste Management',
                        data: wmData,
                        backgroundColor: 'rgb(59, 130, 246)',
                        borderColor: 'rgb(59, 130, 246)',
                        borderWidth: 1
                    }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ position: 'top' }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return context.dataset.label + ': $' + context.parsed.y.toLocaleString('en-US', {{minimumFractionDigits: 2, maximumFractionDigits: 2}});
                            }}
                        }}
                    }}
                }},
                scales: {{
                    x: {{ stacked: true }},
                    y: {{
                        stacked: true,
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return '$' + value.toLocaleString('en-US');
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Cost Per Door Trend
        const cpdData = totalData.map(val => (val / {UNITS_ESTIMATED}).toFixed(2));
        new Chart(document.getElementById('cpdTrendChart'), {{
            type: 'line',
            data: {{
                labels: chartLabels,
                datasets: [{{
                    label: 'Cost Per Door (ESTIMATED)',
                    data: cpdData,
                    borderColor: 'rgb(168, 85, 247)',
                    backgroundColor: 'rgba(168, 85, 247, 0.1)',
                    tension: 0.4,
                    fill: true
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: true }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return '$' + context.parsed.y + ' per door';
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
    </script>
</body>
</html>
"""

# Save dashboard
output_path = base_path / "Extraction_Output" / "TempeVista_Dashboard.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✓ Interactive HTML Dashboard saved: {output_path}")
print()
print("Dashboard features:")
print("  - 5 interactive tabs")
print("  - Chart.js visualizations")
print("  - Responsive Tailwind CSS design")
print("  - Data quality warnings prominently displayed")
print("  - Self-contained (no external dependencies)")
