"""
Flatten Property Folders - Move all files from subfolders to main property folder

This script:
1. Moves all files from Invoices/, Reports/, Contracts/, Documentation/ subfolders
2. Places them directly in the property folder
3. Removes empty subfolders
4. Keeps README.md in the property folder

Goal: Single folder per property with all files directly accessible (no clicking into subfolders)
"""

import os
import shutil
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent
PROPERTIES_DIR = BASE_DIR / "Properties"

# List of all 10 properties
PROPERTIES = [
    "Orion_Prosper",
    "Orion_Prosper_Lakes",
    "Orion_McKinney",
    "McCord_Park_FL",
    "The_Club_at_Millenia",
    "Bella_Mirage",
    "Mandarina",
    "Pavilions_at_Arrowhead",
    "Springs_at_Alta_Mesa",
    "Tempe_Vista"
]

def flatten_property_folder(property_name):
    """Flatten a single property folder by moving all files to root"""
    property_path = PROPERTIES_DIR / property_name
    
    if not property_path.exists():
        print(f"⚠️  Property folder not found: {property_name}")
        return
    
    print(f"\n📁 Processing: {property_name}")
    print("=" * 60)
    
    files_moved = 0
    folders_removed = 0
    
    # Subfolders to flatten
    subfolders = ["Invoices", "Reports", "Contracts", "Documentation"]
    
    for subfolder_name in subfolders:
        subfolder_path = property_path / subfolder_name
        
        if not subfolder_path.exists():
            continue
        
        # Get all files recursively from this subfolder
        all_files = list(subfolder_path.rglob("*"))
        files_only = [f for f in all_files if f.is_file()]
        
        if files_only:
            print(f"\n  📂 {subfolder_name}/ - Found {len(files_only)} files")
        
        # Move each file to property root
        for file_path in files_only:
            # Get relative path from subfolder
            relative_path = file_path.relative_to(subfolder_path)
            
            # Create new filename (flatten nested structure)
            if len(relative_path.parts) > 1:
                # File is in nested folder - flatten the name
                new_filename = "_".join(relative_path.parts)
            else:
                # File is directly in subfolder
                new_filename = file_path.name
            
            # Destination path
            dest_path = property_path / new_filename
            
            # Handle duplicate filenames
            counter = 1
            original_dest = dest_path
            while dest_path.exists():
                stem = original_dest.stem
                suffix = original_dest.suffix
                dest_path = property_path / f"{stem}_{counter}{suffix}"
                counter += 1
            
            # Move the file
            try:
                shutil.move(str(file_path), str(dest_path))
                print(f"    ✓ Moved: {file_path.name} → {dest_path.name}")
                files_moved += 1
            except Exception as e:
                print(f"    ✗ Error moving {file_path.name}: {e}")
        
        # Remove the now-empty subfolder
        try:
            shutil.rmtree(subfolder_path)
            print(f"  🗑️  Removed empty folder: {subfolder_name}/")
            folders_removed += 1
        except Exception as e:
            print(f"  ⚠️  Could not remove {subfolder_name}/: {e}")
    
    print(f"\n  ✅ Summary: {files_moved} files moved, {folders_removed} folders removed")
    
    return files_moved, folders_removed

def main():
    """Flatten all property folders"""
    print("=" * 60)
    print("FLATTENING PROPERTY FOLDERS")
    print("=" * 60)
    print("\nMoving all files from subfolders to property root...")
    print("This will make all files directly accessible in each property folder.\n")
    
    total_files = 0
    total_folders = 0
    
    for property_name in PROPERTIES:
        files, folders = flatten_property_folder(property_name)
        total_files += files
        total_folders += folders
    
    print("\n" + "=" * 60)
    print("FLATTENING COMPLETE!")
    print("=" * 60)
    print(f"\n📊 Total Statistics:")
    print(f"   • Properties processed: {len(PROPERTIES)}")
    print(f"   • Files moved: {total_files}")
    print(f"   • Folders removed: {total_folders}")
    print(f"\n✅ All property files are now directly accessible!")
    print(f"   No more clicking into subfolders - everything is in one place.\n")

if __name__ == "__main__":
    main()

