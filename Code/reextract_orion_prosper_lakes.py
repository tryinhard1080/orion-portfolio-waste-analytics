#!/usr/bin/env python3
"""
Re-extract ALL Orion Prosper Lakes invoices (10 PDFs)
Fixes missing extraction issue from initial batch process
"""

import os
import json
import base64
from pathlib import Path
from datetime import datetime
import anthropic

# Configuration
ORION_PROSPER_LAKES_FOLDER = Path("C:/Users/Richard/Downloads/Orion Data Part 2/Invoices/Orion Prosper Lakes Trash Bills")
OUTPUT_FOLDER = Path("C:/Users/Richard/Downloads/Orion Data Part 2/Extraction_Output")
OUTPUT_FOLDER.mkdir(exist_ok=True)

# Get API key
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable not set")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Find all PDFs
pdf_files = sorted(ORION_PROSPER_LAKES_FOLDER.glob("**/*.pdf"))
print(f" Found {len(pdf_files)} PDFs for Orion Prosper Lakes")
print(f" Source folder: {ORION_PROSPER_LAKES_FOLDER}")
print(f" Output folder: {OUTPUT_FOLDER}\n")

# Extraction schema
extraction_schema = {
    "source_file": None,
    "property_name": "Orion Prosper Lakes",
    "vendor_name": None,
    "vendor_account_number": None,
    "billing_period": {"month_year": None},
    "invoice": {
        "invoice_number": None,
        "invoice_date": None,
        "amount_due": None,
        "line_items": []
    }
}

# Extract each invoice
extracted_invoices = []
failed_extractions = []

for i, pdf_path in enumerate(pdf_files, 1):
    print(f"[{i}/{len(pdf_files)}]  {pdf_path.name}")

    try:
        # Read PDF and encode
        with open(pdf_path, "rb") as f:
            pdf_data = base64.b64encode(f.read()).decode("utf-8")

        # Create extraction prompt
        prompt = f"""Extract all information from this waste management invoice into structured JSON.

Return ONLY valid JSON in this exact format:
{json.dumps(extraction_schema, indent=2)}

For line_items array, include ALL charges with:
- date: Service date in YYYY-MM-DD format (or null if not applicable)
- description: Full line item description text
- category: Classify as one of [base, extra_pickup, contamination, overage, fuel_surcharge, franchise_fee, admin, env_charge, tax, other]
- quantity: Numeric quantity or null
- unit_rate: Unit rate as string without $ symbol (e.g., "2015.86") or null
- extended_amount: Line item total as string without $ symbol (e.g., "2015.86") or null

CRITICAL EXTRACTION RULES:
1. Property name is "Orion Prosper Lakes" (hardcoded)
2. Extract ALL monetary amounts as plain numeric strings (no $ or commas)
3. Extract ALL dates in YYYY-MM-DD format
4. For billing_period.month_year, use "MM-YYYY" format (e.g., "01-2025")
5. If a field cannot be found in the invoice, use null (not empty string)
6. Include EVERY line item from the invoice, even if category is unclear (use "other")
7. For fuel surcharge or environmental charges, use appropriate category
8. Base service charges should be category "base"
9. Extra pickups or overages should be category "extra_pickup" or "overage"

Return ONLY the JSON object, no markdown, no explanations, no code blocks."""

        # Call Claude Vision API
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_data
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }]
        )

        response_text = message.content[0].text

        # Clean markdown code blocks if present
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        # Parse JSON
        extracted_data = json.loads(response_text)

        # Add source file
        extracted_data["source_file"] = pdf_path.name

        # Extract key info for logging
        invoice_num = extracted_data.get("invoice", {}).get("invoice_number", "N/A")
        invoice_date = extracted_data.get("invoice", {}).get("invoice_date", "N/A")
        amount = extracted_data.get("invoice", {}).get("amount_due", "N/A")
        line_count = len(extracted_data.get("invoice", {}).get("line_items", []))

        extracted_invoices.append(extracted_data)
        print(f"   SUCCESS: Invoice #{invoice_num} | Date: {invoice_date} | Amount: ${amount} | Items: {line_count}")

    except json.JSONDecodeError as e:
        print(f"   ERROR: JSON Parse Error: {str(e)}")
        print(f"   Response: {response_text[:200]}...")
        failed_extractions.append({
            "source_file": pdf_path.name,
            "error_type": "json_parse_error",
            "error": str(e)
        })

    except Exception as e:
        print(f"   ERROR: Extraction Error: {str(e)}")
        failed_extractions.append({
            "source_file": pdf_path.name,
            "error_type": "extraction_error",
            "error": str(e)
        })

# Save results
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = OUTPUT_FOLDER / f"OrionProsperLakes_ReExtraction_{timestamp}.json"

output_data = {
    "extraction_metadata": {
        "extraction_date": datetime.now().isoformat(),
        "property": "Orion Prosper Lakes",
        "source_folder": str(ORION_PROSPER_LAKES_FOLDER),
        "total_pdfs_found": len(pdf_files),
        "successful_extractions": len(extracted_invoices),
        "failed_extractions": len(failed_extractions),
        "success_rate": f"{len(extracted_invoices)/len(pdf_files)*100:.1f}%"
    },
    "invoices": extracted_invoices,
    "failures": failed_extractions
}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

# Print summary
print("\n" + "="*80)
print(" EXTRACTION SUMMARY - Orion Prosper Lakes")
print("="*80)
print(f"SUCCESS: Successful: {len(extracted_invoices)}/{len(pdf_files)} invoices")
print(f"ERROR: Failed: {len(failed_extractions)}/{len(pdf_files)} invoices")
print(f" Success Rate: {len(extracted_invoices)/len(pdf_files)*100:.1f}%")
print(f" Output saved to: {output_file}")
print("="*80)

if failed_extractions:
    print("\nWARNING:  Failed Extractions:")
    for failure in failed_extractions:
        print(f"   - {failure['source_file']}: {failure['error_type']}")
