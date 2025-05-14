"""
Fitbit Takeout Extractor

A Python package for extracting and analyzing Fitbit data from Google Takeout exports.
"""

__version__ = "0.1.0"

from .core import FitbitTakeoutExtractor

# Explicitly import extractors with error handling
try:
    from .extractors.heart_rate import HeartRateExtractor
except ImportError:
    HeartRateExtractor = None
    
try:
    from .extractors.calories import CaloriesExtractor
except ImportError:
    CaloriesExtractor = None

__all__ = ['FitbitTakeoutExtractor', 'HeartRateExtractor', 'CaloriesExtractor']