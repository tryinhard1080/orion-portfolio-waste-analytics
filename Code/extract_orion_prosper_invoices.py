#!/usr/bin/env python3
"""
Orion Prosper Invoice Extraction Script
Extracts structured data from all PDF invoices for Orion Prosper property.
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

try:
    import pdfplumber
except ImportError:
    print("Installing pdfplumber...")
    os.system("pip install pdfplumber")
    import pdfplumber

# Constants
PROPERTY_NAME = "Orion Prosper"
UNIT_COUNT = 312
INVOICE_FOLDER = r"C:\Users\Richard\Downloads\Orion Data\Invoices\Orion_Prosper"
OUTPUT_FILE = r"C:\Users\Richard\Downloads\Orion Data\extraction_results\Orion_Prosper_invoices.json"

# Controllable charge keywords (overages, extras, variable services)
CONTROLLABLE_KEYWORDS = [
    'overage', 'extra', 'additional', 'haul', 'disposal', 'dump',
    'per pull', 'on-call', 'special', 'temporary'
]


def extract_text_from_pdf(pdf_path):
    """Extract all text from PDF file."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
    return text


def parse_invoice_number(text, filename):
    """Extract invoice number from text or filename."""
    # Try from text first: "InvoiceNumber 0615-002287935"
    match = re.search(r'InvoiceNumber\s+(\d+-\d+)', text)
    if match:
        return match.group(1)

    # Fallback to filename: Republic Services-16282934_01-2025.pdf
    match = re.search(r'Republic Services-(\d+)_', filename)
    if match:
        return match.group(1)

    return None


def parse_billing_period(text, filename):
    """Extract billing period from text or filename."""
    # Try from text: "InvoiceDate February25,2025"
    match = re.search(r'InvoiceDate\s+([A-Za-z]+)\d+,(\d{4})', text)
    if match:
        month_name = match.group(1)
        year = match.group(2)
        return f"{month_name} {year}"

    # Fallback to filename: _01-2025.pdf -> January 2025
    match = re.search(r'_(\d{2})-(\d{4})\.pdf', filename)
    if match:
        month = int(match.group(1))
        year = match.group(2)
        month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        return f"{month_names[month]} {year}"

    return None


def extract_total_amount(text):
    """Extract total amount from invoice text."""
    # Pattern 1: "TotalAmountDue $1,448.78" (no space)
    match = re.search(r'TotalAmountDue\s*\$?([\d,]+\.\d{2})', text)
    if match:
        amount_str = match.group(1).replace(',', '')
        return float(amount_str)

    # Pattern 2: "Total Amount Due" with amount on same or next line
    match = re.search(r'Total\s+Amount\s+Due[:\s]+\$?([\d,]+\.\d{2})', text, re.IGNORECASE)
    if match:
        amount_str = match.group(1).replace(',', '')
        return float(amount_str)

    # Pattern 3: Look for "CURRENT INVOICE CHARGES" section total
    match = re.search(r'CURRENTINVOICECHARGES\s*\$?([\d,]+\.\d{2})', text)
    if match:
        amount_str = match.group(1).replace(',', '')
        return float(amount_str)

    return None


def extract_line_items(text):
    """Extract line items from invoice text."""
    line_items = []

    # Find the CURRENT INVOICE CHARGES section
    charges_section = re.search(
        r'CURRENT INVOICE CHARGES.*?(?=CURRENTINVOICECHARGES|PleaseReturnThis|$)',
        text,
        re.DOTALL
    )

    if not charges_section:
        return line_items

    charges_text = charges_section.group(0)

    # Pattern for line items in Republic Services format:
    # "Waste/RecyclingOverage02/07 1.0000 $43.60 $43.60"
    # "PickupService 02/01-02/28 2.0000 $625.58 $1,251.16"

    # Split into lines
    lines = charges_text.split('\n')

    for line in lines:
        line = line.strip()

        # Skip header lines and empty lines
        if not line or 'Description' in line or 'Reference' in line:
            continue

        # Look for patterns with dollar amounts
        # Pattern: description followed by quantity, unit price, and amount
        amount_match = re.search(r'\$?([\d,]+\.\d{2})\s*$', line)
        if amount_match:
            amount_str = amount_match.group(1).replace(',', '')
            amount = float(amount_str)

            # Extract description (everything before the numbers)
            description = re.sub(r'\d+\.\d{4}\s+\$?[\d,]+\.\d{2}\s+\$?[\d,]+\.\d{2}\s*$', '', line)
            description = re.sub(r'\d+\.\d+\s+\$?[\d,]+\.\d{2}\s*$', '', description)
            description = description.strip()

            if not description:
                continue

            # Categorize as controllable or base
            is_controllable = any(keyword in line.lower() for keyword in CONTROLLABLE_KEYWORDS)

            if is_controllable:
                category = 'controllable'
            elif 'tax' in line.lower():
                category = 'tax'
            elif 'pickup' in line.lower() or 'service' in line.lower():
                category = 'base'
            else:
                category = 'other'

            line_items.append({
                'description': description,
                'amount': amount,
                'category': category
            })

    return line_items


def parse_invoice_data(pdf_path, filename):
    """Extract structured data from a single invoice PDF."""
    print(f"Processing: {filename}")

    text = extract_text_from_pdf(pdf_path)

    if not text:
        print(f"  WARNING: No text extracted from {filename}")
        return None

    # Initialize data structure
    invoice_data = {
        'filename': filename,
        'invoice_number': None,
        'billing_period': None,
        'property': PROPERTY_NAME,
        'units': UNIT_COUNT,
        'total_amount': None,
        'base_charges': None,
        'controllable_charges': None,
        'controllable_percentage': None,
        'cost_per_door': None,
        'service_type': None,
        'provider': 'Republic Services',
        'line_items': []
    }

    # Extract invoice number
    invoice_data['invoice_number'] = parse_invoice_number(text, filename)

    # Extract billing period
    invoice_data['billing_period'] = parse_billing_period(text, filename)

    # Extract total amount
    invoice_data['total_amount'] = extract_total_amount(text)

    # If we found a total, calculate CPD
    if invoice_data['total_amount']:
        invoice_data['cost_per_door'] = round(invoice_data['total_amount'] / UNIT_COUNT, 2)

    # Determine service type from text
    if 'compactor' in text.lower():
        invoice_data['service_type'] = 'Compactor'
    elif 'frontload' in text.lower() or 'front load' in text.lower():
        invoice_data['service_type'] = 'Front Load Dumpster'
    elif 'dumpster' in text.lower():
        invoice_data['service_type'] = 'Dumpster'

    # Extract line items
    invoice_data['line_items'] = extract_line_items(text)

    # Calculate base and controllable charges from line items
    base_total = 0
    controllable_total = 0

    for item in invoice_data['line_items']:
        if item['category'] == 'base':
            base_total += item['amount']
        elif item['category'] == 'controllable':
            controllable_total += item['amount']

    if base_total > 0:
        invoice_data['base_charges'] = round(base_total, 2)
    if controllable_total > 0:
        invoice_data['controllable_charges'] = round(controllable_total, 2)

    # Calculate controllable percentage
    if invoice_data['total_amount'] and invoice_data['controllable_charges']:
        invoice_data['controllable_percentage'] = round(
            (invoice_data['controllable_charges'] / invoice_data['total_amount']) * 100, 1
        )

    # Validation
    if not invoice_data['total_amount']:
        print(f"  WARNING: Could not extract total amount from {filename}")
        return None

    # Success message
    controllable_msg = f" | Controllable: ${invoice_data['controllable_charges']:.2f} ({invoice_data['controllable_percentage']}%)" if invoice_data['controllable_charges'] else ""
    print(f"  SUCCESS: Total: ${invoice_data['total_amount']:.2f} | CPD: ${invoice_data['cost_per_door']:.2f}{controllable_msg}")

    return invoice_data


def main():
    """Main extraction process."""
    print(f"\n{'='*80}")
    print(f"Orion Prosper Invoice Extraction")
    print(f"{'='*80}")
    print(f"Property: {PROPERTY_NAME}")
    print(f"Units: {UNIT_COUNT}")
    print(f"Invoice Folder: {INVOICE_FOLDER}")
    print(f"Output File: {OUTPUT_FILE}")
    print(f"{'='*80}\n")

    # Get all PDF files
    invoice_folder = Path(INVOICE_FOLDER)
    pdf_files = sorted(invoice_folder.glob("*.pdf"))

    if not pdf_files:
        print(f"ERROR: No PDF files found in {INVOICE_FOLDER}")
        return

    print(f"Found {len(pdf_files)} invoice PDFs\n")

    # Process each invoice
    all_invoices = []
    successful = 0
    failed = 0

    for pdf_file in pdf_files:
        invoice_data = parse_invoice_data(pdf_file, pdf_file.name)
        if invoice_data:
            all_invoices.append(invoice_data)
            successful += 1
        else:
            failed += 1

    # Sort by billing period (filename is chronological)
    all_invoices.sort(key=lambda x: x['filename'])

    # Calculate summary statistics
    if all_invoices:
        total_amounts = [inv['total_amount'] for inv in all_invoices if inv['total_amount']]
        cpd_values = [inv['cost_per_door'] for inv in all_invoices if inv['cost_per_door']]
        controllable_amounts = [inv['controllable_charges'] for inv in all_invoices if inv.get('controllable_charges')]

        summary = {
            'property': PROPERTY_NAME,
            'units': UNIT_COUNT,
            'extraction_date': datetime.now().isoformat(),
            'total_invoices': len(all_invoices),
            'successful_extractions': successful,
            'failed_extractions': failed,
            'statistics': {
                'total_amount': {
                    'min': round(min(total_amounts), 2) if total_amounts else None,
                    'max': round(max(total_amounts), 2) if total_amounts else None,
                    'average': round(sum(total_amounts) / len(total_amounts), 2) if total_amounts else None
                },
                'cost_per_door': {
                    'min': round(min(cpd_values), 2) if cpd_values else None,
                    'max': round(max(cpd_values), 2) if cpd_values else None,
                    'average': round(sum(cpd_values) / len(cpd_values), 2) if cpd_values else None
                },
                'controllable_charges': {
                    'min': round(min(controllable_amounts), 2) if controllable_amounts else None,
                    'max': round(max(controllable_amounts), 2) if controllable_amounts else None,
                    'average': round(sum(controllable_amounts) / len(controllable_amounts), 2) if controllable_amounts else None
                } if controllable_amounts else None
            }
        }
    else:
        summary = {
            'property': PROPERTY_NAME,
            'units': UNIT_COUNT,
            'extraction_date': datetime.now().isoformat(),
            'total_invoices': 0,
            'successful_extractions': 0,
            'failed_extractions': failed
        }

    # Prepare output
    output_data = {
        'summary': summary,
        'invoices': all_invoices
    }

    # Save to JSON file
    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    # Print results
    print(f"\n{'='*80}")
    print(f"EXTRACTION COMPLETE")
    print(f"{'='*80}")
    print(f"Successfully processed: {successful}/{len(pdf_files)} invoices")
    if failed > 0:
        print(f"WARNING: Failed: {failed}/{len(pdf_files)} invoices")

    if all_invoices:
        stats = summary['statistics']
        print(f"\nStatistics:")
        print(f"  Total Amount Range: ${stats['total_amount']['min']:.2f} - ${stats['total_amount']['max']:.2f}")
        print(f"  Average Monthly Total: ${stats['total_amount']['average']:.2f}")
        print(f"  Cost Per Door Range: ${stats['cost_per_door']['min']:.2f} - ${stats['cost_per_door']['max']:.2f}")
        print(f"  Average CPD: ${stats['cost_per_door']['average']:.2f}")

        if stats.get('controllable_charges'):
            print(f"\n  Controllable Charges:")
            print(f"    Range: ${stats['controllable_charges']['min']:.2f} - ${stats['controllable_charges']['max']:.2f}")
            print(f"    Average: ${stats['controllable_charges']['average']:.2f}")

    print(f"\nResults saved to: {OUTPUT_FILE}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
