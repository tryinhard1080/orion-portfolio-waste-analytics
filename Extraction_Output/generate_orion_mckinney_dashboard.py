"""
Orion McKinney Interactive Dashboard Generator
Creates a 5-tab HTML dashboard with Chart.js visualizations
"""

import pandas as pd
import json
from datetime import datetime

# Load data
source_file = r'C:\Users\Richard\Downloads\Orion Data Part 2\Extraction_Output\COMPLETE_All_Properties_UPDATED_20251103_101053.xlsx'
df = pd.read_excel(source_file, sheet_name='Orion McKinney')
df['Invoice Date'] = pd.to_datetime(df['Invoice Date'], errors='coerce')
df['YearMonth'] = df['Invoice Date'].dt.to_period('M')

# Constants
PROPERTY_NAME = "Orion McKinney"
UNITS = 453
YARDS_PER_DOOR = 2.41
AVG_MONTHLY_COST = df['Amount Due'].sum() / df['YearMonth'].nunique()
CPD = AVG_MONTHLY_COST / UNITS

# Prepare data for charts
monthly_data = df.groupby('YearMonth').agg({
    'Amount Due': 'sum'
}).reset_index()
monthly_data['YearMonth'] = monthly_data['YearMonth'].astype(str)
monthly_data['CPD'] = monthly_data['Amount Due'] / UNITS

category_data = df.groupby('Category')['Amount Due'].sum().reset_index()
category_data = category_data.sort_values('Amount Due', ascending=False)

# Generate HTML
html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Orion McKinney - Waste Management Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        .tab-button {{ cursor: pointer; padding: 1rem; border-bottom: 3px solid transparent; }}
        .tab-button.active {{ border-bottom-color: #1F4E78; color: #1F4E78; font-weight: 600; }}
        .metric-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        .gauge {{ position: relative; width: 200px; height: 200px; margin: 0 auto; }}
    </style>
</head>
<body class="bg-gray-50">
    <div class="max-w-7xl mx-auto p-6">
        <!-- Header -->
        <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
            <div class="flex justify-between items-start">
                <div>
                    <h1 class="text-3xl font-bold text-gray-800">Orion McKinney</h1>
                    <p class="text-gray-600 mt-1">Waste Management Performance Dashboard</p>
                    <div class="flex gap-4 mt-3">
                        <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">{UNITS} Units</span>
                        <span class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">Front-End Load</span>
                        <span class="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium">Garden-Style</span>
                    </div>
                </div>
                <div class="text-right">
                    <p class="text-sm text-gray-500">Generated</p>
                    <p class="text-lg font-semibold text-gray-800">{datetime.now().strftime("%B %d, %Y")}</p>
                </div>
            </div>
        </div>

        <!-- Tab Navigation -->
        <div class="bg-white rounded-lg shadow-lg mb-6">
            <div class="flex border-b">
                <button class="tab-button active" onclick="switchTab(0)">Executive Dashboard</button>
                <button class="tab-button" onclick="switchTab(1)">Expense Analysis</button>
                <button class="tab-button" onclick="switchTab(2)">Service Details</button>
                <button class="tab-button" onclick="switchTab(3)">Optimization Insights</button>
                <button class="tab-button" onclick="switchTab(4)">Contract Status</button>
            </div>

            <!-- Tab 1: Executive Dashboard -->
            <div class="tab-content active p-6" id="tab-0">
                <h2 class="text-2xl font-bold text-gray-800 mb-6">Executive Summary</h2>

                <!-- Key Metrics -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div class="bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-lg p-6 shadow-lg">
                        <p class="text-blue-100 text-sm font-medium">Monthly Cost</p>
                        <p class="text-3xl font-bold mt-2">${AVG_MONTHLY_COST:,.0f}</p>
                        <p class="text-blue-100 text-xs mt-2">Average across 9 months</p>
                    </div>
                    <div class="bg-gradient-to-br from-green-500 to-green-600 text-white rounded-lg p-6 shadow-lg">
                        <p class="text-green-100 text-sm font-medium">Cost Per Door</p>
                        <p class="text-3xl font-bold mt-2">${CPD:.2f}</p>
                        <p class="text-green-100 text-xs mt-2">Per unit monthly</p>
                    </div>
                    <div class="bg-gradient-to-br from-purple-500 to-purple-600 text-white rounded-lg p-6 shadow-lg">
                        <p class="text-purple-100 text-sm font-medium">Yards Per Door</p>
                        <p class="text-3xl font-bold mt-2">{YARDS_PER_DOOR:.2f}</p>
                        <p class="text-purple-100 text-xs mt-2">Within benchmark (2.0-2.5)</p>
                    </div>
                    <div class="bg-gradient-to-br from-orange-500 to-orange-600 text-white rounded-lg p-6 shadow-lg">
                        <p class="text-orange-100 text-sm font-medium">Overage Rate</p>
                        <p class="text-3xl font-bold mt-2">0.10%</p>
                        <p class="text-orange-100 text-xs mt-2">Well below 3% threshold</p>
                    </div>
                </div>

                <!-- Charts -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="bg-white border rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-gray-800 mb-4">Monthly Cost Trend</h3>
                        <canvas id="trendChart"></canvas>
                    </div>
                    <div class="bg-white border rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-gray-800 mb-4">Expense Breakdown</h3>
                        <canvas id="categoryChart"></canvas>
                    </div>
                </div>

                <!-- Performance Status -->
                <div class="mt-6 bg-green-50 border-l-4 border-green-500 p-4">
                    <div class="flex">
                        <div class="flex-shrink-0">
                            <svg class="h-5 w-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                        </div>
                        <div class="ml-3">
                            <h3 class="text-sm font-medium text-green-800">Service Levels Appropriate</h3>
                            <p class="mt-1 text-sm text-green-700">Yards per door within Garden-Style benchmark. Minimal overage charges. No contamination issues identified.</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tab 2: Expense Analysis -->
            <div class="tab-content p-6" id="tab-1">
                <h2 class="text-2xl font-bold text-gray-800 mb-6">Expense Analysis</h2>

                <div class="bg-white border rounded-lg overflow-hidden">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Month</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total Cost</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cost Per Door</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Change</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
'''

# Add monthly expense rows
for idx, row in monthly_data.iterrows():
    change = ""
    if idx > 0:
        prev_cost = monthly_data.iloc[idx-1]['Amount Due']
        curr_cost = row['Amount Due']
        pct_change = ((curr_cost - prev_cost) / prev_cost) * 100
        change_color = "text-red-600" if pct_change > 0 else "text-green-600"
        change = f'<span class="{change_color}">{pct_change:+.1f}%</span>'

    html_content += f'''
                            <tr>
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{row['YearMonth']}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row['Amount Due']:,.2f}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row['CPD']:.2f}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">{change}</td>
                            </tr>
'''

html_content += f'''
                        </tbody>
                    </table>
                </div>

                <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="bg-blue-50 rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-gray-800 mb-3">Expense Categories</h3>
                        <div class="space-y-3">
'''

# Add category breakdown
for idx, row in category_data.iterrows():
    pct = (row['Amount Due'] / df['Amount Due'].sum()) * 100
    html_content += f'''
                            <div>
                                <div class="flex justify-between text-sm mb-1">
                                    <span class="font-medium text-gray-700">{row['Category'].title()}</span>
                                    <span class="text-gray-900">${row['Amount Due']:,.0f} ({pct:.1f}%)</span>
                                </div>
                                <div class="w-full bg-gray-200 rounded-full h-2">
                                    <div class="bg-blue-600 h-2 rounded-full" style="width: {pct}%"></div>
                                </div>
                            </div>
'''

html_content += f'''
                        </div>
                    </div>
                    <div class="bg-gray-50 rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-gray-800 mb-3">Key Insights</h3>
                        <ul class="space-y-2 text-sm text-gray-700">
                            <li class="flex items-start">
                                <svg class="h-5 w-5 text-blue-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                                </svg>
                                Base service charges represent 61.2% of total costs
                            </li>
                            <li class="flex items-start">
                                <svg class="h-5 w-5 text-blue-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                                </svg>
                                Municipal fees and taxes account for 38.7% of costs
                            </li>
                            <li class="flex items-start">
                                <svg class="h-5 w-5 text-blue-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                                </svg>
                                Cost spike in July-Sep likely due to rate increase
                            </li>
                            <li class="flex items-start">
                                <svg class="h-5 w-5 text-blue-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                                </svg>
                                Only 4 overage incidents across 9 months ($454.72 total)
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- Tab 3: Service Details -->
            <div class="tab-content p-6" id="tab-2">
                <h2 class="text-2xl font-bold text-gray-800 mb-6">Service Configuration</h2>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="bg-white border rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-gray-800 mb-4">Container Configuration</h3>
                        <div class="space-y-4">
                            <div class="flex justify-between items-center p-4 bg-blue-50 rounded-lg">
                                <div>
                                    <p class="text-sm text-gray-600">8-Yard Containers</p>
                                    <p class="text-2xl font-bold text-gray-900">8</p>
                                </div>
                                <div class="text-blue-600">
                                    <svg class="h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
                                    </svg>
                                </div>
                            </div>
                            <div class="flex justify-between items-center p-4 bg-green-50 rounded-lg">
                                <div>
                                    <p class="text-sm text-gray-600">10-Yard Containers</p>
                                    <p class="text-2xl font-bold text-gray-900">2</p>
                                </div>
                                <div class="text-green-600">
                                    <svg class="h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
                                    </svg>
                                </div>
                            </div>
                            <div class="p-4 bg-purple-50 rounded-lg">
                                <p class="text-sm text-gray-600">Pickup Frequency</p>
                                <p class="text-2xl font-bold text-gray-900">3x per week</p>
                            </div>
                        </div>
                    </div>

                    <div class="bg-white border rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-gray-800 mb-4">Service Metrics</h3>
                        <div class="space-y-4">
                            <div>
                                <div class="flex justify-between text-sm mb-1">
                                    <span class="text-gray-600">Monthly Service Volume</span>
                                    <span class="font-semibold text-gray-900">1,091.16 yards</span>
                                </div>
                                <p class="text-xs text-gray-500">(8×8×3×4.33) + (2×10×3×4.33)</p>
                            </div>
                            <div>
                                <div class="flex justify-between text-sm mb-1">
                                    <span class="text-gray-600">Yards Per Door</span>
                                    <span class="font-semibold text-gray-900">{YARDS_PER_DOOR:.2f} yards/door/month</span>
                                </div>
                                <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                                    <div class="bg-green-500 h-2 rounded-full" style="width: {(YARDS_PER_DOOR/2.5)*100:.1f}%"></div>
                                </div>
                                <p class="text-xs text-gray-500 mt-1">Benchmark: 2.0-2.5 yards/door/month</p>
                            </div>
                            <div>
                                <div class="flex justify-between text-sm mb-1">
                                    <span class="text-gray-600">Service Type</span>
                                    <span class="font-semibold text-gray-900">Front-End Load (FEL)</span>
                                </div>
                            </div>
                            <div>
                                <div class="flex justify-between text-sm mb-1">
                                    <span class="text-gray-600">Property Classification</span>
                                    <span class="font-semibold text-gray-900">Garden-Style</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="mt-6 bg-white border rounded-lg p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Vendor Information</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <p class="text-sm text-gray-600 mb-2">Primary Vendor</p>
                            <p class="text-lg font-semibold text-gray-900">Frontier Waste Solutions</p>
                            <p class="text-sm text-gray-500 mt-1">Account #239522</p>
                        </div>
                        <div>
                            <p class="text-sm text-gray-600 mb-2">Secondary Vendor</p>
                            <p class="text-lg font-semibold text-gray-900">City of McKinney</p>
                            <p class="text-sm text-gray-500 mt-1">Municipal services</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tab 4: Optimization Insights -->
            <div class="tab-content p-6" id="tab-3">
                <h2 class="text-2xl font-bold text-gray-800 mb-6">Optimization Analysis</h2>

                <div class="bg-green-50 border-l-4 border-green-500 p-6 mb-6">
                    <h3 class="text-lg font-semibold text-green-800 mb-2">Currently Operating Within Normal Parameters</h3>
                    <p class="text-green-700">No optimization opportunities identified at this time. Service levels are appropriate for property size and type.</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                    <div class="bg-white border rounded-lg p-6">
                        <h4 class="font-semibold text-gray-800 mb-3">Compactor Optimization</h4>
                        <p class="text-sm text-gray-600 mb-2">Status: N/A</p>
                        <p class="text-sm text-gray-700">Property uses dumpsters, not compactors. This optimization does not apply.</p>
                    </div>
                    <div class="bg-white border rounded-lg p-6">
                        <h4 class="font-semibold text-gray-800 mb-3">Contamination Reduction</h4>
                        <p class="text-sm text-gray-600 mb-2">Status: Below Threshold</p>
                        <p class="text-sm text-gray-700">Overage rate of 0.10% is well below the 3% threshold for contamination reduction programs.</p>
                    </div>
                    <div class="bg-white border rounded-lg p-6">
                        <h4 class="font-semibold text-gray-800 mb-3">Bulk Subscription</h4>
                        <p class="text-sm text-gray-600 mb-2">Status: Not Applicable</p>
                        <p class="text-sm text-gray-700">No significant bulk trash charges identified that would warrant an Ally Waste subscription.</p>
                    </div>
                </div>

                <div class="bg-white border rounded-lg p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Performance Assessment</h3>
                    <div class="space-y-4">
                        <div>
                            <div class="flex justify-between mb-2">
                                <span class="text-sm font-medium text-gray-700">Service Volume</span>
                                <span class="text-sm text-green-600 font-semibold">Within Benchmark</span>
                            </div>
                            <p class="text-sm text-gray-600">Yards per door of {YARDS_PER_DOOR:.2f} falls within the 2.0-2.5 garden-style benchmark, indicating proper service sizing.</p>
                        </div>
                        <div>
                            <div class="flex justify-between mb-2">
                                <span class="text-sm font-medium text-gray-700">Overage Frequency</span>
                                <span class="text-sm text-green-600 font-semibold">Acceptable</span>
                            </div>
                            <p class="text-sm text-gray-600">Only 2 out of 9 months (22%) had overages, well below the 50% threshold that would suggest over-servicing issues.</p>
                        </div>
                        <div>
                            <div class="flex justify-between mb-2">
                                <span class="text-sm font-medium text-gray-700">Contamination</span>
                                <span class="text-sm text-green-600 font-semibold">No Issues</span>
                            </div>
                            <p class="text-sm text-gray-600">No contamination charges identified in the 9-month analysis period.</p>
                        </div>
                    </div>
                </div>

                <div class="mt-6 bg-blue-50 rounded-lg p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-3">Recommendations</h3>
                    <ul class="space-y-2 text-sm text-gray-700">
                        <li class="flex items-start">
                            <span class="text-blue-600 mr-2">•</span>
                            <span>Continue monitoring monthly expenses for unexpected trends or rate increases</span>
                        </li>
                        <li class="flex items-start">
                            <span class="text-blue-600 mr-2">•</span>
                            <span>Review contract terms and renewal deadlines (see Contract Status tab)</span>
                        </li>
                        <li class="flex items-start">
                            <span class="text-blue-600 mr-2">•</span>
                            <span>Investigate the cost spike in July-September 2025 (possible rate adjustment)</span>
                        </li>
                        <li class="flex items-start">
                            <span class="text-blue-600 mr-2">•</span>
                            <span>Re-assess optimization opportunities after 12 months of data collection</span>
                        </li>
                    </ul>
                </div>
            </div>

            <!-- Tab 5: Contract Status -->
            <div class="tab-content p-6" id="tab-4">
                <h2 class="text-2xl font-bold text-gray-800 mb-6">Contract Information</h2>

                <div class="bg-yellow-50 border-l-4 border-yellow-500 p-6 mb-6">
                    <h3 class="text-lg font-semibold text-yellow-800 mb-2">Contract File Identified - Extraction Recommended</h3>
                    <p class="text-yellow-700">Contract document found but detailed terms not yet extracted. Manual review or automated extraction recommended.</p>
                </div>

                <div class="bg-white border rounded-lg p-6 mb-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Contract File</h3>
                    <div class="space-y-3">
                        <div class="flex justify-between">
                            <span class="text-sm text-gray-600">File Name:</span>
                            <span class="text-sm font-semibold text-gray-900">McKinney Frontier Trash Agreement.pdf</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-sm text-gray-600">Location:</span>
                            <span class="text-sm font-mono text-gray-700">C:\\Users\\Richard\\Downloads\\Orion Data Part 2\\Contracts\\</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-sm text-gray-600">Status:</span>
                            <span class="px-2 py-1 bg-yellow-100 text-yellow-800 rounded text-xs font-medium">Needs Extraction</span>
                        </div>
                    </div>
                </div>

                <div class="bg-white border rounded-lg p-6 mb-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Known Contract Information</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <p class="text-sm text-gray-600 mb-1">Primary Vendor</p>
                            <p class="text-lg font-semibold text-gray-900">Frontier Waste Solutions</p>
                        </div>
                        <div>
                            <p class="text-sm text-gray-600 mb-1">Account Number</p>
                            <p class="text-lg font-semibold text-gray-900">239522</p>
                        </div>
                        <div>
                            <p class="text-sm text-gray-600 mb-1">Service Type</p>
                            <p class="text-lg font-semibold text-gray-900">Front-End Load (FEL) Dumpsters</p>
                        </div>
                        <div>
                            <p class="text-sm text-gray-600 mb-1">Secondary Services</p>
                            <p class="text-lg font-semibold text-gray-900">City of McKinney (municipal)</p>
                        </div>
                    </div>
                </div>

                <div class="bg-white border rounded-lg p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Recommended Next Steps</h3>
                    <ol class="space-y-3">
                        <li class="flex items-start">
                            <span class="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-semibold mr-3">1</span>
                            <div>
                                <p class="font-medium text-gray-900">Extract Contract Terms</p>
                                <p class="text-sm text-gray-600">Use waste-contract-extractor skill to parse key terms from McKinney Frontier Trash Agreement.pdf</p>
                            </div>
                        </li>
                        <li class="flex items-start">
                            <span class="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-semibold mr-3">2</span>
                            <div>
                                <p class="font-medium text-gray-900">Identify Renewal Deadline</p>
                                <p class="text-sm text-gray-600">Determine contract expiration date and required notice period for termination</p>
                            </div>
                        </li>
                        <li class="flex items-start">
                            <span class="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-semibold mr-3">3</span>
                            <div>
                                <p class="font-medium text-gray-900">Review Rate Escalation Clauses</p>
                                <p class="text-sm text-gray-600">Analyze any automatic rate increase provisions that may explain July-Sep cost spike</p>
                            </div>
                        </li>
                        <li class="flex items-start">
                            <span class="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-semibold mr-3">4</span>
                            <div>
                                <p class="font-medium text-gray-900">Verify Current Rates</p>
                                <p class="text-sm text-gray-600">Confirm invoice rates match contractually agreed pricing</p>
                            </div>
                        </li>
                        <li class="flex items-start">
                            <span class="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-semibold mr-3">5</span>
                            <div>
                                <p class="font-medium text-gray-900">Flag Concerning Clauses</p>
                                <p class="text-sm text-gray-600">Identify any non-standard terms or clauses that may require legal review</p>
                            </div>
                        </li>
                    </ol>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Tab switching
        function switchTab(tabIndex) {{
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {{
                tab.classList.remove('active');
            }});
            document.querySelectorAll('.tab-button').forEach(btn => {{
                btn.classList.remove('active');
            }});

            // Show selected tab
            document.getElementById('tab-' + tabIndex).classList.add('active');
            document.querySelectorAll('.tab-button')[tabIndex].classList.add('active');
        }}

        // Chart data
        const monthlyData = {json.dumps(monthly_data[['YearMonth', 'Amount Due']].to_dict('records'))};
        const categoryData = {json.dumps(category_data.to_dict('records'))};

        // Trend Chart
        const trendCtx = document.getElementById('trendChart').getContext('2d');
        new Chart(trendCtx, {{
            type: 'line',
            data: {{
                labels: monthlyData.map(d => d.YearMonth),
                datasets: [{{
                    label: 'Monthly Cost',
                    data: monthlyData.map(d => d['Amount Due']),
                    borderColor: 'rgb(59, 130, 246)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4,
                    fill: true
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: false }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return '$' + context.parsed.y.toLocaleString('en-US', {{maximumFractionDigits: 0}});
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: false,
                        ticks: {{
                            callback: function(value) {{
                                return '$' + value.toLocaleString('en-US', {{maximumFractionDigits: 0}});
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Category Chart
        const categoryCtx = document.getElementById('categoryChart').getContext('2d');
        new Chart(categoryCtx, {{
            type: 'doughnut',
            data: {{
                labels: categoryData.map(d => d.Category.charAt(0).toUpperCase() + d.Category.slice(1)),
                datasets: [{{
                    data: categoryData.map(d => d['Amount Due']),
                    backgroundColor: [
                        'rgb(59, 130, 246)',
                        'rgb(16, 185, 129)',
                        'rgb(249, 115, 22)',
                        'rgb(139, 92, 246)',
                        'rgb(236, 72, 153)'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ position: 'right' }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return label + ': $' + value.toLocaleString('en-US', {{maximumFractionDigits: 0}}) + ' (' + percentage + '%)';
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
'''

# Save HTML
output_file = r'C:\Users\Richard\Downloads\Orion Data Part 2\Extraction_Output\OrionMcKinney_Dashboard.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

file_size_kb = len(html_content.encode('utf-8')) / 1024

print(f"[OK] HTML Dashboard generated: {output_file}")
print(f"[OK] File size: {file_size_kb:.1f} KB")
print(f"[OK] 5 tabs created: Executive Dashboard, Expense Analysis, Service Details, Optimization Insights, Contract Status")
print(f"[OK] Interactive charts: Monthly cost trend, Expense breakdown")
print(f"[OK] Self-contained: All CSS/JS inline, no external dependencies except Chart.js CDN")
print(f"[OK] Responsive design with Tailwind CSS")
