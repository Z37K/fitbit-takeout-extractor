import os
import glob
import json
import pandas as pd
from datetime import datetime
import time
from typing import Dict, List, Any, Optional, Union, Tuple

class FitbitTakeoutExtractor:
    """
    Main class for extracting Fitbit data from Google Takeout exports.
    
    This extractor handles the common patterns and structures found in Fitbit data
    exported through Google Takeout, making it easier to work with the raw JSON files.
    """
    
    def __init__(self, takeout_dir: str = None):
        """
        Initialize the extractor with the path to the Google Takeout directory.
        
        Args:
            takeout_dir: Path to Google Takeout directory. If None, will try to locate it.
        """
        self.takeout_dir = takeout_dir
        if takeout_dir is None:
            # Try to find the Takeout directory automatically
            self.takeout_dir = self._find_takeout_dir()
            
        self.fitbit_dir = os.path.join(self.takeout_dir, 'Fitbit') if self.takeout_dir else None
        self.global_export_dir = os.path.join(self.fitbit_dir, 'Global Export Data') if self.fitbit_dir else None
        
    def _find_takeout_dir(self) -> Optional[str]:
        """Try to automatically locate the Takeout directory."""
        # Start from current directory and go up to find Takeout
        current_dir = os.path.abspath(os.path.dirname(__file__))
        for _ in range(5):  # Search up to 5 levels up
            parent_dir = os.path.dirname(current_dir)
            takeout_path = os.path.join(parent_dir, 'Takeout')
            if os.path.exists(takeout_path):
                return takeout_path
            current_dir = parent_dir
        return None
    
    def validate_paths(self) -> Tuple[bool, str]:
        """Validate that the required paths exist."""
        if not self.takeout_dir:
            return False, "Takeout directory not found"
        if not os.path.exists(self.takeout_dir):
            return False, f"Takeout directory doesn't exist: {self.takeout_dir}"
        if not os.path.exists(self.fitbit_dir):
            return False, f"Fitbit directory not found in Takeout: {self.fitbit_dir}"
        if not os.path.exists(self.global_export_dir):
            return False, f"Global Export Data directory not found: {self.global_export_dir}"
        return True, "All paths validated successfully"
    
    def find_files(self, pattern: str) -> List[str]:
        """
        Find files matching a glob pattern within the Fitbit export directory.
        
        Args:
            pattern: Glob pattern to match files (e.g., '*heart*.json')
            
        Returns:
            List of file paths matching the pattern
        """
        valid, message = self.validate_paths()
        if not valid:
            print(f"Error: {message}")
            return []
            
        full_pattern = os.path.join(self.global_export_dir, pattern)
        return glob.glob(full_pattern)
    
    def extract_records(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extract records from a Fitbit data file, handling different JSON structures.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            List of record dictionaries
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            # Extract records from different structures Fitbit uses
            records = []
            if isinstance(data, list):
                records = data
            elif isinstance(data, dict):
                for key in data.keys():
                    if isinstance(data[key], list) and len(data[key]) > 0:
                        records = data[key]
                        break
            return records
        except Exception as e:
            print(f"Error extracting records from {os.path.basename(file_path)}: {e}")
            return []
    
    def examine_file_structure(self, file_path: str) -> Dict[str, Any]:
        """
        Examine the structure of a file to understand its format.
        Useful for debugging and understanding new data types.
        
        Args:
            file_path: Path to the JSON file to examine
            
        Returns:
            Dictionary with information about the file structure
        """
        result = {
            "file_type": None,
            "structure": None,
            "sample": None,
            "keys": None,
            "record_count": 0,
        }
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            if isinstance(data, list):
                result["file_type"] = "list"
                result["record_count"] = len(data)
                if data:
                    result["sample"] = data[0]
                    if isinstance(data[0], dict):
                        result["keys"] = list(data[0].keys())
            elif isinstance(data, dict):
                result["file_type"] = "dict"
                result["keys"] = list(data.keys())
                # Find any lists inside the dictionary
                for key, value in data.items():
                    if isinstance(value, list) and value:
                        result["record_count"] = len(value)
                        result["sample"] = value[0]
                        break
            else:
                result["file_type"] = str(type(data))
                
            return result
        except Exception as e:
            print(f"Error examining file {os.path.basename(file_path)}: {e}")
            return {"error": str(e)}
    
    def extract_data_to_dataframe(
        self, 
        file_pattern: str, 
        value_extractor=None, 
        date_fields=None, 
        limit: int = None
    ) -> pd.DataFrame:
        """
        Extract data from files matching a pattern and convert to DataFrame.
        
        Args:
            file_pattern: Glob pattern to match files
            value_extractor: Function to extract values from records
            date_fields: List of field names to check for date values
            limit: Optional limit on number of files to process
            
        Returns:
            Pandas DataFrame with the extracted data
        """
        if date_fields is None:
            date_fields = ['dateTime', 'startTime', 'date', 'timestamp']
            
        files = self.find_files(file_pattern)
        if limit:
            files = files[:limit]
            
        if not files:
            print(f"No files found matching pattern: {file_pattern}")
            return pd.DataFrame()
            
        print(f"Processing {len(files)} files...")
        all_records = []
        
        for file in files:
            records = self.extract_records(file)
            for record in records:
                # Extract and normalize the record
                normalized = {}
                
                # Handle value extraction if provided
                if value_extractor and 'value' in record:
                    normalized['value'] = value_extractor(record['value'])
                else:
                    normalized['value'] = record.get('value')
                    
                # Extract date from various possible fields
                for field in date_fields:
                    if field in record:
                        normalized['date'] = record[field]
                        break
                
                # Copy other fields that might be useful
                for key in record:
                    if key not in ['value'] + date_fields:
                        normalized[key] = record[key]
                        
                all_records.append(normalized)
                
        # Convert to DataFrame
        df = pd.DataFrame(all_records)
        
        # Convert date to proper datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            
        return df