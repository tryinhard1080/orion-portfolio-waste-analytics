"""
Orion Portfolio - Invoice Data Validation Script
Validates quality and accuracy of all extracted invoice data across 6 properties
Generates validation reports, auto-accept lists, and review queues
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import statistics

# Expected property data from CLAUDE.md
EXPECTED_PROPERTIES = {
    'Bella Mirage': {'units': 715, 'cpd': 10.68},
    'McCord Park FL': {'units': 416, 'cpd': 26.23},
    'Orion McKinney': {'units': 453, 'cpd': 13.28},
    'Orion Prosper': {'units': 312, 'cpd': 13.81},
    'Orion Prosper Lakes': {'units': 308, 'cpd': 13.09},
    'The Club at Millenia': {'units': 560, 'cpd': 21.00}
}

# Validation ranges
CPD_RANGE = (5, 40)
TOTAL_AMOUNT_RANGE = (100, 50000)
CONTROLLABLE_PERCENTAGE_RANGE = (0, 100)
CONFIDENCE_RANGE = (0.0, 1.0)

# Confidence thresholds
HIGH_CONFIDENCE = 0.85
MEDIUM_CONFIDENCE = 0.70


class InvoiceValidator:
    def __init__(self):
        self.warnings = []
        self.errors = []
        self.outliers = []
        self.by_property = {}

    def load_extraction_results(self) -> Dict:
        """Load all extraction result files"""
        extraction_dir = Path("C:/Users/Richard/Downloads/Orion Data/extraction_results")

        all_data = {}

        # Bella Mirage
        with open(extraction_dir / "Bella_Mirage_invoices.json", 'r') as f:
            bella_data = json.load(f)
            all_data['Bella Mirage'] = {
                'invoices': bella_data,
                'property_units': 715
            }

        # McCord Park FL
        with open(extraction_dir / "McCord_Park_FL_invoices.json", 'r') as f:
            mccord_data = json.load(f)
            all_data['McCord Park FL'] = {
                'invoices': mccord_data['invoices'],
                'property_units': mccord_data['property_units']
            }

        # Orion McKinney
        with open(extraction_dir / "Orion_McKinney_invoices.json", 'r') as f:
            mckinney_data = json.load(f)
            all_data['Orion McKinney'] = {
                'invoices': mckinney_data['invoices'],
                'property_units': mckinney_data['units']
            }

        # Orion Prosper
        with open(extraction_dir / "Orion_Prosper_invoices.json", 'r') as f:
            prosper_data = json.load(f)
            all_data['Orion Prosper'] = {
                'invoices': prosper_data['invoices'],
                'property_units': prosper_data['summary']['units']
            }

        # Orion Prosper Lakes
        with open(extraction_dir / "Orion_Prosper_Lakes_invoices.json", 'r') as f:
            prosper_lakes_data = json.load(f)
            all_data['Orion Prosper Lakes'] = {
                'invoices': prosper_lakes_data['invoices'],
                'property_units': prosper_lakes_data['unit_count']
            }

        # The Club at Millenia
        with open(extraction_dir / "The_Club_at_Millenia_invoices.json", 'r') as f:
            millenia_data = json.load(f)
            all_data['The Club at Millenia'] = {
                'invoices': millenia_data['invoices'],
                'property_units': millenia_data['property_units']
            }

        return all_data

    def get_invoice_value(self, invoice: Dict, key: str, default=None):
        """Safely get value from invoice with various structures"""
        # Try direct access
        if key in invoice:
            return invoice[key]

        # Try invoice_data
        if 'invoice_data' in invoice and key in invoice['invoice_data']:
            return invoice['invoice_data'][key]

        # Try calculated_fields
        if 'calculated_fields' in invoice and key in invoice['calculated_fields']:
            return invoice['calculated_fields'][key]

        # Try charges
        if 'charges' in invoice and key in invoice['charges']:
            return invoice['charges'][key]

        # Try calculations
        if 'calculations' in invoice and key in invoice['calculations']:
            return invoice['calculations'][key]

        # Try summary
        if 'summary' in invoice and key in invoice['summary']:
            return invoice['summary'][key]

        return default

    def validate_completeness(self, invoice: Dict, property_name: str) -> Tuple[bool, List[str]]:
        """Check if required fields are present"""
        missing_fields = []

        required_fields = [
            'invoice_number',
            'total_amount',
            'cost_per_door'
        ]

        for field in required_fields:
            if self.get_invoice_value(invoice, field) is None:
                missing_fields.append(field)

        return len(missing_fields) == 0, missing_fields

    def validate_data_types_ranges(self, invoice: Dict, property_name: str) -> Tuple[bool, List[str]]:
        """Validate data types and ranges"""
        issues = []

        # Total amount
        total_amount = self.get_invoice_value(invoice, 'total_amount')
        if total_amount is not None:
            if not (CPD_RANGE[0] * 100 <= total_amount <= TOTAL_AMOUNT_RANGE[1]):
                issues.append(f"Total amount ${total_amount:.2f} outside expected range ${TOTAL_AMOUNT_RANGE[0]}-${TOTAL_AMOUNT_RANGE[1]}")

        # Cost per door
        cpd = self.get_invoice_value(invoice, 'cost_per_door')
        if cpd is not None:
            if not (CPD_RANGE[0] <= cpd <= CPD_RANGE[1]):
                issues.append(f"CPD ${cpd:.2f} outside expected range ${CPD_RANGE[0]}-${CPD_RANGE[1]}")

        # Controllable percentage
        controllable_pct = self.get_invoice_value(invoice, 'controllable_percentage')
        if controllable_pct is not None:
            if not (CONTROLLABLE_PERCENTAGE_RANGE[0] <= controllable_pct <= CONTROLLABLE_PERCENTAGE_RANGE[1]):
                issues.append(f"Controllable percentage {controllable_pct}% outside valid range 0-100%")

        # Confidence
        confidence = self.get_invoice_value(invoice, 'confidence') or self.get_invoice_value(invoice, 'confidence_score')
        if confidence is not None:
            if not (CONFIDENCE_RANGE[0] <= confidence <= CONFIDENCE_RANGE[1]):
                issues.append(f"Confidence {confidence} outside valid range 0.0-1.0")

        return len(issues) == 0, issues

    def validate_cross_fields(self, invoice: Dict, property_name: str, property_units: int) -> Tuple[bool, List[str]]:
        """Validate cross-field calculations"""
        issues = []

        total_amount = self.get_invoice_value(invoice, 'total_amount')
        cpd = self.get_invoice_value(invoice, 'cost_per_door')

        if total_amount is not None and cpd is not None and property_units > 0:
            expected_cpd = total_amount / property_units
            variance = abs(cpd - expected_cpd)

            if variance > 0.02:  # Allow 2 cent variance
                issues.append(f"CPD mismatch: stated ${cpd:.2f} vs calculated ${expected_cpd:.2f} (${total_amount:.2f}/{property_units} units)")

        return len(issues) == 0, issues

    def detect_outliers(self, property_name: str, invoices: List[Dict]) -> List[Dict]:
        """Detect statistical outliers in CPD"""
        outliers = []

        cpds = []
        for inv in invoices:
            cpd = self.get_invoice_value(inv, 'cost_per_door')
            if cpd is not None:
                cpds.append(cpd)

        if len(cpds) < 3:
            return outliers

        mean_cpd = statistics.mean(cpds)
        stdev_cpd = statistics.stdev(cpds) if len(cpds) > 1 else 0

        for inv in invoices:
            cpd = self.get_invoice_value(inv, 'cost_per_door')
            if cpd is not None and stdev_cpd > 0:
                z_score = abs((cpd - mean_cpd) / stdev_cpd)
                if z_score > 2:
                    outliers.append({
                        'property': property_name,
                        'invoice_number': self.get_invoice_value(inv, 'invoice_number', 'unknown'),
                        'cpd': cpd,
                        'mean_cpd': mean_cpd,
                        'stdev': stdev_cpd,
                        'z_score': z_score,
                        'reason': f"CPD ${cpd:.2f} is {z_score:.1f} standard deviations from mean ${mean_cpd:.2f}"
                    })

            # Check controllable percentage
            controllable_pct = self.get_invoice_value(inv, 'controllable_percentage')
            if controllable_pct is not None and controllable_pct > 30:
                outliers.append({
                    'property': property_name,
                    'invoice_number': self.get_invoice_value(inv, 'invoice_number', 'unknown'),
                    'controllable_percentage': controllable_pct,
                    'reason': f"Unusually high controllable percentage: {controllable_pct:.1f}%"
                })

        return outliers

    def validate_property(self, property_name: str, property_data: Dict) -> Dict:
        """Validate all invoices for a property"""
        invoices = property_data['invoices']
        property_units = property_data['property_units']
        expected = EXPECTED_PROPERTIES.get(property_name, {})

        valid_count = 0
        warning_count = 0
        error_count = 0

        cpds = []
        confidences = []

        for invoice in invoices:
            # Completeness check
            complete, missing = self.validate_completeness(invoice, property_name)
            if not complete:
                error_count += 1
                self.errors.append({
                    'property': property_name,
                    'invoice': self.get_invoice_value(invoice, 'invoice_number', 'unknown'),
                    'type': 'completeness',
                    'message': f"Missing required fields: {', '.join(missing)}"
                })

            # Data type and range validation
            ranges_ok, range_issues = self.validate_data_types_ranges(invoice, property_name)
            if not ranges_ok:
                warning_count += 1
                for issue in range_issues:
                    self.warnings.append({
                        'property': property_name,
                        'invoice': self.get_invoice_value(invoice, 'invoice_number', 'unknown'),
                        'type': 'range',
                        'message': issue
                    })

            # Cross-field validation
            cross_ok, cross_issues = self.validate_cross_fields(invoice, property_name, property_units)
            if not cross_ok:
                warning_count += 1
                for issue in cross_issues:
                    self.warnings.append({
                        'property': property_name,
                        'invoice': self.get_invoice_value(invoice, 'invoice_number', 'unknown'),
                        'type': 'calculation',
                        'message': issue
                    })

            # Track metrics
            cpd = self.get_invoice_value(invoice, 'cost_per_door')
            if cpd is not None:
                cpds.append(cpd)

            confidence = self.get_invoice_value(invoice, 'confidence') or self.get_invoice_value(invoice, 'confidence_score')
            if confidence is not None:
                confidences.append(confidence)

            # Count as valid if no errors (warnings are ok)
            if complete and ranges_ok:
                valid_count += 1

        # Detect outliers
        property_outliers = self.detect_outliers(property_name, invoices)
        self.outliers.extend(property_outliers)

        # Calculate averages
        avg_cpd = statistics.mean(cpds) if cpds else 0
        avg_confidence = statistics.mean(confidences) if confidences else 0

        # Check variance from expected
        expected_cpd = expected.get('cpd', 0)
        cpd_variance_pct = 0
        if expected_cpd > 0:
            cpd_variance_pct = ((avg_cpd - expected_cpd) / expected_cpd) * 100

            if abs(cpd_variance_pct) > 10:
                self.warnings.append({
                    'property': property_name,
                    'invoice': 'ALL',
                    'type': 'variance',
                    'message': f"Average CPD ${avg_cpd:.2f} is {cpd_variance_pct:+.1f}% different from expected ${expected_cpd:.2f}"
                })

        return {
            'invoices': len(invoices),
            'valid': valid_count,
            'warnings': warning_count,
            'errors': error_count,
            'avg_confidence': round(avg_confidence, 2),
            'avg_cpd': round(avg_cpd, 2),
            'expected_cpd': expected_cpd,
            'cpd_variance_pct': round(cpd_variance_pct, 1)
        }

    def categorize_by_confidence(self, all_data: Dict) -> Dict:
        """Categorize invoices by confidence level"""
        high_conf = []
        medium_conf = []
        low_conf = []

        for property_name, property_data in all_data.items():
            for invoice in property_data['invoices']:
                confidence = self.get_invoice_value(invoice, 'confidence') or self.get_invoice_value(invoice, 'confidence_score') or 1.0

                invoice_info = {
                    'property': property_name,
                    'invoice_number': self.get_invoice_value(invoice, 'invoice_number', 'unknown'),
                    'confidence': confidence,
                    'total_amount': self.get_invoice_value(invoice, 'total_amount'),
                    'cost_per_door': self.get_invoice_value(invoice, 'cost_per_door')
                }

                if confidence >= HIGH_CONFIDENCE:
                    high_conf.append(invoice_info)
                elif confidence >= MEDIUM_CONFIDENCE:
                    medium_conf.append(invoice_info)
                else:
                    low_conf.append(invoice_info)

        return {
            'high_confidence': high_conf,
            'medium_confidence': medium_conf,
            'low_confidence': low_conf
        }

    def generate_auto_accept_list(self, all_data: Dict) -> List[Dict]:
        """Generate list of invoices ready for auto-acceptance"""
        auto_accept = []

        for property_name, property_data in all_data.items():
            for invoice in property_data['invoices']:
                confidence = self.get_invoice_value(invoice, 'confidence') or self.get_invoice_value(invoice, 'confidence_score') or 1.0
                invoice_number = self.get_invoice_value(invoice, 'invoice_number', 'unknown')

                # Check if this invoice has any errors
                has_errors = any(e['invoice'] == invoice_number and e['property'] == property_name for e in self.errors)

                if confidence >= HIGH_CONFIDENCE and not has_errors:
                    auto_accept.append({
                        'property': property_name,
                        'invoice_number': invoice_number,
                        'confidence': confidence,
                        'total_amount': self.get_invoice_value(invoice, 'total_amount'),
                        'cost_per_door': self.get_invoice_value(invoice, 'cost_per_door'),
                        'status': 'READY_FOR_GOOGLE_SHEETS'
                    })

        return auto_accept

    def generate_review_queue(self, all_data: Dict) -> List[Dict]:
        """Generate list of invoices needing manual review"""
        review_queue = []

        for property_name, property_data in all_data.items():
            for invoice in property_data['invoices']:
                confidence = self.get_invoice_value(invoice, 'confidence') or self.get_invoice_value(invoice, 'confidence_score') or 1.0
                invoice_number = self.get_invoice_value(invoice, 'invoice_number', 'unknown')

                # Check if this invoice has warnings or errors
                has_warnings = any(w['invoice'] == invoice_number and w['property'] == property_name for w in self.warnings)
                has_errors = any(e['invoice'] == invoice_number and e['property'] == property_name for e in self.errors)

                # Needs review if low/medium confidence or has issues
                if confidence < HIGH_CONFIDENCE or has_warnings or has_errors:
                    reasons = []
                    if confidence < HIGH_CONFIDENCE:
                        reasons.append(f"Low/medium confidence: {confidence:.2f}")
                    if has_errors:
                        reasons.append("Has errors")
                    if has_warnings:
                        reasons.append("Has warnings")

                    review_queue.append({
                        'property': property_name,
                        'invoice_number': invoice_number,
                        'confidence': confidence,
                        'total_amount': self.get_invoice_value(invoice, 'total_amount'),
                        'cost_per_door': self.get_invoice_value(invoice, 'cost_per_door'),
                        'review_reasons': reasons
                    })

        return review_queue

    def validate_all(self) -> Dict:
        """Run complete validation suite"""
        print("Loading extraction results...")
        all_data = self.load_extraction_results()

        print("Validating invoices by property...")
        total_invoices = 0
        for property_name, property_data in all_data.items():
            print(f"  Validating {property_name}...")
            self.by_property[property_name] = self.validate_property(property_name, property_data)
            total_invoices += len(property_data['invoices'])

        print("Categorizing by confidence...")
        by_confidence = self.categorize_by_confidence(all_data)

        print("Generating auto-accept list...")
        auto_accept = self.generate_auto_accept_list(all_data)

        print("Generating review queue...")
        review_queue = self.generate_review_queue(all_data)

        # Calculate overall confidence
        all_confidences = []
        for conf_list in by_confidence.values():
            all_confidences.extend([item['confidence'] for item in conf_list])
        avg_confidence = statistics.mean(all_confidences) if all_confidences else 0

        # Summary stats
        fully_valid = sum(1 for p in self.by_property.values() if p['errors'] == 0 and p['warnings'] == 0)
        with_warnings = sum(1 for p in self.by_property.values() if p['warnings'] > 0 and p['errors'] == 0)
        with_errors = sum(1 for p in self.by_property.values() if p['errors'] > 0)

        validation_report = {
            'validation_timestamp': datetime.now().isoformat(),
            'summary': {
                'total_invoices': total_invoices,
                'properties_processed': len(all_data),
                'fully_valid': fully_valid,
                'with_warnings': with_warnings,
                'with_errors': with_errors,
                'avg_confidence': round(avg_confidence, 2)
            },
            'by_confidence': {
                'high_confidence': len(by_confidence['high_confidence']),
                'medium_confidence': len(by_confidence['medium_confidence']),
                'low_confidence': len(by_confidence['low_confidence'])
            },
            'by_property': self.by_property,
            'warnings': self.warnings,
            'errors': self.errors,
            'outliers': self.outliers,
            'quality_metrics': {
                'auto_accept_count': len(auto_accept),
                'auto_accept_rate_pct': round((len(auto_accept) / total_invoices * 100), 1) if total_invoices > 0 else 0,
                'review_queue_count': len(review_queue),
                'review_queue_rate_pct': round((len(review_queue) / total_invoices * 100), 1) if total_invoices > 0 else 0
            }
        }

        return {
            'validation_report': validation_report,
            'auto_accept_list': auto_accept,
            'review_queue': review_queue
        }


def generate_markdown_summary(validation_results: Dict) -> str:
    """Generate human-readable markdown summary"""
    report = validation_results['validation_report']
    auto_accept = validation_results['auto_accept_list']
    review_queue = validation_results['review_queue']

    md = f"""# Invoice Data Validation Summary

**Validation Date:** {report['validation_timestamp']}

## Executive Summary

- **Total Invoices Processed:** {report['summary']['total_invoices']}
- **Properties Analyzed:** {report['summary']['properties_processed']}
- **Average Confidence Score:** {report['summary']['avg_confidence']:.2%}

### Quality Status

- ✅ **Fully Valid:** {report['summary']['fully_valid']} properties
- ⚠️ **With Warnings:** {report['summary']['with_warnings']} properties
- ❌ **With Errors:** {report['summary']['with_errors']} properties

## Confidence Distribution

- 🟢 **High Confidence (≥85%):** {report['by_confidence']['high_confidence']} invoices
- 🟡 **Medium Confidence (70-84%):** {report['by_confidence']['medium_confidence']} invoices
- 🔴 **Low Confidence (<70%):** {report['by_confidence']['low_confidence']} invoices

## Auto-Accept Analysis

- **Auto-Accept Count:** {len(auto_accept)} invoices
- **Auto-Accept Rate:** {report['quality_metrics']['auto_accept_rate_pct']}%
- **Status:** {'✅ TARGET MET (≥85%)' if report['quality_metrics']['auto_accept_rate_pct'] >= 85 else '⚠️ BELOW TARGET'}

## Review Queue

- **Manual Review Required:** {len(review_queue)} invoices
- **Review Rate:** {report['quality_metrics']['review_queue_rate_pct']}%

## Property-Level Results

"""

    for property_name, stats in report['by_property'].items():
        status_icon = '✅' if stats['errors'] == 0 else '❌'
        md += f"""### {status_icon} {property_name}

- **Invoices:** {stats['invoices']}
- **Valid:** {stats['valid']} | **Warnings:** {stats['warnings']} | **Errors:** {stats['errors']}
- **Avg Confidence:** {stats['avg_confidence']:.2%}
- **Avg CPD:** ${stats['avg_cpd']:.2f} (Expected: ${stats['expected_cpd']:.2f})
- **Variance:** {stats['cpd_variance_pct']:+.1f}%

"""

    if report['errors']:
        md += "\n## ❌ Errors Found\n\n"
        for error in report['errors']:
            md += f"- **{error['property']}** - Invoice {error['invoice']}: {error['message']}\n"

    if report['warnings']:
        md += "\n## ⚠️ Warnings\n\n"
        for warning in report['warnings'][:20]:  # Limit to first 20
            md += f"- **{warning['property']}** - Invoice {warning['invoice']}: {warning['message']}\n"

        if len(report['warnings']) > 20:
            md += f"\n*...and {len(report['warnings']) - 20} more warnings*\n"

    if report['outliers']:
        md += "\n## 📊 Outliers Detected\n\n"
        for outlier in report['outliers'][:10]:  # Limit to first 10
            md += f"- **{outlier['property']}** - Invoice {outlier.get('invoice_number', 'unknown')}: {outlier['reason']}\n"

        if len(report['outliers']) > 10:
            md += f"\n*...and {len(report['outliers']) - 10} more outliers*\n"

    md += f"""
## Next Steps

1. **Auto-Accept ({len(auto_accept)} invoices):**
   - Review `auto_accept_list.json`
   - Upload high-confidence invoices to Google Sheets

2. **Manual Review ({len(review_queue)} invoices):**
   - Review `review_queue.json`
   - Address errors and warnings
   - Verify outliers

3. **Data Quality:**
   - Target: ≥85% auto-accept rate ({'ACHIEVED ✅' if report['quality_metrics']['auto_accept_rate_pct'] >= 85 else 'NOT MET ⚠️'})
   - Target: ≥90% avg confidence ({'ACHIEVED ✅' if report['summary']['avg_confidence'] >= 0.90 else 'NOT MET ⚠️'})
   - Target: <10% CPD variance ({'ACHIEVED ✅' if all(abs(p['cpd_variance_pct']) < 10 for p in report['by_property'].values()) else 'REVIEW NEEDED ⚠️'})

---
*Generated by Orion Portfolio Invoice Validation System*
"""

    return md


def main():
    """Main validation execution"""
    print("=" * 80)
    print("ORION PORTFOLIO - INVOICE DATA VALIDATION")
    print("=" * 80)
    print()

    # Create validation directory
    validation_dir = Path("C:/Users/Richard/Downloads/Orion Data/validation_reports")
    validation_dir.mkdir(exist_ok=True)

    # Run validation
    validator = InvoiceValidator()
    results = validator.validate_all()

    # Save validation report JSON
    print("\nSaving validation_report.json...")
    with open(validation_dir / "validation_report.json", 'w') as f:
        json.dump(results['validation_report'], f, indent=2)

    # Save auto-accept list
    print("Saving auto_accept_list.json...")
    with open(validation_dir / "auto_accept_list.json", 'w') as f:
        json.dump(results['auto_accept_list'], f, indent=2)

    # Save review queue
    print("Saving review_queue.json...")
    with open(validation_dir / "review_queue.json", 'w') as f:
        json.dump(results['review_queue'], f, indent=2)

    # Generate and save markdown summary
    print("Generating validation_summary.md...")
    summary_md = generate_markdown_summary(results)
    with open(validation_dir / "validation_summary.md", 'w', encoding='utf-8') as f:
        f.write(summary_md)

    print("\n" + "=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80)
    print(f"\nResults saved to: {validation_dir}")
    print(f"  - validation_report.json")
    print(f"  - auto_accept_list.json ({len(results['auto_accept_list'])} invoices)")
    print(f"  - review_queue.json ({len(results['review_queue'])} invoices)")
    print(f"  - validation_summary.md")
    print()

    # Print summary stats
    report = results['validation_report']
    print("SUMMARY STATISTICS:")
    print(f"  Total Invoices: {report['summary']['total_invoices']}")
    print(f"  Auto-Accept Rate: {report['quality_metrics']['auto_accept_rate_pct']}%")
    print(f"  Average Confidence: {report['summary']['avg_confidence']:.2%}")
    print(f"  Errors: {len(report['errors'])}")
    print(f"  Warnings: {len(report['warnings'])}")
    print(f"  Outliers: {len(report['outliers'])}")
    print()


if __name__ == "__main__":
    main()
