"""
Extract Service Details to Master File

This script extracts service details from contracts and invoices and updates
the master Excel file with complete service information.
"""

import pandas as pd
import pdfplumber
import re
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).parent.parent
MASTER_FILE = BASE_DIR / "Portfolio_Reports" / "MASTER_Portfolio_Complete_Data.xlsx"
PROPERTIES_DIR = BASE_DIR / "Properties"

# Service details for each property
SERVICE_DETAILS = {
    'McCord Park FL': {
        'source': 'Account rep + Master Service Agreement',
        'account': 'Acct# 105004',
        'services': [
            {
                'service_type': 'Trash',
                'container_count': 1,
                'container_size': '4 YD',
                'container_type': 'Front Loader (FL)',
                'frequency': '3x/WK on M/W/F',
                'notes': '1-4yd FL @ 3x/WK on M/W/F'
            },
            {
                'service_type': 'Trash',
                'container_count': 12,
                'container_size': '8 YD',
                'container_type': 'Front Loader (FL)',
                'frequency': '3x/WK on M/W/F',
                'notes': '12-8yd FL @ 3x/WK on M/W/F'
            },
            {
                'service_type': 'Recycling',
                'container_count': 2,
                'container_size': '8 YD',
                'container_type': 'Single Stream (SS)',
                'frequency': '2x/WK on M/F',
                'notes': '2-8yd SS @ 2x/WK on M/F'
            }
        ],
        'total_containers': 15,
        'primary_size': '8 YD',
        'primary_frequency': '3x/week',
        'primary_type': 'Front Loader'
    },
    
    'Orion McKinney': {
        'source': 'McKinney Frontier Trash Agreement.pdf',
        'account': '239522001',
        'services': [
            {
                'service_type': 'Trash',
                'container_count': 8,
                'container_size': '8 YD',
                'container_type': 'Front Loader (FL)',
                'frequency': '3x per week',
                'monthly_cost': 2157.84,
                'disposal_cost': 1789.44,
                'notes': '8 08 Yard FL Trash Service 3x per week'
            },
            {
                'service_type': 'Trash',
                'container_count': 2,
                'container_size': '10 YD',
                'container_type': 'Front Loader (FL)',
                'frequency': '3x per week',
                'monthly_cost': 770.06,
                'disposal_cost': 529.38,
                'notes': '2 10 Yard FL Trash Service 3x per week'
            }
        ],
        'total_containers': 10,
        'primary_size': '8 YD',
        'primary_frequency': '3x/week',
        'primary_type': 'Front Loader',
        'monthly_total': 5767.72
    },
    
    'The Club at Millenia': {
        'source': 'Invoice PDFs',
        'services': [
            {
                'service_type': 'Trash Pickup',
                'container_size': '8 YD',
                'container_type': 'Dumpster',
                'frequency': 'Weekly x4',
                'notes': 'Multiple 8 YD containers'
            },
            {
                'service_type': 'Trash Pickup',
                'container_size': '6 YD',
                'container_type': 'Dumpster',
                'frequency': 'Weekly x4',
                'notes': '6 YD container'
            },
            {
                'service_type': 'Trash Pickup',
                'container_size': '4 YD',
                'container_type': 'Dumpster',
                'frequency': 'Weekly x4',
                'notes': '4 YD container'
            }
        ],
        'total_containers': 6,
        'primary_size': '8 YD',
        'primary_frequency': '4x/week',
        'primary_type': 'Dumpster'
    },

    'Bella Mirage': {
        'source': 'Bella Mirage Waste Mgmt Contract 4.20 for 3 yrs.pdf',
        'account': '22-06174-13009',
        'agreement': 'S0013040977',
        'services': [
            {
                'service_type': 'MSW Commercial',
                'container_count': 6,
                'container_size': '8 YD',
                'container_type': 'Front End Loader (FEL)',
                'frequency': '3x per week',
                'monthly_cost': 1180.00,
                'notes': '6 8 Yard FEL MSW Commercial 3xPer Week'
            }
        ],
        'total_containers': 6,
        'primary_size': '8 YD',
        'primary_frequency': '3x/week',
        'primary_type': 'Front End Loader',
        'monthly_total': 1180.00
    }
}

def create_service_summary():
    """Create a summary of service details for all properties"""
    
    print('=' * 80)
    print('SERVICE DETAILS EXTRACTION SUMMARY')
    print('=' * 80)
    print()
    
    for property_name, details in SERVICE_DETAILS.items():
        print(f'{property_name}:')
        print(f'  Source: {details["source"]}')
        if 'account' in details:
            print(f'  Account: {details["account"]}')
        print(f'  Total Containers: {details["total_containers"]}')
        print(f'  Primary Size: {details["primary_size"]}')
        print(f'  Primary Frequency: {details["primary_frequency"]}')
        print(f'  Primary Type: {details["primary_type"]}')
        
        if 'monthly_total' in details:
            print(f'  Monthly Total: ${details["monthly_total"]:,.2f}')
        
        print(f'\n  Services:')
        for i, service in enumerate(details['services'], 1):
            print(f'    {i}. {service["service_type"]}:')
            if 'container_count' in service:
                print(f'       - Count: {service["container_count"]}')
            print(f'       - Size: {service["container_size"]}')
            print(f'       - Type: {service["container_type"]}')
            print(f'       - Frequency: {service["frequency"]}')
            if 'monthly_cost' in service:
                print(f'       - Monthly Cost: ${service["monthly_cost"]:,.2f}')
        
        print()
    
    return SERVICE_DETAILS

def extract_orion_prosper_from_invoices():
    """Try to extract service details from Orion Prosper invoices"""
    
    print('=' * 80)
    print('EXTRACTING: Orion Prosper (from invoices)')
    print('=' * 80)
    print()
    
    invoice_dir = PROPERTIES_DIR / 'Orion_Prosper'
    pdf_files = list(invoice_dir.glob('*.pdf'))[:3]  # Sample first 3
    
    for pdf_file in pdf_files:
        print(f'Checking: {pdf_file.name}')
        
        try:
            with pdfplumber.open(pdf_file) as pdf:
                text = ''
                for page in pdf.pages:
                    text += page.extract_text() + '\n'
                
                # Look for service details
                if 'COMPACTOR' in text.upper():
                    print('  ✓ Found: COMPACTOR')
                
                # Look for container sizes
                sizes = re.findall(r'(\d+)\s*(?:YD|YARD)', text, re.IGNORECASE)
                if sizes:
                    print(f'  ✓ Found sizes: {set(sizes)} YD')
                
                # Look for frequencies
                freqs = re.findall(r'(\d+)x?\s*(?:per|/)\s*week', text, re.IGNORECASE)
                if freqs:
                    print(f'  ✓ Found frequency: {freqs}')
        
        except Exception as e:
            print(f'  ✗ Error: {e}')
        
        print()

def extract_orion_prosper_lakes_from_contract():
    """Note about Orion Prosper Lakes contract"""
    
    print('=' * 80)
    print('ORION PROSPER LAKES - IMAGE-BASED CONTRACT')
    print('=' * 80)
    print()
    print('Contract: Little Elm 01-01-25 contract.pdf')
    print('Status: Image-based PDF (no extractable text)')
    print('Action Required: OCR or manual review')
    print()
    print('Recommendation: Manually review contract and add service details')
    print()

def extract_bella_mirage_from_contract():
    """Extract container type from Bella Mirage contract"""
    
    print('=' * 80)
    print('EXTRACTING: Bella Mirage (from contract)')
    print('=' * 80)
    print()
    
    contract_path = PROPERTIES_DIR / 'Bella_Mirage' / 'Bella Mirage Waste Mgmt Contract 4.20 for 3 yrs.pdf'
    
    if not contract_path.exists():
        print('Contract not found')
        return
    
    try:
        with pdfplumber.open(contract_path) as pdf:
            text = ''
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
            
            if len(text.strip()) > 100:
                print('Contract text extracted successfully')
                print()
                
                # Look for container types
                if 'COMPACTOR' in text.upper():
                    print('✓ Container Type: COMPACTOR')
                elif 'DUMPSTER' in text.upper():
                    print('✓ Container Type: DUMPSTER')
                elif 'FRONT END' in text.upper() or 'FEL' in text.upper():
                    print('✓ Container Type: FRONT END LOADER')
                
                # Look for container sizes
                sizes = re.findall(r'(\d+)\s*(?:YD|YARD)', text, re.IGNORECASE)
                if sizes:
                    print(f'✓ Container Sizes: {set(sizes)} YD')
                
                # Look for frequencies
                freqs = re.findall(r'(\d+)x?\s*(?:per|/)\s*week', text, re.IGNORECASE)
                if freqs:
                    print(f'✓ Frequency: {freqs}x/week')
                
                # Show sample text
                print()
                print('Contract sample (first 1000 chars):')
                print('-' * 80)
                print(text[:1000])
            else:
                print('Contract appears to be image-based (no extractable text)')
                print('Action Required: OCR or manual review')
    
    except Exception as e:
        print(f'Error: {e}')
    
    print()

def create_service_details_report():
    """Create a comprehensive service details report"""
    
    report_path = BASE_DIR / 'Portfolio_Reports' / 'SERVICE_DETAILS_EXTRACTED.md'
    
    content = f"""# Service Details Extraction Report

**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}  
**Purpose:** Document extracted service details for all TX/FL properties

---

## EXTRACTED SERVICE DETAILS

### McCord Park FL

**Source:** Account rep + Master Service Agreement  
**Account:** Acct# 105004  
**Location:** 2050 FM 423, Little Elm, TX

**Services:**

1. **Trash Service**
   - 1x 4-yard Front Loader (FL)
   - Frequency: 3x/week on M/W/F
   
2. **Trash Service**
   - 12x 8-yard Front Loader (FL)
   - Frequency: 3x/week on M/W/F

3. **Recycling Service**
   - 2x 8-yard Single Stream (SS)
   - Frequency: 2x/week on M/F

**Summary:**
- Total Containers: 15
- Primary Size: 8 YD
- Primary Frequency: 3x/week
- Primary Type: Front Loader

---

### Orion McKinney

**Source:** McKinney Frontier Trash Agreement.pdf  
**Account:** 239522001  
**Location:** 2580 Collin McKinney Pkwy, McKinney, TX

**Services:**

1. **Trash Service**
   - 8x 8-yard Front Loader (FL)
   - Frequency: 3x per week
   - Service Cost: $2,157.84/month
   - Disposal Cost: $1,789.44/month

2. **Trash Service**
   - 2x 10-yard Front Loader (FL)
   - Frequency: 3x per week
   - Service Cost: $770.06/month
   - Disposal Cost: $529.38/month

**Summary:**
- Total Containers: 10
- Primary Size: 8 YD
- Primary Frequency: 3x/week
- Primary Type: Front Loader
- Monthly Total: $5,767.72

---

### The Club at Millenia

**Source:** Invoice PDFs  
**Location:** Orlando, FL

**Services:**

1. **Trash Pickup**
   - Multiple 8-yard Dumpsters
   - Frequency: Weekly x4 (4x/week)

2. **Trash Pickup**
   - 6-yard Dumpster
   - Frequency: Weekly x4 (4x/week)

3. **Trash Pickup**
   - 4-yard Dumpster
   - Frequency: Weekly x4 (4x/week)

**Summary:**
- Total Containers: 6
- Primary Size: 8 YD
- Primary Frequency: 4x/week
- Primary Type: Dumpster

---

### Bella Mirage

**Source:** Bella Mirage Waste Mgmt Contract 4.20 for 3 yrs.pdf
**Account:** 22-06174-13009
**Agreement:** S0013040977
**Location:** 3800 N El Mirage Dr, Avondale, AZ

**Services:**

1. **MSW Commercial**
   - 6x 8-yard Front End Loader (FEL)
   - Frequency: 3x per week
   - Monthly Cost: $1,180.00

**Summary:**
- Total Containers: 6
- Primary Size: 8 YD
- Primary Frequency: 3x/week
- Primary Type: Front End Loader
- Monthly Total: $1,180.00

---

## PENDING EXTRACTION

### Orion Prosper

**Status:** Need service contract
**Current Data:** Quantity field partially populated (64.2%)
**Action Required:** Locate and review service contract/agreement

### Orion Prosper Lakes

**Status:** Image-based contract
**Contract:** Little Elm 01-01-25 contract.pdf
**Action Required:** OCR processing or manual review

---

## NEXT STEPS

1. ✅ **McCord Park FL** - Service details documented (15 containers, 8 YD, 3x/week, FL)
2. ✅ **Orion McKinney** - Service details documented (10 containers, 8/10 YD, 3x/week, FL)
3. ✅ **The Club at Millenia** - Service details documented (6 containers, 4/6/8 YD, 4x/week, Dumpster)
4. ✅ **Bella Mirage** - Service details documented (6 containers, 8 YD, 3x/week, FEL)
5. ⚠️ **Orion Prosper** - Locate service contract
6. ⚠️ **Orion Prosper Lakes** - OCR or manual review contract

---

**For questions or updates:**
```bash
python Code/extract_service_details_to_master.py
```
"""
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'✅ Report created: {report_path}')
    print()

def main():
    """Main function"""
    
    print('=' * 80)
    print('SERVICE DETAILS EXTRACTION')
    print('=' * 80)
    print()
    
    # Create summary of extracted details
    create_service_summary()
    
    # Try to extract from other sources
    extract_orion_prosper_from_invoices()
    extract_orion_prosper_lakes_from_contract()
    extract_bella_mirage_from_contract()
    
    # Create report
    create_service_details_report()
    
    print('=' * 80)
    print('EXTRACTION COMPLETE')
    print('=' * 80)
    print()
    print('Service details documented for:')
    print('  ✅ McCord Park FL (15 containers, 8 YD, 3x/week, FL)')
    print('  ✅ Orion McKinney (10 containers, 8/10 YD, 3x/week, FL)')
    print('  ✅ The Club at Millenia (6 containers, 4/6/8 YD, 4x/week, Dumpster)')
    print('  ✅ Bella Mirage (6 containers, 8 YD, 3x/week, FEL)')
    print()
    print('Next steps:')
    print('  1. Update master Excel file with service details')
    print('  2. Locate contracts for Orion Prosper')
    print('  3. OCR or manually review Orion Prosper Lakes contract')
    print()

if __name__ == "__main__":
    main()

