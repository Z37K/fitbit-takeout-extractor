"""
Basic example of using the Fitbit Takeout Extractor library.
This example shows how to extract basic information about your Fitbit export.
"""
import os
import sys
from datetime import datetime

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from fitbit_extractor import FitbitTakeoutExtractor

def main():
    """Run a basic example of using the FitbitTakeoutExtractor class."""
    print("Fitbit Takeout Extractor - Basic Example")
    print("-" * 50)
    
    # Initialize the extractor
    extractor = FitbitTakeoutExtractor()
    
    # Print information about the Takeout directory
    valid, message = extractor.validate_paths()
    print(f"Path validation: {message}")
    
    if valid:
        print(f"\nTakeout directory: {extractor.takeout_dir}")
        print(f"Fitbit directory: {extractor.fitbit_dir}")
        print(f"Global Export directory: {extractor.global_export_dir}")
        
        # Find different types of files
        file_types = {
            "Heart rate": extractor.find_files("*heart*.json"),
            "Sleep": extractor.find_files("*sleep*.json"),
            "Calories": extractor.find_files("*calories*.json"),
            "Steps": extractor.find_files("*steps*.json"),
            "Activity": extractor.find_files("*activity*.json"),
        }
        
        print("\nAvailable data types:")
        for data_type, files in file_types.items():
            if files:
                print(f"  - {data_type}: {len(files)} files")
                # Print date range if possible
                if files and len(files) >= 2:
                    try:
                        # Extract dates from filenames (common format: type-YYYY-MM-DD.json)
                        first_file = os.path.basename(min(files))
                        last_file = os.path.basename(max(files))
                        print(f"    Range: {first_file} to {last_file}")
                    except:
                        pass
        
        # Example of examining a specific file
        print("\nExamining a sample file:")
        sample_files = file_types["Heart rate"]
        if sample_files:
            sample_file = sample_files[0]
            print(f"  Sample file: {os.path.basename(sample_file)}")
            
            structure = extractor.examine_file_structure(sample_file)
            print(f"  File type: {structure['file_type']}")
            print(f"  Record count: {structure['record_count']}")
            if structure.get('keys'):
                print(f"  Available fields: {', '.join(structure['keys'])}")
    else:
        print("\nCouldn't find valid Fitbit data. Please specify the Takeout directory path.")

if __name__ == "__main__":
    main()
