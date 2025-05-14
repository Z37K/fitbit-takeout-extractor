import os
import pandas as pd
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

def find_takeout_dir(start_dir: Optional[str] = None, max_levels: int = 5) -> Optional[str]:
    """
    Recursively find the Takeout directory by going up through parent directories.
    
    Args:
        start_dir: Directory to start searching from (default: current working directory)
        max_levels: Maximum number of directory levels to go up
        
    Returns:
        Path to Takeout directory if found, otherwise None
    """
    if start_dir is None:
        start_dir = os.getcwd()
    
    current_dir = os.path.abspath(start_dir)
    
    for _ in range(max_levels):
        takeout_path = os.path.join(current_dir, 'Takeout')
        if os.path.exists(takeout_path):
            return takeout_path
            
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:  # Reached the root directory
            break
            
        current_dir = parent_dir
    
    return None

def normalize_date(date_str: Any) -> Optional[datetime]:
    """
    Try to normalize a date string into a datetime object using multiple formats.
    
    Args:
        date_str: Date string to normalize
        
    Returns:
        Datetime object if successful, None if parsing failed
    """
    if isinstance(date_str, datetime):
        return date_str
        
    if not isinstance(date_str, str):
        return None
        
    # List of date formats to try
    formats = [
        '%Y-%m-%d %H:%M:%S',  # 2023-11-20 19:37:23
        '%Y-%m-%dT%H:%M:%S',  # 2023-11-20T19:37:23
        '%Y-%m-%dT%H:%M:%S.%f',  # 2023-11-20T19:37:23.000
        '%Y-%m-%dT%H:%M:%S.%fZ',  # 2023-11-20T19:37:23.000Z
        '%m/%d/%y %H:%M:%S',  # 11/20/23 19:37:23
        '%m/%d/%Y %H:%M:%S',  # 11/20/2023 19:37:23
        '%Y-%m-%d',  # 2023-11-20
        '%m/%d/%y',  # 11/20/23
        '%m/%d/%Y',  # 11/20/2023
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    # If all formats failed, try pandas which is more flexible
    try:
        return pd.to_datetime(date_str)
    except:
        return None

def calculate_time_window(df: pd.DataFrame, date_column: str = 'datetime', 
                          window: str = 'day') -> Dict[str, Any]:
    """
    Calculate statistics for different time windows (day, week, month).
    
    Args:
        df: DataFrame with time series data
        date_column: Name of the column containing datetime values
        window: Time window to group by ('day', 'week', 'month')
        
    Returns:
        Dictionary with time window statistics
    """
    if df.empty or date_column not in df.columns:
        return {'window': window, 'count': 0, 'groups': []}
        
    # Ensure datetime column is datetime type
    if not pd.api.types.is_datetime64_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        
    # Drop rows with invalid dates
    df = df.dropna(subset=[date_column])
    
    if df.empty:
        return {'window': window, 'count': 0, 'groups': []}
    
    # Group by the specified window
    if window == 'day':
        df['group'] = df[date_column].dt.date
    elif window == 'week':
        df['group'] = df[date_column].dt.to_period('W').dt.start_time.dt.date
    elif window == 'month':
        df['group'] = df[date_column].dt.to_period('M').dt.start_time.dt.date
    else:
        return {'window': 'invalid', 'count': 0, 'groups': []}
    
    # Count records per group
    counts = df.groupby('group').size().reset_index(name='count')
    counts = counts.sort_values('group')
    
    return {
        'window': window,
        'count': len(counts),
        'groups': counts.to_dict('records')
    }
