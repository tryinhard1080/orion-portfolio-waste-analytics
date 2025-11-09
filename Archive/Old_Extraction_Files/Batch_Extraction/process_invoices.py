#!/usr/bin/env python3
"""
Invoice Processing Script for Claude Code
Processes waste management invoices by reading PDFs and organizing data
"""

import os
import json
from pathlib import Path
from datetime import datetime

def categorize_invoices():
    """Categorize all invoices by property"""

    base_path = Path(r"C:\Users\Richard\Downloads\Orion Data Part 2\Invoices")

    categories = {
        "Orion McKinney": {
            "path": "Orion McKinney Trash Bills",
            "vendor": "Frontier Waste",
            "units": 453,
            "container_size": "30yd",
            "invoices": []
        },
        "Orion Prosper": {
            "path": "Orion Prosper Trash Bills",
            "vendor": "Republic Services",
            "units": 312,
            "container_size": "30yd",
            "invoices": []
        },
        "Orion Prosper Lakes": {
            "path": "Orion Prosper Lakes Trash Bills",
            "vendor": "Republic Services",
            "units": 308,
            "container_size": "30yd",
            "invoices": []
        },
        "Orion McCord Park": {
            "path": "Orion McCord Trash Bills",
            "vendor": "Community Waste Disposal",
            "units": None,
            "container_size": None,
            "invoices": []
        },
        "The Club at Millenia": {
            "path": None,
            "vendor": "Various",
            "units": 560,
            "container_size": "40yd",
            "invoices": []
        }
    }

    # Scan for all PDFs
    for pdf_file in base_path.rglob("*.pdf"):
        rel_path = str(pdf_file.relative_to(base_path))

        # Categorize
        if "McKinney" in str(pdf_file):
            categories["Orion McKinney"]["invoices"].append(str(pdf_file))
        elif "Prosper Lakes" in str(pdf_file):
            categories["Orion Prosper Lakes"]["invoices"].append(str(pdf_file))
        elif "Prosper Trash" in str(pdf_file):
            categories["Orion Prosper"]["invoices"].append(str(pdf_file))
        elif "McCord" in str(pdf_file):
            categories["Orion McCord Park"]["invoices"].append(str(pdf_file))
        elif "TCAM" in pdf_file.name or "invoice (" in pdf_file.name:
            categories["The Club at Millenia"]["invoices"].append(str(pdf_file))

    return categories

def create_processing_manifest(categories):
    """Create a manifest for processing"""

    manifest = {
        "extraction_date": datetime.now().isoformat(),
        "total_invoices": sum(len(cat["invoices"]) for cat in categories.values()),
        "properties": {}
    }

    for prop_name, prop_data in categories.items():
        manifest["properties"][prop_name] = {
            "vendor": prop_data["vendor"],
            "units": prop_data["units"],
            "container_size": prop_data["container_size"],
            "invoice_count": len(prop_data["invoices"]),
            "invoice_files": [Path(f).name for f in prop_data["invoices"]]
        }

    return manifest

if __name__ == "__main__":
    print("Categorizing invoices...")
    categories = categorize_invoices()

    print("\nCreating manifest...")
    manifest = create_processing_manifest(categories)

    output_file = Path(r"C:\Users\Richard\Downloads\Orion Data Part 2\Reports\Batch_Extraction\processing_manifest.json")
    with open(output_file, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nManifest saved to: {output_file}")
    print(f"\nTotal invoices to process: {manifest['total_invoices']}")

    for prop_name, prop_info in manifest["properties"].items():
        print(f"  {prop_name}: {prop_info['invoice_count']} invoices")

    # Save full categories for later processing
    categories_file = output_file.parent / "invoice_categories.json"
    categories_serializable = {
        k: {
            "vendor": v["vendor"],
            "units": v["units"],
            "container_size": v["container_size"],
            "invoices": v["invoices"]
        }
        for k, v in categories.items()
    }

    with open(categories_file, "w") as f:
        json.dump(categories_serializable, f, indent=2)

    print(f"\nFull categories saved to: {categories_file}")
