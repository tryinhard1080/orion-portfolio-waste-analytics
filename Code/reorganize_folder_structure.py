"""
Reorganize Orion Portfolio folder structure into property-centric organization.

Goal: Create clean, property-focused structure with:
- One folder per property containing all related files
- Portfolio-level folder for master data and portfolio reports
- Archive folder for old/duplicate files
- Clean root directory with only essential files
"""

import os
import shutil
from pathlib import Path

# Base directory
BASE_DIR = Path(r"C:\Users\Richard\Downloads\Orion Data Part 2")

# Property list (10 properties)
PROPERTIES = {
    # Texas Properties (6)
    "Orion_Prosper": {"state": "TX", "units": 312},
    "Orion_Prosper_Lakes": {"state": "TX", "units": 308},
    "Orion_McKinney": {"state": "TX", "units": 453},
    "McCord_Park_FL": {"state": "FL", "units": 416},
    "The_Club_at_Millenia": {"state": "FL", "units": 560},
    "Bella_Mirage": {"state": "AZ", "units": 715},
    # Arizona Properties (4)
    "Mandarina": {"state": "AZ", "units": 180},
    "Pavilions_at_Arrowhead": {"state": "AZ", "units": None},  # TBD
    "Springs_at_Alta_Mesa": {"state": "AZ", "units": 200},
    "Tempe_Vista": {"state": "AZ", "units": 150},  # Estimated
}

def create_folder_structure():
    """Create the new property-centric folder structure."""
    print("=" * 80)
    print("CREATING PROPERTY-CENTRIC FOLDER STRUCTURE")
    print("=" * 80)
    
    # Create Properties folder
    properties_dir = BASE_DIR / "Properties"
    properties_dir.mkdir(exist_ok=True)
    print(f"\n✓ Created: Properties/")
    
    # Create folder for each property
    for prop_name, prop_info in PROPERTIES.items():
        prop_dir = properties_dir / prop_name
        prop_dir.mkdir(exist_ok=True)
        
        # Create subfolders
        (prop_dir / "Invoices").mkdir(exist_ok=True)
        (prop_dir / "Reports").mkdir(exist_ok=True)
        (prop_dir / "Contracts").mkdir(exist_ok=True)
        (prop_dir / "Documentation").mkdir(exist_ok=True)
        
        print(f"✓ Created: Properties/{prop_name}/ (with 4 subfolders)")
    
    # Create Portfolio_Reports folder
    portfolio_dir = BASE_DIR / "Portfolio_Reports"
    portfolio_dir.mkdir(exist_ok=True)
    print(f"\n✓ Created: Portfolio_Reports/")
    
    # Create Archive folder
    archive_dir = BASE_DIR / "Archive"
    archive_dir.mkdir(exist_ok=True)
    (archive_dir / "Old_Scripts").mkdir(exist_ok=True)
    (archive_dir / "Old_Extraction_Files").mkdir(exist_ok=True)
    (archive_dir / "Temporary_Files").mkdir(exist_ok=True)
    print(f"✓ Created: Archive/ (with 3 subfolders)")
    
    print("\n" + "=" * 80)
    print("FOLDER STRUCTURE CREATED SUCCESSFULLY")
    print("=" * 80)

def move_invoices():
    """Move invoice files to property folders."""
    print("\n" + "=" * 80)
    print("MOVING INVOICES TO PROPERTY FOLDERS")
    print("=" * 80)
    
    properties_dir = BASE_DIR / "Properties"
    invoices_dir = BASE_DIR / "Invoices"
    
    # Mapping of invoice folders/files to properties
    invoice_mapping = {
        "Orion Prosper Trash Bills": "Orion_Prosper",
        "Orion Prosper Lakes Trash Bills": "Orion_Prosper_Lakes",
        "Orion McKinney Trash Bills": "Orion_McKinney",
        "Orion McCord Trash Bills": "McCord_Park_FL",
        "Bella Mirage - Trash Bills.xlsx": "Bella_Mirage",
        "TCAM 4.15.25.pdf": "The_Club_at_Millenia",
        "TCAM 5.15.25.pdf": "The_Club_at_Millenia",
        "TCAM 6.15.25.pdf": "The_Club_at_Millenia",
        "TCAM 7.15.25 (1).pdf": "The_Club_at_Millenia",
        "TCAM 8.15.25.pdf": "The_Club_at_Millenia",
        "TCAM 9.15.25.pdf": "The_Club_at_Millenia",
    }
    
    # Move invoice folders and files
    for item_name, prop_name in invoice_mapping.items():
        source = invoices_dir / item_name
        if source.exists():
            dest = properties_dir / prop_name / "Invoices" / item_name
            if source.is_dir():
                shutil.copytree(source, dest, dirs_exist_ok=True)
                print(f"✓ Copied folder: {item_name} → Properties/{prop_name}/Invoices/")
            else:
                shutil.copy2(source, dest)
                print(f"✓ Copied file: {item_name} → Properties/{prop_name}/Invoices/")
    
    # Move loose invoice PDFs from root
    root_invoices = {
        "McKinney trash invoice for Sept 2025.pdf": "Orion_McKinney",
        "Trash Invoice  for McCord Park.pdf": "McCord_Park_FL",
        "Mandarina - Ally Waste.pdf": "Mandarina",
        "Mandarina - Waste Management.pdf": "Mandarina",
    }
    
    for filename, prop_name in root_invoices.items():
        source = BASE_DIR / filename
        if source.exists():
            dest = properties_dir / prop_name / "Invoices" / filename
            shutil.copy2(source, dest)
            print(f"✓ Copied: {filename} → Properties/{prop_name}/Invoices/")
    
    # Move Arizona invoice Excel files
    arizona_dir = BASE_DIR / "rearizona4packtrashanalysis"
    if arizona_dir.exists():
        arizona_mapping = {
            "Mandarina - Ally Waste.xlsx": "Mandarina",
            "Mandarina - Waste Management Compactor.xlsx": "Mandarina",
            "Mandarina - Waste Management Hauling.xlsx": "Mandarina",
            "Pavilions - Ally Waste.xlsx": "Pavilions_at_Arrowhead",
            "Pavilions - City of Glendale Trash.xlsx": "Pavilions_at_Arrowhead",
            "Springs at Alta Mesa - Ally Waste.xlsx": "Springs_at_Alta_Mesa",
            "Springs at Alta Mesa - City of Mesa Trash.xlsx": "Springs_at_Alta_Mesa",
            "Tempe Vista - Ally Waste.xlsx": "Tempe_Vista",
            "Tempe Vista - Waste Management Hauling.xlsx": "Tempe_Vista",
        }
        
        for filename, prop_name in arizona_mapping.items():
            source = arizona_dir / filename
            if source.exists():
                dest = properties_dir / prop_name / "Invoices" / filename
                shutil.copy2(source, dest)
                print(f"✓ Copied: {filename} → Properties/{prop_name}/Invoices/")
    
    # Move generic invoice PDFs to TCAM (based on file pattern)
    for i in range(1, 11):
        filename = f"invoice ({i}).pdf" if i > 1 else "invoice (1).pdf"
        source = invoices_dir / filename
        if source.exists():
            dest = properties_dir / "The_Club_at_Millenia" / "Invoices" / filename
            shutil.copy2(source, dest)
            print(f"✓ Copied: {filename} → Properties/The_Club_at_Millenia/Invoices/")

def move_contracts():
    """Move contract files to property folders."""
    print("\n" + "=" * 80)
    print("MOVING CONTRACTS TO PROPERTY FOLDERS")
    print("=" * 80)
    
    properties_dir = BASE_DIR / "Properties"
    contracts_dir = BASE_DIR / "Contracts"
    
    # Contract mapping
    contract_mapping = {
        "131941 The club at millenia_05252021113150 (2) (1).pdf": "The_Club_at_Millenia",
        "Bella Mirage Waste Mgmt Contract 4.20 for 3 yrs.pdf": "Bella_Mirage",
        "Little Elm 01-01-25 contract.pdf": "Orion_Prosper_Lakes",
        "McKinney Frontier Trash  Agreement.pdf": "Orion_McKinney",
    }
    
    # Move contracts from Contracts folder
    for filename, prop_name in contract_mapping.items():
        source = contracts_dir / filename
        if source.exists():
            dest = properties_dir / prop_name / "Contracts" / filename
            shutil.copy2(source, dest)
            print(f"✓ Copied: {filename} → Properties/{prop_name}/Contracts/")
    
    # Move contracts from root directory
    root_contracts = {
        "Pavilions at Arrowhead - Waste Consolidators Inc Bulk Agreement.pdf": "Pavilions_at_Arrowhead",
        "Springs at Alta Mesa - City of Mesa Solid Waste Department.pdf": "Springs_at_Alta_Mesa",
        "Springs at Alta Mesa - WCI Bulk Agreement.pdf": "Springs_at_Alta_Mesa",
        "Tempe Vista - WCI Bulk Agreement.pdf": "Tempe_Vista",
        "Tempe Vista - Waste Management Agreement.pdf": "Tempe_Vista",
    }
    
    for filename, prop_name in root_contracts.items():
        source = BASE_DIR / filename
        if source.exists():
            dest = properties_dir / prop_name / "Contracts" / filename
            shutil.copy2(source, dest)
            print(f"✓ Copied: {filename} → Properties/{prop_name}/Contracts/")

def move_reports():
    """Move property-specific reports to property folders."""
    print("\n" + "=" * 80)
    print("MOVING REPORTS TO PROPERTY FOLDERS")
    print("=" * 80)
    
    properties_dir = BASE_DIR / "Properties"
    extraction_dir = BASE_DIR / "Extraction_Output"
    
    # Property name mapping (file prefix → property folder)
    report_mapping = {
        "BellaMirage": "Bella_Mirage",
        "McCordParkFL": "McCord_Park_FL",
        "OrionMcKinney": "Orion_McKinney",
        "OrionProsper_": "Orion_Prosper",  # Note: underscore to avoid matching OrionProsperLakes
        "OrionProsperLakes": "Orion_Prosper_Lakes",
        "Mandarina": "Mandarina",
        "PavilionsAtArrowhead": "Pavilions_at_Arrowhead",
        "SpringsAtAltaMesa": "Springs_at_Alta_Mesa",
        "TempeVista": "Tempe_Vista",
        "TheClubAtMillenia": "The_Club_at_Millenia",
    }
    
    # Move validated Excel reports and dashboards
    for file in extraction_dir.glob("*"):
        if file.is_file():
            for prefix, prop_name in report_mapping.items():
                if file.name.startswith(prefix):
                    # Determine if it's a report file
                    if any(ext in file.suffix for ext in ['.xlsx', '.html', '.txt', '.md', '.json']):
                        if 'WasteAnalysis' in file.name or 'Dashboard' in file.name or 'ValidationReport' in file.name or 'Summary' in file.name:
                            dest = properties_dir / prop_name / "Reports" / file.name
                            shutil.copy2(file, dest)
                            print(f"✓ Copied: {file.name} → Properties/{prop_name}/Reports/")
                            break

def move_master_file():
    """Move master data file to Portfolio_Reports folder."""
    print("\n" + "=" * 80)
    print("MOVING MASTER DATA FILE")
    print("=" * 80)
    
    portfolio_dir = BASE_DIR / "Portfolio_Reports"
    extraction_dir = BASE_DIR / "Extraction_Output"
    
    # Copy the comprehensive master file
    source = extraction_dir / "COMPREHENSIVE_Orion_Portfolio_Waste_Analysis.xlsx"
    dest = portfolio_dir / "MASTER_Portfolio_Complete_Data.xlsx"
    
    if source.exists():
        shutil.copy2(source, dest)
        print(f"✓ Copied and renamed: COMPREHENSIVE_Orion_Portfolio_Waste_Analysis.xlsx")
        print(f"  → Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx")
        print(f"\n  This is the SINGLE SOURCE OF TRUTH for all property data.")
        print(f"  Contains: All 10 properties with complete invoice extraction data")
    else:
        print(f"✗ ERROR: Master file not found at {source}")

def main():
    """Main execution function."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  ORION PORTFOLIO - FOLDER REORGANIZATION SCRIPT".center(78) + "║")
    print("║" + "  Property-Centric Structure".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Confirm before proceeding
    print("This script will:")
    print("  1. Create Properties/ folder with 10 property subfolders")
    print("  2. Create Portfolio_Reports/ folder for master data")
    print("  3. Create Archive/ folder for old files")
    print("  4. COPY (not move) all files to new structure")
    print("  5. Original files will remain in place")
    print()
    
    response = input("Proceed with reorganization? (yes/no): ").strip().lower()
    if response != 'yes':
        print("\nReorganization cancelled.")
        return
    
    # Execute reorganization steps
    create_folder_structure()
    move_invoices()
    move_contracts()
    move_reports()
    move_master_file()
    
    print("\n" + "=" * 80)
    print("REORGANIZATION COMPLETE!")
    print("=" * 80)
    print("\nNext steps:")
    print("  1. Review the new Properties/ folder structure")
    print("  2. Verify all files copied correctly")
    print("  3. Run cleanup script to archive old files from root/Extraction_Output")
    print("  4. Update CLAUDE.md with new folder structure")
    print("  5. Commit to GitHub")
    print()

if __name__ == "__main__":
    main()

