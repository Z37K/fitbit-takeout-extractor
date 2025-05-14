import sys
import os

# Add parent directory to path so we can import the package
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import matplotlib.pyplot as plt
import pandas as pd
from fitbit_extractor.extractors.calories import CaloriesExtractor

def main():
    """
    Example demonstrating how to use the CaloriesExtractor.
    """
    print("Fitbit Takeout Extractor - Calories Example")
    print("-" * 50)

    # Write to a log file as well for debugging
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calories_log.txt")
    with open(log_file, "w") as f:
        f.write("Starting calories extraction\n")
    
    # Initialize the calories extractor
    calories_extractor = CaloriesExtractor()
    
    # Find calories files
    files = calories_extractor.base_extractor.find_files('*calories*.json')
    print(f"Found {len(files)} calories files")
    with open(log_file, "a") as f:
        f.write(f"Found {len(files)} calories files\n")
    
    if files:
        print(f"First file: {os.path.basename(files[0])}")
        with open(log_file, "a") as f:
            f.write(f"First file: {os.path.basename(files[0])}\n")
    
    # Extract all calories data
    print("Extracting calories data...")
    with open(log_file, "a") as f:
        f.write("Extracting calories data...\n")
    
    calories_df = calories_extractor.extract_all_calories_data()
    
    if calories_df.empty:
        print("No calories data found!")
        return
        
    # Get statistics
    stats = calories_extractor.get_statistics(calories_df)
    print("\nCalories Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Calculate daily totals
    daily_totals = calories_extractor.get_daily_total(calories_df)
    print(f"\nCalculated daily totals for {len(daily_totals)} days")
    
    # Calculate hourly averages
    hourly_avg = calories_extractor.get_hourly_average(calories_df)
    print(f"Calculated hourly averages for a 24-hour day")
    
    # Determine output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Create visualizations
    print("Creating visualizations...")
    
    # Plot 1: Daily total calories
    if len(daily_totals) > 0:
        plt.figure(figsize=(12, 6))
        plt.plot(daily_totals['date'], daily_totals['total_calories'])
        plt.title('Daily Total Calories')
        plt.xlabel('Date')
        plt.ylabel('Calories')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        plot_path = os.path.join(output_dir, 'daily_calories.png')
        plt.savefig(plot_path)
        print(f"Daily calories plot saved as '{plot_path}'")
    
    # Plot 2: Hourly average calories
    if not hourly_avg.empty:
        plt.figure(figsize=(10, 6))
        plt.bar(hourly_avg['hour'], hourly_avg['average_calories'])
        plt.title('Average Calories Burned by Hour of Day')
        plt.xlabel('Hour of Day')
        plt.ylabel('Average Calories')
        plt.xticks(range(0, 24))
        plt.grid(True, axis='y', alpha=0.3)
        plt.tight_layout()
        
        plot_path = os.path.join(output_dir, 'hourly_calories.png')
        plt.savefig(plot_path)
        print(f"Hourly calories plot saved as '{plot_path}'")
    
    # Save to CSV
    calories_csv = os.path.join(output_dir, 'calories_data.csv')
    daily_totals_csv = os.path.join(output_dir, 'daily_calories.csv')
    hourly_avg_csv = os.path.join(output_dir, 'hourly_calories.csv')
    
    # Save samples to avoid huge files
    if len(calories_df) > 10000:
        sample_size = 10000
        print(f"Saving {sample_size} random samples out of {len(calories_df)} records to CSV (full dataset is large)")
        calories_df.sample(sample_size).to_csv(calories_csv, index=False)
    else:
        calories_df.to_csv(calories_csv, index=False)
    
    daily_totals.to_csv(daily_totals_csv, index=False)
    hourly_avg.to_csv(hourly_avg_csv, index=False)
    
    print(f"\nData saved as:")
    print(f"- '{calories_csv}'")
    print(f"- '{daily_totals_csv}'")
    print(f"- '{hourly_avg_csv}'")

if __name__ == "__main__":
    main()
