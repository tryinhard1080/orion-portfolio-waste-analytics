# SUBAGENT DATA EXTRACTION STRATEGY
## Orion Portfolio Waste Management Analytics

**Created:** October 23, 2025
**Status:** STRATEGY DESIGN
**Purpose:** Automate and parallelize invoice data extraction using AI subagents

---

## EXECUTIVE SUMMARY

This strategy outlines an intelligent subagent-based system to extract data from 49 PDF invoices across 6 properties in **parallel**, reducing extraction time from hours to minutes while maintaining high accuracy.

**Current State:**
- 49 PDF invoices requiring manual data extraction
- ~25-30 seconds per invoice with GPU OCR (legacy system)
- Manual process prone to errors and inconsistencies
- Google Sheets is single source of truth

**Proposed Solution:**
- Multi-agent orchestration for parallel processing
- Specialized agents for extraction, validation, and updating
- Estimated time reduction: **75-90%** (hours → 10-20 minutes)
- Improved accuracy through automated validation

---

## ARCHITECTURE OVERVIEW

### Agent Topology

```
┌─────────────────────────────────────────────────────────────┐
│                    COORDINATOR AGENT                         │
│            (Orchestrates entire workflow)                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┬──────────────┐
        ▼             ▼             ▼              ▼
┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│   Property   │ │ Property │ │ Property │ │ Property │
│   Agent 1    │ │ Agent 2  │ │ Agent 3  │ │ Agent 4-6│
│ (Parallel)   │ │(Parallel)│ │(Parallel)│ │(Parallel)│
└──────┬───────┘ └─────┬────┘ └─────┬────┘ └─────┬────┘
       │               │            │            │
       └───────────────┴────────────┴────────────┘
                       │
              ┌────────▼────────┐
              │  VALIDATION     │
              │     AGENT       │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │ SHEETS UPDATER  │
              │     AGENT       │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │    REPORT       │
              │   GENERATOR     │
              └─────────────────┘
```

### Agent Types & Responsibilities

#### 1. **Coordinator Agent** (Primary Orchestrator)
- **Type:** `task-orchestrator`
- **Role:** Overall workflow management
- **Tasks:**
  - Scan invoice folders and identify all PDF files
  - Group invoices by property
  - Spawn property-specific extraction agents in parallel
  - Aggregate results from all agents
  - Trigger validation, updating, and reporting

#### 2. **Property Extraction Agents** (6 parallel agents)
- **Type:** `coder` or `general-purpose`
- **Role:** Extract all invoices for a single property
- **Input:** Property name, invoice folder path, unit count
- **Output:** Structured JSON data for all invoices
- **Tasks:**
  - Read all PDF invoices for assigned property
  - Use multimodal capabilities (Claude can read PDFs via Read tool)
  - Extract all required fields using regex patterns
  - Calculate derived fields (CPD, controllable %)
  - Return structured data with confidence scores

**Key Innovation:** Each property agent processes 4-16 invoices sequentially, but all 6 property agents run **in parallel**.

#### 3. **Validation Agent**
- **Type:** `reviewer`
- **Role:** Quality assurance and data validation
- **Input:** Extracted data from all property agents
- **Output:** Validation report with issues flagged
- **Tasks:**
  - Check for missing required fields
  - Validate data types and ranges (e.g., CPD $5-$40)
  - Cross-check totals against individual charges
  - Flag low-confidence extractions (<80%)
  - Identify outliers and anomalies
  - Generate validation report

#### 4. **Google Sheets Updater Agent**
- **Type:** `general-purpose`
- **Role:** Update Google Sheets with validated data
- **Input:** Validated invoice data
- **Output:** Updated Google Sheets, update report
- **Tasks:**
  - Connect to Google Sheets via API
  - Update "Invoice Data" sheet with new records
  - Recalculate property-level aggregates
  - Update "Property Details" sheet with current metrics
  - Verify formulas still working correctly

#### 5. **Report Generator Agent**
- **Type:** `general-purpose`
- **Role:** Regenerate HTML reports
- **Input:** Updated Google Sheets data
- **Output:** 7 HTML reports
- **Tasks:**
  - Run `generate_reports_from_sheets.py`
  - Validate report content
  - Check for language compliance
  - Generate distribution summary

---

## DATA EXTRACTION SPECIFICATIONS

### Required Invoice Fields (Priority Order)

**Tier 1: Critical Fields (Required for basic reporting)**
```json
{
  "invoice_number": "2024-12345",
  "invoice_date": "2024-10-01",
  "month": "10-2024",
  "property_name": "Bella Mirage",
  "hauler": "Community Waste Disposal, LP",
  "total_amount": 7636.20,
  "account_number": "123456"
}
```

**Tier 2: Financial Breakdown (Required for controllable cost analysis)**
```json
{
  "base_service_charge": 6800.00,
  "fuel_surcharge_dollar": 450.00,
  "environmental_fee_dollar": 120.00,
  "overage_charges": 200.00,
  "contamination_charges": 0.00,
  "other_charges": 66.20,
  "city_sales_tax": 0.00,
  "state_sales_tax": 0.00
}
```

**Tier 3: Service Configuration (Required for performance metrics)**
```json
{
  "container_type": "Dumpster",
  "container_size_yd3": 8,
  "pickups_per_week": 3,
  "service_description": "4x 8-yd, 1x 6-yd, 1x 4-yd Dumpsters (4x/week)"
}
```

**Tier 4: Operational Metrics (Optional, for detailed analysis)**
```json
{
  "disposal_tonnage": 12.5,
  "disposal_cost": 450.00,
  "recycling_cost": 0.00,
  "container_rental": 0.00
}
```

**Tier 5: Calculated Fields (Computed from extracted data)**
```json
{
  "cost_per_door": 10.68,
  "controllable_charges": 266.20,
  "controllable_percentage": 3.5,
  "extraction_confidence": 0.92
}
```

### Extraction Patterns & Methods

**Method 1: Multimodal PDF Reading (Preferred)**
- Use Claude Code's Read tool with PDF support
- Claude can directly extract text and understand PDF structure
- No need for external OCR tools
- Faster and more accurate than OCR

**Method 2: Text-Based Regex Extraction**
```python
# Sample patterns from archived code
invoice_number_patterns = [
    r'Invoice\s*(?:Number|#)?\s*:?\s*(\d{4,}[-\d]*)',
    r'INV(?:OICE)?\s*(?:NO|#)?\s*:?\s*(\d{4,}[-\d]*)',
]

total_amount_patterns = [
    r'Total\s*(?:Amount\s*)?Due\s*:?\s*\$?\s*([\d,]+\.?\d{2})',
    r'Amount\s*Due\s*:?\s*\$?\s*([\d,]+\.?\d{2})',
    r'Current\s*(?:Invoice\s*)?Charges?\s*:?\s*\$?\s*([\d,]+\.?\d{2})',
]
```

**Method 3: Intelligent Table Detection**
- Identify line items in invoice tables
- Sum charges by category
- Validate totals against stated invoice total

---

## IMPLEMENTATION STRATEGY

### Phase 1: Property-Level Parallel Extraction (Est. 10-15 minutes)

**Coordinator spawns 6 property agents in parallel:**

```python
# Pseudo-code for agent spawning
properties = {
    'Bella Mirage': {'units': 715, 'invoices': 11},
    'McCord Park FL': {'units': 416, 'invoices': 8},
    'Orion McKinney': {'units': 453, 'invoices': 16},
    'Orion Prosper': {'units': 312, 'invoices': 4},
    'Orion Prosper Lakes': {'units': 308, 'invoices': 10},
    'The Club at Millenia': {'units': 560, 'invoices': 0}  # Awaiting
}

# Spawn agents in parallel (single message with multiple Task calls)
for property_name, config in properties.items():
    Task(
        subagent_type='coder',
        description=f'Extract {property_name} invoices',
        prompt=f"""
        Extract all invoice data from PDF files in:
        C:/Users/Richard/Downloads/Orion Data/Invoices/{property_name}/

        Property: {property_name}
        Units: {config['units']}
        Expected invoices: {config['invoices']}

        For each invoice PDF:
        1. Read the PDF file
        2. Extract all fields (see EXTRACTION_SCHEMA.json)
        3. Calculate CPD = total_amount / units
        4. Calculate controllable % = (overage + contamination + other) / total
        5. Assign confidence score (0-1)

        Return JSON array with all invoices:
        [
          {{
            "filename": "invoice.pdf",
            "property": "{property_name}",
            "invoice_data": {{ ... }},
            "confidence": 0.95
          }},
          ...
        ]

        Save results to: extraction_results/{property_name}_invoices.json
        """
    )
```

**Why Parallel?**
- Properties are independent (no data dependencies)
- Total time = max(individual_property_time), not sum
- Bella Mirage (11 invoices) runs simultaneously with McCord Park (8 invoices)

### Phase 2: Validation & Quality Check (Est. 2-3 minutes)

**Validation agent checks all extracted data:**

```python
Task(
    subagent_type='reviewer',
    description='Validate extracted invoice data',
    prompt="""
    Review all extracted invoice data from:
    extraction_results/*_invoices.json

    Validation checks:
    1. Required fields present (invoice_number, date, total_amount)
    2. Data type validation (numbers are numeric, dates are valid)
    3. Range validation (CPD between $5-$40, confidence 0-1)
    4. Cross-field validation (sum of charges ≈ total_amount ±5%)
    5. Outlier detection (CPD >2 std dev from property mean)
    6. Confidence threshold (flag if <0.80)

    Generate validation_report.json with:
    - Total invoices processed: X
    - Fully valid: Y
    - Warnings: Z (list issues)
    - Errors: W (list critical issues)
    - Recommended actions for low-confidence extractions
    """
)
```

### Phase 3: Google Sheets Update (Est. 2-3 minutes)

**Sheets updater agent:**

```python
Task(
    subagent_type='general-purpose',
    description='Update Google Sheets with validated data',
    prompt="""
    Update Google Sheets with validated invoice data.

    Spreadsheet: 1oy-F3p_CPpJaGGmGUMcjQMubRIRi7p4IID7mfpNLZJQ

    Steps:
    1. Read validation_report.json
    2. Filter to fully valid + high-confidence invoices (≥0.80)
    3. Create/update "Invoice Data" sheet with all invoice records
    4. Aggregate by property to update "Property Details" sheet:
       - Monthly Cost = sum(total_amount) / count(months)
       - Avg CPD = Monthly Cost / Units
       - Overage Frequency = count(invoices with overages) / total
    5. Verify formulas in "Performance Metrics" still work
    6. Generate update_summary.json

    Report:
    - Invoices added/updated: X
    - Properties updated: Y
    - Data quality: Z% high confidence
    """
)
```

### Phase 4: Report Regeneration (Est. 1-2 minutes)

**Report generator agent:**

```python
Task(
    subagent_type='general-purpose',
    description='Regenerate HTML reports',
    prompt="""
    Regenerate all 7 HTML reports from updated Google Sheets.

    Steps:
    1. Run: python Code/generate_reports_from_sheets.py
    2. Run: python Code/validate_reports.py
    3. Verify all 7 reports generated:
       - PortfolioSummaryDashboard.html
       - BellaMirageAnalysis.html
       - OrionMcKinneyAnalysis.html
       - OrionProsperAnalysis.html
       - OrionProsperLakesAnalysis.html
       - McCordParkFLAnalysis.html
       - TheClubAtMilleniaAnalysis.html
    4. Check language compliance (no "savings", "crisis" terms)
    5. Generate report_generation_summary.md
    """
)
```

---

## TOOLS & INFRASTRUCTURE NEEDED

### 1. Extraction Schema Definition

**File:** `Code/extraction_schema.json`
```json
{
  "invoice_schema": {
    "required_fields": [
      "invoice_number",
      "invoice_date",
      "month",
      "property_name",
      "hauler",
      "total_amount"
    ],
    "financial_fields": [
      "base_service_charge",
      "fuel_surcharge_dollar",
      "environmental_fee_dollar",
      "overage_charges",
      "contamination_charges",
      "other_charges"
    ],
    "service_fields": [
      "container_type",
      "container_size_yd3",
      "pickups_per_week",
      "service_description"
    ],
    "calculated_fields": [
      "cost_per_door",
      "controllable_charges",
      "controllable_percentage",
      "extraction_confidence"
    ]
  },
  "validation_rules": {
    "total_amount": {"min": 100, "max": 50000},
    "cost_per_door": {"min": 5, "max": 40},
    "extraction_confidence": {"min": 0, "max": 1},
    "controllable_percentage": {"min": 0, "max": 100}
  }
}
```

### 2. Orchestration Script

**File:** `Code/orchestrate_extraction.py`
```python
"""
Main orchestration script for subagent-based extraction
Spawns all agents using Claude Code Task tool
"""

import json
from pathlib import Path

def orchestrate_extraction():
    """
    Orchestrate multi-agent invoice extraction workflow
    """

    # Property configurations
    properties = load_property_config()

    # Phase 1: Spawn property extraction agents (PARALLEL)
    print("Phase 1: Spawning property extraction agents...")
    # Use Task tool 6 times in single message for parallel execution

    # Phase 2: Validation
    print("Phase 2: Validating extracted data...")
    # Use Task tool once for validation agent

    # Phase 3: Google Sheets update
    print("Phase 3: Updating Google Sheets...")
    # Use Task tool once for updater agent

    # Phase 4: Report regeneration
    print("Phase 4: Regenerating reports...")
    # Use Task tool once for report generator

    print("Extraction complete!")

if __name__ == '__main__':
    orchestrate_extraction()
```

### 3. Agent Prompt Templates

**File:** `Code/agent_prompts.py`
```python
"""
Standardized prompts for each agent type
"""

PROPERTY_EXTRACTION_PROMPT = """
You are a property-specific invoice extraction agent.

PROPERTY: {property_name}
UNITS: {units}
INVOICE FOLDER: {invoice_folder}

YOUR TASK:
Extract all invoice data from PDF files in the folder.

FOR EACH INVOICE:
1. Read the PDF using the Read tool
2. Extract all fields according to extraction_schema.json
3. Use regex patterns from archived code for field matching
4. Calculate derived fields:
   - cost_per_door = total_amount / units
   - controllable_charges = overage + contamination + other
   - controllable_percentage = (controllable_charges / total_amount) * 100
5. Assign confidence score based on:
   - Required fields present: +0.3
   - Financial breakdown complete: +0.3
   - Service details present: +0.2
   - No parsing errors: +0.2

OUTPUT:
Save JSON array to: extraction_results/{property_name}_invoices.json

IMPORTANT:
- Be thorough but efficient
- Use multimodal PDF reading (preferred over OCR)
- Flag any invoices you cannot parse confidently
"""

VALIDATION_PROMPT = """
You are a data validation specialist.

INPUT: All extracted invoice data from extraction_results/

YOUR TASK:
Validate data quality across all 49 invoices.

VALIDATION CHECKS:
1. Completeness: Required fields present
2. Data types: Numbers numeric, dates valid
3. Ranges: CPD $5-40, confidence 0-1
4. Cross-validation: Σ(charges) ≈ total_amount (±5%)
5. Outliers: Flag CPD >2 std dev from property mean
6. Confidence: Flag extractions <0.80

OUTPUT:
Generate validation_report.json with:
- Summary statistics
- List of warnings (minor issues)
- List of errors (critical issues)
- Recommended manual review items

QUALITY TARGETS:
- Auto-accept: confidence ≥0.85 (no errors)
- Review: confidence 0.70-0.84 (warnings only)
- Manual: confidence <0.70 or errors present
"""

SHEETS_UPDATE_PROMPT = """
You are a Google Sheets integration specialist.

SPREADSHEET: {spreadsheet_id}
INPUT: validation_report.json, extraction_results/*.json

YOUR TASK:
Update Google Sheets with validated invoice data.

WORKFLOW:
1. Load validation report
2. Filter to auto-accept invoices (confidence ≥0.85, no errors)
3. Create "Invoice Data" sheet if not exists
4. Bulk insert all invoice records
5. Aggregate by property:
   - Avg Monthly Cost = mean(total_amount)
   - Avg CPD = Avg Monthly Cost / Units
   - Overage Frequency = % invoices with overages
6. Update "Property Details" sheet with aggregates
7. Verify "Performance Metrics" formulas recalculate

OUTPUT:
Generate update_summary.json with:
- Invoices processed: X
- Invoices added to Sheets: Y
- Properties updated: Z
- Data quality: % high confidence
"""

REPORT_GENERATION_PROMPT = """
You are a report generation specialist.

YOUR TASK:
Regenerate all 7 HTML reports from updated Google Sheets.

WORKFLOW:
1. Run: python Code/generate_reports_from_sheets.py
2. Run: python Code/validate_reports.py
3. Verify all 7 reports generated
4. Check language compliance
5. Generate distribution summary

OUTPUT:
- 7 HTML reports in Reports/ folder
- Validation results
- Distribution summary

QUALITY CHECKS:
- All 7 reports present
- Data matches Google Sheets
- No prohibited language ("savings", "crisis")
- Professional tone maintained
"""
```

### 4. Result Aggregation Tool

**File:** `Code/aggregate_results.py`
```python
"""
Aggregate results from all property agents
"""

import json
from pathlib import Path

def aggregate_extraction_results():
    """
    Combine results from all property agents into single dataset
    """
    results_dir = Path('extraction_results')
    all_invoices = []

    for json_file in results_dir.glob('*_invoices.json'):
        with open(json_file) as f:
            property_invoices = json.load(f)
            all_invoices.extend(property_invoices)

    # Generate summary statistics
    summary = {
        'total_invoices': len(all_invoices),
        'by_property': {},
        'by_confidence': {
            'high': 0,      # ≥0.85
            'medium': 0,    # 0.70-0.84
            'low': 0        # <0.70
        },
        'avg_confidence': 0
    }

    for invoice in all_invoices:
        prop = invoice['property']
        conf = invoice.get('confidence', 0)

        if prop not in summary['by_property']:
            summary['by_property'][prop] = {'count': 0, 'avg_confidence': 0}

        summary['by_property'][prop]['count'] += 1

        if conf >= 0.85:
            summary['by_confidence']['high'] += 1
        elif conf >= 0.70:
            summary['by_confidence']['medium'] += 1
        else:
            summary['by_confidence']['low'] += 1

    # Save aggregated data
    with open('extraction_results/all_invoices.json', 'w') as f:
        json.dump(all_invoices, f, indent=2)

    with open('extraction_results/summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    return summary
```

---

## PERFORMANCE ESTIMATES

### Time Comparison

| Phase | Manual | OCR (GPU) | Subagent (Parallel) | Speedup |
|-------|--------|-----------|---------------------|---------|
| **Extraction** | 4-6 hours | 25 min | **10-15 min** | 16-24x |
| **Validation** | 1 hour | 30 min | **2-3 min** | 10-20x |
| **Sheets Update** | 30 min | 15 min | **2-3 min** | 5-10x |
| **Report Gen** | 10 min | 5 min | **1-2 min** | 5x |
| **TOTAL** | **6-8 hrs** | **75 min** | **15-23 min** | **16-32x** |

### Accuracy Expectations

| Metric | Manual | OCR | Subagent | Notes |
|--------|--------|-----|----------|-------|
| **Field Extraction** | 98-99% | 85-90% | **92-96%** | Multimodal PDF reading |
| **Calculation Accuracy** | 99%+ | 95% | **99%+** | Automated formulas |
| **Data Consistency** | Variable | 90% | **98%+** | Standardized validation |
| **Overall Quality** | High | Medium | **High** | Best of both worlds |

### Cost-Benefit Analysis

**Benefits:**
- 75-90% time reduction (hours → minutes)
- Improved consistency and accuracy
- Scalable to more properties/invoices
- Reduced manual effort and errors
- Real-time validation and quality checks

**Costs:**
- Initial setup: 2-3 hours (schema, scripts, prompts)
- Testing and refinement: 1-2 hours
- Ongoing: ~0 (fully automated)

**ROI:** Payback after **1-2 monthly cycles**

---

## RISK MITIGATION

### Risk 1: Low Extraction Confidence
**Mitigation:**
- Multi-pattern regex matching (fallback patterns)
- Confidence scoring flags low-quality extractions
- Validation agent reviews all data
- Manual review queue for confidence <0.80

### Risk 2: Agent Coordination Failures
**Mitigation:**
- Coordinator tracks all agent states
- Timeout handling (10 min per property agent)
- Retry logic for failed extractions
- Fallback to sequential processing if needed

### Risk 3: Google Sheets API Issues
**Mitigation:**
- Batch operations (reduce API calls)
- Rate limiting and retry logic
- Local backup of extracted data
- Rollback capability

### Risk 4: Report Generation Errors
**Mitigation:**
- Automated validation checks
- Language compliance scanning
- Data accuracy verification
- Keep previous reports as backup

---

## SUCCESS METRICS

### Primary Metrics
- ✅ **Time to completion:** <25 minutes for 49 invoices
- ✅ **Extraction accuracy:** ≥92% average confidence
- ✅ **Auto-accept rate:** ≥85% of invoices (confidence ≥0.85)
- ✅ **Manual review rate:** ≤15% of invoices

### Secondary Metrics
- ✅ **Data completeness:** 100% of required fields
- ✅ **Validation pass rate:** ≥95% with no errors
- ✅ **Sheets update success:** 100% of valid invoices
- ✅ **Report generation:** 7 of 7 reports with validation

---

## EXECUTION PLAN

### Prerequisites (Do First)
1. ✅ Review this strategy document
2. ⬜ Create `extraction_schema.json`
3. ⬜ Create `agent_prompts.py` with prompt templates
4. ⬜ Create `orchestrate_extraction.py` skeleton
5. ⬜ Test Read tool on sample invoice PDF

### Phase 1: Proof of Concept (1 property)
1. Manually test extraction on Bella Mirage (11 invoices)
2. Verify data quality and confidence scores
3. Validate against known good data
4. Refine extraction patterns

### Phase 2: Parallel Execution (All 6 properties)
1. Run orchestrator with all property agents in parallel
2. Monitor agent execution and timing
3. Aggregate results
4. Review validation report

### Phase 3: Integration (Sheets + Reports)
1. Update Google Sheets with validated data
2. Regenerate reports
3. Compare with previous reports
4. Verify data accuracy

### Phase 4: Production (Monthly Workflow)
1. Document execution procedure
2. Create monthly checklist
3. Establish quality gates
4. Set up monitoring and alerts

---

## NEXT STEPS

### Immediate (Today)
1. **Review this strategy** - Confirm approach and agent topology
2. **Create schema file** - Define extraction structure
3. **Test PDF reading** - Verify Claude can read invoice PDFs

### Short-term (This Week)
1. **Build orchestrator** - Implement agent coordination
2. **Test on subset** - Run on 5-10 invoices
3. **Refine patterns** - Adjust extraction logic based on results

### Medium-term (This Month)
1. **Full deployment** - Process all 49 invoices
2. **Validate results** - Compare with manual extraction
3. **Document workflow** - Create user guide

### Long-term (Ongoing)
1. **Monthly execution** - Regular invoice processing
2. **Continuous improvement** - Refine based on performance
3. **Scale up** - Handle more properties/invoices as needed

---

## CONCLUSION

This subagent strategy leverages parallel processing, specialized agents, and intelligent orchestration to **reduce invoice extraction time by 75-90%** while maintaining high accuracy. The approach is scalable, repeatable, and provides built-in quality assurance through validation and automated reporting.

**Key Advantages:**
- ✅ Parallel execution (6 properties simultaneously)
- ✅ Specialized agents (extraction, validation, updating)
- ✅ Quality assurance (automated validation)
- ✅ End-to-end automation (PDFs → Reports)
- ✅ Scalable architecture (easily add more properties)

**Ready to proceed?** Start with the Proof of Concept phase to validate the approach on a single property.

---

**Status:** STRATEGY READY FOR REVIEW
**Next Action:** User approval to proceed with implementation
