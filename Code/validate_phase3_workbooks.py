"""
Validate all 7 Phase 3 workbooks
"""

import subprocess
import sys

# Phase 3 properties
properties = [
    'Bella Mirage',
    'Mandarina',
    'Pavilions at Arrowhead',
    'Tempe Vista',
    'Orion Prosper Lakes',
    'McCord Park FL',
    'Orion McKinney'
]

print(f"\n{'='*70}")
print("PHASE 3 WORKBOOK VALIDATION")
print(f"{'='*70}")
print(f"Validating {len(properties)} workbooks...\n")

# Run validation for each property
for prop in properties:
    print(f"\n[{properties.index(prop) + 1}/{len(properties)}] Validating: {prop}")
    result = subprocess.run(
        [sys.executable, 'Code/validate_expense_workbooks.py', prop],
        capture_output=True,
        text=True
    )

    # Show output
    print(result.stdout)

    if result.returncode != 0:
        print(f"[ERROR] Validation failed for {prop}")
        print(result.stderr)

print(f"\n{'='*70}")
print("PHASE 3 VALIDATION COMPLETE")
print(f"{'='*70}")
