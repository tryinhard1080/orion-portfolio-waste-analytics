"""
Check Invoice PDFs for Service Details

This script samples invoice PDFs to check if service details (container size, 
frequency, type) are present in the invoices but were missed during extraction.
"""

import pdfplumber
import re
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
PROPERTIES_DIR = BASE_DIR / "Properties"

# Properties to check (excluding 4 AZ properties)
PROPERTIES_TO_CHECK = {
    'Orion_Prosper': 'Orion Prosper',
    'Orion_Prosper_Lakes': 'Orion Prosper Lakes',
    'Orion_McKinney': 'Orion McKinney',
    'McCord_Park_FL': 'McCord Park FL',
    'The_Club_at_Millenia': 'The Club at Millenia',
    'Bella_Mirage': 'Bella Mirage'
}

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        return f"ERROR: {e}"

def find_service_details(text):
    """Search for service details in invoice text"""
    
    details = {
        'container_sizes': [],
        'frequencies': [],
        'container_types': [],
        'service_descriptions': []
    }
    
    # Pattern for container sizes (e.g., "30 YD", "40 YARD", "2 CY")
    size_patterns = [
        r'(\d+)\s*(?:YD|YARD|CY|CUBIC YARD)',
        r'(\d+)\s*(?:yard|yd)',
    ]
    
    for pattern in size_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        details['container_sizes'].extend(matches)
    
    # Pattern for frequencies (e.g., "3X/WEEK", "WEEKLY", "DAILY")
    freq_patterns = [
        r'(\d+)\s*(?:X|TIMES?)\s*(?:/|PER)\s*(?:WEEK|WK)',
        r'(WEEKLY|DAILY|MONTHLY|BI-WEEKLY)',
        r'(\d+)\s*(?:PER WEEK|/WEEK|/WK)',
    ]
    
    for pattern in freq_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        details['frequencies'].extend(matches)
    
    # Pattern for container types
    type_keywords = [
        'COMPACTOR', 'DUMPSTER', 'FEL', 'FRONT END LOADER', 'FRONT-END LOADER',
        'REAR LOAD', 'ROLL-OFF', 'ROLLOFF', 'CONTAINER', 'CART'
    ]
    
    for keyword in type_keywords:
        if keyword in text.upper():
            details['container_types'].append(keyword)
    
    # Extract service description lines (lines that might contain service info)
    lines = text.split('\n')
    for line in lines:
        line_upper = line.upper()
        # Look for lines with service-related keywords
        if any(keyword in line_upper for keyword in ['SERVICE', 'CONTAINER', 'PICKUP', 'HAUL', 'DISPOSAL']):
            if len(line.strip()) > 10 and len(line.strip()) < 200:  # Reasonable length
                details['service_descriptions'].append(line.strip())
    
    return details

def check_property_invoices(property_folder_name, property_display_name):
    """Check invoices for a property"""
    
    print(f'\n{"=" * 80}')
    print(f'{property_display_name}')
    print(f'{"=" * 80}')
    
    property_path = PROPERTIES_DIR / property_folder_name
    
    # Get PDF invoices (exclude contracts)
    pdf_files = list(property_path.glob('*.pdf'))
    invoice_pdfs = [p for p in pdf_files if 'contract' not in p.name.lower() and 'agreement' not in p.name.lower()]
    
    if not invoice_pdfs:
        print('No invoice PDFs found')
        return
    
    print(f'Found {len(invoice_pdfs)} invoice PDFs')
    print()
    
    # Sample first 2 invoices
    sample_count = min(2, len(invoice_pdfs))
    
    for i, pdf_path in enumerate(invoice_pdfs[:sample_count], 1):
        print(f'INVOICE {i}: {pdf_path.name}')
        print('-' * 80)
        
        text = extract_text_from_pdf(pdf_path)
        
        if text.startswith('ERROR'):
            print(f'  {text}')
            continue
        
        details = find_service_details(text)
        
        # Report findings
        if details['container_sizes']:
            unique_sizes = list(set(details['container_sizes']))
            print(f'  ✓ CONTAINER SIZES FOUND: {", ".join(unique_sizes)} YD')
        else:
            print(f'  ✗ No container sizes found')
        
        if details['frequencies']:
            unique_freqs = list(set(details['frequencies']))
            print(f'  ✓ FREQUENCIES FOUND: {", ".join(unique_freqs)}')
        else:
            print(f'  ✗ No frequencies found')
        
        if details['container_types']:
            unique_types = list(set(details['container_types']))
            print(f'  ✓ CONTAINER TYPES FOUND: {", ".join(unique_types)}')
        else:
            print(f'  ✗ No container types found')
        
        # Show sample service descriptions
        if details['service_descriptions']:
            print(f'\n  Sample Service Descriptions:')
            for desc in details['service_descriptions'][:5]:  # Show first 5
                print(f'    - {desc}')
        
        print()

def check_bella_mirage_excel():
    """Check Bella Mirage Excel file"""
    
    print(f'\n{"=" * 80}')
    print(f'Bella Mirage (Excel File)')
    print(f'{"=" * 80}')
    
    import pandas as pd
    
    excel_path = PROPERTIES_DIR / 'Bella_Mirage' / 'Bella Mirage - Trash Bills.xlsx'
    
    if not excel_path.exists():
        print('Excel file not found')
        return
    
    try:
        # Try to read the Excel file
        xl = pd.ExcelFile(excel_path)
        print(f'Sheets in file: {xl.sheet_names}')
        print()
        
        # Read first sheet
        df = pd.read_excel(xl, xl.sheet_names[0])
        
        print(f'Columns in sheet: {list(df.columns)}')
        print()
        
        # Check for service-related columns
        service_cols = []
        for col in df.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['size', 'frequency', 'type', 'container', 'service', 'yard']):
                service_cols.append(col)
        
        if service_cols:
            print(f'Service-related columns found:')
            for col in service_cols:
                non_null = df[col].notna().sum()
                print(f'  - {col}: {non_null}/{len(df)} populated')
                
                # Show sample values
                sample_values = df[col].dropna().unique()[:5]
                if len(sample_values) > 0:
                    print(f'    Sample values: {", ".join(str(v) for v in sample_values)}')
        else:
            print('No service-related columns found')
        
        print()
        
    except Exception as e:
        print(f'ERROR reading Excel: {e}')

def main():
    """Main function"""
    
    print('=' * 80)
    print('INVOICE SERVICE DETAILS CHECK')
    print('Checking if service details are in invoices but missed during extraction')
    print('=' * 80)
    
    # Check PDF-based properties
    for folder_name, display_name in PROPERTIES_TO_CHECK.items():
        if folder_name == 'Bella_Mirage':
            check_bella_mirage_excel()
        else:
            check_property_invoices(folder_name, display_name)
    
    # Summary
    print('\n' + '=' * 80)
    print('SUMMARY')
    print('=' * 80)
    print()
    print('This analysis shows what service details are visible in the invoice PDFs.')
    print('If details are found here but missing in the master file, they need to be')
    print('re-extracted or manually added.')
    print()

if __name__ == "__main__":
    main()

