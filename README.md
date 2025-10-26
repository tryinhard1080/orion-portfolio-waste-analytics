# Orion Portfolio Waste Management Analytics System

**Version 3.0 - Clean Build**

A streamlined waste management performance monitoring and reporting platform for 6 garden-style apartment properties in Texas.

## Quick Start

**For Claude Code Users:**
- Read `CLAUDE.md` first - complete project guide
- All commands and workflows documented there

**For Developers:**
1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment: `cp .env.example .env`
3. Generate reports: `python Code/generate_reports_from_sheets.py`
4. Validate reports: `python Code/validate_reports.py`

## Key Features

- ✅ **Google Sheets Integration** - Single source of truth for all property data
- ✅ **AI-Powered Invoice Extraction** - Automated data extraction using subagents
- ✅ **Automated Report Generation** - HTML performance reports with Jinja2 templates
- ✅ **Contract Analysis** - Comparative contract performance reports
- ✅ **Validation System** - Language and data accuracy validation
- ✅ **PDF Export** - Convert HTML reports to PDF

## Portfolio Summary

| Metric | Value |
|--------|-------|
| **Properties** | 6 (Bella Mirage, McCord Park FL, Orion McKinney, Orion Prosper, Orion Prosper Lakes, The Club at Millenia) |
| **Total Units** | 2,764 residential units |
| **Total Monthly Cost** | $44,664.16 |
| **Average CPD** | $16.15 per door |

## Folder Structure

```
Orion Data Part 2/
├── Invoices/          # Invoice PDFs by property
├── Contracts/         # Service contracts
├── Reports/           # Generated HTML reports
├── Code/              # Python scripts and templates
├── Documentation/     # Project documentation
├── requirements.txt   # Python dependencies
├── .env.example       # Configuration template
├── CLAUDE.md          # Complete project guide (READ THIS FIRST)
└── README.md          # This file
```

## Core Commands

```bash
# Generate performance reports
python Code/generate_reports_from_sheets.py

# Generate contract analysis
python Code/generate_contract_reports.py

# Validate reports (CRITICAL before distribution)
python Code/validate_reports.py

# Extract invoice data (AI-powered)
python Code/orchestrate_extraction.py

# Update Google Sheets with extracted data
python Code/update_google_sheets.py

# Convert reports to PDF
python Code/convert_to_pdf_puppeteer.py
```

## Documentation

**Main Guide:**
- `CLAUDE.md` - Complete project guide with all commands and workflows

**Specialized Guides:**
- `Documentation/SUBAGENT_EXTRACTION_STRATEGY.md` - Invoice extraction workflow
- `Documentation/SUBAGENT_QUICK_START.md` - Quick start for extraction
- `Documentation/REPORT_CORRECTION_SUMMARY.md` - Language validation rules
- `Documentation/REPORT_CRITERIA_ANALYSIS.md` - Report quality standards

## Data Source

**Google Sheets:** "Orion Portfolio - Waste Management Analytics"
- **Spreadsheet ID:** `1oy-F3p_CPpJaGGmGUMcjQMubRIRi7p4IID7mfpNLZJQ`
- **URL:** https://docs.google.com/spreadsheets/d/1oy-F3p_CPpJaGGmGUMcjQMubRIRi7p4IID7mfpNLZJQ/edit

Single source of truth for all property data, metrics, and performance tracking.

## Performance Metrics

### Key Performance Indicators

- **Yards Per Door (YPD):** Container capacity per unit (Target: 2.0-2.25)
- **Cost Per Door (CPD):** Monthly waste cost per unit (Target: $20-$30)
- **Overage Frequency:** Extra pickups beyond contract (Target: ≤15%)

### Performance Tiers

- 🟢 **Good:** 80-100 points
- 🟡 **Average:** 60-79 points
- 🔴 **Poor:** 0-59 points

## Monthly Workflow

1. **Collect Invoices** - Save PDFs to `Invoices/{PropertyName}/`
2. **Extract Data** - Run `orchestrate_extraction.py`
3. **Update Sheets** - Run `update_google_sheets.py`
4. **Generate Reports** - Run report generation scripts
5. **Validate** - Run `validate_reports.py` (CRITICAL)
6. **Distribute** - Share validated reports with stakeholders

## Technology Stack

- **Python 3.8+** - Core language
- **Jinja2** - HTML templating
- **Google Sheets API** - Data source (optional)
- **AI Subagents** - Invoice extraction
- **Puppeteer MCP** - PDF conversion

## Critical Reminders

1. **Always validate reports** before distribution (`validate_reports.py`)
2. **Never use "savings" language** in reports (see validation rules)
3. **Google Sheets is authoritative** - update there, not in code
4. **Clean folder structure** - keep files organized by type
5. **Use subagent extraction** for consistency and accuracy

## Support

**Issues or Questions:**
1. Check `CLAUDE.md` first (comprehensive guide)
2. Review relevant documentation in `Documentation/`
3. Verify Google Sheets data is current
4. Check that dependencies are installed

## Version Information

- **Version:** 3.0 (Clean Build)
- **Status:** Production Ready
- **Last Updated:** October 25, 2025
- **Data Source:** Google Sheets (Single Source of Truth)

---

**For complete project guidance, see `CLAUDE.md`**
