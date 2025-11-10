"""
Identify files that can be cleaned up
"""

from pathlib import Path
from datetime import datetime

print('=' * 80)
print('FILE CLEANUP ANALYSIS')
print('=' * 80)
print()

base_dir = Path('.')

# Categories of files to review
backup_files = []
temp_scripts = []
duplicate_reports = []
old_documentation = []

# Find backup files
print('BACKUP FILES:')
print('-' * 80)
for backup in Path('Portfolio_Reports').glob('*BACKUP*.xlsx'):
    backup_files.append(backup)
    print(f'  {backup.name}')
print(f'Total: {len(backup_files)} files')
print()

# Find temporary/test scripts
print('TEMPORARY/TEST SCRIPTS:')
print('-' * 80)
temp_script_patterns = [
    'check_*.py',
    'test_*.py',
    'verify_*.py',
    'export_*.py',
    'analyze_*.py'
]

for pattern in temp_script_patterns:
    for script in Path('Code').glob(pattern):
        temp_scripts.append(script)
        print(f'  {script.name}')
print(f'Total: {len(temp_scripts)} files')
print()

# Find duplicate/old reports
print('PROPERTY REPORTS (check for duplicates):')
print('-' * 80)
for prop_dir in Path('Properties').iterdir():
    if prop_dir.is_dir():
        reports_dir = prop_dir / 'Reports'
        if reports_dir.exists():
            reports = list(reports_dir.glob('*.xlsx'))
            if len(reports) > 1:
                print(f'  {prop_dir.name}:')
                for report in reports:
                    print(f'    - {report.name}')
                duplicate_reports.extend(reports)
print()

# Find old documentation files
print('DOCUMENTATION FILES (check for outdated):')
print('-' * 80)
doc_files = list(Path('Portfolio_Reports').glob('*.md'))
for doc in doc_files:
    old_documentation.append(doc)
    print(f'  {doc.name}')
print(f'Total: {len(doc_files)} files')
print()

# Summary
print('=' * 80)
print('CLEANUP RECOMMENDATIONS')
print('=' * 80)
print()

print('1. BACKUP FILES (keep most recent, archive older):')
print(f'   Found {len(backup_files)} backup files')
print('   Recommendation: Keep 2-3 most recent, delete older ones')
print()

print('2. TEMPORARY SCRIPTS (review and consolidate):')
print(f'   Found {len(temp_scripts)} temporary/test scripts')
print('   Recommendation: Keep useful verification scripts, delete one-off tests')
print()

print('3. DUPLICATE REPORTS (keep latest version):')
print(f'   Found {len(duplicate_reports)} report files across properties')
print('   Recommendation: Keep one report per property, delete duplicates')
print()

print('4. DOCUMENTATION FILES (consolidate):')
print(f'   Found {len(doc_files)} markdown documentation files')
print('   Recommendation: Review and consolidate into main README or archive')
print()

# Create cleanup script
print('=' * 80)
print('CREATING CLEANUP SCRIPT')
print('=' * 80)
print()
print('A cleanup script will be created to help remove unnecessary files.')
print('Review the recommendations above before running the cleanup.')
print()

