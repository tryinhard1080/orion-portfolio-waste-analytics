"""
Create README.md files for each property folder.
Simple, fact-based documentation of what's in each folder.
"""

from pathlib import Path

BASE_DIR = Path(r"C:\Users\Richard\Downloads\Orion Data Part 2")
PROPERTIES_DIR = BASE_DIR / "Properties"

# Property information
PROPERTIES = {
    "Orion_Prosper": {
        "name": "Orion Prosper",
        "location": "Prosper, TX",
        "units": 312,
        "vendor": "Republic Services",
        "service_type": "FEL Dumpsters",
    },
    "Orion_Prosper_Lakes": {
        "name": "Orion Prosper Lakes",
        "location": "Prosper, TX (Little Elm)",
        "units": 308,
        "vendor": "Republic Services",
        "service_type": "Compactor",
    },
    "Orion_McKinney": {
        "name": "Orion McKinney",
        "location": "McKinney, TX",
        "units": 453,
        "vendor": "Frontier Waste",
        "service_type": "FEL Dumpsters",
    },
    "McCord_Park_FL": {
        "name": "McCord Park FL",
        "location": "Florida",
        "units": 416,
        "vendor": "Community Waste Disposal",
        "service_type": "Dumpster",
    },
    "The_Club_at_Millenia": {
        "name": "The Club at Millenia",
        "location": "Orlando, FL",
        "units": 560,
        "vendor": "Waste Connections",
        "service_type": "Compactor",
    },
    "Bella_Mirage": {
        "name": "Bella Mirage",
        "location": "Phoenix, AZ",
        "units": 715,
        "vendor": "Waste Management",
        "service_type": "Dumpster",
    },
    "Mandarina": {
        "name": "Mandarina",
        "location": "Phoenix, AZ",
        "units": 180,
        "vendor": "Waste Management + Ally Waste",
        "service_type": "Compactor + Bulk",
    },
    "Pavilions_at_Arrowhead": {
        "name": "Pavilions at Arrowhead",
        "location": "Glendale, AZ",
        "units": "TBD",
        "vendor": "City of Glendale + Ally Waste",
        "service_type": "Mixed",
    },
    "Springs_at_Alta_Mesa": {
        "name": "Springs at Alta Mesa",
        "location": "Mesa, AZ",
        "units": 200,
        "vendor": "City of Mesa + Ally Waste",
        "service_type": "Dumpster + Bulk",
    },
    "Tempe_Vista": {
        "name": "Tempe Vista",
        "location": "Tempe, AZ",
        "units": "150 (estimated)",
        "vendor": "Waste Management + Ally Waste",
        "service_type": "Mixed",
    },
}

def create_readme(prop_folder, prop_info):
    """Create README.md for a property folder."""
    
    readme_content = f"""# {prop_info['name']}

## Property Information

- **Location:** {prop_info['location']}
- **Units:** {prop_info['units']}
- **Vendor:** {prop_info['vendor']}
- **Service Type:** {prop_info['service_type']}

---

## Folder Contents

### 📄 Invoices/
Contains all invoice files for this property:
- PDF invoices from vendor(s)
- Excel files with extracted invoice data
- Organized by service period

### 📊 Reports/
Contains generated analysis reports:
- **WasteAnalysis_Validated.xlsx** - Complete waste analysis workbook
- **Dashboard.html** - Interactive HTML dashboard
- **ValidationReport.txt** - Data quality validation results
- **ExecutiveSummary.md** - Summary of findings (if available)

### 📋 Contracts/
Contains service contracts and agreements:
- Current waste management service contracts
- Vendor agreements
- Contract terms and pricing schedules

### 📝 Documentation/
Property-specific documentation:
- Service specifications
- Special notes or requirements
- Historical context

---

## Data Source

All invoice data for this property is extracted and consolidated in:

**Portfolio Master File:**
```
Portfolio_Reports/MASTER_Portfolio_Complete_Data.xlsx
```

This master file contains:
- Complete invoice extraction data for all 10 properties
- Individual property tabs with detailed invoice line items
- Portfolio summary and analysis tabs

---

## How to Generate Fresh Reports

To generate updated reports for this property using the latest data:

1. **Ensure data is current** in the master file
2. **Run report generation** using your Claude skill
3. **Reports will be saved** to this property's `Reports/` folder

The reporting system uses:
- Real data from invoices and contracts
- Fact-based analysis only
- No projections or optimization recommendations
- Validated calculations and benchmarks

---

## Notes

- All data extracted from actual invoices and contracts
- Reports focus on performance insights based on real spend data
- No hallucinated data or unrealistic projections
- Benchmarks based on industry standards for garden-style apartments

---

**Last Updated:** {Path(__file__).stat().st_mtime if Path(__file__).exists() else 'N/A'}
"""
    
    readme_path = prop_folder / "README.md"
    readme_path.write_text(readme_content, encoding='utf-8')
    print(f"✓ Created: {prop_folder.name}/README.md")

def main():
    """Create README files for all properties."""
    print("=" * 80)
    print("CREATING PROPERTY README FILES")
    print("=" * 80)
    print()
    
    for folder_name, prop_info in PROPERTIES.items():
        prop_folder = PROPERTIES_DIR / folder_name
        if prop_folder.exists():
            create_readme(prop_folder, prop_info)
        else:
            print(f"✗ Folder not found: {folder_name}")
    
    print()
    print("=" * 80)
    print("README FILES CREATED SUCCESSFULLY")
    print("=" * 80)

if __name__ == "__main__":
    main()

