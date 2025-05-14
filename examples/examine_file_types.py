from fitbit_extractor import FitbitTakeoutExtractor
import os
import glob

def main():
    """
    Example script to examine different types of files in the Fitbit takeout export.
    This is useful for understanding the structure of different data types.
    """
    print("Fitbit Takeout File Explorer")
    print("-" * 50)

    # Initialize the base extractor
    extractor = FitbitTakeoutExtractor()
    
    # Validate paths
    valid, message = extractor.validate_paths()
    print(f"Path validation: {message}")

    if not valid:
        print("Please check the path to your Takeout directory.")
        return
    
    # Get all JSON files in the export
    files = extractor.find_files('*.json')
    print(f"Found {len(files)} JSON files in the Fitbit export")
    
    # Limit the number of files to examine to avoid too much output
    max_files = 20
    files_to_examine = files[:max_files] if len(files) > max_files else files
    print(f"Examining {len(files_to_examine)} files...")
    
    # Group files by type
    file_types = {}
    
    for file in files_to_examine:
        file_name = os.path.basename(file)
        structure = extractor.examine_file_structure(file)
        
        # Try to categorize by filename
        file_category = file_name.split('_')[0] if '_' in file_name else 'unknown'
        
        if file_category not in file_types:
            file_types[file_category] = []
        
        file_types[file_category].append({
            'filename': file_name,
            'structure': structure
        })
    
    # Print results by category
    print("\nFitbit Export File Categories:")
    print("-" * 50)
    
    for category, files in file_types.items():
        print(f"\n{category.upper()} FILES ({len(files)}):")
        for file_info in files:
            print(f"  - {file_info['filename']}")
            print(f"    Type: {file_info['structure']['file_type']}")
            print(f"    Records: {file_info['structure']['record_count']}")
            if file_info['structure'].get('keys'):
                print(f"    Keys: {', '.join(file_info['structure'].get('keys', []))}")
            print()

if __name__ == "__main__":
    main()
