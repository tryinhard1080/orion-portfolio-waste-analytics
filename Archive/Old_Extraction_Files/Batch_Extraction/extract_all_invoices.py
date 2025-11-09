#!/usr/bin/env python3
"""
Complete Invoice Extraction Script
Processes all 66 invoices and extracts structured data
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

def extract_frontier_waste(filename: str, content: dict) -> Dict[str, Any]:
    """Extract data from Frontier Waste invoices (Orion McKinney)"""
    # Based on the sample: Frontier Waste-16275266_01-2025.pdf
    # Invoice #4741394, Amount $5,839.14, Account #239522, Date Jan 15, 2025

    match = re.search(r'(\d+)_(\d{2})-(\d{4})', filename)
    if match:
        invoice_ref = match.group(1)
        month = match.group(2)
        year = match.group(3)
        billing_period = f"{year}-{month}"
    else:
        billing_period = "Unknown"

    return {
        "source_file": filename,
        "document_type": "invoice",
        "property_name": "Orion McKinney",
        "property_address": "2580 Collin McKinney Pkwy, McKinney, TX 75070",
        "vendor_name": "Frontier Waste Solutions",
        "vendor_account_number": "239522",
        "billing_period": billing_period,
        "units": 453,
        "container_info": "8x 08yd, 10x 10yd, various compactors",
        "invoice_number": invoice_ref,
        "needs_manual_review": True,
        "extraction_method": "filename_pattern"
    }

def extract_republic_services(filename: str, property_name: str) -> Dict[str, Any]:
    """Extract data from Republic Services invoices (Prosper & Prosper Lakes)"""

    match = re.search(r'(\d+)_(\d{2})-(\d{4})', filename)
    if match:
        invoice_ref = match.group(1)
        month = match.group(2)
        year = match.group(3)
        billing_period = f"{year}-{month}"
    else:
        billing_period = "Unknown"

    if "Prosper Lakes" in property_name:
        address = "980 S Coit Rd, Prosper, TX"
        units = 308
    else:
        address = "980 S Coit Rd, Prosper, TX"
        units = 312

    return {
        "source_file": filename,
        "document_type": "invoice",
        "property_name": property_name,
        "property_address": address,
        "vendor_name": "Republic Services",
        "vendor_account_number": "3-0615-0156865",
        "billing_period": billing_period,
        "units": units,
        "container_info": "4 Front Load 10yd containers, 12 lifts/week",
        "invoice_number": invoice_ref,
        "needs_manual_review": True,
        "extraction_method": "filename_pattern"
    }

def extract_community_waste(filename: str) -> Dict[str, Any]:
    """Extract data from Community Waste Disposal (McCord Park)"""

    match = re.search(r'(\d+)_(\d{2})-(\d{4})', filename)
    if match:
        invoice_ref = match.group(1)
        month = match.group(2)
        year = match.group(3)
        billing_period = f"{year}-{month}"
    else:
        billing_period = "Unknown"

    return {
        "source_file": filename,
        "document_type": "invoice",
        "property_name": "Orion McCord Park",
        "property_address": "2050 FM 423, Little Elm, TX 75068",
        "vendor_name": "Community Waste Disposal, LP",
        "vendor_account_number": "105004",
        "billing_period": billing_period,
        "units": None,
        "container_info": "Front Load Refuse Service, Apartment Recycle Program",
        "invoice_number": invoice_ref,
        "needs_manual_review": True,
        "extraction_method": "filename_pattern"
    }

def extract_tcam_millenia(filename: str) -> Dict[str, Any]:
    """Extract data from The Club at Millenia invoices"""

    # TCAM format: TCAM 4.15.25.pdf or invoice (X).pdf
    if "TCAM" in filename:
        match = re.search(r'(\d+)\.15\.25', filename)
        if match:
            month_num = match.group(1)
            billing_period = f"2025-{month_num.zfill(2)}"
        else:
            billing_period = "2025"
    else:
        # invoice (X).pdf format
        billing_period = "2025"

    return {
        "source_file": filename,
        "document_type": "invoice",
        "property_name": "The Club at Millenia",
        "property_address": "5826 PGA Blvd, Orlando, FL",
        "vendor_name": "Waste Connections of Florida",
        "vendor_account_number": "6460-131941",
        "billing_period": billing_period,
        "units": 560,
        "container_info": "30yd Roll-Off containers, on-call service",
        "invoice_number": filename.replace(".pdf", ""),
        "needs_manual_review": True,
        "extraction_method": "filename_pattern"
    }

def process_all_invoices():
    """Process all invoices from the categories file"""

    categories_file = Path(r"C:\Users\Richard\Downloads\Orion Data Part 2\Reports\Batch_Extraction\invoice_categories.json")

    with open(categories_file, 'r') as f:
        categories = json.load(f)

    all_extractions = []
    property_summaries = {}

    for prop_name, prop_data in categories.items():
        print(f"\nProcessing {prop_name}: {len(prop_data['invoices'])} invoices")

        property_summaries[prop_name] = {
            "vendor": prop_data["vendor"],
            "units": prop_data["units"],
            "container_size": prop_data["container_size"],
            "invoice_count": len(prop_data["invoices"]),
            "invoices_processed": 0,
            "total_amount": 0,
            "invoices": []
        }

        for invoice_path in prop_data["invoices"]:
            filename = Path(invoice_path).name

            # Extract based on property type
            if "McKinney" in prop_name:
                extraction = extract_frontier_waste(filename, {})
            elif "Prosper Lakes" in prop_name:
                extraction = extract_republic_services(filename, "Orion Prosper Lakes")
            elif "Prosper" in prop_name and "Lakes" not in prop_name:
                extraction = extract_republic_services(filename, "Orion Prosper")
            elif "McCord" in prop_name:
                extraction = extract_community_waste(filename)
            elif "Millenia" in prop_name:
                extraction = extract_tcam_millenia(filename)
            else:
                continue

            extraction["file_path"] = invoice_path
            all_extractions.append(extraction)
            property_summaries[prop_name]["invoices"].append(extraction)
            property_summaries[prop_name]["invoices_processed"] += 1

    return all_extractions, property_summaries

def create_summary_report(property_summaries: Dict) -> Dict:
    """Create comprehensive summary report"""

    total_invoices = sum(p["invoices_processed"] for p in property_summaries.values())

    summary = {
        "extraction_date": datetime.now().isoformat(),
        "extraction_method": "Filename pattern analysis + manual review required",
        "total_invoices_processed": total_invoices,
        "successful_extractions": total_invoices,
        "properties": {},
        "flags": {
            "critical": 0,
            "needs_review": total_invoices,  # All need full PDF review
            "validate": total_invoices
        },
        "next_steps": [
            "Full PDF extraction using Claude Vision API required for:",
            "- Invoice amounts and totals",
            "- Line item details",
            "- Service dates and descriptions",
            "- Tax and fee breakdowns"
        ]
    }

    for prop_name, prop_data in property_summaries.items():
        summary["properties"][prop_name] = {
            "vendor": prop_data["vendor"],
            "units": prop_data["units"],
            "invoices": prop_data["invoice_count"],
            "invoices_processed": prop_data["invoices_processed"],
            "needs_full_extraction": True,
            "extraction_status": "Metadata only - PDF review required"
        }

    return summary

if __name__ == "__main__":
    print("="*70)
    print("WASTE INVOICE BATCH EXTRACTION - Stage 1: Metadata")
    print("="*70)

    print("\nProcessing all invoices...")
    all_extractions, property_summaries = process_all_invoices()

    # Save extraction data
    output_dir = Path(r"C:\Users\Richard\Downloads\Orion Data Part 2\Reports\Batch_Extraction")

    extraction_file = output_dir / "extraction_data_stage1.json"
    with open(extraction_file, 'w') as f:
        json.dump({"document_records": all_extractions}, f, indent=2)
    print(f"\nExtraction data saved: {extraction_file}")

    # Create summary report
    summary = create_summary_report(property_summaries)

    summary_file = output_dir / "batch_extraction_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Summary report saved: {summary_file}")

    # Print summary
    print("\n" + "="*70)
    print("EXTRACTION SUMMARY")
    print("="*70)
    print(f"Total invoices processed: {summary['total_invoices_processed']}")
    print(f"Successful extractions: {summary['successful_extractions']}")
    print(f"\nBy Property:")
    for prop_name, prop_info in summary["properties"].items():
        print(f"  {prop_name}: {prop_info['invoices']} invoices ({prop_info['vendor']})")

    print(f"\n⚠️  NOTE: This is Stage 1 - Metadata extraction only")
    print(f"⚠️  Full PDF extraction with amounts and line items requires Claude Vision API")
    print(f"\nFiles created:")
    print(f"  - {extraction_file.name}")
    print(f"  - {summary_file.name}")
