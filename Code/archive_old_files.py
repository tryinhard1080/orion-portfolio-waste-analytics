"""
Archive old and duplicate files to clean up the repository.
Moves files that are no longer needed for active use to Archive folder.
"""

import os
import shutil
from pathlib import Path

BASE_DIR = Path(r"C:\Users\Richard\Downloads\Orion Data Part 2")
ARCHIVE_DIR = BASE_DIR / "Archive"

def archive_root_files():
    """Archive loose files from root directory."""
    print("\n" + "=" * 80)
    print("ARCHIVING ROOT DIRECTORY FILES")
    print("=" * 80)
    
    # Files to archive from root
    root_files_to_archive = [
        # Loose invoice/contract PDFs (now in Properties folders)
        "McKinney trash invoice for Sept 2025.pdf",
        "Trash Invoice  for McCord Park.pdf",
        "Mandarina - Ally Waste.pdf",
        "Mandarina - Waste Management.pdf",
        "Pavilions at Arrowhead - Waste Consolidators Inc Bulk Agreement.pdf",
        "Springs at Alta Mesa - City of Mesa Solid Waste Department.pdf",
        "Springs at Alta Mesa - WCI Bulk Agreement.pdf",
        "Tempe Vista - WCI Bulk Agreement.pdf",
        "Tempe Vista - Waste Management Agreement.pdf",
        
        # Old scripts (now in Code folder or superseded)
        "create_mandarina_dashboard.py",
        "create_mandarina_excel.py",
        "create_summary_report.py",
        "extract_invoices.py",
        "extract_mccord_data.py",
        "generate_mandarina_wastewise.py",
        "generate_mccord_analysis.py",
        "generate_mccord_dashboard.py",
        "generate_orion_prosper_excel.py",
        
        # JSON/data files (now in Extraction_Output)
        "batch_extraction_summary.json",
        "contract_analysis.json",
        "extraction_results.json",
        "mccord_park_ocr_results.json",
        "property_analysis.json",
        "validation_report.json",
        
        # Old documentation (superseded by new structure)
        "EXTRACTION_FIX_COMPLETE.txt",
        "EXTRACTION_SUMMARY_REPORT_20251026_073954.txt",
        "QUICK_REFERENCE.txt",
        "QUICK_START.txt",
        
        # ZIP file
        "rearizona4packtrashanalysis.zip",
    ]
    
    for filename in root_files_to_archive:
        source = BASE_DIR / filename
        if source.exists():
            dest = ARCHIVE_DIR / "Temporary_Files" / filename
            shutil.move(str(source), str(dest))
            print(f"✓ Archived: {filename}")
    
    # Archive the rearizona4packtrashanalysis folder
    arizona_folder = BASE_DIR / "rearizona4packtrashanalysis"
    if arizona_folder.exists():
        dest = ARCHIVE_DIR / "Temporary_Files" / "rearizona4packtrashanalysis"
        shutil.move(str(arizona_folder), str(dest))
        print(f"✓ Archived folder: rearizona4packtrashanalysis/")

def archive_extraction_output():
    """Archive old extraction files from Extraction_Output."""
    print("\n" + "=" * 80)
    print("ARCHIVING OLD EXTRACTION OUTPUT FILES")
    print("=" * 80)
    
    extraction_dir = BASE_DIR / "Extraction_Output"
    
    # Files to archive (old summaries, dashboards, etc.)
    files_to_archive = [
        # Old summary/documentation files
        "ARIZONA_CONSOLIDATION_SUMMARY.md",
        "BEFORE_AFTER_COMPARISON.md",
        "BELLA_MIRAGE_DASHBOARD_README.md",
        "CRITICAL_ACTION_REQUIRED.txt",
        "EXTRACTION_COMPLETE_SUMMARY.md",
        "EXTRACTION_FIX_SUMMARY.md",
        "FILE_CLEANUP_SUMMARY.md",
        "INVOICE_EXTRACTION_VERIFICATION.md",
        "MANDARINA_COMPLETION_SUMMARY.md",
        "McCordParkFL_COMPLETION_SUMMARY.md",
        "PORTFOLIO_COMPLETION_SUMMARY.md",
        "PORTFOLIO_EXECUTIVE_SUMMARY.md",
        "PROPERTY_INVENTORY_20251103_084251.md",
        "PavilionsAtArrowhead_COMPLETION_SUMMARY.md",
        "TCAM_EXTRACTION_SUMMARY.txt",
        "TCAM_QUICK_REFERENCE.md",
        "TEMPE_VISTA_QUICK_REFERENCE.md",
        "VERIFICATION_EXECUTIVE_SUMMARY.md",
        
        # Old analysis summaries
        "BellaMirage_Analysis_Summary.md",
        "BellaMirage_ExecutiveSummary.txt",
        "OrionMcKinney_ExecutiveSummary.md",
        "OrionProsper_DataGapAnalysis.md",
        "OrionProsperLakes_MissionCompletionSummary.md",
        "OrionProsper_MissionCompletionSummary.md",
        "Mandarina_DataGapAnalysis.md",
        "SpringsAtAltaMesa_ExecutiveSummary.md",
        
        # Old data files (superseded by master file)
        "arizona_invoices_consolidated.json",
        "arizona_invoices_summary.csv",
        "bella_mirage_data_summary.txt",
        "bella_mirage_invoice_data.csv",
        "bella_mirage_structure.json",
        "orion_prosper_lakes_summary.json",
        "property_master_data.json",
        
        # Re-extraction JSON files (now in master file)
        "OrionProsperLakes_ReExtraction_20251104_044525.json",
        "OrionProsper_ReExtraction_20251104_044254.json",
        
        # Old Excel files (keeping only COMPREHENSIVE and MASTER_Property_Waste_Data)
        "COMPLETE_All_Properties_FIXED_20251104_044641.xlsx",
        "FINAL_Orion_Portfolio_Master_Extraction.xlsx",
        "MASTER_Orion_Portfolio_Complete_Extraction.xlsx",
        "MASTER_Orion_Portfolio_Complete_Extraction_STANDARDIZED.xlsx",
        "MASTER_Orion_Portfolio_Complete_Extraction_UPDATED.xlsx",
        "arizona_amounts_extracted.xlsx",
        
        # CSV files (data now in master Excel)
        "category_spend.csv",
        "contract_terms.csv",
        "property_master_clean.csv",
        "service_details.csv",
        "service_details_clean.csv",
        "spend_summary.csv",
        "spend_summary_clean.csv",
        "yards_per_door.csv",
        
        # Old Python scripts in Extraction_Output
        "analyze_orion_mckinney.py",
        "analyze_springs_alta_mesa.py",
        "generate_dashboard.py",
        "generate_dashboard_fixed.py",
        "generate_excel.py",
        "generate_orion_mckinney_dashboard.py",
        "generate_orion_mckinney_excel.py",
        "generate_tcam_excel.py",
        "generate_tempe_vista_dashboard.py",
        "run_validation.py",
        "tempe_vista_complete_analysis.py",
    ]
    
    for filename in files_to_archive:
        source = extraction_dir / filename
        if source.exists():
            dest = ARCHIVE_DIR / "Old_Extraction_Files" / filename
            shutil.move(str(source), str(dest))
            print(f"✓ Archived: Extraction_Output/{filename}")

def archive_old_reports():
    """Archive old report folders."""
    print("\n" + "=" * 80)
    print("ARCHIVING OLD REPORT FOLDERS")
    print("=" * 80)
    
    reports_dir = BASE_DIR / "Reports"
    
    # Archive old report folders (reports now in Properties folders)
    folders_to_archive = [
        "Batch_Extraction",
        "Detailed_Analysis",
        "HTML",
    ]
    
    for folder_name in folders_to_archive:
        source = reports_dir / folder_name
        if source.exists():
            dest = ARCHIVE_DIR / "Old_Extraction_Files" / folder_name
            shutil.move(str(source), str(dest))
            print(f"✓ Archived folder: Reports/{folder_name}/")
    
    # Archive Final Reports folder
    final_reports = BASE_DIR / "Final Reports"
    if final_reports.exists():
        dest = ARCHIVE_DIR / "Old_Extraction_Files" / "Final Reports"
        shutil.move(str(final_reports), str(dest))
        print(f"✓ Archived folder: Final Reports/")
    
    # Archive old portfolio data file
    old_portfolio_file = reports_dir / "Orion_Portfolio_Data.xlsx"
    if old_portfolio_file.exists():
        dest = ARCHIVE_DIR / "Old_Extraction_Files" / "Orion_Portfolio_Data.xlsx"
        shutil.move(str(old_portfolio_file), str(dest))
        print(f"✓ Archived: Reports/Orion_Portfolio_Data.xlsx")

def archive_old_invoice_folders():
    """Archive old invoice folders (now in Properties)."""
    print("\n" + "=" * 80)
    print("ARCHIVING OLD INVOICE FOLDERS")
    print("=" * 80)
    
    invoices_dir = BASE_DIR / "Invoices"
    
    # These folders have been copied to Properties, can archive originals
    folders_to_archive = [
        "Orion Prosper Trash Bills",
        "Orion Prosper Lakes Trash Bills",
        "Orion McKinney Trash Bills",
        "Orion McCord Trash Bills",
    ]
    
    for folder_name in folders_to_archive:
        source = invoices_dir / folder_name
        if source.exists():
            dest = ARCHIVE_DIR / "Old_Extraction_Files" / folder_name
            shutil.move(str(source), str(dest))
            print(f"✓ Archived folder: Invoices/{folder_name}/")
    
    # Archive loose invoice files
    invoice_files = [
        "Bella Mirage - Trash Bills.xlsx",
        "TCAM 4.15.25.pdf",
        "TCAM 5.15.25.pdf",
        "TCAM 6.15.25.pdf",
        "TCAM 7.15.25 (1).pdf",
        "TCAM 8.15.25.pdf",
        "TCAM 9.15.25.pdf",
    ]
    
    for filename in invoice_files:
        source = invoices_dir / filename
        if source.exists():
            dest = ARCHIVE_DIR / "Old_Extraction_Files" / filename
            shutil.move(str(source), str(dest))
            print(f"✓ Archived: Invoices/{filename}")
    
    # Archive generic invoice PDFs
    for i in range(1, 11):
        filename = f"invoice ({i}).pdf" if i > 1 else "invoice (1).pdf"
        source = invoices_dir / filename
        if source.exists():
            dest = ARCHIVE_DIR / "Old_Extraction_Files" / filename
            shutil.move(str(source), str(dest))
            print(f"✓ Archived: Invoices/{filename}")

def main():
    """Main execution function."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  ORION PORTFOLIO - ARCHIVE OLD FILES".center(78) + "║")
    print("║" + "  Clean up repository by archiving superseded files".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    print("This script will MOVE (not copy) old files to Archive/ folder:")
    print("  - Loose PDFs and scripts from root directory")
    print("  - Old extraction output files")
    print("  - Old report folders")
    print("  - Old invoice folders (now in Properties/)")
    print()
    print("Files will be preserved in Archive/ for reference.")
    print()
    
    response = input("Proceed with archiving? (yes/no): ").strip().lower()
    if response != 'yes':
        print("\nArchiving cancelled.")
        return
    
    # Execute archiving steps
    archive_root_files()
    archive_extraction_output()
    archive_old_reports()
    archive_old_invoice_folders()
    
    print("\n" + "=" * 80)
    print("ARCHIVING COMPLETE!")
    print("=" * 80)
    print("\nAll old files have been moved to Archive/ folder.")
    print("The repository is now clean and organized.")
    print()

if __name__ == "__main__":
    main()

