import os
import unittest
import pandas as pd


class TestDataLoading(unittest.TestCase):
    """Basic tests to ensure data files load correctly"""

    def setUp(self):
        """Set file paths"""
        self.data_path = "data/raw/ethiopia_fi_unified_data.csv"

    def test_dataset_exists(self):
        """Test that the dataset file exists"""
        self.assertTrue(
            os.path.exists(self.data_path),
            "ethiopia_fi_unified_data.csv does not exist"
        )

    def test_dataset_loads(self):
        """Test that the dataset loads into a DataFrame"""
        df = pd.read_csv(self.data_path)
        self.assertFalse(df.empty, "Dataset loaded but is empty")

    def test_required_columns_exist(self):
        """Test that required columns are present"""
        df = pd.read_csv(self.data_path)

        required_columns = [
            "record_type",
            "indicator",
            "indicator_code",
            "observation_date",
            "confidence"
        ]

        for col in required_columns:
            self.assertIn(col, df.columns, f"Missing required column: {col}")


if __name__ == "__main__":
    unittest.main()
