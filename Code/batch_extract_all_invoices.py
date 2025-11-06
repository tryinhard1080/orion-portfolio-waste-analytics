"""
Batch Invoice Extraction - Orion Portfolio
Extracts data from all invoices using Claude Vision API and exports to Excel
"""

import os
import json
import base64
from pathlib import Path
from datetime import datetime
import anthropic
import pandas as pd

# Configuration
INVOICES_FOLDER = Path("../Invoices")
ROOT_FOLDER = Path("..")
OUTPUT_FOLDER = Path("../Extraction_Output")
OUTPUT_FOLDER.mkdir(exist_ok=True)

# API Key from environment
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("WARNING: WARNING: ANTHROPIC_API_KEY not set. Extraction will fail.")
    print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def categorize_pdfs():
    """Scan and categorize all PDFs as invoices or contracts"""

    invoices = []
    contracts = []

    # Contract keywords
    contract_keywords = ["agreement", "contract", "bulk agreement", "wci bulk"]

    # Scan Invoices folder
    if INVOICES_FOLDER.exists():
        for pdf_file in INVOICES_FOLDER.rglob("*.pdf"):
            invoices.append(pdf_file)

    # Scan root folder
    for pdf_file in ROOT_FOLDER.glob("*.pdf"):
        filename_lower = pdf_file.name.lower()

        # Check if it's a contract
        if any(keyword in filename_lower for keyword in contract_keywords):
            contracts.append(pdf_file)
        elif "invoice" in filename_lower or "trash" in filename_lower:
            invoices.append(pdf_file)

    print(f"\n>> Found {len(invoices)} invoices and {len(contracts)} contracts")
    print(f"   Invoices will be extracted, contracts will be skipped.\n")

    return invoices, contracts


def extract_invoice_with_vision(pdf_path):
    """Extract invoice data using Claude Vision API"""

    print(f"   Extracting: {pdf_path.name}...")

    # Read PDF as base64
    with open(pdf_path, "rb") as f:
        pdf_data = base64.b64encode(f.read()).decode("utf-8")

    # Extraction schema
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
            "raw": None
        },
        "invoice": {
            "invoice_number": None,
            "invoice_date": None,
            "due_date": None,
            "amount_due": None,
            "subtotal": None,
            "line_items": []
        }
    }

    prompt = f"""Extract all information from this waste management invoice into structured JSON.

Return ONLY valid JSON in this exact format:
{json.dumps(extraction_schema, indent=2)}

For line_items, include:
- date: Service date (YYYY-MM-DD)
- description: Full line item description
- category: One of [base, extra_pickup, contamination, overage, fuel_surcharge, franchise_fee, admin, env_charge, tax]
- quantity: Number value
- uom: Unit of measure (month, lift, incident, etc)
- container_size_yd: Container size in yards (number or null)
- container_type: FEL, COMPACTOR, REL, or null
- frequency_per_week: Number or null
- unit_rate: Numeric string without $
- extended_amount: Numeric string without $
- notes: Any additional context or null

CRITICAL RULES:
- Extract ALL amounts as strings without $ or commas (e.g., "1250.00")
- Extract ALL dates in YYYY-MM-DD format
- If a field cannot be found, use null
- Property name is CRITICAL - extract carefully (look for property/location name at top of invoice)
- Include ALL line items, even small fees
- For vendor name, use the company name (Republic Services, Frontier Waste, Community Waste, etc.)
- For category, classify charges appropriately

Return ONLY the JSON, no explanations."""

    try:
        # Call Claude Vision API
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

        # Parse response
        response_text = message.content[0].text

        # Clean markdown code blocks if present
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        extracted_data = json.loads(response_text)
        extracted_data["source_file"] = pdf_path.name

        return extracted_data, None

    except Exception as e:
        error_msg = f"ERROR: ERROR: {str(e)}"
        print(f"      {error_msg}")
        return None, error_msg


def validate_extraction(extracted_data):
    """Validate extraction quality and calculate confidence score"""

    if extracted_data is None:
        return {
            "source_file": "unknown",
            "confidence_score": 0.0,
            "critical_missing": ["ALL_FIELDS"],
            "warnings": ["Extraction failed"],
            "needs_review": True
        }

    validation = {
        "source_file": extracted_data.get("source_file"),
        "property_name": extracted_data.get("property_name"),
        "confidence_score": 1.0,
        "critical_missing": [],
        "warnings": [],
        "needs_review": False
    }

    # Check critical fields
    critical_fields = [
        ("property_name", extracted_data.get("property_name")),
        ("vendor_name", extracted_data.get("vendor_name")),
        ("invoice.invoice_number", extracted_data.get("invoice", {}).get("invoice_number")),
        ("invoice.invoice_date", extracted_data.get("invoice", {}).get("invoice_date")),
        ("invoice.amount_due", extracted_data.get("invoice", {}).get("amount_due"))
    ]

    for field_name, field_value in critical_fields:
        if field_value is None or field_value == "":
            validation["critical_missing"].append(field_name)
            validation["confidence_score"] -= 0.15

    # Validate line items
    invoice = extracted_data.get("invoice", {})
    line_items = invoice.get("line_items", [])

    if not line_items:
        validation["warnings"].append("No line items extracted")
        validation["confidence_score"] -= 0.10
    else:
        # Check if line items sum to total
        try:
            line_total = sum(
                float(item.get("extended_amount", 0) or 0)
                for item in line_items
            )
            invoice_total = float(invoice.get("amount_due", 0) or 0)

            if invoice_total > 0 and abs(line_total - invoice_total) > 1.0:
                validation["warnings"].append(
                    f"Line items total (${line_total:.2f}) != Invoice total (${invoice_total:.2f})"
                )
                validation["confidence_score"] -= 0.10
        except:
            pass

    # Determine if review needed
    validation["confidence_score"] = round(max(0, validation["confidence_score"]), 2)
    validation["needs_review"] = (
        validation["confidence_score"] < 0.70 or
        len(validation["critical_missing"]) > 0
    )

    return validation


def organize_by_property(all_extractions, all_validations):
    """Organize extracted data by property name"""

    by_property = {}

    for extraction, validation in zip(all_extractions, all_validations):
        if extraction is None:
            continue

        prop_name = extraction.get("property_name") or "Unknown Property"

        if prop_name not in by_property:
            by_property[prop_name] = {
                "invoices": [],
                "validations": []
            }

        by_property[prop_name]["invoices"].append(extraction)
        by_property[prop_name]["validations"].append(validation)

    return by_property


def export_to_excel(by_property, output_path):
    """Export organized data to Excel with multiple tabs"""

    print(f"\n Exporting to Excel: {output_path.name}")

    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        workbook = writer.book

        # Format definitions
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4472C4',
            'font_color': 'white',
            'border': 1
        })

        red_format = workbook.add_format({'bg_color': '#FFC7CE'})
        yellow_format = workbook.add_format({'bg_color': '#FFEB9C'})

        # Summary tab
        summary_data = []
        for property_name, data in sorted(by_property.items()):
            validations = data["validations"]
            summary_data.append({
                "Property Name": property_name,
                "Invoice Count": len(data["invoices"]),
                "Needs Review": sum(v["needs_review"] for v in validations),
                "Avg Confidence": round(
                    sum(v["confidence_score"] for v in validations) / len(validations)
                    if validations else 0, 2
                ),
                "Critical Issues": sum(1 for v in validations if v["critical_missing"])
            })

        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Summary', index=False)

        # Format summary
        worksheet = writer.sheets['Summary']
        for col_num, value in enumerate(df_summary.columns.values):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, 18)

        # Property tabs
        for property_name, data in sorted(by_property.items()):
            # Clean sheet name (Excel 31 char limit)
            sheet_name = property_name[:28] + "..." if len(property_name) > 31 else property_name
            sheet_name = sheet_name.replace("/", "-").replace("\\", "-").replace("[", "").replace("]", "")

            rows = []
            for invoice_data in data["invoices"]:
                invoice = invoice_data.get("invoice", {})

                # Base row
                base_row = {
                    "Source File": invoice_data.get("source_file"),
                    "Property": invoice_data.get("property_name"),
                    "Vendor": invoice_data.get("vendor_name"),
                    "Account #": invoice_data.get("vendor_account_number"),
                    "Invoice #": invoice.get("invoice_number"),
                    "Invoice Date": invoice.get("invoice_date"),
                    "Due Date": invoice.get("due_date"),
                    "Amount Due": invoice.get("amount_due"),
                }

                # Expand line items
                line_items = invoice.get("line_items", [])
                if line_items:
                    for item in line_items:
                        row = base_row.copy()
                        row.update({
                            "Service Date": item.get("date"),
                            "Description": item.get("description"),
                            "Category": item.get("category"),
                            "Quantity": item.get("quantity"),
                            "UOM": item.get("uom"),
                            "Container Size (yd)": item.get("container_size_yd"),
                            "Container Type": item.get("container_type"),
                            "Frequency/Week": item.get("frequency_per_week"),
                            "Unit Rate": item.get("unit_rate"),
                            "Extended Amount": item.get("extended_amount"),
                            "Notes": item.get("notes")
                        })
                        rows.append(row)
                else:
                    # No line items, just add base row
                    rows.append(base_row)

            if rows:
                df_property = pd.DataFrame(rows)
                df_property.to_excel(writer, sheet_name=sheet_name, index=False)

                # Format
                worksheet = writer.sheets[sheet_name]
                for col_num, value in enumerate(df_property.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                    # Auto-width
                    max_len = max(
                        df_property[value].astype(str).apply(len).max(),
                        len(str(value))
                    )
                    worksheet.set_column(col_num, col_num, min(max_len + 2, 50))

        # Validation tab
        validation_rows = []
        for property_name, data in sorted(by_property.items()):
            for val in data["validations"]:
                validation_rows.append({
                    "Property": property_name,
                    "Source File": val["source_file"],
                    "Confidence": val["confidence_score"],
                    "Needs Review": "YES" if val["needs_review"] else "NO",
                    "Missing Fields": "; ".join(val["critical_missing"]) if val["critical_missing"] else "",
                    "Warnings": "; ".join(val["warnings"]) if val["warnings"] else ""
                })

        df_validation = pd.DataFrame(validation_rows)
        df_validation.to_excel(writer, sheet_name='Validation', index=False)

        # Format validation tab
        worksheet = writer.sheets['Validation']
        for col_num, value in enumerate(df_validation.columns.values):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, 20)

        # Highlight rows needing review
        for idx, row in enumerate(validation_rows, start=1):
            if row["Needs Review"] == "YES":
                for col in range(len(df_validation.columns)):
                    worksheet.write(idx, col, df_validation.iloc[idx-1, col], red_format)
            elif row["Confidence"] < 0.85:
                for col in range(len(df_validation.columns)):
                    worksheet.write(idx, col, df_validation.iloc[idx-1, col], yellow_format)

    print(f"   OK: Excel export complete: {output_path}")


def generate_validation_report(all_validations, by_property, output_path):
    """Generate detailed validation report in Markdown"""

    report = []
    report.append("# BATCH INVOICE EXTRACTION - VALIDATION REPORT")
    report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"\n## SUMMARY\n")

    total_docs = len(all_validations)
    needs_review = sum(1 for v in all_validations if v["needs_review"])
    avg_confidence = sum(v["confidence_score"] for v in all_validations) / total_docs if total_docs > 0 else 0
    critical_issues = sum(1 for v in all_validations if v["critical_missing"])

    report.append(f"- **Total Invoices Processed**: {total_docs}")
    report.append(f"- **Invoices Needing Review**: {needs_review} ({needs_review/total_docs*100:.1f}%)")
    report.append(f"- **Average Confidence Score**: {avg_confidence:.2f}")
    report.append(f"- **Critical Issues**: {critical_issues}")

    # Property breakdown
    report.append(f"\n## PROPERTY BREAKDOWN\n")
    for property_name, data in sorted(by_property.items()):
        validations = data["validations"]
        prop_needs_review = sum(1 for v in validations if v["needs_review"])
        prop_avg_confidence = sum(v["confidence_score"] for v in validations) / len(validations) if validations else 0

        status = "OK:" if prop_needs_review == 0 else "WARNING:"
        report.append(f"{status} **{property_name}**")
        report.append(f"   - Invoices: {len(data['invoices'])}")
        report.append(f"   - Needs Review: {prop_needs_review}")
        report.append(f"   - Avg Confidence: {prop_avg_confidence:.2f}")

    # Critical issues
    if critical_issues > 0:
        report.append(f"\n## CRITICAL ISSUES\n")
        for val in all_validations:
            if val["critical_missing"]:
                report.append(f"\n**{val['source_file']}** (Property: {val.get('property_name', 'UNKNOWN')})")
                report.append(f"- Missing: {', '.join(val['critical_missing'])}")
                report.append(f"- Confidence: {val['confidence_score']}")

    # Warnings
    warnings_count = sum(1 for v in all_validations if v["warnings"])
    if warnings_count > 0:
        report.append(f"\n## WARNINGS ({warnings_count} invoices)\n")
        for val in all_validations:
            if val["warnings"]:
                report.append(f"\n**{val['source_file']}**")
                for warning in val["warnings"]:
                    report.append(f"- WARNING: {warning}")

    # Write report
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report))

    print(f"   OK: Validation report: {output_path}")


def main():
    """Main extraction workflow"""

    print("=" * 70)
    print("BATCH INVOICE EXTRACTION - ORION PORTFOLIO")
    print("=" * 70)

    # Step 1: Scan and categorize
    print("\n STEP 1: Scanning for invoices...")
    invoices, contracts = categorize_pdfs()

    if not invoices:
        print("ERROR: No invoices found!")
        return

    print(f"OK: Found {len(invoices)} invoices to process")

    # Step 2: Extract with Vision API
    print(f"\n STEP 2: Extracting data from {len(invoices)} invoices...")
    print("   (This may take several minutes...)\n")

    all_extractions = []
    all_validations = []

    for i, invoice_path in enumerate(invoices, 1):
        print(f"[{i}/{len(invoices)}]", end=" ")

        extraction, error = extract_invoice_with_vision(invoice_path)
        validation = validate_extraction(extraction)

        all_extractions.append(extraction)
        all_validations.append(validation)

        # Show status
        if validation["needs_review"]:
            print(f"      WARNING: Needs Review (Confidence: {validation['confidence_score']})")
        else:
            print(f"      OK: OK (Confidence: {validation['confidence_score']})")

    # Step 3: Organize by property
    print(f"\n STEP 3: Organizing by property...")
    by_property = organize_by_property(all_extractions, all_validations)
    print(f"OK: Organized into {len(by_property)} properties")

    # Step 4: Export to Excel
    print(f"\n STEP 4: Exporting to Excel...")
    excel_output = OUTPUT_FOLDER / f"Orion_Invoice_Extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    export_to_excel(by_property, excel_output)

    # Step 5: Generate validation report
    print(f"\n STEP 5: Generating validation report...")
    report_output = OUTPUT_FOLDER / f"Validation_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    generate_validation_report(all_validations, by_property, report_output)

    # Step 6: Save raw JSON
    print(f"\n STEP 6: Saving raw JSON data...")
    json_output = OUTPUT_FOLDER / f"Extraction_Data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_output, "w", encoding="utf-8") as f:
        json.dump({
            "extraction_date": datetime.now().isoformat(),
            "total_invoices": len(invoices),
            "by_property": {
                prop: {
                    "invoice_count": len(data["invoices"]),
                    "invoices": data["invoices"]
                }
                for prop, data in by_property.items()
            }
        }, f, indent=2)
    print(f"   OK: Raw data: {json_output}")

    # Final summary
    print("\n" + "=" * 70)
    print("EXTRACTION COMPLETE!")
    print("=" * 70)
    print(f"\n Output Files:")
    print(f"   - Excel: {excel_output}")
    print(f"   - Validation Report: {report_output}")
    print(f"   - Raw JSON: {json_output}")

    needs_review = sum(1 for v in all_validations if v["needs_review"])
    if needs_review > 0:
        print(f"\nWARNING: {needs_review} invoices need review (see Validation tab in Excel)")
    else:
        print(f"\nOK: All extractions passed validation!")


if __name__ == "__main__":
    main()
