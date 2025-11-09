"""
Create Property Reference Sheet - Master property information with file counts

This script creates a comprehensive Excel file with:
- Property name, address, location
- Unit count and property type
- Vendor and service type
- File counts (PDF invoices, Excel files, contracts)
- Extracted records count from master file
- Status and notes
"""

import pandas as pd
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent
PROPERTIES_DIR = BASE_DIR / "Properties"
MASTER_FILE = BASE_DIR / "Portfolio_Reports" / "MASTER_Portfolio_Complete_Data.xlsx"

# Property information with addresses
PROPERTY_INFO = {
    "Orion_Prosper": {
        "Property Name": "Orion Prosper",
        "Address": "TBD",  # Need to verify
        "City": "Prosper",
        "State": "TX",
        "Zip": "",
        "Units": 312,
        "Property Type": "Garden-Style Apartments",
        "Vendor": "Republic Services",
        "Service Type": "FEL Dumpsters",
    },
    "Orion_Prosper_Lakes": {
        "Property Name": "Orion Prosper Lakes",
        "Address": "TBD",  # Need to verify
        "City": "Little Elm",
        "State": "TX",
        "Zip": "",
        "Units": 308,
        "Property Type": "Garden-Style Apartments",
        "Vendor": "Republic Services",
        "Service Type": "Compactor",
    },
    "Orion_McKinney": {
        "Property Name": "Orion McKinney",
        "Address": "TBD",  # Need to verify
        "City": "McKinney",
        "State": "TX",
        "Zip": "",
        "Units": 453,
        "Property Type": "Garden-Style Apartments",
        "Vendor": "Frontier Waste",
        "Service Type": "FEL Dumpsters",
    },
    "McCord_Park_FL": {
        "Property Name": "McCord Park FL",
        "Address": "2050 FM 423",
        "City": "Little Elm",
        "State": "TX",
        "Zip": "75068",
        "Units": 416,
        "Property Type": "Garden-Style Apartments",
        "Vendor": "Community Waste Disposal",
        "Service Type": "Dumpster",
    },
    "The_Club_at_Millenia": {
        "Property Name": "The Club at Millenia",
        "Address": "TBD",  # Need to verify
        "City": "Orlando",
        "State": "FL",
        "Zip": "",
        "Units": 560,
        "Property Type": "Garden-Style Apartments",
        "Vendor": "Waste Connections",
        "Service Type": "Compactor",
    },
    "Bella_Mirage": {
        "Property Name": "Bella Mirage",
        "Address": "TBD",  # Need to verify
        "City": "Avondale",
        "State": "AZ",
        "Zip": "",
        "Units": 715,
        "Property Type": "Garden-Style Apartments",
        "Vendor": "Waste Management",
        "Service Type": "Dumpster",
    },
    "Mandarina": {
        "Property Name": "Mandarina",
        "Address": "TBD",  # Need to verify
        "City": "Phoenix",
        "State": "AZ",
        "Zip": "",
        "Units": 180,
        "Property Type": "Garden-Style Apartments",
        "Vendor": "WM + Ally Waste",
        "Service Type": "Compactor + Bulk",
    },
    "Pavilions_at_Arrowhead": {
        "Property Name": "Pavilions at Arrowhead",
        "Address": "TBD",  # Need to verify
        "City": "Glendale",
        "State": "AZ",
        "Zip": "",
        "Units": None,  # TBD
        "Property Type": "Garden-Style Apartments",
        "Vendor": "City + Ally Waste",
        "Service Type": "Mixed",
    },
    "Springs_at_Alta_Mesa": {
        "Property Name": "Springs at Alta Mesa",
        "Address": "TBD",  # Need to verify
        "City": "Mesa",
        "State": "AZ",
        "Zip": "",
        "Units": 200,
        "Property Type": "Garden-Style Apartments",
        "Vendor": "City + Ally Waste",
        "Service Type": "Dumpster + Bulk",
    },
    "Tempe_Vista": {
        "Property Name": "Tempe Vista",
        "Address": "TBD",  # Need to verify
        "City": "Tempe",
        "State": "AZ",
        "Zip": "",
        "Units": 150,  # Estimated
        "Property Type": "Garden-Style Apartments",
        "Vendor": "WM + Ally Waste",
        "Service Type": "Mixed",
    },
}

def count_files_in_property(property_folder_name):
    """Count files in a property folder"""
    property_path = PROPERTIES_DIR / property_folder_name
    
    if not property_path.exists():
        return {"pdf_invoices": 0, "excel_files": 0, "contracts": 0}
    
    # Count PDF invoices (exclude contracts)
    pdfs = list(property_path.glob("*.pdf"))
    invoice_pdfs = [p for p in pdfs if "contract" not in p.name.lower() and "agreement" not in p.name.lower()]
    
    # Count contracts
    contracts = [p for p in pdfs if "contract" in p.name.lower() or "agreement" in p.name.lower()]
    
    # Count Excel files (exclude analysis/report files)
    excel_files = list(property_path.glob("*.xlsx"))
    invoice_excel = [e for e in excel_files if "analysis" not in e.name.lower() and "validated" not in e.name.lower()]
    
    return {
        "pdf_invoices": len(invoice_pdfs),
        "excel_files": len(invoice_excel),
        "contracts": len(contracts)
    }

def get_extracted_records_count(property_name):
    """Get count of extracted records from master file"""
    try:
        xl = pd.ExcelFile(MASTER_FILE)
        
        # Find the property tab
        if property_name in xl.sheet_names:
            df = pd.read_excel(xl, property_name)
            return len(df)
        else:
            return 0
    except Exception as e:
        print(f"Error reading master file for {property_name}: {e}")
        return 0

def create_property_reference_sheet():
    """Create comprehensive property reference Excel file"""
    
    print("=" * 80)
    print("CREATING PROPERTY REFERENCE SHEET")
    print("=" * 80)
    print()
    
    # Build data rows
    data_rows = []
    
    for folder_name, info in PROPERTY_INFO.items():
        # Get file counts
        file_counts = count_files_in_property(folder_name)
        
        # Get extracted records count
        records_count = get_extracted_records_count(info["Property Name"])
        
        # Build row
        row = {
            "Property Name": info["Property Name"],
            "Address": info["Address"],
            "City": info["City"],
            "State": info["State"],
            "Zip Code": info["Zip"],
            "Units": info["Units"],
            "Property Type": info["Property Type"],
            "Vendor": info["Vendor"],
            "Service Type": info["Service Type"],
            "PDF Invoices": file_counts["pdf_invoices"],
            "Excel Files": file_counts["excel_files"],
            "Contracts": file_counts["contracts"],
            "Extracted Records": records_count,
            "Status": "Complete" if records_count > 0 else "Pending",
            "Notes": ""
        }
        
        # Add notes for properties needing attention
        if info["Units"] is None:
            row["Notes"] = "Unit count TBD"
        elif info["Address"] == "TBD":
            row["Notes"] = "Address needs verification"
        
        data_rows.append(row)
        
        print(f"✓ {info['Property Name']:30} - {file_counts['pdf_invoices']} PDFs, {file_counts['excel_files']} Excel, {records_count} records")
    
    # Create DataFrame
    df = pd.DataFrame(data_rows)
    
    # Sort by state, then city
    df = df.sort_values(["State", "City"])
    
    # Create Excel file with formatting
    output_file = BASE_DIR / "Portfolio_Reports" / "Property_Reference_Sheet.xlsx"
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Property Reference', index=False)
        
        # Get the worksheet
        worksheet = writer.sheets['Property Reference']
        
        # Set column widths
        column_widths = {
            'A': 30,  # Property Name
            'B': 30,  # Address
            'C': 15,  # City
            'D': 8,   # State
            'E': 10,  # Zip Code
            'F': 8,   # Units
            'G': 25,  # Property Type
            'H': 25,  # Vendor
            'I': 20,  # Service Type
            'J': 12,  # PDF Invoices
            'K': 12,  # Excel Files
            'L': 12,  # Contracts
            'M': 15,  # Extracted Records
            'N': 12,  # Status
            'O': 40,  # Notes
        }
        
        for col, width in column_widths.items():
            worksheet.column_dimensions[col].width = width
    
    print()
    print("=" * 80)
    print("PROPERTY REFERENCE SHEET CREATED!")
    print("=" * 80)
    print(f"\nFile saved: {output_file}")
    print(f"Total properties: {len(data_rows)}")
    print(f"Total units: {df['Units'].sum()}")
    print(f"Total extracted records: {df['Extracted Records'].sum()}")
    print()

if __name__ == "__main__":
    create_property_reference_sheet()

