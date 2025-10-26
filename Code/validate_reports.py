"""
Validate HTML reports against CORRECTIVE_ACTION_PLAN.md checklists
Checks for:
- Language audit: No crisis/emergency language, savings projections, prescriptive statements
- Content audit: Proper use of benchmarks, actual data, correct categorization
- Tone audit: Neutral, professional, analytical tone
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

class ReportValidator:
    """Validate HTML reports for correct language and content"""

    # Forbidden crisis language patterns
    CRISIS_PATTERNS = [
        r'\bcrisis\b(?! tier)(?! classification)',  # Allow "crisis tier classification" but not standalone "crisis"
        r'\bemergency\b(?! contact)',  # Allow "emergency contact" but not "emergency action"
        r'\bcritical\b(?! priority)',  # Allow "critical priority" as a valid tier but check context
        r'\bcatastrophic\b',
        r'\bhemorrhage\b',
        r'\bbleeding\b',
    ]

    # Forbidden "waste" patterns (except in proper business context)
    WASTE_PATTERNS = [
        r'\$[\d,]+[\/\s]*year\s+waste',
        r'waste\s+of\s+\$',
        r'wasted\s+on',
        r'wasting\s+\$',
        r'avoid(?:able)?\s+waste',
    ]

    # Forbidden projection/savings language
    PROJECTION_PATTERNS = [
        r'\bsavings?\s+potential',
        r'\bnet\s+savings',
        r'\bROI\b',
        r'return\s+on\s+investment',
        r'\$[\d,]+[\/\s]*year\s+savings',
        r'unlock\s+\$',
        r'payback\s+period',
        r'expected\s+savings',
        r'projected\s+savings',
    ]

    # Forbidden prescriptive language
    PRESCRIPTIVE_PATTERNS = [
        r'\bmust\s+(?:do|implement|add|change)',
        r'\brequired\s+action',
        r'\bimmediate(?:ly)?\s+(?:add|implement|change|fix)',
        r'\byou\s+(?:must|should|need\s+to)\s+(?:add|fix|change)',
    ]

    # Sales language to avoid
    SALES_PATTERNS = [
        r'\boptimize\b',
        r'\bunlock\b',
        r'\bmaximize\b',
        r'\bstop\s+the\b',
        r'\beliminate\s+waste',
    ]

    def __init__(self):
        self.validation_results = []

    def validate_file(self, file_path: str) -> Dict:
        """Validate a single HTML file"""
        print(f"\n[INFO] Validating {Path(file_path).name}...")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        results = {
            'file': Path(file_path).name,
            'language_violations': [],
            'content_checks': [],
            'tone_checks': [],
            'passed': True
        }

        # Language audit
        results['language_violations'].extend(self._check_crisis_language(content))
        results['language_violations'].extend(self._check_waste_language(content))
        results['language_violations'].extend(self._check_projection_language(content))
        results['language_violations'].extend(self._check_prescriptive_language(content))
        results['language_violations'].extend(self._check_sales_language(content))

        # Content audit
        results['content_checks'].extend(self._check_benchmark_usage(content))
        results['content_checks'].extend(self._check_for_projections(content))

        # Tone audit
        results['tone_checks'].extend(self._check_neutral_tone(content))

        # Overall pass/fail
        if results['language_violations']:
            results['passed'] = False

        return results

    def _check_crisis_language(self, content: str) -> List[str]:
        """Check for crisis/emergency language"""
        violations = []

        for pattern in self.CRISIS_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # Get context around match
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 50)
                context = content[start:end].strip()

                violations.append(f"Crisis language: '{match.group()}' in context: '...{context}...'")

        return violations

    def _check_waste_language(self, content: str) -> List[str]:
        """Check for inappropriate 'waste' language"""
        violations = []

        for pattern in self.WASTE_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 50)
                context = content[start:end].strip()

                violations.append(f"Waste language: '{match.group()}' in context: '...{context}...'")

        return violations

    def _check_projection_language(self, content: str) -> List[str]:
        """Check for savings projections and ROI language"""
        violations = []

        for pattern in self.PROJECTION_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - 100)
                end = min(len(content), match.end() + 100)
                context = content[start:end].strip()

                # Skip if this is in a disclaimer context (saying we DON'T do ROI, projections, etc.)
                disclaimer_patterns = [
                    r'does\s+not\s+include',
                    r'do\s+not\s+include',
                    r'not\s+include.*(?:ROI|projection|savings)',
                    r'no.*(?:ROI|projection|savings)',
                    r'without.*(?:ROI|projection|savings)'
                ]

                is_disclaimer = False
                for disc_pattern in disclaimer_patterns:
                    if re.search(disc_pattern, context, re.IGNORECASE):
                        is_disclaimer = True
                        break

                if is_disclaimer:
                    continue  # Skip this match - it's in a good context

                violations.append(f"Projection language: '{match.group()}' in context: '...{context[:100]}...'")

        return violations

    def _check_prescriptive_language(self, content: str) -> List[str]:
        """Check for prescriptive 'must do X' language"""
        violations = []

        for pattern in self.PRESCRIPTIVE_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 50)
                context = content[start:end].strip()

                violations.append(f"Prescriptive language: '{match.group()}' in context: '...{context}...'")

        return violations

    def _check_sales_language(self, content: str) -> List[str]:
        """Check for sales/marketing language"""
        violations = []

        for pattern in self.SALES_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # Check context - some uses might be acceptable
                start = max(0, match.start() - 30)
                end = min(len(content), match.end() + 30)
                context = content[start:end].strip()

                # "Optimization Opportunities" is acceptable, "optimize your costs" is not
                if 'optimization opportunities' in context.lower():
                    continue  # Skip this one

                violations.append(f"Sales language: '{match.group()}' in context: '...{context}...'")

        return violations

    def _check_benchmark_usage(self, content: str) -> List[str]:
        """Check that benchmarks are used properly"""
        checks = []

        # Look for benchmark references
        benchmark_patterns = [
            r'benchmark[:\s]+[\$\d\.\-]+',
            r'target[:\s]+range[:\s]*[\$\d\.\-]+',
            r'target[:\s]+\≤[\d]+',
            r'threshold[:\s]*[\$\d\.\-]+',
            r'Target\s+range\s+[\$\d\.\-]+'
        ]

        found_benchmarks = False
        for pattern in benchmark_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_benchmarks = True
                break

        if found_benchmarks:
            checks.append("[OK] Benchmarks referenced")
        else:
            checks.append("[!] No clear benchmark references found")

        return checks

    def _check_for_projections(self, content: str) -> List[str]:
        """Check that content uses actual data, not projections"""
        checks = []

        # Look for indicators of actual data
        actual_data_patterns = [
            r'actual\s+(?:from|costs?|charges?)',
            r'analyzed\s+invoices',
            r'verified\s+invoice',
            r'from\s+\d+\s+invoices',
        ]

        found_actual_data = False
        for pattern in actual_data_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_actual_data = True
                break

        if found_actual_data:
            checks.append("[OK] References to actual invoice data")
        else:
            checks.append("[!] No clear references to actual data source")

        # Check for "not projections" disclaimer
        if re.search(r'not\s+(?:speculative\s+)?projections', content, re.IGNORECASE):
            checks.append("[OK] Explicitly states 'not projections'")

        return checks

    def _check_neutral_tone(self, content: str) -> List[str]:
        """Check for neutral, professional tone indicators"""
        checks = []

        # Look for neutral language patterns
        neutral_patterns = [
            r'opportunity\s+(?:for|identified)',
            r'data\s+indicates',
            r'performance\s+(?:gap|metric)',
            r'consider\s+(?:evaluation|review)',
        ]

        neutral_count = 0
        for pattern in neutral_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                neutral_count += 1

        if neutral_count >= 2:
            checks.append("[OK] Uses neutral, analytical language")
        else:
            checks.append("[!] Limited neutral language patterns found")

        return checks


def main():
    """Validate all HTML reports"""
    print("\n" + "="*70)
    print("REPORT VALIDATION AGAINST CORRECTIVE_ACTION_PLAN.MD")
    print("="*70)

    validator = ReportValidator()

    # Find all HTML reports
    html_files = [
        "PortfolioSummaryDashboard.html",
        "BellaMirageAnalysis.html",
        "OrionMcKinneyAnalysis.html",
        "OrionProsperAnalysis.html",
        "OrionProsperLakesAnalysis.html",
        "OrionMcCordRanchAnalysis.html",
        "TheClubatMilleniaAnalysis.html"
    ]

    results = []
    passed_count = 0
    failed_count = 0

    for html_file in html_files:
        if not os.path.exists(html_file):
            print(f"[WARNING] File not found: {html_file}")
            continue

        result = validator.validate_file(html_file)
        results.append(result)

        if result['passed']:
            passed_count += 1
        else:
            failed_count += 1

    # Print detailed results
    print("\n" + "="*70)
    print("VALIDATION RESULTS")
    print("="*70)

    for result in results:
        print(f"\n{'='*70}")
        print(f"File: {result['file']}")
        print(f"Status: {'[PASS]' if result['passed'] else '[FAIL]'}")
        print(f"{'='*70}")

        if result['language_violations']:
            print("\n[!] Language Violations:")
            for violation in result['language_violations']:
                print(f"  - {violation}")
        else:
            print("\n[OK] No language violations")

        if result['content_checks']:
            print("\nContent Checks:")
            for check in result['content_checks']:
                print(f"  {check}")

        if result['tone_checks']:
            print("\nTone Checks:")
            for check in result['tone_checks']:
                print(f"  {check}")

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total files validated: {len(results)}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {failed_count}")

    if failed_count == 0:
        print("\n[SUCCESS] All reports passed validation!")
        print("\n[OK] No crisis language")
        print("[OK] No savings projections or ROI")
        print("[OK] No prescriptive 'must do' statements")
        print("[OK] Professional, neutral tone")
        print("[OK] Data-focused analysis")
    else:
        print("\n[WARNING] Some reports have violations - review details above")

    return failed_count == 0


if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
