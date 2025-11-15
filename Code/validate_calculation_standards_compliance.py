"""
Calculation Standards Compliance Validator

Scans project files to identify uses of old formulas and ensures
compliance with official calculation standards.

Reference: Documentation/CONTAINER_SPECIFICATIONS_AND_CALCULATION_STANDARDS.md
"""

import os
import re
from pathlib import Path


def scan_file_for_old_formulas(file_path):
    """
    Scan a file for references to old/incorrect formulas

    Returns: List of issues found
    """
    issues = []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')

            # Check for old "14.49" factor usage
            if '14.49' in content:
                # Find line numbers
                for i, line in enumerate(lines, 1):
                    if '14.49' in line:
                        issues.append({
                            'type': 'OLD_FORMULA_FACTOR',
                            'line': i,
                            'content': line.strip(),
                            'severity': 'WARNING',
                            'message': 'Uses 14.49 shortcut - should show full formula (Tons × 2000 / 138)'
                        })

            # Check for incorrect density factor (225 for compactors)
            if re.search(r'(compactor|ton).*225', content, re.IGNORECASE):
                for i, line in enumerate(lines, 1):
                    if re.search(r'(compactor|ton).*225', line, re.IGNORECASE):
                        issues.append({
                            'type': 'INCORRECT_DENSITY',
                            'line': i,
                            'content': line.strip(),
                            'severity': 'ERROR',
                            'message': 'Uses 225 lbs/yd³ density - should use 138 for loose MSW'
                        })

            # Check for incorrect weeks/month multiplier
            # Skip lines that say "not 4.0" as they're warning AGAINST it
            if re.search(r'(weeks?.*month|per.*month).*[^4\.]4\.0[^\d]', content, re.IGNORECASE):
                for i, line in enumerate(lines, 1):
                    if re.search(r'4\.0[^\d]', line) and 'month' in line.lower():
                        # Skip if line is saying NOT to use 4.0
                        if 'not 4.0' in line.lower() or 'not 4.5' in line.lower():
                            continue
                        issues.append({
                            'type': 'INCORRECT_WEEKS_MULTIPLIER',
                            'line': i,
                            'content': line.strip(),
                            'severity': 'ERROR',
                            'message': 'Uses 4.0 weeks/month - should use 4.33 (52/12)'
                        })

    except Exception as e:
        issues.append({
            'type': 'READ_ERROR',
            'line': 0,
            'content': str(e),
            'severity': 'ERROR',
            'message': f'Could not read file: {e}'
        })

    return issues


def scan_project(base_path="."):
    """
    Scan entire project for calculation compliance issues

    Args:
        base_path: Root directory to scan

    Returns:
        dict: Results by file
    """
    print("="*70)
    print("CALCULATION STANDARDS COMPLIANCE VALIDATION")
    print("="*70)
    print(f"\nScanning: {os.path.abspath(base_path)}")
    print(f"Reference: Documentation/CONTAINER_SPECIFICATIONS_AND_CALCULATION_STANDARDS.md\n")

    # File extensions to scan
    scan_extensions = {
        '.py',   # Python scripts
        '.md',   # Documentation
        '.txt',  # Text files
        '.yml',  # Config files
        '.yaml',
        '.json'
    }

    # Directories to skip
    skip_dirs = {
        '.git',
        '__pycache__',
        'node_modules',
        'venv',
        'Archive',
        '.venv'
    }

    results = {}
    total_files_scanned = 0
    total_issues_found = 0

    base_path = Path(base_path)

    for root, dirs, files in os.walk(base_path):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for file in files:
            file_path = Path(root) / file

            # Check if file should be scanned
            if file_path.suffix not in scan_extensions:
                continue

            # Skip this validation script itself
            if file_path.name == 'validate_calculation_standards_compliance.py':
                continue

            # Scan file
            issues = scan_file_for_old_formulas(file_path)

            if issues:
                relative_path = file_path.relative_to(base_path)
                results[str(relative_path)] = issues
                total_issues_found += len(issues)

            total_files_scanned += 1

    return results, total_files_scanned, total_issues_found


def generate_report(results, total_files_scanned, total_issues_found):
    """Generate compliance report"""

    # Set console encoding to UTF-8 for Windows
    import sys
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("\n" + "="*70)
    print("SCAN RESULTS")
    print("="*70)

    print(f"\nFiles Scanned: {total_files_scanned}")
    print(f"Issues Found: {total_issues_found}")
    print(f"Files with Issues: {len(results)}\n")

    if total_issues_found == 0:
        print("[OK] No compliance issues found!")
        print("\nAll files comply with official calculation standards.")
        return

    # Group by severity
    errors = []
    warnings = []

    for file_path, issues in sorted(results.items()):
        for issue in issues:
            if issue['severity'] == 'ERROR':
                errors.append((file_path, issue))
            else:
                warnings.append((file_path, issue))

    # Report errors
    if errors:
        print("\n" + "="*70)
        print(f"ERRORS ({len(errors)}) - Must be fixed")
        print("="*70)

        for file_path, issue in errors:
            print(f"\n[ERROR] {file_path}:{issue['line']}")
            print(f"  Type: {issue['type']}")
            print(f"  Issue: {issue['message']}")
            print(f"  Line: {issue['content'][:80]}")

    # Report warnings
    if warnings:
        print("\n" + "="*70)
        print(f"WARNINGS ({len(warnings)}) - Should be reviewed")
        print("="*70)

        for file_path, issue in warnings:
            print(f"\n[WARNING] {file_path}:{issue['line']}")
            print(f"  Type: {issue['type']}")
            print(f"  Issue: {issue['message']}")
            print(f"  Line: {issue['content'][:80]}")

    # Summary
    print("\n" + "="*70)
    print("RECOMMENDATIONS")
    print("="*70)
    print("\n1. Review all flagged files")
    print("2. Update formulas to use official standards:")
    print("   - Compactors: (Tons × 2000 / 138) / Units")
    print("   - Dumpsters: (Size × Containers × Pickups/Week × 4.33) / Units")
    print("3. Reference: Documentation/CONTAINER_SPECIFICATIONS_AND_CALCULATION_STANDARDS.md")
    print("4. Update skill documentation if needed")
    print("5. Re-run this validator to confirm fixes\n")


def main():
    """Main validation routine"""

    # Scan project
    results, total_files, total_issues = scan_project()

    # Generate report
    generate_report(results, total_files, total_issues)

    print("="*70)
    print("VALIDATION COMPLETE")
    print("="*70)
    print()

    # Return exit code
    return 0 if total_issues == 0 else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
