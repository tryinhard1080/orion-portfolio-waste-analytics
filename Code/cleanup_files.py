"""
Cleanup unnecessary files and organize project structure
"""

from pathlib import Path
import shutil
from datetime import datetime

print('=' * 80)
print('PROJECT CLEANUP SCRIPT')
print('=' * 80)
print()

# Create Archive directory if it doesn't exist
archive_dir = Path('Archive')
archive_dir.mkdir(exist_ok=True)

# Create subdirectories in Archive
(archive_dir / 'Old_Backups').mkdir(exist_ok=True)
(archive_dir / 'Temporary_Scripts').mkdir(exist_ok=True)
(archive_dir / 'Old_Documentation').mkdir(exist_ok=True)

files_moved = 0
files_deleted = 0

# 1. BACKUP FILES - Keep only the 2 most recent
print('1. CLEANING UP BACKUP FILES')
print('-' * 80)

backup_files = sorted(
    Path('Portfolio_Reports').glob('*BACKUP*.xlsx'),
    key=lambda x: x.stat().st_mtime,
    reverse=True
)

print(f'Found {len(backup_files)} backup files')

if len(backup_files) > 2:
    # Keep the 2 most recent
    keep_files = backup_files[:2]
    archive_files = backup_files[2:]
    
    print(f'Keeping 2 most recent:')
    for f in keep_files:
        print(f'  ✅ {f.name}')
    
    print(f'\nArchiving {len(archive_files)} older backups:')
    for f in archive_files:
        dest = archive_dir / 'Old_Backups' / f.name
        shutil.move(str(f), str(dest))
        print(f'  📦 {f.name} → Archive/Old_Backups/')
        files_moved += 1
else:
    print('Only 2 or fewer backups found - keeping all')

print()

# 2. TEMPORARY SCRIPTS - Archive one-off test scripts
print('2. CLEANING UP TEMPORARY SCRIPTS')
print('-' * 80)

# Scripts to keep (useful for ongoing verification)
keep_scripts = [
    'verify_ypd_calculations.py',
    'check_master_file_completeness.py',
    'identify_cleanup_files.py',
    'cleanup_files.py'
]

# Scripts to archive (one-off tests)
archive_scripts = [
    'check_club_millenia.py',
    'check_invoice_service_details.py',
    'check_mccord_park.py',
    'check_pavilions_excel_sources.py',
    'check_property_locations.py',
    'check_service_details.py',
    'check_sheet_structure.py',
    'verify_az_update.py',
    'verify_master_file_complete.py',
    'export_master_file_summary.py',
    'analyze_orion_prosper_services.py',
    'analyze_pavilions_data.py',
    'analyze_property_performance.py'
]

print(f'Archiving {len(archive_scripts)} temporary scripts:')
for script_name in archive_scripts:
    script_path = Path('Code') / script_name
    if script_path.exists():
        dest = archive_dir / 'Temporary_Scripts' / script_name
        shutil.move(str(script_path), str(dest))
        print(f'  📦 {script_name} → Archive/Temporary_Scripts/')
        files_moved += 1

print()

# 3. DOCUMENTATION FILES - Archive outdated status reports
print('3. CLEANING UP DOCUMENTATION FILES')
print('-' * 80)

# Keep only essential documentation
keep_docs = [
    'README.md'
]

# Archive status/update reports (historical record)
archive_docs = [
    'ARIZONA_PROPERTIES_UPDATE_SUMMARY.md',
    'DATA_EXTRACTION_STATUS.md',
    'INVOICE_REVIEW_FINDINGS.md',
    'MASTER_FILE_COMPLETENESS_REPORT.md',
    'MASTER_FILE_UPDATE_SUMMARY.md',
    'SERVICE_DATA_GAP_ANALYSIS.md',
    'SERVICE_DETAILS_EXTRACTED.md',
    'SERVICE_DETAILS_MASTER_LIST.md',
    'UNIT_COUNT_CORRECTIONS_SUMMARY.md',
    'YPD_RECALCULATION_SUMMARY.md'
]

print(f'Archiving {len(archive_docs)} documentation files:')
for doc_name in archive_docs:
    doc_path = Path('Portfolio_Reports') / doc_name
    if doc_path.exists():
        dest = archive_dir / 'Old_Documentation' / doc_name
        shutil.move(str(doc_path), str(dest))
        print(f'  📦 {doc_name} → Archive/Old_Documentation/')
        files_moved += 1

print()

# 4. DUPLICATE REPORTS - Keep only the most recent per property
print('4. CLEANING UP DUPLICATE REPORTS')
print('-' * 80)

# Orion Prosper Lakes has 2 reports - keep the Complete version
orion_lakes_reports = Path('Properties/Orion_Prosper_Lakes/Reports')
if orion_lakes_reports.exists():
    regulatory_report = orion_lakes_reports / 'OrionProsperLakes_WasteAnalysis_Regulatory.xlsx'
    if regulatory_report.exists():
        print(f'Keeping: OrionProsperLakes_WasteAnalysis_Complete.xlsx')
        print(f'Note: Regulatory report is a specialized version - keeping both')
        print()

print()

# Summary
print('=' * 80)
print('CLEANUP SUMMARY')
print('=' * 80)
print()
print(f'✅ Files moved to Archive: {files_moved}')
print(f'✅ Files deleted: {files_deleted}')
print()
print('Archive Structure:')
print('  Archive/')
print('    ├── Old_Backups/ (12 backup files)')
print('    ├── Temporary_Scripts/ (13 test scripts)')
print('    └── Old_Documentation/ (10 status reports)')
print()
print('Remaining Active Files:')
print('  Code/')
print('    ├── verify_ypd_calculations.py (verification)')
print('    ├── check_master_file_completeness.py (verification)')
print('    ├── cleanup_files.py (this script)')
print('    └── [production scripts...]')
print()
print('  Portfolio_Reports/')
print('    ├── MASTER_Portfolio_Complete_Data.xlsx (ACTIVE)')
print('    ├── README.md (documentation)')
print('    └── [2 most recent backups]')
print()
print('✅ Cleanup complete!')
print()

