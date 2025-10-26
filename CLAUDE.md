# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Orion Portfolio Waste Management Analytics System (Version 3.0 - Clean Build)** - A streamlined waste management performance monitoring and reporting platform for 6 garden-style apartment properties in Texas. The system generates HTML performance reports directly from Google Sheets data, providing real-time insights into cost efficiency, service utilization, and performance metrics.

**Key Technologies:**
- Python 3.8+ with Google Sheets API integration
- Jinja2 HTML templating for report generation
- Google Sheets as single source of truth for all property data
- AI-powered invoice extraction using subagents
- Automated performance analysis and benchmarking

## Critical Path Information

**IMPORTANT - Dropbox Migration:** Do NOT run, save, or operate in any path containing "dropbox". All data has been migrated to create better system performance. If you encounter a dropbox path, flag the user to change directories.

**Current Working Directory:** `C:\Users\Richard\Downloads\Orion Data Part 2`

**Google Sheets Spreadsheet:** "Orion Portfolio - Waste Management Analytics"
- **Spreadsheet ID:** `1oy-F3p_CPpJaGGmGUMcjQMubRIRi7p4IID7mfpNLZJQ`
- **URL:** https://docs.google.com/spreadsheets/d/1oy-F3p_CPpJaGGmGUMcjQMubRIRi7p4IID7mfpNLZJQ/edit
- **Sheets:** Property Details, Portfolio Summary, Invoice Data

## Folder Structure

```
Orion Data Part 2/
│
├── Invoices/                          # Invoice PDFs organized by property
│   ├── Bella_Mirage/
│   ├── McCord_Park_FL/
│   ├── Orion_McKinney/
│   ├── Orion_Prosper/
│   ├── Orion_Prosper_Lakes/
│   └── The_Club_at_Millenia/
│
├── Contracts/                         # Service contracts by property
│   └── (PDF contracts)
│
├── Reports/                           # Generated HTML reports
│   ├── PortfolioSummaryDashboard.html
│   ├── {Property}Analysis.html (6 files)
│   └── Contract_Comparison/
│       └── {Property}_Report.html (6 files)
│
├── Code/                              # Python scripts
│   ├── agent_prompts.py              # LLM prompts for extraction
│   ├── orchestrate_extraction.py     # Extraction workflow orchestration
│   ├── extract_orion_prosper_invoices.py  # Example extraction script
│   ├── validate_extracted_data.py    # Data validation
│   ├── update_google_sheets.py       # Update spreadsheet with extracted data
│   ├── comprehensive_validation.py   # Extended validation
│   ├── generate_reports_from_sheets.py    # Main report generator
│   ├── generate_reports_from_sheets_data.py  # Hardcoded data fallback
│   ├── validate_reports.py           # Report validation
│   ├── generate_contract_reports.py  # Contract analysis reports
│   ├── convert_to_pdf_puppeteer.py   # PDF conversion
│   └── templates/                    # Jinja2 HTML templates
│       ├── portfolio_summary.html
│       └── property_detail.html
│
├── Documentation/                     # Project documentation
│   ├── SUBAGENT_EXTRACTION_STRATEGY.md    # Extraction workflow guide
│   ├── SUBAGENT_QUICK_START.md            # Quick start for extraction
│   ├── REPORT_CORRECTION_SUMMARY.md       # Language validation rules
│   ├── REPORT_CRITERIA_ANALYSIS.md        # Report quality standards
│   └── CORRECTIVE_ACTION_PLAN.md          # Data correction methodology
│
├── .env.example                      # Configuration template
├── requirements.txt                  # Python dependencies
└── CLAUDE.md                         # This file
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
- Reads from Google Sheets API or hardcoded data fallback
- Generates 7 HTML reports (1 portfolio + 6 properties)
- Uses Jinja2 templates in `Code/templates/`
- Output: `Reports/{PropertyName}Analysis.html`

**`generate_reports_from_sheets_data.py`**
- Contains hardcoded property data fallback
- Used when Google Sheets API unavailable
- Must be manually updated when data changes

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
- Cross-references invoice data with Google Sheets

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
- Updates Google Sheets with extracted invoice data
- Batch upload capability
- Validates before uploading

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

# 3. Update Google Sheets with validated data
python Code/update_google_sheets.py

# 4. Regenerate reports with new data
python Code/generate_reports_from_sheets.py
```

**See `Documentation/SUBAGENT_EXTRACTION_STRATEGY.md` for complete extraction workflow.**

## Data Source: Google Sheets (Primary) or Hardcoded Data (Fallback)

The system supports two data source modes:

**Mode 1: Google Sheets API (Recommended)**
- Reads live data from spreadsheet
- Real-time updates reflected in reports
- Requires Google Sheets API credentials

**Mode 2: Hardcoded Data (Fallback)**
- Uses static data in `Code/generate_reports_from_sheets_data.py`
- No API credentials required
- Must manually update Python file for data changes

The system automatically falls back to hardcoded data if Google Sheets API is unavailable.

### Spreadsheet Structure

**Sheet: "Property Details"**
- Column A: Property Name
- Column B: Unit Count
- Column C: Service Type (Compactor/Dumpster)
- Column D: Cost Per Door (CPD)
- Column E-H: Performance metrics
- Column I: Monthly Cost

**Sheet: "Portfolio Summary"**
- Total units across all properties
- Average CPD
- Total monthly cost
- Portfolio performance score

**Sheet: "Invoice Data"**
- Historical invoice data
- Extracted field values
- Month/year tracking

## Key Property Data (Current)

### All 6 Properties - Verified Data

| Property | Units | Monthly Cost | CPD | Status |
|----------|-------|--------------|-----|--------|
| **Orion Prosper** | 312 | $4,308.72 | $13.81 | ✓ |
| **McCord Park FL** | 416 | $10,911.68 | $26.23 | ✓ |
| **Orion McKinney** | 453 | $6,015.84 | $13.28 | ✓ |
| **The Club at Millenia** | **560** | $11,760.00 | **$21.00** | ✓ |
| **Bella Mirage** | 715 | $7,636.20 | $10.68 | ✓ |
| **Orion Prosper Lakes** | 308 | $4,031.72 | $13.09 | ✓ |
| **TOTALS** | **2,764** | **$44,664.16** | **$16.15** | ✓ |

**Property Constants (for code):**
```python
PROPERTIES = {
    'Orion Prosper': 312,
    'McCord Park FL': 416,
    'Orion McKinney': 453,
    'The Club at Millenia': 560,
    'Bella Mirage': 715,
    'Orion Prosper Lakes': 308
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
- Unit counts match Google Sheets
- CPD calculations accurate (Monthly Cost ÷ Units)
- Performance scores within 0-100 range
- All 6 properties included in portfolio summary
- Portfolio totals calculated correctly

## Invoice Extraction Workflow

The system uses AI subagents to extract invoice data. See `Documentation/SUBAGENT_EXTRACTION_STRATEGY.md` for complete details.

### Quick Start

1. **Place invoices** in `Invoices/{PropertyName}/` folder
2. **Run extraction** using `python Code/orchestrate_extraction.py`
3. **Validate data** using `python Code/validate_extracted_data.py`
4. **Update Google Sheets** using `python Code/update_google_sheets.py`
5. **Regenerate reports** using `python Code/generate_reports_from_sheets.py`

### Extraction Strategy

The subagent extraction system:
- Uses specialized AI agents for different extraction tasks
- Validates extracted data automatically
- Provides confidence scores for extracted fields
- Handles multiple invoice formats
- See `Documentation/SUBAGENT_QUICK_START.md` for detailed guide

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
   python Code/update_google_sheets.py
   # OR manually update Google Sheets
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
1. Open Google Sheets spreadsheet
2. Navigate to "Property Details" sheet
3. Update relevant cells (units, costs, metrics)
4. Regenerate reports: `python Code/generate_reports_from_sheets.py`

**Example: Update Unit Count**
- Find property row in "Property Details" sheet
- Update Column B (Unit Count)
- CPD will auto-recalculate if using formulas
- Regenerate reports to reflect changes

## Troubleshooting

### Report Generation Issues

**Problem:** Script fails to run
- **Check:** Python environment activated
- **Check:** Dependencies installed (`pip install -r requirements.txt`)
- **Check:** Working directory is correct

**Problem:** Reports not updating
- **Check:** Google Sheets data is current
- **Check:** Script completed without errors
- **Check:** Reports saved to `Reports/` folder

**Problem:** Data doesn't match Google Sheets
- **Check:** `Code/generate_reports_from_sheets_data.py` has latest data
- **Check:** Script is reading from correct spreadsheet ID
- **Check:** Property names match exactly

### Google Sheets Access

**Problem:** Cannot access spreadsheet
- **Check:** Spreadsheet ID is correct
- **Check:** Sharing permissions allow access
- **Check:** Google Sheets API credentials configured (if using API mode)

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

## Version Information

**Current Version:** 3.0 (Clean Build)
**Last Updated:** October 25, 2025
**Status:** PRODUCTION READY
**Data Source:** Google Sheets (Single Source of Truth)

**Key Features:**
- Clean folder structure with logical organization
- Google Sheets integration (primary data source)
- AI-powered invoice extraction using subagents
- Automated report generation with validation
- Contract comparison analysis
- HTML to PDF conversion

## Critical Reminders

1. **Single Source of Truth:** Google Sheets spreadsheet (ID: 1oy-F3p_CPpJaGGmGUMcjQMubRIRi7p4IID7mfpNLZJQ)
2. **Language Validation:** Never use "cost savings" or similar terms in reports
3. **Always Validate:** Run `validate_reports.py` before distributing to clients
4. **Clean Structure:** All active code in `Code/`, all docs in `Documentation/`
5. **Invoice Organization:** Invoices organized by property in `Invoices/{property_name}/`
6. **Subagent Extraction:** Use AI-powered extraction for consistency and accuracy
7. **Data Accuracy:** Verify all property data before report generation
8. **Data Integrity:** Never hallucinate data - flag missing fields for user review

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
3. Verify Google Sheets data is current
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
