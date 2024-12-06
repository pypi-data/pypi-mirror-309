import unittest
import pandas as pd
import numpy as np
from typing import List

from relative_abundance.calculate_abundance import *


class TestMathFunctions(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.series = pd.Series([1, 2, 3, 4, 5])
        self.df = pd.DataFrame({
            "Compound": ["A", "B", "C"],
            "control_peptide": [1.0, 1.5, 2.0],
            "peptide1": [2.0, 3.0, 4.0],
            "peptide2": [5.0, 6.0, 7.0]
        })

    # Test scale_series
    def test_scale_series(self):
        scaled_series = scale_series(self.series)

        # Check that the series is within the expected range
        self.assertTrue(scaled_series.min() >= 0.00001)
        self.assertTrue(scaled_series.max() <= 1)

        # Check that the mean is close to the target mean
        np.testing.assert_almost_equal(scaled_series.mean(), 0.5, decimal=1)

    # Test normalize
    def test_normalize(self):
        control_peptide = "control_peptide"
        normalized_df = normalize(self.df, control_peptide)

        # Check that control peptide values are now 1 (relative abundance)
        self.assertTrue((normalized_df[control_peptide] == 1).all())

        # Verify that normalization scales other columns relative to the control
        expected_values = self.df["peptide1"] / self.df[control_peptide]
        pd.testing.assert_series_equal(
            normalized_df["peptide1"], expected_values, check_names=False
        )

    def test_normalize_nan_handling(self):
        # Add NaN values to test NaN handling
        df_with_nan = self.df.copy()
        df_with_nan.loc[0, "peptide1"] = np.nan

        control_peptide = "control_peptide"
        normalized_df = normalize(df_with_nan, control_peptide)

        # Check that the NaN is preserved in the normalized DataFrame
        self.assertTrue(pd.isna(normalized_df.loc[0, "peptide1"]))


if __name__ == "__main__":
    unittest.main()