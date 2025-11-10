# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Orion Portfolio Waste Management Analytics System (Version 3.0 - Property-Centric Structure)** - A fact-based waste management performance monitoring and reporting platform for 10 garden-style apartment properties (6 in TX/FL, 4 in AZ). The system extracts real data from invoices and contracts, consolidates it into a master Excel file, and generates performance reports based on actual spend and service utilization.

**Portfolio Context:** This is an Orion portfolio managed by Greystar, one of the largest multifamily property management companies. The waste management optimization approach follows Greystar's operational standards and industry best practices.

**Key Technologies:**
- Python 3.8+ for data extraction and report generation
- Excel as single source of truth for all property data
- AI-powered invoice extraction using Claude Vision API
- Fact-based performance analysis and benchmarking
- Property-centric folder organization

## Critical Path Information

**IMPORTANT - Dropbox Migration:** Do NOT run, save, or operate in any path containing "dropbox". All data has been migrated to create better system performance. If you encounter a dropbox path, flag the user to change directories.

**Current Working Directory:** `C:\Users\Richard\Downloads\Orion Data Part 2`

**Master Data File:** `Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx`
- **Single Source of Truth** for all property data
- **10 Properties:** All TX, FL, and AZ properties
- **894 Invoice Line Items:** Complete extraction from all invoices
- **17 Tabs:** 7 summary tabs + 10 property-specific tabs

## CALCULATION STANDARDS (MANDATORY)

**CRITICAL:** All waste management calculations MUST comply with official project standards.

**Reference Document:** `Documentation/CONTAINER_SPECIFICATIONS_AND_CALCULATION_STANDARDS.md`

**Official Formulas:**

**Yards Per Door (Dumpster Service):**
```
YPD = (Container Size × Num Containers × Pickups/Week × 4.33) / Units
```

**Yards Per Door (Compactor Service):**
```
YPD = (Total Tons × 2000 / 138) / Units
```
- **138 lbs/yd³:** EPA/ENERGY STAR standard density for loose MSW
- **Already accounts for 3:1 compaction ratio**
- **DO NOT use 225 lbs/yd³ or 14.49 shortcut in official calculations**

**Industry Benchmarks:**
- Garden-style: 2.0-2.5 yards/door/month (existing), 2.0-2.25 (new build)
- Mid-rise: 1.5-2.0 yards/door/month (existing), ~1.5 (new build)
- High-rise: 1.0-1.5 yards/door/month (existing & new build)

**All scripts, skills, and workbooks must reference these standards.**

## Folder Structure (Property-Centric Organization)

```
Orion Data Part 2/
│
├── Properties/                        # Property-centric organization (10 properties)
│   ├── Orion_Prosper/
│   │   ├── Invoices/                 # All invoices for this property
│   │   ├── Reports/                  # Generated reports (Excel, HTML, validation)
│   │   ├── Contracts/                # Service contracts and agreements
│   │   ├── Documentation/            # Property-specific notes
│   │   └── README.md                 # Property information and guide
│   │
│   ├── Orion_Prosper_Lakes/
│   ├── Orion_McKinney/
│   ├── McCord_Park_FL/
│   ├── The_Club_at_Millenia/
│   ├── Bella_Mirage/
│   ├── Mandarina/
│   ├── Pavilions_at_Arrowhead/
│   ├── Springs_at_Alta_Mesa/
│   └── Tempe_Vista/
│       └── (same structure as Orion_Prosper)
│
├── Portfolio_Reports/                 # Portfolio-wide reports and master data
│   ├── MASTER_Portfolio_Complete_Data.xlsx  # ⭐ SINGLE SOURCE OF TRUTH
│   └── README.md                     # Master file documentation
│
├── Code/                              # Python scripts
│   ├── agent_prompts.py              # LLM prompts for extraction
│   ├── orchestrate_extraction.py     # Extraction workflow orchestration
│   ├── validate_extracted_data.py    # Data validation
│   ├── reorganize_folder_structure.py # Folder reorganization script
│   ├── create_property_readmes.py    # README generation script
│   └── templates/                    # Jinja2 HTML templates
│       ├── portfolio_summary.html
│       └── property_detail.html
│
├── Documentation/                     # Project documentation
│   ├── DATA_INTEGRITY_GUIDE.md       # Data quality standards
│   ├── SUBAGENT_EXTRACTION_STRATEGY.md    # Extraction workflow guide
│   ├── SUBAGENT_QUICK_START.md            # Quick start for extraction
│   ├── REPORT_CORRECTION_SUMMARY.md       # Language validation rules
│   └── REPORT_CRITERIA_ANALYSIS.md        # Report quality standards
│
├── Archive/                           # Old files (not for active use)
│   ├── Old_Scripts/
│   ├── Old_Extraction_Files/
│   └── Temporary_Files/
│
├── .env.example                      # Configuration template
├── requirements.txt                  # Python dependencies
├── CLAUDE.md                         # This file
└── README.md                         # Project overview
```

## Environment Setup

### Python Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment (if needed for API keys)
cp .env.example .env
# Edit .env and add your API keys if needed
```

### Key Dependencies
- `jinja2` - HTML templating
- `google-auth` - Google API authentication (optional)
- `google-auth-oauthlib` - OAuth flow (optional)
- `google-auth-httplib2` - HTTP transport (optional)
- `google-api-python-client` - Google Sheets API (optional)
- `python-dotenv` - Environment management
- `pandas` - Data processing
- `pdfplumber` - PDF text extraction
- `requests` - HTTP requests

## Python Script Architecture

### Core Report Generation
**`generate_reports_from_sheets.py`**
- Main report generator
- Reads from Excel master file: `Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx`
- Generates HTML reports for all 10 properties
- Uses Jinja2 templates in `Code/templates/`
- Output: `Reports/{PropertyName}Analysis.html`

**`generate_reports_from_sheets_data.py`**
- Legacy fallback script (deprecated)
- Previously used when Google Sheets API unavailable
- Use Excel master file instead

**`generate_contract_reports.py`**
- Generates contract comparison analysis for each property
- Output: `Reports/Contract_Comparison/{PropertyName}_Report.html`

### Validation & Quality Assurance
**`validate_reports.py`**
- **CRITICAL** - Run before distributing reports
- Validates language (no "savings" language)
- Validates data accuracy
- Checks HTML structure

**`comprehensive_validation.py`**
- Extended validation across all data sources
- Cross-references invoice data with Excel master file

**`validate_extracted_data.py`**
- Validates extracted invoice data quality
- Checks field completeness and accuracy

### Invoice Extraction (AI-Powered)
**`orchestrate_extraction.py`**
- Orchestrates invoice extraction using AI subagents
- Coordinates multi-step extraction workflow
- See `Documentation/SUBAGENT_EXTRACTION_STRATEGY.md` for details

**`extract_orion_prosper_invoices.py`**
- Example property-specific extraction script
- Template for creating property extractors

**`agent_prompts.py`**
- LLM prompts for extraction assistance
- Structured prompts for field extraction
- Validation prompts

**`update_google_sheets.py`**
- Legacy script - updates Google Sheets (if still used for syncing)
- Primarily update Excel master file directly now
- Batch upload capability, validates before uploading

### PDF Conversion
**`convert_to_pdf_puppeteer.py`**
- Converts HTML reports to PDF using Puppeteer MCP
- Recommended for production use

## Core Commands

### Generate All Reports

```bash
# Generate performance reports (portfolio + 6 properties)
python Code/generate_reports_from_sheets.py

# Generate contract comparison reports (6 properties)
python Code/generate_contract_reports.py

# Validate all reports (CRITICAL before distribution)
python Code/validate_reports.py

# Convert to PDF (optional)
python Code/convert_to_pdf_puppeteer.py
```

### Invoice Extraction Workflow

```bash
# 1. Extract data from invoices using AI subagents
python Code/orchestrate_extraction.py

# 2. Validate extracted data
python Code/validate_extracted_data.py

# 3. Update Excel master file with validated data
# Manually update Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx
# Or use update_google_sheets.py if syncing to Google Sheets

# 4. Regenerate reports with new data
python Code/generate_reports_from_sheets.py
```

**See `Documentation/SUBAGENT_EXTRACTION_STRATEGY.md` for complete extraction workflow.**

## Data Source: Master Excel File

**Primary Data Source:** `Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx`

This is the **SINGLE SOURCE OF TRUTH** for all property data.

### Master File Structure

**17 Tabs Total:**

**Summary/Analysis Tabs (7):**
1. Executive Summary - Portfolio overview and key metrics
2. Property Overview - All 10 properties comparison
3. Spend Summary - Total spend by property
4. Spend by Category - Breakdown of service categories
5. Service Details - Container types, sizes, frequencies
6. Yards Per Door - YPD calculations for all properties
7. Contract Terms - Contract status and renewal dates

**Property-Specific Tabs (10):**
8. Orion Prosper - 95 invoice line items
9. McCord Park FL - 42 invoice line items
10. Orion McKinney - 95 invoice line items
11. The Club at Millenia - 146 invoice line items
12. Bella Mirage - 102 invoice line items
13. Orion Prosper Lakes - 104 invoice line items
14. Mandarina - 37 invoice line items
15. Pavilions at Arrowhead - 47 invoice line items
16. Springs at Alta Mesa - 203 invoice line items
17. Tempe Vista - 23 invoice line items

**Total Invoice Line Items:** 894

### How to Use the Master File

**For Report Generation:**
- Your Claude skill reads from this file to generate property reports
- All calculations based on real invoice data in property tabs
- Summary tabs provide portfolio-wide insights

**For Data Updates:**
1. Extract new invoice data using extraction workflow
2. Update appropriate property tab in master file
3. Regenerate reports using Claude skill

**For Analysis:**
- Review Executive Summary for portfolio overview
- Compare properties in Property Overview tab
- Analyze spend trends in Spend Summary tab
- Drill into property tabs for detailed invoice data

## Key Property Data (Current)

### All 10 Properties - Portfolio Overview

**Texas/Florida Properties (6):**

| Property | Units | Location | Vendor | Service Type |
|----------|-------|----------|--------|--------------|
| **Orion Prosper** | 312 | Prosper, TX | Republic Services | FEL Dumpsters |
| **Orion Prosper Lakes** | 308 | Prosper, TX | Republic Services | Compactor |
| **Orion McKinney** | 453 | McKinney, TX | Frontier Waste | FEL Dumpsters |
| **McCord Park FL** | 416 | Florida | Community Waste | Dumpster |
| **The Club at Millenia** | 560 | Orlando, FL | Waste Connections | Compactor |
| **Bella Mirage** | 715 | Phoenix, AZ | Waste Management | Dumpster |

**Arizona Properties (4):**

| Property | Units | Location | Vendor | Service Type |
|----------|-------|----------|--------|--------------|
| **Mandarina** | 180 | Phoenix, AZ | WM + Ally Waste | Compactor + Bulk |
| **Pavilions at Arrowhead** | TBD | Glendale, AZ | City + Ally Waste | Mixed |
| **Springs at Alta Mesa** | 200 | Mesa, AZ | City + Ally Waste | Dumpster + Bulk |
| **Tempe Vista** | 150* | Tempe, AZ | WM + Ally Waste | Mixed |

*Estimated - needs verification

**Portfolio Totals:**
- **Total Units:** 3,578 (verified for 9 properties)
- **Total Properties:** 10
- **Annual Spend:** ~$662K (based on extracted invoice data)

**Property Constants (for code):**
```python
PROPERTIES = {
    # Texas/Florida
    'Orion Prosper': {'units': 312, 'state': 'TX'},
    'Orion Prosper Lakes': {'units': 308, 'state': 'TX'},
    'Orion McKinney': {'units': 453, 'state': 'TX'},
    'McCord Park FL': {'units': 416, 'state': 'FL'},
    'The Club at Millenia': {'units': 560, 'state': 'FL'},
    'Bella Mirage': {'units': 715, 'state': 'AZ'},
    # Arizona
    'Mandarina': {'units': 180, 'state': 'AZ'},
    'Pavilions at Arrowhead': {'units': None, 'state': 'AZ'},  # TBD
    'Springs at Alta Mesa': {'units': 200, 'state': 'AZ'},
    'Tempe Vista': {'units': 150, 'state': 'AZ'},  # Estimated
}
```

## Performance Metrics

### Key Performance Indicators (KPIs)

**Yards Per Door (YPD):**
- Measures service container capacity per unit
- Target: 2.0 - 2.25 yards/door
- Threshold: ≤ 2.75 yards/door
- Lower is better (more efficient service sizing)

**Cost Per Door (CPD):**
- Monthly waste cost per apartment unit
- Target: $20 - $30 per door
- Threshold: ≤ $30 per door
- Lower is better (cost efficiency)

**Overage Frequency:**
- Percentage of months with extra pickups beyond contract
- Target: ≤ 15%
- Threshold: ≤ 50%
- Lower is better (service right-sizing)

### Performance Tiers

- 🟢 **Good:** 80-100 points
- 🟡 **Average:** 60-79 points
- 🔴 **Poor:** 0-59 points

### Scoring Calculation

```
Portfolio Score (0-100) = Weighted Average of Property Scores

Property Score = (YPD Score × 35%) + (CPD Score × 40%) + (Overage Score × 25%)
```

## Report Generation Details

### Templates

**Portfolio Summary Template** (`Code/templates/portfolio_summary.html`)
- Overview dashboard with all 6 properties
- Portfolio-level metrics and totals
- Performance comparison across properties
- Key insights and trends

**Property Detail Template** (`Code/templates/property_detail.html`)
- Individual property deep-dive
- Service details and contract information
- Performance metrics vs. benchmarks
- Month-over-month trends
- Focus areas and recommendations

### Report Content

**Each Report Includes:**
1. **Property Information** - Name, location, unit count, service type
2. **Performance Metrics** - CPD, YPD, overage frequency, overall score
3. **Financial Summary** - Monthly costs, year-to-date totals
4. **Analysis & Insights** - Performance status, benchmark comparison, trends

## Validation Criteria

### Language Validation

**PROHIBITED TERMS** (Do not use in reports):
- "cost savings"
- "savings opportunity"
- "reduce costs by"
- "save $X per month"
- "potential savings"

**REQUIRED APPROACH:**
- Focus on "performance gaps"
- Use "cost efficiency opportunity"
- Describe "areas for improvement"
- Provide "benchmark comparison"

**See `Documentation/REPORT_CORRECTION_SUMMARY.md` for complete validation rules.**

### Data Validation

**Required Checks:**
- Unit counts match Excel master file data
- CPD calculations accurate (Monthly Cost ÷ Units)
- Performance scores within 0-100 range
- All 10 properties included in portfolio summary
- Portfolio totals calculated correctly

## Invoice Extraction Workflow

The system uses AI subagents to extract invoice data. See `Documentation/SUBAGENT_EXTRACTION_STRATEGY.md` for complete details.

### Quick Start

1. **Place invoices** in `Properties/{PropertyName}/Invoices/` folder
2. **Run extraction** using `python Code/orchestrate_extraction.py`
3. **Validate data** using `python Code/validate_extracted_data.py`
4. **Update Excel master file** - manually add data to `Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx`
5. **Regenerate reports** using `python Code/generate_reports_from_sheets.py`

### Extraction Strategy

The subagent extraction system:
- Uses specialized AI agents for different extraction tasks
- Validates extracted data automatically
- Provides confidence scores for extracted fields
- Handles multiple invoice formats
- See `Documentation/SUBAGENT_QUICK_START.md` for detailed guide

## Available Claude Skills

The project has access to specialized Claude skills for waste management analysis. Skills are installed in `.claude/skills/` directory.

### Active Skills (6)

**1. wastewise-analytics-validated**
- Complete WasteWise analysis with comprehensive validation framework
- Ensures contract tabs, optimization criteria, formula accuracy, data completeness
- Quality-scored evaluation with validation report
- Use for standard waste management analysis with quality assurance

**2. wastewise-regulatory** ⭐ NEW
- Enhanced WasteWise analysis + automated regulatory compliance research
- Researches local waste/recycling/organics ordinances
- Documents penalties, enforcement, licensed haulers
- Generates property-specific compliance checklists
- Confidence scoring (HIGH/MEDIUM/LOW) for research quality
- Use when you need waste analysis AND regulatory compliance documentation

**3. compactor-optimization**
- Specialized compactor performance analysis (NOT open tops)
- Calculates yards per door for compacted service (0.08-0.15 target)
- Identifies over-servicing and optimization opportunities
- Use for properties with compactor service

**4. waste-batch-extractor**
- Batch process multiple invoices using Claude Vision API
- Creates location-specific Excel tabs with validation reports
- Use for processing many invoices at once

**5. waste-contract-extractor**
- Extract critical data from waste service contracts (PDF/Word/scanned)
- Parses pricing, terms, service specifications
- Use when analyzing contract documents

**6. waste-visual-reporter**
- Generate interactive HTML dashboards with Chart.js visualizations
- 5 tabs: Dashboard, Expense Analysis, Haul Log, Optimization, Contract Terms
- Use for stakeholder presentations and visual reports

### When to Use Skills

**Use wastewise-regulatory when:**
- Property needs regulatory compliance documentation
- Local ordinances (recycling/composting mandates) apply
- Client wants to verify compliance with city/county requirements
- Need licensed hauler directory for location

**Use wastewise-analytics-validated when:**
- Standard waste analysis without regulatory research
- Quality assurance is critical
- Need validation report for client confidence

**Use specialized skills (compactor-optimization, etc.) when:**
- Focused analysis of specific service type
- Quick assessment without full validation suite
- Specialized output format needed (HTML dashboards, etc.)

## Slash Commands

The project includes 12 custom slash commands for streamlined workflows.

### Quick Reference

**Script Wrappers** (wrap existing Python scripts):
- `/generate-reports` - Generate all performance and contract reports
- `/validate-all` - Validate reports for language and data accuracy
- `/extract-invoices` - Extract data from invoice PDFs (AI subagents)
- `/update-sheets` - Upload extracted data to Google Sheets
- `/convert-to-pdf` - Convert HTML reports to PDF

**Skill-Based Commands** (use installed Claude skills):
- `/batch-extract` - Batch extraction using Claude Vision API
- `/extract-contracts` - Extract contract terms and dates
- `/optimize-compactor [property]` - Compactor optimization analysis

**Workflow Orchestration** (multi-step automated workflows):
- `/monthly-workflow` - Complete monthly processing cycle
- `/quick-report [property]` - Single property analysis
- `/full-analysis` - Comprehensive portfolio analysis

**Data Quality**:
- `/review-flags` - Interactive flag resolution for extraction data

### Command Categories

**When to use Python scripts directly:**
- Production workflows
- Automated scheduling
- Custom modifications needed
- Scripting and automation

**When to use slash commands:**
- Interactive sessions
- Learning the system
- Quick ad-hoc analyses
- Guided multi-step processes
- Data quality review

**When to use skill commands:**
- Alternative extraction methods (Vision API)
- Excel output needed
- Parallel batch processing
- Optimization analysis
- Contract term extraction

### Command Details

All slash command specifications are in `.claude/commands/` directory.
Each command includes:
- What it does
- How to execute it
- When to use it
- Expected output
- Related commands

See individual command files for complete documentation.

## Common Workflows

### Complete Report Generation Workflow

```bash
# 1. Generate all performance reports
python Code/generate_reports_from_sheets.py

# 2. Generate contract comparison reports
python Code/generate_contract_reports.py

# 3. Validate all reports (CRITICAL before distribution)
python Code/validate_reports.py

# 4. (Optional) Convert to PDF
python Code/convert_to_pdf_puppeteer.py
```

**OR use slash command:**

```bash
/generate-reports   # Runs steps 1-2
/validate-all       # Runs step 3
/convert-to-pdf     # Runs step 4
```

### Monthly Operations Workflow

1. **Collect New Invoices**
   - Save PDFs to `Invoices/{PropertyName}/` folders

2. **Extract Invoice Data**
   ```bash
   python Code/orchestrate_extraction.py
   python Code/validate_extracted_data.py
   ```

3. **Update Data Source**
   ```bash
   # Manually update Excel master file: Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx
   # Add extracted invoice data to appropriate property tab
   ```

4. **Regenerate All Reports**
   ```bash
   python Code/generate_reports_from_sheets.py
   python Code/generate_contract_reports.py
   ```

5. **Validate & Distribute**
   ```bash
   python Code/validate_reports.py
   # Review reports in Reports/ folder
   # Share with stakeholders
   ```

### Updating Property Data

**To Update Property Information:**
1. Open Excel master file: `Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx`
2. Navigate to appropriate tab (Property Overview or specific property tab)
3. Update relevant cells (units, costs, service details, invoice line items)
4. Save Excel file
5. Regenerate reports: `python Code/generate_reports_from_sheets.py`

**Example: Update Unit Count**
- Open MASTER_Portfolio_Complete_Data.xlsx
- Find property in "Property Overview" tab
- Update unit count in appropriate column
- Recalculate YPD/CPD formulas if needed
- Save file and regenerate reports

## Troubleshooting

### Report Generation Issues

**Problem:** Script fails to run
- **Check:** Python environment activated
- **Check:** Dependencies installed (`pip install -r requirements.txt`)
- **Check:** Working directory is correct

**Problem:** Reports not updating
- **Check:** Excel master file has been saved with latest data
- **Check:** Script completed without errors
- **Check:** Reports saved to `Reports/` folder

**Problem:** Data doesn't match expectations
- **Check:** Excel master file `MASTER_Portfolio_Complete_Data.xlsx` has latest data
- **Check:** Script is reading from correct Excel file path
- **Check:** Property names match exactly between Excel tabs and script

### Excel File Access

**Problem:** Cannot open or read Excel file
- **Check:** File path is correct: `Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx`
- **Check:** File is not currently open in Excel (can cause read locks)
- **Check:** Required Python packages installed (pandas, openpyxl)

### Invoice Extraction Issues

**Problem:** Extraction fails or low quality
- **Check:** Invoice PDF quality (not scanned images)
- **Check:** Invoice format is supported
- **Review:** `Documentation/SUBAGENT_EXTRACTION_STRATEGY.md` for troubleshooting
- **Check:** AI agent prompts in `Code/agent_prompts.py`

## Documentation Index

**Current Documentation** (in `Documentation/` folder):
- `SUBAGENT_EXTRACTION_STRATEGY.md` - Complete extraction workflow and strategy
- `SUBAGENT_QUICK_START.md` - Quick start guide for invoice extraction
- `REPORT_CORRECTION_SUMMARY.md` - Language validation rules and prohibited terms
- `REPORT_CRITERIA_ANALYSIS.md` - Report quality standards and criteria
- `CORRECTIVE_ACTION_PLAN.md` - Data correction methodology

## Quick Reference

```bash
# Primary Workflow
cd "C:\Users\Richard\Downloads\Orion Data Part 2"

# Generate all reports
python Code/generate_reports_from_sheets.py    # Performance reports
python Code/generate_contract_reports.py       # Contract analysis

# Validate reports (CRITICAL before distribution)
python Code/validate_reports.py

# Invoice extraction
python Code/orchestrate_extraction.py          # Extract from PDFs
python Code/validate_extracted_data.py         # Validate extraction
python Code/update_google_sheets.py            # Update spreadsheet

# Convert to PDF (optional)
python Code/convert_to_pdf_puppeteer.py

# File Locations
# - Code: Code/
# - Reports: Reports/
# - Documentation: Documentation/
# - Invoices: Invoices/{property_name}/
# - Contracts: Contracts/
# - Templates: Code/templates/
```

## Data Integrity Philosophy

**Core Principle:** Realistic, data-driven insights based on actual findings.

### What We Do ✓

- Extract exact data from invoices (no interpretation)
- Identify real overages and inefficiencies
- Flag missing or ambiguous data for user review
- Base recommendations on verifiable facts
- Example: "Found $3,000 in overage charges in Q1 invoices"

### What We DON'T Do ✗

- Hallucinate missing data
- Guess frequencies or container counts
- Project unrealistic savings
- Recommend removing essential services
- Example: "Could save $50,000 by eliminating containers"

### Required Field Validation

All invoice extractions must validate:
- ✓ Property Name (CRITICAL)
- ✓ Invoice Date (CRITICAL)
- ✓ Total Amount (CRITICAL)
- ✓ Service Period (CRITICAL)
- ✓ Pickup Frequency (flag if missing)
- ⚠️ Container Count (flag if ambiguous)
- ⚠️ Overage vs Base Charges (flag if can't separate)

### Flagging System

**🔴 CRITICAL** - Cannot proceed, manual review required
- Missing property name
- Missing invoice amount
- Missing date

**🟡 NEEDS REVIEW** - Data ambiguous, user input needed
- Container mentioned but no count
- Frequency unclear
- Charges not itemized

**🟢 VALIDATION SUGGESTED** - Calculated/inferred, spot-check recommended
- Derived frequency from pickup dates
- Pattern-based extraction
- Medium confidence extractions

### Quality Workflow

1. Extract data with strict validation
2. Review all flags (use `/review-flags` command)
3. Resolve critical issues before proceeding
4. Validate data completeness
5. Generate reports based on verified data only

See `Documentation/DATA_INTEGRITY_GUIDE.md` for complete validation rules.

## Support & Maintenance

**For Issues:**
1. Check this CLAUDE.md file first
2. Review error messages carefully
3. Verify master data file is current
4. Ensure working directory is correct
5. Check that dependencies are installed

**For Questions:**
- Refer to documentation in `Documentation/` folder
- Review extraction strategy: `SUBAGENT_EXTRACTION_STRATEGY.md`
- Review validation rules: `REPORT_CORRECTION_SUMMARY.md`

**For Invoice Extraction Help:**
- Quick start: `Documentation/SUBAGENT_QUICK_START.md`
- Full strategy: `Documentation/SUBAGENT_EXTRACTION_STRATEGY.md`
- Agent prompts: `Code/agent_prompts.py`

## Version Information

**Current Version:** 3.0 (Property-Centric Structure)
**Last Updated:** November 9, 2025
**Status:** PRODUCTION READY
**Data Source:** Excel Master File (Single Source of Truth)

**Key Features:**
- Property-centric folder organization
- Master Excel file with all 10 properties
- AI-powered invoice extraction
- Fact-based reporting (no projections)
- Validated calculations and benchmarks

**Recent Changes (v3.0):**
- Reorganized into property-centric structure
- Created Properties/ folder with 10 property subfolders
- Consolidated master data file: MASTER_Portfolio_Complete_Data.xlsx
- Added README.md to each property folder
- Created Portfolio_Reports/ folder for portfolio-wide data
- Archived old/duplicate files

## Critical Reminders

1. **Single Source of Truth:** `Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx`
2. **Property-Centric Structure:** All files organized by property in `Properties/` folder
3. **Fact-Based Reporting:** No projections, optimizations, or unrealistic savings claims
4. **Language Validation:** Never use "cost savings" or similar terms in reports
5. **Always Validate:** Run validation before distributing reports
6. **Data Integrity:** Never hallucinate data - flag missing fields for user review
7. **Real Data Only:** All insights based on actual invoice and contract data
