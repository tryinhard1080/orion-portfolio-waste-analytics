"""Retry saving the Arizona properties update"""

import shutil
from pathlib import Path
import time

# Paths
BASE_DIR = Path(__file__).parent.parent
BACKUP_FILE = BASE_DIR / "Portfolio_Reports" / "MASTER_Portfolio_Complete_Data_BACKUP_AZ_UPDATE_20251109_152756.xlsx"
MASTER_FILE = BASE_DIR / "Portfolio_Reports" / "MASTER_Portfolio_Complete_Data.xlsx"

print('=' * 80)
print('RETRYING SAVE OF ARIZONA PROPERTIES UPDATE')
print('=' * 80)
print()

# Check if backup exists
if not BACKUP_FILE.exists():
    print(f'❌ Backup file not found: {BACKUP_FILE.name}')
    print('The update may not have been saved.')
    exit(1)

print(f'✅ Backup file found: {BACKUP_FILE.name}')
print()

# Try to copy backup to master file
print('Attempting to save updated file...')
print()

max_retries = 5
for attempt in range(1, max_retries + 1):
    try:
        # Copy backup to master
        shutil.copy2(BACKUP_FILE, MASTER_FILE)
        print(f'✅ Successfully saved on attempt {attempt}')
        print()
        print('Master file has been updated with Arizona property service details!')
        break
    except PermissionError:
        if attempt < max_retries:
            print(f'⚠️ Attempt {attempt} failed - file is open in Excel')
            print(f'Please close the Excel file. Retrying in 3 seconds...')
            print()
            time.sleep(3)
        else:
            print(f'❌ Failed after {max_retries} attempts')
            print()
            print('MANUAL ACTION REQUIRED:')
            print(f'1. Close the Excel file: {MASTER_FILE.name}')
            print(f'2. Copy this file: {BACKUP_FILE.name}')
            print(f'3. To this location: {MASTER_FILE.name}')
            print()
            exit(1)

