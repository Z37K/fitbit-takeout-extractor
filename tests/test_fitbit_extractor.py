import pytest
import os
import sys
import pandas as pd

# Add parent directory to path to import package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fitbit_extractor import FitbitTakeoutExtractor
from fitbit_extractor.utils import normalize_date


def test_normalize_date():
    """Test the date normalization function."""
    # Test various date formats
    assert normalize_date("2023-11-20 19:37:23") is not None
    assert normalize_date("11/20/23 19:37:23") is not None
    assert normalize_date("2023-11-20T19:37:23.000Z") is not None
    assert normalize_date("2023-11-20") is not None
    
    # Test invalid date
    assert normalize_date("not-a-date") is None
    assert normalize_date(123) is None
    assert normalize_date(None) is None


def test_extractor_initialization():
    """Test the FitbitTakeoutExtractor initialization."""
    # Create with explicit path
    extractor = FitbitTakeoutExtractor("./Takeout")
    assert extractor.takeout_dir == "./Takeout"
    assert extractor.fitbit_dir == os.path.join("./Takeout", "Fitbit")
    
    # Create without path (should try to find it)
    extractor = FitbitTakeoutExtractor()
    # Can't assert exact path, but structure should be consistent
    if extractor.takeout_dir:
        assert os.path.basename(extractor.takeout_dir) == "Takeout"
        assert extractor.fitbit_dir == os.path.join(extractor.takeout_dir, "Fitbit")


def test_extract_records_empty():
    """Test extract_records with non-existent file."""
    extractor = FitbitTakeoutExtractor()
    records = extractor.extract_records("non_existent_file.json")
    assert records == []


# Run the tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])
