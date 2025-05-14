"""
Command line interface for Fitbit Takeout Extractor.
Provides easy-to-use commands for extracting and analyzing Fitbit data.
"""

import os
import sys
import argparse
import matplotlib.pyplot as plt

def heart_rate_command():
    """
    Command line tool for extracting heart rate data.
    """
    from fitbit_extractor.extractors.heart_rate import HeartRateExtractor

    parser = argparse.ArgumentParser(description="Extract heart rate data from Fitbit Takeout")
    parser.add_argument("--takeout", "-t", help="Path to the Google Takeout directory")
    parser.add_argument("--output", "-o", help="Output directory for extracted data and plots")
    parser.add_argument("--daily", "-d", action="store_true", help="Calculate daily averages")
    parser.add_argument("--plot", "-p", action="store_true", help="Generate plots")
    parser.add_argument("--limit", "-l", type=int, help="Limit number of files to process")
    
    args = parser.parse_args()
    
    # Set output directory
    output_dir = args.output or os.getcwd()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("Fitbit Takeout Extractor - Heart Rate")
    print("-" * 50)
    
    # Initialize extractor
    extractor = HeartRateExtractor(args.takeout)
    
    # Extract data
    print("Extracting heart rate data...")
    heart_rate_df = extractor.extract_all_heart_rate_data(args.limit)
    
    if heart_rate_df.empty:
        print("No heart rate data found!")
        return
    
    # Get statistics
    stats = extractor.get_statistics(heart_rate_df)
    print("\nHeart Rate Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Save data
    csv_path = os.path.join(output_dir, "heart_rate_data.csv")
    heart_rate_df.to_csv(csv_path, index=False)
    print(f"\nSaved heart rate data to {csv_path}")
    
    # Calculate daily averages if requested
    if args.daily:
        daily_avg = extractor.get_daily_average(heart_rate_df)
        daily_csv_path = os.path.join(output_dir, "daily_heart_rate.csv")
        daily_avg.to_csv(daily_csv_path, index=False)
        print(f"Saved daily averages to {daily_csv_path}")
        
        if args.plot:
            print("Generating heart rate plots...")
            plt.figure(figsize=(12, 6))
            plt.plot(daily_avg['date'], daily_avg['average_heart_rate'])
            plt.title('Daily Average Heart Rate')
            plt.xlabel('Date')
            plt.ylabel('Heart Rate (BPM)')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            plot_path = os.path.join(output_dir, 'heart_rate_trend.png')
            plt.savefig(plot_path)
            print(f"Saved plot to {plot_path}")


def calories_command():
    """
    Command line tool for extracting calories data.
    """
    from fitbit_extractor.extractors.calories import CaloriesExtractor

    parser = argparse.ArgumentParser(description="Extract calories data from Fitbit Takeout")
    parser.add_argument("--takeout", "-t", help="Path to the Google Takeout directory")
    parser.add_argument("--output", "-o", help="Output directory for extracted data and plots")
    parser.add_argument("--daily", "-d", action="store_true", help="Calculate daily totals")
    parser.add_argument("--hourly", "-hr", action="store_true", help="Calculate hourly averages")
    parser.add_argument("--plot", "-p", action="store_true", help="Generate plots")
    parser.add_argument("--limit", "-l", type=int, help="Limit number of files to process")
    
    args = parser.parse_args()
    
    # Set output directory
    output_dir = args.output or os.getcwd()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("Fitbit Takeout Extractor - Calories")
    print("-" * 50)
    
    # Initialize extractor
    extractor = CaloriesExtractor(args.takeout)
    
    # Extract data
    print("Extracting calories data...")
    calories_df = extractor.extract_all_calories_data(args.limit)
    
    if calories_df.empty:
        print("No calories data found!")
        return
    
    # Get statistics
    stats = extractor.get_statistics(calories_df)
    print("\nCalories Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Save data (save a sample if it's large)
    if len(calories_df) > 10000:
        sample_df = calories_df.sample(10000)
        csv_path = os.path.join(output_dir, "calories_data_sample.csv")
        sample_df.to_csv(csv_path, index=False)
        print(f"\nSaved sample of calories data to {csv_path} (data is large)")
    else:
        csv_path = os.path.join(output_dir, "calories_data.csv")
        calories_df.to_csv(csv_path, index=False)
        print(f"\nSaved calories data to {csv_path}")
    
    # Calculate daily totals if requested
    if args.daily:
        daily_totals = extractor.get_daily_total(calories_df)
        daily_csv_path = os.path.join(output_dir, "daily_calories.csv")
        daily_totals.to_csv(daily_csv_path, index=False)
        print(f"Saved daily totals to {daily_csv_path}")
        
        if args.plot:
            print("Generating daily calories plot...")
            plt.figure(figsize=(12, 6))
            plt.plot(daily_totals['date'], daily_totals['total_calories'])
            plt.title('Daily Total Calories')
            plt.xlabel('Date')
            plt.ylabel('Calories')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            plot_path = os.path.join(output_dir, 'daily_calories.png')
            plt.savefig(plot_path)
            print(f"Saved daily calories plot to {plot_path}")
    
    # Calculate hourly averages if requested
    if args.hourly:
        hourly_avg = extractor.get_hourly_average(calories_df)
        hourly_csv_path = os.path.join(output_dir, "hourly_calories.csv")
        hourly_avg.to_csv(hourly_csv_path, index=False)
        print(f"Saved hourly averages to {hourly_csv_path}")
        
        if args.plot:
            print("Generating hourly calories plot...")
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
            print(f"Saved hourly calories plot to {plot_path}")


if __name__ == "__main__":
    print("This module provides command line tools for Fitbit Takeout Extractor")
    print("Run 'extract-heart-rate --help' or 'extract-calories --help' for usage information")
