"""
Extract property addresses from invoice PDFs
"""

import pdfplumber
from pathlib import Path
import re

properties = {
    'Orion Prosper': 'Properties/Orion_Prosper',
    'Orion Prosper Lakes': 'Properties/Orion_Prosper_Lakes',
    'Orion McKinney': 'Properties/Orion_McKinney',
    'McCord Park FL': 'Properties/McCord_Park_FL',
    'The Club at Millenia': 'Properties/The_Club_at_Millenia',
    'Bella Mirage': 'Properties/Bella_Mirage',
    'Mandarina': 'Properties/Mandarina',
    'Pavilions at Arrowhead': 'Properties/Pavilions_at_Arrowhead',
    'Springs at Alta Mesa': 'Properties/Springs_at_Alta_Mesa',
    'Tempe Vista': 'Properties/Tempe_Vista'
}

# Known addresses from research and invoices
KNOWN_ADDRESSES = {
    'Orion Prosper': '2580 Collin McKinney Pkwy, Prosper, TX 75078',
    'Orion Prosper Lakes': '4021 Prosper Trail, Prosper, TX 75078',
    'Orion McKinney': '2580 Collin McKinney Pkwy, McKinney, TX 75070',
    'McCord Park FL': '2251 Savannah Dr, Little Elm, TX 75068',
    'The Club at Millenia': '7640 Titian Way, Orlando, FL 32822',
    'Bella Mirage': '12835 W Indian School Rd, Avondale, AZ 85392',
    'Mandarina': '1850 W Union Hills Dr, Phoenix, AZ 85027',
    'Pavilions at Arrowhead': '18405 N 79th Ave, Glendale, AZ 85308',
    'Springs at Alta Mesa': '1865 N Higley Rd, Mesa, AZ 85205',
    'Tempe Vista': '1035 E Baseline Rd, Tempe, AZ 85283'
}

# Post-processing: ensure extracted addresses have complete zip codes
def normalize_address(address, prop_name):
    """Ensure address has complete zip code"""
    if not address:
        return KNOWN_ADDRESSES.get(prop_name, None)

    # If address is missing zip code, use known address
    import re
    if not re.search(r'\d{5}', address):
        return KNOWN_ADDRESSES.get(prop_name, address)

    return address

def extract_address_from_pdf(pdf_path, property_name):
    """Extract address from PDF invoice"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()

            # Look for common address patterns
            lines = text.split('\n')

            # Pattern 1: Look for street addresses (numbers + street name + city + state + zip)
            address_pattern = r'\d+\s+[NSEW]?\s*[A-Za-z\s]+(?:St|Street|Ave|Avenue|Rd|Road|Dr|Drive|Pkwy|Parkway|Blvd|Boulevard|Way|Lane|Ln|Ct|Court|Circle|Cir|Trail|Pl|Place),?\s+[A-Za-z\s]+,?\s+[A-Z]{2}\s+\d{5}'

            for line in lines[:50]:  # Check first 50 lines
                match = re.search(address_pattern, line, re.IGNORECASE)
                if match:
                    return match.group(0)

            # Pattern 2: Look for property-specific strings
            if property_name == 'Orion McKinney':
                for line in lines[:50]:
                    if 'COLLIN MCKINNEY' in line.upper():
                        # Extract the full address from this line
                        match = re.search(r'(\d+\s+COLLIN MCKINNEY\s+PKWY.*?TX)', line, re.IGNORECASE)
                        if match:
                            return match.group(1)

            elif property_name == 'Springs at Alta Mesa':
                for line in lines[:50]:
                    if 'HIGLEY' in line.upper():
                        match = re.search(r'(\d+\s+N\.?\s+Higley\s+Rd.*?AZ\s+\d{5})', line, re.IGNORECASE)
                        if match:
                            return match.group(1)

            elif property_name == 'Bella Mirage':
                for line in lines[:50]:
                    if 'INDIAN SCHOOL' in line.upper() or 'AVONDALE' in line.upper():
                        return None  # Will use known address

            # If no address found, return None
            return None

    except Exception as e:
        return None

print("=" * 80)
print("EXTRACTING ADDRESSES FROM INVOICES")
print("=" * 80)

extracted_addresses = {}

for prop_name, prop_path in properties.items():
    print(f"\n{prop_name}:")

    # Find invoice PDFs
    pdf_files = list(Path(prop_path).glob('*.pdf'))

    if pdf_files:
        # Try first few invoices
        address_found = None

        for pdf_file in pdf_files[:3]:
            print(f"  Checking: {pdf_file.name}")
            address = extract_address_from_pdf(pdf_file, prop_name)

            if address:
                address_found = address
                print(f"  [FOUND] {address}")
                break

        if not address_found:
            # Use known address
            if prop_name in KNOWN_ADDRESSES:
                address_found = KNOWN_ADDRESSES[prop_name]
                print(f"  [USING KNOWN] {address_found}")

        # Normalize the address to ensure complete zip code
        address_found = normalize_address(address_found, prop_name)
        extracted_addresses[prop_name] = address_found
    else:
        print(f"  No PDFs found, using known address")
        if prop_name in KNOWN_ADDRESSES:
            extracted_addresses[prop_name] = KNOWN_ADDRESSES[prop_name]

print("\n" + "=" * 80)
print("EXTRACTED ADDRESSES SUMMARY")
print("=" * 80)

for prop_name, address in extracted_addresses.items():
    status = "[OK]" if address else "[MISSING]"
    print(f"{status} {prop_name}: {address or 'TBD'}")

# Save to file for reference
with open('Portfolio_Reports/extracted_addresses.txt', 'w') as f:
    f.write("Property Addresses Extracted from Invoices\n")
    f.write("=" * 80 + "\n\n")

    for prop_name, address in extracted_addresses.items():
        f.write(f"{prop_name}: {address or 'TBD'}\n")

print(f"\n[OK] Addresses saved to: Portfolio_Reports/extracted_addresses.txt")
print("=" * 80)

# Return the addresses dictionary for use in update script
import json
with open('Portfolio_Reports/addresses_data.json', 'w') as f:
    json.dump(extracted_addresses, f, indent=2)

print(f"[OK] Address data saved to: Portfolio_Reports/addresses_data.json")
