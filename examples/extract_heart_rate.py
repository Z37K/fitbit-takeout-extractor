import sys
import os

# Add parent directory to path so we can import the package
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import matplotlib.pyplot as plt
import pandas as pd
from fitbit_extractor.extractors.heart_rate import HeartRateExtractor

def main():
    """
    Example demonstrating how to use the HeartRateExtractor.
    """
    print("Fitbit Takeout Extractor - Heart Rate Example")
    print("-" * 50)

    # Initialize the heart rate extractor
    hr_extractor = HeartRateExtractor()
    
    # Extract all heart rate data
    print("Extracting heart rate data...")
    heart_rate_df = hr_extractor.extract_all_heart_rate_data()
    
    if heart_rate_df.empty:
        print("No heart rate data found!")
        return
        
    # Get statistics
    stats = hr_extractor.get_statistics(heart_rate_df)
    print("\nHeart Rate Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Calculate daily averages
    daily_avg = hr_extractor.get_daily_average(heart_rate_df)
    print(f"\nCalculated daily averages for {len(daily_avg)} days")
    
    # Determine output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Visualize data (if there's enough)
    if len(daily_avg) > 0:
        print("Creating visualization...")
        plt.figure(figsize=(12, 6))
        plt.plot(daily_avg['date'], daily_avg['average_heart_rate'])
        plt.title('Daily Average Heart Rate')
        plt.xlabel('Date')
        plt.ylabel('Heart Rate (BPM)')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        plot_path = os.path.join(output_dir, 'heart_rate_trend.png')
        plt.savefig(plot_path)
        print(f"Plot saved as '{plot_path}'")
    
    # Save to CSV
    heart_rate_csv = os.path.join(output_dir, 'heart_rate_data.csv')
    daily_avg_csv = os.path.join(output_dir, 'daily_heart_rate.csv')
    
    heart_rate_df.to_csv(heart_rate_csv, index=False)
    daily_avg.to_csv(daily_avg_csv, index=False)
    
    print(f"\nData saved as:")
    print(f"- '{heart_rate_csv}'")
    print(f"- '{daily_avg_csv}'")

if __name__ == "__main__":
    main()
