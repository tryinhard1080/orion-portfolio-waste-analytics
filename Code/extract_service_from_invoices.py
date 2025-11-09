"""
Extract Service Details from Invoice Descriptions for Orion Prosper Properties

This script analyzes invoice line item descriptions to extract:
- Container sizes
- Container counts
- Service frequencies
- Container types
"""

import pandas as pd
import re
from pathlib import Path
from collections import Counter

# Paths
BASE_DIR = Path(__file__).parent.parent
MASTER_FILE = BASE_DIR / "Portfolio_Reports" / "MASTER_Portfolio_Complete_Data.xlsx"

# Properties to extract
PROPERTIES = ['Orion Prosper', 'Orion Prosper Lakes']

def extract_container_info(description):
    """Extract container size, type, and frequency from description"""
    
    if pd.isna(description):
        return None
    
    desc = str(description).upper()
    
    info = {
        'size': None,
        'type': None,
        'frequency': None,
        'count': None
    }
    
    # Extract container size (e.g., "4 YD", "6YD", "8-YD")
    size_match = re.search(r'(\d+)\s*[-]?\s*YD', desc)
    if size_match:
        info['size'] = int(size_match.group(1))
    
    # Extract container type
    if 'COMPACTOR' in desc:
        info['type'] = 'Compactor'
    elif 'FRONT' in desc or 'FEL' in desc or 'FL' in desc:
        info['type'] = 'Front Loader'
    elif 'DUMPSTER' in desc:
        info['type'] = 'Dumpster'
    elif 'CART' in desc:
        info['type'] = 'Cart'
    
    # Extract frequency (e.g., "3X", "3 X WK", "WEEKLY")
    freq_match = re.search(r'(\d+)\s*X', desc)
    if freq_match:
        info['frequency'] = int(freq_match.group(1))
    elif 'WEEKLY' in desc or '1X' in desc:
        info['frequency'] = 1
    elif 'DAILY' in desc:
        info['frequency'] = 7
    
    # Extract count (e.g., "QTY 2", "2 EA")
    count_match = re.search(r'(?:QTY|QUANTITY)\s*(\d+)', desc)
    if count_match:
        info['count'] = int(count_match.group(1))
    
    return info

def analyze_property_invoices(property_name):
    """Analyze all invoice descriptions for a property"""
    
    print('=' * 80)
    print(f'ANALYZING: {property_name}')
    print('=' * 80)
    print()
    
    # Load property data
    df = pd.read_excel(MASTER_FILE, sheet_name=property_name)
    
    print(f'Total Invoice Rows: {len(df)}')
    print()
    
    # Extract info from all descriptions
    all_sizes = []
    all_types = []
    all_frequencies = []
    all_descriptions = []
    
    for idx, row in df.iterrows():
        desc = row.get('Description', '')
        if pd.notna(desc):
            all_descriptions.append(desc)
            info = extract_container_info(desc)
            if info:
                if info['size']:
                    all_sizes.append(info['size'])
                if info['type']:
                    all_types.append(info['type'])
                if info['frequency']:
                    all_frequencies.append(info['frequency'])
    
    print(f'Descriptions Analyzed: {len(all_descriptions)}')
    print()
    
    # Show sample descriptions
    print('SAMPLE DESCRIPTIONS:')
    print('-' * 80)
    for i, desc in enumerate(all_descriptions[:10], 1):
        print(f'{i}. {desc}')
    print()
    
    if len(all_descriptions) > 10:
        print(f'... and {len(all_descriptions) - 10} more')
        print()
    
    # Analyze patterns
    print('EXTRACTED PATTERNS:')
    print('-' * 80)
    
    if all_sizes:
        size_counts = Counter(all_sizes)
        print(f'Container Sizes Found:')
        for size, count in size_counts.most_common():
            print(f'  {size} YD: {count} occurrences')
        print()
    else:
        print('  No container sizes found')
        print()
    
    if all_types:
        type_counts = Counter(all_types)
        print(f'Container Types Found:')
        for ctype, count in type_counts.most_common():
            print(f'  {ctype}: {count} occurrences')
        print()
    else:
        print('  No container types found')
        print()
    
    if all_frequencies:
        freq_counts = Counter(all_frequencies)
        print(f'Service Frequencies Found:')
        for freq, count in freq_counts.most_common():
            print(f'  {freq}x per week: {count} occurrences')
        print()
    else:
        print('  No frequencies found')
        print()
    
    # Determine most common values
    most_common_size = Counter(all_sizes).most_common(1)[0][0] if all_sizes else None
    most_common_type = Counter(all_types).most_common(1)[0][0] if all_types else None
    most_common_freq = Counter(all_frequencies).most_common(1)[0][0] if all_frequencies else None
    
    # Try to determine container count
    # Look for unique service line items
    unique_services = set()
    for desc in all_descriptions:
        info = extract_container_info(desc)
        if info and info['size'] and info['type']:
            service_key = f"{info['size']}YD {info['type']}"
            unique_services.add(service_key)
    
    container_count = len(unique_services) if unique_services else None
    
    print('RECOMMENDED SERVICE DETAILS:')
    print('-' * 80)
    print(f'Container Size: {most_common_size} YD' if most_common_size else 'Container Size: Unable to determine')
    print(f'Container Type: {most_common_type}' if most_common_type else 'Container Type: Unable to determine')
    print(f'Service Frequency: {most_common_freq}x per week' if most_common_freq else 'Service Frequency: Unable to determine')
    print(f'Container Count: {container_count}' if container_count else 'Container Count: Unable to determine')
    print()
    
    # Look for specific service patterns
    print('DETAILED SERVICE BREAKDOWN:')
    print('-' * 80)
    
    service_patterns = {}
    for desc in all_descriptions:
        info = extract_container_info(desc)
        if info and info['size']:
            key = f"{info['size']}YD {info['type'] or 'Unknown'} @ {info['frequency'] or '?'}x/week"
            service_patterns[key] = service_patterns.get(key, 0) + 1
    
    if service_patterns:
        for pattern, count in sorted(service_patterns.items(), key=lambda x: x[1], reverse=True):
            print(f'  {pattern}: {count} invoice lines')
    else:
        print('  No clear patterns found')
    
    print()
    print()
    
    return {
        'property': property_name,
        'sizes': all_sizes,
        'types': all_types,
        'frequencies': all_frequencies,
        'most_common_size': most_common_size,
        'most_common_type': most_common_type,
        'most_common_freq': most_common_freq,
        'container_count': container_count,
        'unique_services': unique_services,
        'service_patterns': service_patterns
    }

def main():
    """Main function"""
    
    print('=' * 80)
    print('EXTRACTING SERVICE DETAILS FROM INVOICE DESCRIPTIONS')
    print('=' * 80)
    print()
    
    results = {}
    
    for property_name in PROPERTIES:
        result = analyze_property_invoices(property_name)
        results[property_name] = result
    
    # Summary
    print('=' * 80)
    print('EXTRACTION SUMMARY')
    print('=' * 80)
    print()
    
    for property_name, data in results.items():
        print(f'{property_name}:')
        print(f'  Most Common Size: {data["most_common_size"]} YD' if data["most_common_size"] else '  Size: Not found')
        print(f'  Most Common Type: {data["most_common_type"]}' if data["most_common_type"] else '  Type: Not found')
        print(f'  Most Common Frequency: {data["most_common_freq"]}x/week' if data["most_common_freq"] else '  Frequency: Not found')
        print(f'  Estimated Container Count: {data["container_count"]}' if data["container_count"] else '  Count: Not found')
        print()
        
        if data['unique_services']:
            print(f'  Unique Services:')
            for service in sorted(data['unique_services']):
                print(f'    - {service}')
        print()
    
    return results

if __name__ == "__main__":
    main()

