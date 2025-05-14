# Fitbit Takeout Extractor Examples

This directory contains example scripts demonstrating how to use the Fitbit Takeout Extractor package.

## Available Examples

1. **basic_example.py** - Shows how to initialize the extractor and explore available data
2. **extract_heart_rate.py** - Demonstrates extracting and analyzing heart rate data
3. **extract_calories.py** - Demonstrates extracting and analyzing calories data
4. **examine_file_types.py** - Explores the structure of different file types in your Fitbit export

## Running the Examples

To run any example:

```bash
# Navigate to the repository root directory
cd /path/to/fitbit-takeout-extractor

# Run an example
python -m examples.extract_heart_rate
```

## Output Directory

The examples create output files (CSV data and plots) in the `examples/output` directory.

## Notes

- If you don't specify a Takeout directory path, the scripts will try to find it automatically
- Some examples may take a while to run if you have a large amount of Fitbit data
