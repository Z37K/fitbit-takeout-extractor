# Fitbit Takeout Extractor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package for extracting and analyzing Fitbit data from Google Takeout exports. This tool helps you extract the Fitbit data from Google Takeout JSON files into pandas DataFrames for analysis.

## Features

- Extract data from Fitbit Google Takeout exports
- Handle complex nested JSON structures in Fitbit data files
- Supported data types:
  - Heart Rate data
  - Calories data
- Calculate daily averages, totals, and statistics
- Generate visualizations of trends
- Command line interface for quick data extraction

## Installation

```bash
# Clone the repository
git clone https://github.com/Z37K/fitbit-takeout-extractor.git
cd fitbit-takeout-extractor

# Install the package
pip install -e .
```

## Command Line Usage

After installation, you can use the command line tools:

```bash
# Extract heart rate data
extract-heart-rate --takeout /path/to/Takeout --output ./output --daily --plot

# Extract calories data
extract-calories --takeout /path/to/Takeout --output ./output --daily --hourly --plot
```

Use `--help` to see all available options:

```bash
extract-heart-rate --help
extract-calories --help
```

## Python API Usage

### Heart Rate Data

```python
import sys
import os
sys.path.insert(0, "/path/to/Google-Takeout-FitBit-Extractor")

from fitbit_extractor.extractors.heart_rate import HeartRateExtractor
import matplotlib.pyplot as plt

# Initialize the extractor with path to your Google Takeout directory
extractor = HeartRateExtractor("/path/to/Takeout")

# Extract heart rate data
heart_rate_df = extractor.extract_all_heart_rate_data()

# Get statistics
stats = extractor.get_statistics(heart_rate_df)
print(stats)

# Calculate daily averages
daily_avg = extractor.get_daily_average(heart_rate_df)

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(daily_avg['date'], daily_avg['average_heart_rate'])
plt.title('Daily Average Heart Rate')
plt.show()

# Save to CSV
heart_rate_df.to_csv('heart_rate_data.csv', index=False)
```

### Calories Data

```python
from fitbit_extractor.extractors.calories import CaloriesExtractor

# Initialize the extractor
extractor = CaloriesExtractor("/path/to/Takeout")

# Extract calories data
calories_df = extractor.extract_all_calories_data()

# Get daily totals
daily_totals = extractor.get_daily_total(calories_df)

# Get hourly averages
hourly_avg = extractor.get_hourly_average(calories_df)

# Save to CSV
daily_totals.to_csv('daily_calories.csv', index=False)
```

## Examples

Check the `examples` directory for more detailed usage examples:

- `extract_heart_rate.py`: Extracts and analyzes heart rate data
- `extract_calories.py`: Extracts and analyzes calories data
- `examine_file_types.py`: Explores the structure of different file types in your Fitbit export

## Data Formats

### Heart Rate Data

Heart rate data is returned as a pandas DataFrame with these columns:
- `datetime`: Timestamp of the heart rate measurement
- `heart_rate`: Heart rate in beats per minute (BPM)

### Calories Data

Calories data is returned as a pandas DataFrame with these columns:
- `datetime`: Timestamp of the calories measurement
- `calories`: Estimated calories burned per minute

## Extending the Package

This package is designed to be easily extended to handle other Fitbit data types:

1. Create a new extractor in the `fitbit_extractor/extractors/` directory
2. Use the base `FitbitTakeoutExtractor` for file handling and data extraction
3. Add your specialized data processing logic
4. Add a command-line interface in `command_line.py` if desired

## Contributing

Here's how you can contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Submit a pull request

Some ideas for contributions:
- Add support for more Fitbit data types (steps, distance, sleep, etc.)
- Improve visualization options
- Add more analysis features

## License

This project is licensed under the MIT License - see the LICENSE file for details.