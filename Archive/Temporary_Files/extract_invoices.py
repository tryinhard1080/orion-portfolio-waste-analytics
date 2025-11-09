#!/usr/bin/env python3
"""
Invoice Extraction Script for Orion Portfolio
Processes 66 PDF invoices and extracts structured data with validation
"""

import json
import re
import os
import glob
from datetime import datetime
from pathlib import Path
import subprocess

class InvoiceExtractor:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.results = {
            "extraction_date": datetime.now().strftime("%Y-%m-%d"),
            "total_invoices": 0,
            "properties": [],
            "invoices": [],
            "summary": {
                "red_flags": 0,
                "yellow_flags": 0,
                "green_flags": 0,
                "clean_extractions": 0
            }
        }

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF using pdftotext"""
        try:
            result = subprocess.run(
                ['pdftotext', '-layout', str(pdf_path), '-'],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            return ""

    def add_flag(self, flags, level, field, message, action=""):
        """Add a flag to the flags list"""
        flags.append({
            "level": level,
            "field": field,
            "message": message,
            "action": action if action else "Review invoice manually"
        })

    def extract_community_waste_disposal(self, text, filename):
        """Extract data from Community Waste Disposal (CWD) invoices"""
        data = {
            "filename": filename,
            "vendor": "Community Waste Disposal, LP",
            "property_name": None,
            "invoice_date": None,
            "invoice_number": None,
            "total_amount": None,
            "service_period": None,
            "confidence": 0,
            "flags": [],
            "all_fields": {}
        }

        # Extract invoice number
        inv_match = re.search(r'INVOICE\s*#\s*(\d+)', text)
        if inv_match:
            data["invoice_number"] = inv_match.group(1)

        # Extract date
        date_match = re.search(r'DATE\s+(\d{2}/\d{2}/\d{4})', text)
        if date_match:
            date_str = date_match.group(1)
            try:
                dt = datetime.strptime(date_str, "%m/%d/%Y")
                data["invoice_date"] = dt.strftime("%Y-%m-%d")
            except:
                self.add_flag(data["flags"], "RED_FLAG", "invoice_date",
                            f"Could not parse date: {date_str}")
        else:
            self.add_flag(data["flags"], "RED_FLAG", "invoice_date",
                        "Invoice date not found in document")

        # Extract property name
        if "MCCORD PARK FL" in text:
            data["property_name"] = "Orion McCord"
        else:
            self.add_flag(data["flags"], "RED_FLAG", "property_name",
                        "Property name not clearly identified")

        # Extract total amount
        amount_match = re.search(r'AMOUNT\s+DUE:\s*\$?\s*([\d,]+\.\d{2})', text)
        if not amount_match:
            amount_match = re.search(r'Invoice\s+Total:\s*\$?\s*([\d,]+\.\d{2})', text)

        if amount_match:
            amount_str = amount_match.group(1).replace(',', '')
            data["total_amount"] = float(amount_str)
        else:
            self.add_flag(data["flags"], "RED_FLAG", "total_amount",
                        "Total amount not found")

        # Extract service period
        period_match = re.search(r'(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)\s+\d+,\s+\d{4}', text)
        if period_match:
            data["service_period"] = period_match.group(0)
        else:
            self.add_flag(data["flags"], "NEEDS_REVIEW", "service_period",
                        "Service period not clearly stated")

        # Extract container details
        front_load_match = re.search(r'FRONT\s+LOAD\s+REFUSE\s+SERVICE\s+(\d+(?:\.\d+)?)', text)
        if front_load_match:
            data["all_fields"]["container_count"] = int(float(front_load_match.group(1)))
            data["all_fields"]["container_type"] = "Front Load"
        else:
            self.add_flag(data["flags"], "NEEDS_REVIEW", "container_details",
                        "Container count/type not explicitly stated")

        # Extract itemized charges
        charges = []
        for line in text.split('\n'):
            if re.search(r'(FRONT LOAD|SALES TAX|APARTMENT RECYCLE)', line):
                charge_match = re.search(r'\$?\s*([\d,]+\.\d{2})$', line.strip())
                if charge_match:
                    charges.append(charge_match.group(1))

        if charges:
            data["all_fields"]["itemized_charges"] = charges

        # Calculate confidence
        confidence = 0
        if data["invoice_number"]: confidence += 20
        if data["invoice_date"]: confidence += 25
        if data["property_name"]: confidence += 25
        if data["total_amount"]: confidence += 25
        if data["service_period"]: confidence += 5

        data["confidence"] = confidence

        return data

    def extract_frontier_waste(self, text, filename):
        """Extract data from Frontier Waste invoices"""
        data = {
            "filename": filename,
            "vendor": "Frontier Waste - McKinney",
            "property_name": "Orion McKinney",
            "invoice_date": None,
            "invoice_number": None,
            "total_amount": None,
            "service_period": None,
            "confidence": 0,
            "flags": [],
            "all_fields": {}
        }

        # Extract invoice number
        inv_match = re.search(r'INVOICE\s*#\s*(\d+)', text)
        if inv_match:
            data["invoice_number"] = inv_match.group(1)

        # Extract date
        date_match = re.search(r'DATE\s+([A-Za-z]+\s+\d+,\s+\d{4})', text)
        if date_match:
            date_str = date_match.group(1)
            try:
                dt = datetime.strptime(date_str, "%b %d, %Y")
                data["invoice_date"] = dt.strftime("%Y-%m-%d")
            except:
                try:
                    dt = datetime.strptime(date_str, "%B %d, %Y")
                    data["invoice_date"] = dt.strftime("%Y-%m-%d")
                except:
                    self.add_flag(data["flags"], "RED_FLAG", "invoice_date",
                                f"Could not parse date: {date_str}")

        # Extract total amount
        amount_match = re.search(r'INVOICE\s+TOTAL\s*\$\s*([\d,]+\.\d{2})', text)
        if amount_match:
            amount_str = amount_match.group(1).replace(',', '')
            data["total_amount"] = float(amount_str)
        else:
            self.add_flag(data["flags"], "RED_FLAG", "total_amount",
                        "Total amount not found")

        # Extract service period from line items
        period_match = re.search(r'(\d{2}/\d{2}/\d{2})\s*-\s*(\d{2}/\d{2}/\d{2})', text)
        if period_match:
            data["service_period"] = f"{period_match.group(1)} - {period_match.group(2)}"

        # Extract container details
        yard_matches = re.findall(r'(\d+)\s+Yard\s+(FL\s+)?Trash\s+(?:Service|Disposal)', text)
        if yard_matches:
            sizes = [int(m[0]) for m in yard_matches]
            data["all_fields"]["container_sizes"] = sizes
            data["all_fields"]["container_count"] = len(sizes)
            data["all_fields"]["container_type"] = "Dumpster"
        else:
            self.add_flag(data["flags"], "NEEDS_REVIEW", "container_details",
                        "Container details not clearly stated")

        # Extract pickup frequency
        if "Weekly" in text or "per month" in text:
            data["all_fields"]["pickup_frequency"] = "Weekly"
        else:
            self.add_flag(data["flags"], "NEEDS_REVIEW", "pickup_frequency",
                        "Pickup frequency not stated", "Check contract")

        # Calculate confidence
        confidence = 0
        if data["invoice_number"]: confidence += 20
        if data["invoice_date"]: confidence += 25
        if data["property_name"]: confidence += 25
        if data["total_amount"]: confidence += 25
        if data["service_period"]: confidence += 5

        data["confidence"] = confidence

        return data

    def extract_city_of_mckinney(self, text, filename):
        """Extract data from City of McKinney utility bills"""
        data = {
            "filename": filename,
            "vendor": "City of McKinney",
            "property_name": "Orion McKinney",
            "invoice_date": None,
            "invoice_number": None,
            "total_amount": None,
            "service_period": None,
            "confidence": 0,
            "flags": [],
            "all_fields": {}
        }

        # Extract account number (used as invoice reference)
        acct_match = re.search(r'ACCOUNT\s+NUMBER\s+(\d+-\d+)', text)
        if acct_match:
            data["invoice_number"] = acct_match.group(1)

        # Extract invoice date
        date_match = re.search(r'Invoice\s+Date\s+([A-Za-z]+\s+\d+,\s+\d{4})', text)
        if date_match:
            date_str = date_match.group(1)
            try:
                dt = datetime.strptime(date_str, "%B %d, %Y")
                data["invoice_date"] = dt.strftime("%Y-%m-%d")
            except:
                self.add_flag(data["flags"], "RED_FLAG", "invoice_date",
                            f"Could not parse date: {date_str}")

        # Extract total amount
        amount_match = re.search(r'Total\s+Amount\s+Due\s*\$\s*([\d,]+\.\d{2})', text)
        if not amount_match:
            amount_match = re.search(r'AMOUNT\s+DUE\s*\$\s*([\d,]+\.\d{2})', text)

        if amount_match:
            amount_str = amount_match.group(1).replace(',', '')
            data["total_amount"] = float(amount_str)
        else:
            self.add_flag(data["flags"], "RED_FLAG", "total_amount",
                        "Total amount not found")

        # Extract service period
        period_match = re.search(r'for\s+the\s+service\s+period\s+from\s+(\d{2}/\d{2}/\d{4})\s+to\s+(\d{2}/\d{2}/\d{4})', text)
        if period_match:
            data["service_period"] = f"{period_match.group(1)} - {period_match.group(2)}"

        # This is water/sewer, not trash
        data["all_fields"]["service_type"] = "Water/Sewer"
        self.add_flag(data["flags"], "VALIDATE", "service_type",
                    "This is a water/sewer bill, not trash service")

        # Calculate confidence
        confidence = 0
        if data["invoice_number"]: confidence += 20
        if data["invoice_date"]: confidence += 25
        if data["property_name"]: confidence += 25
        if data["total_amount"]: confidence += 25
        if data["service_period"]: confidence += 5

        data["confidence"] = confidence

        return data

    def extract_republic_services(self, text, filename):
        """Extract data from Republic Services invoices"""
        data = {
            "filename": filename,
            "vendor": "Republic Services",
            "property_name": None,
            "invoice_date": None,
            "invoice_number": None,
            "total_amount": None,
            "service_period": None,
            "confidence": 0,
            "flags": [],
            "all_fields": {}
        }

        # Determine property from filename or text
        if "Prosper Lakes" in text or "PROSPER LAKES" in text:
            data["property_name"] = "Orion Prosper Lakes"
        elif "PROSPER" in text and "Prosper, TX" in text:
            if "980 S Coit Rd" in text:
                data["property_name"] = "Orion Prosper (980 S Coit Rd)"
            elif "880 S Coit Rd" in text:
                data["property_name"] = "Orion Prosper Lakes (880 S Coit Rd)"
            else:
                data["property_name"] = "Orion Prosper"
        else:
            self.add_flag(data["flags"], "NEEDS_REVIEW", "property_name",
                        "Property name needs verification from address")

        # Extract invoice number
        inv_match = re.search(r'Invoice\s+Number\s+(\d+-\d+)', text)
        if inv_match:
            data["invoice_number"] = inv_match.group(1)

        # Extract invoice date
        date_match = re.search(r'Invoice\s+Date\s+([A-Za-z]+\s+\d+,\s+\d{4})', text)
        if date_match:
            date_str = date_match.group(1)
            try:
                dt = datetime.strptime(date_str, "%B %d, %Y")
                data["invoice_date"] = dt.strftime("%Y-%m-%d")
            except:
                self.add_flag(data["flags"], "RED_FLAG", "invoice_date",
                            f"Could not parse date: {date_str}")

        # Extract total amount
        amount_match = re.search(r'Total\s+Amount\s+Due\s*\$\s*([\d,]+\.\d{2})', text)
        if not amount_match:
            amount_match = re.search(r'CURRENT\s+INVOICE\s+CHARGES\s*\$\s*([\d,]+\.\d{2})', text)

        if amount_match:
            amount_str = amount_match.group(1).replace(',', '')
            data["total_amount"] = float(amount_str)
        else:
            self.add_flag(data["flags"], "RED_FLAG", "total_amount",
                        "Total amount not found")

        # Extract service details from contract line
        contract_match = re.search(r'Contract:\s+(\d+)', text)
        if contract_match:
            data["all_fields"]["contract_number"] = contract_match.group(1)

        # Extract container details
        compactor_match = re.search(r'(\d+)\s+Waste\s+Compactor\s+(\d+)\s+Cu\s+Yd', text)
        if compactor_match:
            data["all_fields"]["container_count"] = int(compactor_match.group(1))
            data["all_fields"]["container_size"] = f"{compactor_match.group(2)} Cu Yd"
            data["all_fields"]["container_type"] = "Waste Compactor"

        front_load_match = re.search(r'(\d+)\s+Front\s+Load\s+(\d+)\s+Yd', text)
        if front_load_match:
            data["all_fields"]["container_count"] = int(front_load_match.group(1))
            data["all_fields"]["container_size"] = f"{front_load_match.group(2)} Yd"
            data["all_fields"]["container_type"] = "Front Load"

        # Extract pickup frequency
        if "12 Lifts Per Week" in text:
            data["all_fields"]["pickup_frequency"] = "12 lifts/week"
        elif "On Call Service" in text:
            data["all_fields"]["pickup_frequency"] = "On Call"
        else:
            self.add_flag(data["flags"], "NEEDS_REVIEW", "pickup_frequency",
                        "Pickup frequency not stated", "Check contract")

        # Extract pickup service dates
        pickup_match = re.search(r'Pickup\s+Service\s+(\d{2}/\d{2})', text)
        if pickup_match:
            data["service_period"] = pickup_match.group(1)

        # Calculate confidence
        confidence = 0
        if data["invoice_number"]: confidence += 20
        if data["invoice_date"]: confidence += 25
        if data["property_name"]: confidence += 25
        if data["total_amount"]: confidence += 25
        if data["service_period"]: confidence += 5

        data["confidence"] = confidence

        return data

    def extract_waste_management(self, text, filename):
        """Extract data from Waste Management invoices"""
        data = {
            "filename": filename,
            "vendor": "Waste Management",
            "property_name": "Bella Mirage",
            "invoice_date": None,
            "invoice_number": None,
            "total_amount": None,
            "service_period": None,
            "confidence": 0,
            "flags": [],
            "all_fields": {}
        }

        # Extract invoice number
        inv_match = re.search(r'Invoice\s+Number:\s+(\d+)', text)
        if inv_match:
            data["invoice_number"] = inv_match.group(1)

        # Extract invoice date
        date_match = re.search(r'Invoice\s+Date:\s+(\d+/\d+/\d{4})', text)
        if date_match:
            date_str = date_match.group(1)
            try:
                dt = datetime.strptime(date_str, "%m/%d/%Y")
                data["invoice_date"] = dt.strftime("%Y-%m-%d")
            except:
                self.add_flag(data["flags"], "RED_FLAG", "invoice_date",
                            f"Could not parse date: {date_str}")

        # Extract total amount
        amount_match = re.search(r'Amount\s+Due:\s+USD\s+([\d,]+\.\d{2})', text)
        if not amount_match:
            amount_match = re.search(r'Total\s+Amount\s+Due:\s+USD\s+([\d,]+\.\d{2})', text)

        if amount_match:
            amount_str = amount_match.group(1).replace(',', '')
            data["total_amount"] = float(amount_str)
        else:
            self.add_flag(data["flags"], "RED_FLAG", "total_amount",
                        "Total amount not found")

        # Extract service period
        period_match = re.search(r'Service\s+Period:\s+(\d+/\d+/\d{4})\s*-\s*(\d+/\d+/\d{4})', text)
        if period_match:
            data["service_period"] = f"{period_match.group(1)} - {period_match.group(2)}"

        # Extract container details from line items
        yard_matches = re.findall(r'(\d+)\s+Yards\s+Dumpster', text)
        if yard_matches:
            data["all_fields"]["container_sizes"] = [int(y) for y in yard_matches]

        # Extract pickup frequency
        if "Weekly x4" in text:
            data["all_fields"]["pickup_frequency"] = "Weekly (4x/month)"
        elif "Weekly" in text:
            data["all_fields"]["pickup_frequency"] = "Weekly"

        # Count excess pickups
        excess_count = len(re.findall(r'Trash\s+Excess\s+Yards', text))
        if excess_count > 0:
            data["all_fields"]["excess_pickups"] = excess_count
            self.add_flag(data["flags"], "VALIDATE", "excess_charges",
                        f"Invoice includes {excess_count} excess yard charges")

        # Calculate confidence
        confidence = 0
        if data["invoice_number"]: confidence += 20
        if data["invoice_date"]: confidence += 25
        if data["property_name"]: confidence += 25
        if data["total_amount"]: confidence += 25
        if data["service_period"]: confidence += 5

        data["confidence"] = confidence

        return data

    def extract_waste_connections(self, text, filename):
        """Extract data from Waste Connections invoices"""
        data = {
            "filename": filename,
            "vendor": "Waste Connections of Florida",
            "property_name": "Bonita Fountains",
            "invoice_date": None,
            "invoice_number": None,
            "total_amount": None,
            "service_period": None,
            "confidence": 0,
            "flags": [],
            "all_fields": {}
        }

        # Extract invoice number
        inv_match = re.search(r'INVOICE\s+NO\.\s+(\w+)', text)
        if inv_match:
            data["invoice_number"] = inv_match.group(1)

        # Extract statement date
        date_match = re.search(r'STATEMENT\s+DATE\s+(\d{2}/\d{2}/\d{2})', text)
        if date_match:
            date_str = date_match.group(1)
            try:
                dt = datetime.strptime(date_str, "%m/%d/%y")
                data["invoice_date"] = dt.strftime("%Y-%m-%d")
            except:
                self.add_flag(data["flags"], "RED_FLAG", "invoice_date",
                            f"Could not parse date: {date_str}")

        # Extract total amount (PAY THIS AMOUNT or INVOICE TOTAL)
        amount_match = re.search(r'PAY\s+THIS\s+AMOUNT\s+([\d,]+\.\d{2})', text)
        if not amount_match:
            amount_match = re.search(r'Invoice\s+Total\s*\$\s*([\d,]+\.\d{2})', text)

        if amount_match:
            amount_str = amount_match.group(1).replace(',', '')
            data["total_amount"] = float(amount_str)
        else:
            self.add_flag(data["flags"], "RED_FLAG", "total_amount",
                        "Total amount not found")

        # Extract billing period
        period_match = re.search(r'BILLING\s+PERIOD\s+(.*)', text)
        if period_match:
            data["service_period"] = period_match.group(1).strip()

        # Extract container details
        container_match = re.search(r'(\d+\.\d+)\s+(\d+\.\d+)YD\s+C', text)
        if container_match:
            data["all_fields"]["container_size"] = f"{container_match.group(2)} YD"
            data["all_fields"]["container_type"] = "Compactor"

        # Count RO DUMP & RETURN occurrences (on-call pickups)
        pickup_count = len(re.findall(r'RO\s+DUMP\s+&\s+RETURN', text))
        if pickup_count > 0:
            data["all_fields"]["pickup_count_this_period"] = pickup_count
            data["all_fields"]["pickup_frequency"] = "On Call"

        # Calculate confidence
        confidence = 0
        if data["invoice_number"]: confidence += 20
        if data["invoice_date"]: confidence += 25
        if data["property_name"]: confidence += 25
        if data["total_amount"]: confidence += 25
        if data["service_period"]: confidence += 5

        data["confidence"] = confidence

        return data

    def identify_vendor_and_extract(self, text, filename):
        """Identify vendor and extract data accordingly"""
        if "Community Waste Disposal" in text or "CWD" in text:
            return self.extract_community_waste_disposal(text, filename)
        elif "FRONTIER WASTE" in text:
            return self.extract_frontier_waste(text, filename)
        elif "CITY OF MCKINNEY" in text:
            return self.extract_city_of_mckinney(text, filename)
        elif "REPUBLIC SERVICES" in text or "Republic Services" in text:
            return self.extract_republic_services(text, filename)
        elif "Waste Management" in text or "WM" in text:
            return self.extract_waste_management(text, filename)
        elif "WASTE CONNECTIONS" in text:
            return self.extract_waste_connections(text, filename)
        else:
            # Unknown vendor
            data = {
                "filename": filename,
                "vendor": "UNKNOWN",
                "property_name": None,
                "invoice_date": None,
                "invoice_number": None,
                "total_amount": None,
                "service_period": None,
                "confidence": 0,
                "flags": [{
                    "level": "RED_FLAG",
                    "field": "vendor",
                    "message": "Vendor could not be identified",
                    "action": "Manual review required"
                }],
                "all_fields": {}
            }
            return data

    def process_invoice(self, pdf_path):
        """Process a single invoice"""
        filename = pdf_path.name
        print(f"Processing: {filename}")

        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return {
                "filename": filename,
                "vendor": "ERROR",
                "confidence": 0,
                "flags": [{
                    "level": "RED_FLAG",
                    "field": "extraction",
                    "message": "Could not extract text from PDF",
                    "action": "Check PDF integrity"
                }]
            }

        return self.identify_vendor_and_extract(text, filename)

    def process_all_invoices(self):
        """Process all invoices in the directory"""
        invoices_path = self.base_path / "Invoices"
        pdf_files = list(invoices_path.glob("**/*.pdf"))

        print(f"Found {len(pdf_files)} PDF files")
        self.results["total_invoices"] = len(pdf_files)

        for pdf_file in sorted(pdf_files):
            invoice_data = self.process_invoice(pdf_file)
            self.results["invoices"].append(invoice_data)

            # Track properties
            if invoice_data.get("property_name") and invoice_data["property_name"] not in self.results["properties"]:
                self.results["properties"].append(invoice_data["property_name"])

            # Count flags
            for flag in invoice_data.get("flags", []):
                if flag["level"] == "RED_FLAG":
                    self.results["summary"]["red_flags"] += 1
                elif flag["level"] == "NEEDS_REVIEW":
                    self.results["summary"]["yellow_flags"] += 1
                elif flag["level"] == "VALIDATE":
                    self.results["summary"]["green_flags"] += 1

            # Count clean extractions
            if not invoice_data.get("flags"):
                self.results["summary"]["clean_extractions"] += 1

        return self.results

    def save_results(self, output_path):
        """Save results to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResults saved to: {output_path}")


def main():
    base_path = r"C:\Users\Richard\Downloads\Orion Data Part 2"
    output_path = os.path.join(base_path, "extraction_results.json")

    print("=" * 80)
    print("ORION PORTFOLIO INVOICE EXTRACTION")
    print("=" * 80)

    extractor = InvoiceExtractor(base_path)
    results = extractor.process_all_invoices()
    extractor.save_results(output_path)

    # Print summary
    print("\n" + "=" * 80)
    print("EXTRACTION SUMMARY")
    print("=" * 80)
    print(f"Total Invoices Processed: {results['total_invoices']}")
    print(f"Properties Found: {len(results['properties'])}")
    print(f"  - {', '.join(results['properties'])}")
    print(f"\nData Quality Flags:")
    print(f"  [RED] CRITICAL FLAGS:        {results['summary']['red_flags']}")
    print(f"  [YELLOW] NEEDS REVIEW:       {results['summary']['yellow_flags']}")
    print(f"  [GREEN] VALIDATE:            {results['summary']['green_flags']}")
    print(f"  [OK] CLEAN EXTRACTIONS:      {results['summary']['clean_extractions']}")
    print("=" * 80)


if __name__ == "__main__":
    main()
