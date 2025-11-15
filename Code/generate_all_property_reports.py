"""
Generate Validated Reports for ALL 10 Properties

Systematically process entire portfolio and generate comprehensive validated
reports for each property based on actual master file data.
"""

import sys
sys.path.append('Code')
from property_validated_analysis import PropertyAnalyzer
import json
from datetime import datetime

def main():
    print("="*80)
    print("PORTFOLIO-WIDE VALIDATED ANALYSIS")
    print("="*80)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)

    master_file = 'Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx'

    # All 10 properties
    properties = [
        'Orion Prosper',
        'Orion Prosper Lakes',
        'Orion McKinney',
        'McCord Park FL',
        'The Club at Millenia',
        'Bella Mirage',
        'Mandarina',
        'Pavilions at Arrowhead',
        'Springs at Alta Mesa',
        'Tempe Vista'
    ]

    # Initialize analyzer
    analyzer = PropertyAnalyzer(master_file)

    # Track results
    results_summary = {
        'total_properties': len(properties),
        'successful': 0,
        'failed': 0,
        'properties': {},
        'start_time': datetime.now().isoformat()
    }

    # Process each property
    for i, property_name in enumerate(properties, 1):
        print(f"\n\n{'#'*80}")
        print(f"PROPERTY {i}/{len(properties)}: {property_name}")
        print(f"{'#'*80}")

        try:
            # Generate report
            output_path = analyzer.generate_property_report(property_name)

            # Get analysis results
            analysis = analyzer.analysis_results.get(property_name, {})

            results_summary['properties'][property_name] = {
                'status': 'SUCCESS',
                'output_path': output_path,
                'data_quality': analysis.get('data_quality', 'UNKNOWN'),
                'opportunities_count': len(analysis.get('savings_opportunities', [])),
                'has_compactor': analysis.get('compactor_analysis') is not None
            }

            results_summary['successful'] += 1

            print(f"\n[DONE] {property_name} - Report Generated Successfully")

        except Exception as e:
            print(f"\n[ERROR] {property_name} - Failed: {str(e)}")

            results_summary['properties'][property_name] = {
                'status': 'FAILED',
                'error': str(e)
            }

            results_summary['failed'] += 1

    # Final summary
    results_summary['end_time'] = datetime.now().isoformat()

    print(f"\n\n{'='*80}")
    print("PORTFOLIO ANALYSIS COMPLETE")
    print(f"{'='*80}")
    print(f"Total Properties: {results_summary['total_properties']}")
    print(f"Successful: {results_summary['successful']}")
    print(f"Failed: {results_summary['failed']}")
    print(f"Success Rate: {(results_summary['successful']/results_summary['total_properties']*100):.1f}%")

    # Save summary
    with open('Portfolio_Reports/analysis_summary.json', 'w') as f:
        json.dump(results_summary, f, indent=2)

    print(f"\nSummary saved: Portfolio_Reports/analysis_summary.json")

    # Display property-by-property results
    print(f"\n{'='*80}")
    print("PROPERTY-BY-PROPERTY RESULTS")
    print(f"{'='*80}")

    for prop, result in results_summary['properties'].items():
        status_icon = "[DONE]" if result['status'] == 'SUCCESS' else "[ERROR]"
        print(f"\n{status_icon} {prop}")

        if result['status'] == 'SUCCESS':
            print(f"  Report: {result['output_path']}")
            print(f"  Data Quality: {result['data_quality']}")
            print(f"  Opportunities: {result['opportunities_count']}")
            print(f"  Has Compactor: {'Yes' if result['has_compactor'] else 'No'}")
        else:
            print(f"  Error: {result['error']}")

    print(f"\n{'='*80}")
    print(f"[DONE] ALL REPORTS GENERATED")
    print(f"{'='*80}")

if __name__ == '__main__':
    main()
