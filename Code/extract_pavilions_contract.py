import pdfplumber
import re

contract_path = r'C:\Users\Richard\Downloads\Orion Data Part 2\Pavilions at Arrowhead - Waste Consolidators Inc Bulk Agreement.pdf'

print("="*80)
print("PAVILIONS AT ARROWHEAD - WCI BULK AGREEMENT")
print("="*80)

try:
    with pdfplumber.open(contract_path) as pdf:
        print(f"\nTotal pages: {len(pdf.pages)}")

        all_text = ""
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                all_text += text + "\n"
                print(f"\nPage {i} text:\n{text}\n")
                print("-"*80)

        # Search for key information
        print("\n" + "="*80)
        print("SEARCHING FOR KEY INFORMATION")
        print("="*80)

        # Search for unit count
        unit_patterns = [
            r'(\d+)\s*(?:unit|apartment|dwelling)',
            r'unit[s]?[:\s]+(\d+)',
            r'apartment[s]?[:\s]+(\d+)',
            r'total\s*(?:of\s*)?(\d+)\s*(?:unit|apartment)',
        ]

        print("\n1. UNIT COUNT:")
        found_units = False
        for pattern in unit_patterns:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            if matches:
                print(f"   Pattern '{pattern}' found: {matches}")
                found_units = True

        if not found_units:
            print("   NOT FOUND - will need manual review")

        # Search for service type
        print("\n2. SERVICE TYPE:")
        if re.search(r'compactor', all_text, re.IGNORECASE):
            print("   Compactor service detected")
        if re.search(r'dumpster|container|open\s*top', all_text, re.IGNORECASE):
            print("   Dumpster/container service detected")
        if re.search(r'bulk', all_text, re.IGNORECASE):
            print("   Bulk service detected")

        # Search for rates
        print("\n3. RATES/PRICING:")
        price_patterns = [
            r'\$[\d,]+\.?\d*',
        ]
        prices = re.findall(r'\$[\d,]+\.?\d*', all_text)
        if prices:
            print(f"   Prices found: {prices[:10]}")  # First 10
        else:
            print("   NO prices found")

        # Search for frequency
        print("\n4. SERVICE FREQUENCY:")
        freq_patterns = [
            r'(\d+)\s*(?:times?|x)\s*(?:per|/)?\s*(?:week|month)',
            r'(?:weekly|monthly|daily)',
        ]
        for pattern in freq_patterns:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            if matches:
                print(f"   Pattern '{pattern}' found: {matches}")

        # Search for vendor
        print("\n5. VENDOR:")
        if re.search(r'waste\s*consolidator', all_text, re.IGNORECASE):
            print("   Waste Consolidators Inc (WCI) confirmed")

        # Search for term dates
        print("\n6. CONTRACT TERM:")
        date_pattern = r'(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+\d{4}'
        dates = re.findall(date_pattern, all_text, re.IGNORECASE)
        if dates:
            print(f"   Dates found: {dates}")

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
