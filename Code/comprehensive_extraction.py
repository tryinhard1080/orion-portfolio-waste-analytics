"""
Comprehensive Extraction - All Invoices & Contracts
Scans entire folder structure and extracts ALL PDFs (invoices + contracts)
"""

import os
import json
import base64
from pathlib import Path
from datetime import datetime
import anthropic
import pandas as pd

# Configuration
ROOT_FOLDER = Path("..")
OUTPUT_FOLDER = Path("../Extraction_Output")
OUTPUT_FOLDER.mkdir(exist_ok=True)

# API Key
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("WARNING: ANTHROPIC_API_KEY not set")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def comprehensive_scan():
    """Scan entire folder structure for ALL PDFs"""

    all_pdfs = {
        "invoices": [],
        "contracts": [],
        "unknown": []
    }

    # Keywords for classification
    invoice_keywords = [
        "invoice", "statement", "bill", "trash bills",
        "republic services", "frontier waste", "community waste",
        "city of mckinney", "tcam"
    ]

    contract_keywords = [
        "agreement", "contract", "bulk agreement"
    ]

    print("\nScanning all folders for PDFs...")

    for root, dirs, files in os.walk(ROOT_FOLDER):
        for file in files:
            if file.lower().endswith('.pdf'):
                full_path = Path(root) / file
                rel_path = full_path.relative_to(ROOT_FOLDER)

                file_lower = file.lower()
                folder_lower = str(rel_path.parent).lower()

                file_info = {
                    "path": str(full_path),
                    "filename": file,
                    "relative_path": str(rel_path),
                    "folder": str(rel_path.parent)
                }

                # Classify by folder and filename
                is_invoice = False
                is_contract = False

                # Check folder structure
                if "trash bills" in folder_lower or folder_lower == "invoices":
                    is_invoice = True
                elif "contracts" in folder_lower:
                    is_contract = True

                # Check filename
                if any(kw in file_lower for kw in invoice_keywords):
                    is_invoice = True
                if any(kw in file_lower for kw in contract_keywords):
                    is_contract = True

                # Classify (invoice takes precedence)
                if is_invoice:
                    all_pdfs["invoices"].append(file_info)
                elif is_contract:
                    all_pdfs["contracts"].append(file_info)
                else:
                    all_pdfs["unknown"].append(file_info)

    print(f"\nFound {len(all_pdfs['invoices'])} invoices")
    print(f"Found {len(all_pdfs['contracts'])} contracts")
    print(f"Found {len(all_pdfs['unknown'])} unknown PDFs")

    return all_pdfs


def extract_invoice_with_vision(pdf_path, filename):
    """Extract invoice data using Claude Vision API"""

    print(f"   Extracting: {filename}...")

    with open(pdf_path, "rb") as f:
        pdf_data = base64.b64encode(f.read()).decode("utf-8")

    extraction_schema = {
        "source_file": "",
        "document_type": "invoice",
        "property_name": None,
        "property_address": None,
        "vendor_name": None,
        "vendor_account_number": None,
        "billing_period": {
            "start_date": None,
            "end_date": None,
            "month_year": None
        },
        "invoice": {
            "invoice_number": None,
            "invoice_date": None,
            "due_date": None,
            "amount_due": None,
            "previous_balance": None,
            "payments": None,
            "subtotal": None,
            "taxes": None,
            "line_items": []
        }
    }

    prompt = f"""Extract all information from this waste management invoice/bill into structured JSON.

Return ONLY valid JSON in this exact format:
{json.dumps(extraction_schema, indent=2)}

For line_items, include:
- date: Service date (YYYY-MM-DD)
- description: Full line item description
- category: One of [base, extra_pickup, contamination, overage, fuel_surcharge, franchise_fee, admin, env_charge, tax, other]
- quantity: Number value or null
- uom: Unit of measure (month, lift, incident, etc) or null
- container_size_yd: Container size in yards (number or null)
- container_type: FEL, COMPACTOR, REL, or null
- frequency_per_week: Number or null
- unit_rate: Numeric string without $ or null
- extended_amount: Numeric string without $ or null
- notes: Any additional context or null

CRITICAL EXTRACTION RULES:
1. Property name is CRITICAL - look at top of document for property/location name
2. Extract ALL amounts as strings without $ or commas (e.g., "1250.00")
3. Extract ALL dates in YYYY-MM-DD format
4. If a field cannot be found, use null (not empty string)
5. For vendor, use company name (Republic Services, Frontier Waste, etc.)
6. Include ALL line items, fees, and charges
7. For billing period, extract the service month/period
8. Categorize charges appropriately

Return ONLY the JSON, no explanations or markdown."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[
                {
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
                }
            ]
        )

        response_text = message.content[0].text

        # Clean markdown
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        extracted_data = json.loads(response_text)
        extracted_data["source_file"] = filename

        return extracted_data, None

    except Exception as e:
        return None, str(e)


def extract_contract_with_vision(pdf_path, filename):
    """Extract contract data using Claude Vision API"""

    print(f"   Extracting: {filename}...")

    with open(pdf_path, "rb") as f:
        pdf_data = base64.b64encode(f.read()).decode("utf-8")

    extraction_schema = {
        "source_file": "",
        "document_type": "contract",
        "property_name": None,
        "property_address": None,
        "vendor_name": None,
        "contract_details": {
            "effective_date": None,
            "expiration_date": None,
            "initial_term_years": None,
            "renewal_term_months": None,
            "auto_renew": None,
            "notice_term_days": None,
            "termination_clause": None,
            "price_increase_clause": None
        },
        "service_schedules": [],
        "pricing": {
            "monthly_total": None,
            "annual_total": None,
            "base_charges": [],
            "additional_charges": []
        }
    }

    prompt = f"""Extract all contract information into structured JSON.

Return ONLY valid JSON in this format:
{json.dumps(extraction_schema, indent=2)}

For service_schedules, include:
- container_type: Type of container
- container_size_yd: Size in yards
- quantity: Number of containers
- frequency_per_week: Pickup frequency
- monthly_rate: Monthly cost

CRITICAL:
1. Property name is CRITICAL
2. Extract all dates in YYYY-MM-DD format
3. Extract pricing details
4. Look for auto-renewal and termination clauses
5. If field not found, use null

Return ONLY JSON, no explanations."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[
                {
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
                }
            ]
        )

        response_text = message.content[0].text

        # Clean markdown
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        extracted_data = json.loads(response_text)
        extracted_data["source_file"] = filename

        return extracted_data, None

    except Exception as e:
        return None, str(e)


def validate_extraction(extracted_data, doc_type="invoice"):
    """Quick validation"""

    if extracted_data is None:
        return {"needs_review": True, "confidence": 0.0, "errors": ["Extraction failed"]}

    errors = []
    confidence = 1.0

    if not extracted_data.get("property_name"):
        errors.append("Missing property name")
        confidence -= 0.20

    if not extracted_data.get("vendor_name"):
        errors.append("Missing vendor name")
        confidence -= 0.15

    if doc_type == "invoice":
        invoice = extracted_data.get("invoice", {})
        if not invoice.get("amount_due"):
            errors.append("Missing amount")
            confidence -= 0.15

    return {
        "needs_review": confidence < 0.70,
        "confidence": round(max(0, confidence), 2),
        "errors": errors
    }


def export_comprehensive_excel(all_invoices, all_contracts, output_path):
    """Export everything to Excel"""

    print(f"\nExporting to Excel: {output_path.name}")

    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        workbook = writer.book

        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4472C4',
            'font_color': 'white'
        })

        # Invoice Summary
        invoice_summary = []
        invoices_by_property = {}

        for inv_data, validation in all_invoices:
            if inv_data:
                prop = inv_data.get("property_name") or "Unknown"
                if prop not in invoices_by_property:
                    invoices_by_property[prop] = []
                invoices_by_property[prop].append((inv_data, validation))

        for prop, invoices in sorted(invoices_by_property.items()):
            invoice_summary.append({
                "Property": prop,
                "Invoice Count": len(invoices),
                "Needs Review": sum(1 for _, v in invoices if v["needs_review"]),
                "Avg Confidence": round(sum(v["confidence"] for _, v in invoices) / len(invoices), 2)
            })

        df_inv_summary = pd.DataFrame(invoice_summary)
        df_inv_summary.to_excel(writer, sheet_name='Invoice Summary', index=False)

        # Contract Summary
        contract_summary = []
        for con_data, validation in all_contracts:
            if con_data:
                contract_summary.append({
                    "Source File": con_data.get("source_file"),
                    "Property": con_data.get("property_name"),
                    "Vendor": con_data.get("vendor_name"),
                    "Effective Date": con_data.get("contract_details", {}).get("effective_date"),
                    "Expiration Date": con_data.get("contract_details", {}).get("expiration_date"),
                    "Monthly Total": con_data.get("pricing", {}).get("monthly_total"),
                    "Confidence": validation["confidence"]
                })

        if contract_summary:
            df_con_summary = pd.DataFrame(contract_summary)
            df_con_summary.to_excel(writer, sheet_name='Contract Summary', index=False)

        # Property tabs for invoices
        for prop, invoices in sorted(invoices_by_property.items()):
            sheet_name = prop[:28] + "..." if len(prop) > 31 else prop
            sheet_name = sheet_name.replace("/", "-").replace("\\", "-")

            rows = []
            for inv_data, _ in invoices:
                invoice = inv_data.get("invoice", {})
                base_row = {
                    "Source File": inv_data.get("source_file"),
                    "Property": inv_data.get("property_name"),
                    "Vendor": inv_data.get("vendor_name"),
                    "Invoice #": invoice.get("invoice_number"),
                    "Invoice Date": invoice.get("invoice_date"),
                    "Amount Due": invoice.get("amount_due"),
                    "Billing Period": inv_data.get("billing_period", {}).get("month_year")
                }

                line_items = invoice.get("line_items", [])
                if line_items:
                    for item in line_items:
                        row = base_row.copy()
                        row.update({
                            "Description": item.get("description"),
                            "Category": item.get("category"),
                            "Quantity": item.get("quantity"),
                            "Unit Rate": item.get("unit_rate"),
                            "Amount": item.get("extended_amount")
                        })
                        rows.append(row)
                else:
                    rows.append(base_row)

            if rows:
                df = pd.DataFrame(rows)
                df.to_excel(writer, sheet_name=sheet_name, index=False)

                worksheet = writer.sheets[sheet_name]
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)

    print(f"   Excel complete: {output_path}")


def main():
    """Main comprehensive extraction"""

    print("=" * 80)
    print("COMPREHENSIVE EXTRACTION - ALL INVOICES & CONTRACTS")
    print("=" * 80)

    # Step 1: Scan everything
    all_pdfs = comprehensive_scan()

    # Step 2: Extract invoices
    print(f"\nExtracting {len(all_pdfs['invoices'])} invoices...")
    all_invoices = []

    for i, pdf_info in enumerate(all_pdfs['invoices'], 1):
        print(f"[{i}/{len(all_pdfs['invoices'])}]", end=" ")
        extraction, error = extract_invoice_with_vision(pdf_info['path'], pdf_info['filename'])
        validation = validate_extraction(extraction, "invoice")
        all_invoices.append((extraction, validation))

        status = "OK" if not validation["needs_review"] else "NEEDS REVIEW"
        print(f"      {status} (Confidence: {validation['confidence']})")

    # Step 3: Extract contracts
    print(f"\nExtracting {len(all_pdfs['contracts'])} contracts...")
    all_contracts = []

    for i, pdf_info in enumerate(all_pdfs['contracts'], 1):
        print(f"[{i}/{len(all_pdfs['contracts'])}]", end=" ")
        extraction, error = extract_contract_with_vision(pdf_info['path'], pdf_info['filename'])
        validation = validate_extraction(extraction, "contract")
        all_contracts.append((extraction, validation))

        status = "OK" if not validation["needs_review"] else "NEEDS REVIEW"
        print(f"      {status} (Confidence: {validation['confidence']})")

    # Step 4: Export
    print("\nExporting to Excel...")
    excel_output = OUTPUT_FOLDER / f"Complete_Extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    export_comprehensive_excel(all_invoices, all_contracts, excel_output)

    # Step 5: Save JSON
    json_output = OUTPUT_FOLDER / f"Complete_Data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_output, "w", encoding="utf-8") as f:
        json.dump({
            "extraction_date": datetime.now().isoformat(),
            "total_invoices": len(all_invoices),
            "total_contracts": len(all_contracts),
            "invoices": [inv for inv, _ in all_invoices if inv],
            "contracts": [con for con, _ in all_contracts if con]
        }, f, indent=2)

    print("\n" + "=" * 80)
    print("EXTRACTION COMPLETE!")
    print("=" * 80)
    print(f"\nFiles:")
    print(f"  - Excel: {excel_output}")
    print(f"  - JSON: {json_output}")
    print(f"\nExtracted:")
    print(f"  - {len(all_invoices)} invoices")
    print(f"  - {len(all_contracts)} contracts")

    needs_review_inv = sum(1 for _, v in all_invoices if v["needs_review"])
    needs_review_con = sum(1 for _, v in all_contracts if v["needs_review"])

    if needs_review_inv > 0:
        print(f"\n  WARNING: {needs_review_inv} invoices need review")
    if needs_review_con > 0:
        print(f"  WARNING: {needs_review_con} contracts need review")


if __name__ == "__main__":
    main()
