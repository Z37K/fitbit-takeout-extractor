"""
Calories extractor for Fitbit Takeout data.
This module extracts and processes calories data from Fitbit exports.
"""

import os
import glob
import json
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List, Optional, Union

# Import core extractor class if available, else create a simple version
try:
    from ..core import FitbitTakeoutExtractor
    has_core = True
except ImportError:
    has_core = False
    # Define a minimal version for standalone use
    class FitbitTakeoutExtractor:
        def __init__(self, takeout_dir=None):
            self.takeout_dir = takeout_dir
            if takeout_dir:
                self.fitbit_dir = os.path.join(takeout_dir, 'Fitbit')
                self.global_export_dir = os.path.join(self.fitbit_dir, 'Global Export Data')
            else:
                self.fitbit_dir = None
                self.global_export_dir = None

        def find_files(self, pattern):
            if not self.global_export_dir or not os.path.exists(self.global_export_dir):
                return []
            return glob.glob(os.path.join(self.global_export_dir, pattern))
            
        def extract_records(self, file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    for key in data.keys():
                        if isinstance(data[key], list) and len(data[key]) > 0:
                            return data[key]
                return []
            except Exception as e:
                print(f"Error reading {os.path.basename(file_path)}: {e}")
                return []

class CaloriesExtractor:
    """
    Specialized extractor for Fitbit calories data from Google Takeout.
    
    This extractor handles calories data which tracks estimated calories burned
    throughout the day.
    """
    
    def __init__(self, takeout_dir=None):
        """
        Initialize the calories extractor.
        
        Args:
            takeout_dir: Path to Google Takeout directory. If None, will try to locate it.
        """
        self.base_extractor = FitbitTakeoutExtractor(takeout_dir)
    
    def extract_all_calories_data(self, limit=None):
        """
        Extract all calories data from the Fitbit export.
        
        Args:
            limit: Optional limit on number of files to process
            
        Returns:
            DataFrame with calories data
        """
        # Find calories files
        files = self.base_extractor.find_files('*calories*.json')
        if limit:
            files = files[:limit]
            
        if not files:
            print("No calories files found.")
            return pd.DataFrame(columns=['datetime', 'calories'])
        
        print(f"Processing {len(files)} calories files...")
        all_records = []
        
        for file in files:
            records = self.base_extractor.extract_records(file)
            for record in records:
                if 'dateTime' in record and 'value' in record:
                    try:
                        all_records.append({
                            'datetime': record['dateTime'],
                            'calories': float(record['value'])
                        })
                    except (ValueError, TypeError):
                        pass
        
        # Convert to DataFrame
        df = pd.DataFrame(all_records)
        if df.empty:
            return df
            
        # Convert datetime to proper datetime
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        
        # Drop invalid values
        df = df.dropna(subset=['datetime', 'calories'])
        
        # Sort by datetime
        df = df.sort_values('datetime')
        
        return df
    
    def get_daily_total(self, df=None):
        """
        Calculate daily total calories burned.
        
        Args:
            df: Optional DataFrame of calories data. If None, extracts the data.
            
        Returns:
            DataFrame with daily totals
        """
        if df is None:
            df = self.extract_all_calories_data()
        
        if df.empty:
            return pd.DataFrame(columns=['date', 'total_calories'])
        
        # Add date column if only datetime exists
        df['date'] = df['datetime'].dt.date
        
        # Group by date and sum calories
        daily_total = df.groupby('date')['calories'].sum().reset_index()
        daily_total = daily_total.rename(columns={'calories': 'total_calories'})
        
        return daily_total
    
    def test(self):
        """Test method to verify the class is working"""
        return "Calories extractor works!"
    
    def extract_all_calories_data(self, limit: int = None) -> pd.DataFrame:
        """
        Extract all calories data from the Fitbit export.
        
        Args:
            limit: Optional limit on number of files to process
            
        Returns:
            DataFrame with calories data
        """
        # Find calories files
        pattern = '*calories*.json'
        
        # Use the base extractor to process files
        df = self.base_extractor.extract_data_to_dataframe(
            file_pattern=pattern,
            limit=limit
        )
        
        if df.empty:
            return df
        
        # Rename columns for clarity
        if 'value' in df.columns:
            df = df.rename(columns={'value': 'calories'})
        if 'date' in df.columns:
            df = df.rename(columns={'date': 'datetime'})
        
        # Filter out invalid values
        df = df.dropna(subset=['calories', 'datetime'])
        
        # Convert calories to numeric if not already
        df['calories'] = pd.to_numeric(df['calories'], errors='coerce')
        
        # Sort by datetime
        df = df.sort_values('datetime')
        
        return df
    
    def get_daily_total(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Calculate daily total calories burned.
        
        Args:
            df: Optional DataFrame of calories data. If None, extracts the data.
            
        Returns:
            DataFrame with daily totals
        """
        if df is None:
            df = self.extract_all_calories_data()
        
        if df.empty:
            return pd.DataFrame(columns=['date', 'total_calories'])
        
        # Add date column if only datetime exists
        if 'datetime' in df.columns and 'date' not in df.columns:
            df['date'] = df['datetime'].dt.date
        
        # Group by date and sum calories
        daily_total = df.groupby('date')['calories'].sum().reset_index()
        daily_total = daily_total.rename(columns={'calories': 'total_calories'})
        
        return daily_total
    
    def get_hourly_average(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Calculate hourly average calories burned.
        
        Args:
            df: Optional DataFrame of calories data. If None, extracts the data.
            
        Returns:
            DataFrame with hourly averages
        """
        if df is None:
            df = self.extract_all_calories_data()
        
        if df.empty:
            return pd.DataFrame(columns=['hour', 'average_calories'])
        
        # Extract hour from datetime
        df['hour'] = df['datetime'].dt.hour
        
        # Group by hour and calculate average
        hourly_avg = df.groupby('hour')['calories'].mean().reset_index()
        hourly_avg = hourly_avg.rename(columns={'calories': 'average_calories'})
        
        return hourly_avg
    
    def get_statistics(self, df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """
        Calculate calories statistics from the data.
        
        Args:
            df: Optional DataFrame of calories data. If None, extracts the data.
            
        Returns:
            Dictionary of statistics
        """
        if df is None:
            df = self.extract_all_calories_data()
        
        if df.empty:
            return {
                'record_count': 0,
                'start_date': None,
                'end_date': None,
                'average_per_minute': None,
                'min': None,
                'max': None,
                'estimated_daily_avg': None
            }
        
        # Daily totals for overall daily average
        daily_totals = self.get_daily_total(df)
        
        # Basic statistics
        stats = {
            'record_count': len(df),
            'start_date': df['datetime'].min(),
            'end_date': df['datetime'].max(),
            'average_per_minute': df['calories'].mean(),
            'min': df['calories'].min(),
            'max': df['calories'].max(),
            'days_covered': len(daily_totals),
            'estimated_daily_avg': daily_totals['total_calories'].mean() if not daily_totals.empty else None
        }
        
        return stats
