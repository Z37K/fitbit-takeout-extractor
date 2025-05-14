from typing import Dict, Any, List, Optional, Union
import pandas as pd
import os
from ..core import FitbitTakeoutExtractor

class HeartRateExtractor:
    """
    Specialized extractor for Fitbit heart rate data from Google Takeout.
    
    This extractor handles the specific structure of heart rate data, including
    the nested BPM values and confidence scores.
    """
    
    def __init__(self, takeout_dir: str = None):
        """
        Initialize the heart rate extractor.
        
        Args:
            takeout_dir: Path to Google Takeout directory. If None, will try to locate it.
        """
        self.base_extractor = FitbitTakeoutExtractor(takeout_dir)
    
    def extract_heart_rate_value(self, value: Any) -> Dict[str, Any]:
        """
        Extract heart rate BPM and confidence from the value field.
        
        Args:
            value: The value field from a heart rate record
            
        Returns:
            Dictionary with 'bpm' and 'confidence' keys
        """
        result = {'bpm': None, 'confidence': None}
        
        if isinstance(value, dict):
            # Typical format: {'bpm': 64, 'confidence': 2}
            result['bpm'] = value.get('bpm')
            result['confidence'] = value.get('confidence')
        elif isinstance(value, (int, float)):
            # Sometimes it's just a direct BPM value
            result['bpm'] = value
        
        return result
    
    def extract_all_heart_rate_data(self, limit: int = None) -> pd.DataFrame:
        """
        Extract all heart rate data from the Fitbit export.
        
        Args:
            limit: Optional limit on number of files to process
            
        Returns:
            DataFrame with heart rate data
        """
        # Find heart rate files
        pattern = '*heart*.json'
        
        # Define value extraction function
        def extract_values(value):
            hr_data = self.extract_heart_rate_value(value)
            return hr_data['bpm']  # Just return the BPM for the primary value
        
        # Use the base extractor to process files
        df = self.base_extractor.extract_data_to_dataframe(
            file_pattern=pattern,
            value_extractor=extract_values,
            limit=limit
        )
        
        if df.empty:
            return df
        
        # Rename columns for clarity
        if 'value' in df.columns:
            df = df.rename(columns={'value': 'heart_rate'})
        if 'date' in df.columns:
            df = df.rename(columns={'date': 'datetime'})
        
        # Filter out invalid values
        df = df.dropna(subset=['heart_rate', 'datetime'])
        
        # Sort by datetime
        df = df.sort_values('datetime')
        
        return df
    
    def get_daily_average(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Calculate daily average heart rates.
        
        Args:
            df: Optional DataFrame of heart rate data. If None, extracts the data.
            
        Returns:
            DataFrame with daily average heart rates
        """
        if df is None:
            df = self.extract_all_heart_rate_data()
        
        if df.empty:
            return pd.DataFrame(columns=['date', 'average_heart_rate'])
        
        # Add date column if only datetime exists
        if 'datetime' in df.columns and 'date' not in df.columns:
            df['date'] = df['datetime'].dt.date
        
        # Group by date and calculate average
        daily_avg = df.groupby('date')['heart_rate'].mean().reset_index()
        daily_avg = daily_avg.rename(columns={'heart_rate': 'average_heart_rate'})
        
        return daily_avg
    
    def get_statistics(self, df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """
        Calculate heart rate statistics from the data.
        
        Args:
            df: Optional DataFrame of heart rate data. If None, extracts the data.
            
        Returns:
            Dictionary of statistics
        """
        if df is None:
            df = self.extract_all_heart_rate_data()
        
        if df.empty:
            return {
                'record_count': 0,
                'start_date': None,
                'end_date': None,
                'average': None,
                'min': None,
                'max': None
            }
        
        # Basic statistics
        stats = {
            'record_count': len(df),
            'start_date': df['datetime'].min(),
            'end_date': df['datetime'].max(),
            'average': df['heart_rate'].mean(),
            'min': df['heart_rate'].min(),
            'max': df['heart_rate'].max(),
            'days_covered': len(df['datetime'].dt.date.unique())
        }
        
        return stats
