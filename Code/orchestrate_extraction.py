"""
Invoice Extraction Orchestration System
Coordinates multi-agent parallel extraction workflow using Claude Code subagents

USAGE:
    python Code/orchestrate_extraction.py

This script serves as a template. The actual orchestration is performed
by calling Claude Code with the appropriate agent spawn instructions.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Property configurations
PROPERTY_CONFIG = {
    'Bella Mirage': {
        'units': 715,
        'folder': 'Invoices/Bella_Mirage',
        'expected_invoices': 11,
        'typical_cpd_range': [9, 12]
    },
    'McCord Park FL': {
        'units': 416,
        'folder': 'Invoices/McCord_Park_FL',
        'expected_invoices': 8,
        'typical_cpd_range': [24, 28]
    },
    'Orion McKinney': {
        'units': 453,
        'folder': 'Invoices/Orion_McKinney',
        'expected_invoices': 16,
        'typical_cpd_range': [12, 15]
    },
    'Orion Prosper': {
        'units': 312,
        'folder': 'Invoices/Orion_Prosper',
        'expected_invoices': 4,
        'typical_cpd_range': [13, 15]
    },
    'Orion Prosper Lakes': {
        'units': 308,
        'folder': 'Invoices/Orion_Prosper_Lakes',
        'expected_invoices': 10,
        'typical_cpd_range': [12, 15]
    },
    'The Club at Millenia': {
        'units': 560,
        'folder': 'Invoices/The_Club_at_Millenia',
        'expected_invoices': 0,  # Awaiting invoices
        'typical_cpd_range': [20, 22]
    }
}

SPREADSHEET_ID = "1oy-F3p_CPpJaGGmGUMcjQMubRIRi7p4IID7mfpNLZJQ"


def setup_directories():
    """Create necessary output directories"""
    dirs = [
        'extraction_results',
        'validation_reports',
        'update_logs'
    ]

    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"[OK] Directory ready: {dir_name}/")


def validate_prerequisites():
    """Ensure all required files and folders exist"""
    print("\\n" + "="*60)
    print("VALIDATING PREREQUISITES")
    print("="*60)

    checks = {
        'Schema file': 'Code/extraction_schema.json',
        'Prompts module': 'Code/agent_prompts.py',
        'Report generator': 'Code/generate_reports_from_sheets.py',
        'Invoice folder': 'Invoices/'
    }

    all_passed = True
    for name, path in checks.items():
        exists = Path(path).exists()
        status = "✓" if exists else "✗"
        print(f"{status} {name}: {path}")
        if not exists:
            all_passed = False

    if not all_passed:
        print("\\n⚠️  Some prerequisites missing. Please resolve before proceeding.")
        return False

    print("\\n✓ All prerequisites satisfied")
    return True


def count_invoices():
    """Count available invoices per property"""
    print("\\n" + "="*60)
    print("INVOICE INVENTORY")
    print("="*60)

    total_invoices = 0
    for prop_name, config in PROPERTY_CONFIG.items():
        folder_path = Path(config['folder'])
        if folder_path.exists():
            invoices = list(folder_path.glob('*.pdf')) + list(folder_path.glob('*.PDF'))
            count = len(invoices)
            expected = config['expected_invoices']
            status = "✓" if count == expected else "⚠️"
            print(f"{status} {prop_name}: {count} invoices (expected {expected})")
            total_invoices += count
        else:
            print(f"✗ {prop_name}: Folder not found")

    print(f"\\n📊 Total invoices to process: {total_invoices}")
    return total_invoices


def generate_orchestration_instructions():
    """
    Generate instructions for Claude Code to spawn agents

    NOTE: This is a template. Actual agent spawning must be done
    through Claude Code's Task tool with appropriate prompts.
    """
    print("\\n" + "="*60)
    print("AGENT ORCHESTRATION INSTRUCTIONS")
    print("="*60)

    print("\\nTo execute this workflow, instruct Claude Code to:")
    print("\\n1. SPAWN PROPERTY EXTRACTION AGENTS (IN PARALLEL)")
    print("   Use single message with multiple Task tool calls:")
    print()

    for prop_name, config in PROPERTY_CONFIG.items():
        if config['expected_invoices'] == 0:
            continue

        safe_name = prop_name.replace(' ', '_')
        print(f"""   Task(
     subagent_type='coder',
     description='Extract {prop_name} invoices',
     prompt='''
       Extract invoice data from: {config['folder']}
       Property: {prop_name}
       Units: {config['units']}
       Expected invoices: {config['expected_invoices']}

       Use extraction_schema.json for field patterns.
       Save results to: extraction_results/{safe_name}_invoices.json
     '''
   )
   """)

    print("\\n2. VALIDATE EXTRACTED DATA")
    print("""   Task(
     subagent_type='reviewer',
     description='Validate all extracted invoices',
     prompt='''
       Load extraction results from extraction_results/*_invoices.json
       Validate per extraction_schema.json rules
       Generate validation_report.json
     '''
   )
   """)

    print("\\n3. UPDATE GOOGLE SHEETS")
    print(f"""   Task(
     subagent_type='general-purpose',
     description='Update Google Sheets with validated data',
     prompt='''
       Spreadsheet: {SPREADSHEET_ID}
       Load validation_report.json and auto_accept_list.json
       Update Invoice Data and Property Details sheets
       Generate sheets_update_summary.json
     '''
   )
   """)

    print("\\n4. REGENERATE REPORTS")
    print("""   Task(
     subagent_type='general-purpose',
     description='Regenerate HTML reports',
     prompt='''
       Run: python Code/generate_reports_from_sheets.py
       Run: python Code/validate_reports.py
       Generate report_generation_summary.json
     '''
   )
   """)


def generate_execution_summary():
    """Generate execution summary and next steps"""
    print("\\n" + "="*60)
    print("EXECUTION SUMMARY")
    print("="*60)

    summary = {
        'timestamp': datetime.now().isoformat(),
        'status': 'READY_TO_EXECUTE',
        'prerequisites': 'SATISFIED',
        'total_properties': len(PROPERTY_CONFIG),
        'properties_with_invoices': sum(1 for c in PROPERTY_CONFIG.values() if c['expected_invoices'] > 0),
        'estimated_time': '15-23 minutes',
        'phases': [
            'Phase 1: Property extraction (parallel) - 10-15 min',
            'Phase 2: Validation - 2-3 min',
            'Phase 3: Google Sheets update - 2-3 min',
            'Phase 4: Report generation - 1-2 min'
        ]
    }

    # Save summary
    with open('orchestration_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\\n⏱️  Estimated total time: {summary['estimated_time']}")
    print(f"🏢 Properties to process: {summary['properties_with_invoices']}")
    print("\\n📋 Execution phases:")
    for phase in summary['phases']:
        print(f"   • {phase}")

    print("\\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print("""
1. Review the orchestration instructions above
2. Confirm you want to proceed with automated extraction
3. Instruct Claude Code to spawn agents per the instructions
4. Monitor agent execution and review results
5. Verify extracted data before Google Sheets update
6. Review regenerated reports for accuracy

⚠️  IMPORTANT: Property extraction agents will run in PARALLEL
   This means all 6 properties will be processed simultaneously.
   Ensure system resources are adequate for parallel execution.
   """)


def main():
    """Main orchestration script"""
    print("\\n" + "="*80)
    print(" ORION PORTFOLIO - INVOICE EXTRACTION ORCHESTRATION SYSTEM")
    print("="*80)
    print(f"\\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Mode: Multi-Agent Parallel Extraction")
    print("="*80)

    # Setup
    setup_directories()

    # Validate prerequisites
    if not validate_prerequisites():
        return 1

    # Count invoices
    total_invoices = count_invoices()
    if total_invoices == 0:
        print("\\n⚠️  No invoices found to process.")
        return 1

    # Generate orchestration instructions
    generate_orchestration_instructions()

    # Generate execution summary
    generate_execution_summary()

    print("\n[SUCCESS] Orchestration system ready!")
    print("[INFO] Summary saved to: orchestration_summary.json")
    print("\nFollow the instructions above to begin extraction.")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
