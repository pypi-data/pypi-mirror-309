import unittest
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from typing import List

from relative_abundance.calculate_abundance import *


class TestFunctions(unittest.TestCase):

    def setUp(self):
        # Set up a sample DataFrame for testing
        self.df = pd.DataFrame({
            "Compound": ["A", "B", "C"],
            "peptide1_mean": [0.2, 0.5, 1.5],
            "peptide1_std": [0.1, 0.15, 0.2],
            "peptide2_mean": [1.0, 0.7, 1.2],
            "peptide2_std": [0.05, 0.1, 0.08]
        })
        self.melted_df = pd.DataFrame({
            "Genes": ["Gene1"] * 6,
            "Precursor.Id": ["pep1", "pep1", "pep2", "pep2", "pep3", "pep3"],
            "Abundance": [1.0, 1.2, 0.8, 1.1, 0.9, 1.3],
            "Compound": ["A", "A", "B", "B", "C", "C"]
        })

    # Test make_manhattan_plot
    def test_make_manhattan_plot(self):
        # Test without ax (creates a new plot)
        make_manhattan_plot(self.df, "peptide1", show=False)
        plt.close()

        # Test with ax parameter
        fig, ax = plt.subplots()
        make_manhattan_plot(self.df, "peptide1", show=False, ax=ax)
        plt.close(fig)

    # Test aggregate_reps
    def test_aggregate_reps(self):
        # Create a test DataFrame with replicate columns
        test_df = pd.DataFrame({
            "Compound": ["A", "B", "C"],
            "pep1_1": [1.0, 2.0, np.nan],
            "pep1_2": [1.2, 2.1, 0.9],
            "pep1_3": [0.8, np.nan, 1.0]
        })
        result = aggregate_reps(test_df, "pep1_1")
        # Check that mean and std columns were added correctly
        self.assertIn("pep1_mean", result.columns)
        self.assertIn("pep1_std", result.columns)
        self.assertFalse(result["pep1_mean"].isna().any())  # No NaNs in means
        self.assertFalse(result["pep1_std"].isna().any())   # No NaNs in stds

    # Test drop_max_compound
    def test_drop_max_compound(self):
        result = aggregate_reps(self.df,"pep1_1")
        result = drop_max_compound(result)
        self.assertEqual(len(result), len(self.df) - 1)
        self.assertNotIn("C", result["Compound"].values)  # "C" has max in sample

    # # Test get_relative_abundance
    def test_get_relative_abundance_single_gene(self):
        melted_df = pd.DataFrame({
            "Genes": ["Gene1"] * 12,
            "Precursor.Id": ["pep1C", "pep1C", "pep2C", "pep2C", "pep3",
                             "pep3"]*2,
            "Abundance": [1.0, 1.2, 0.8, 1.1, 0.9, 1.3,
                         2.0, 1.4, 0.6, 0.9, 1.0, 1.2],
            "Compound": ["A", "B", "A", "B", "A", "B"]*2
        })
        # Test with single gene data
        result = get_relative_abundance(melted_df)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (1,10))

    def test_get_relative_abundance_multiple_genes(self):
        # Test with multiple genes to check ValueError
        df_multiple_genes = self.melted_df.copy()
        df_multiple_genes.loc[0, "Genes"] = "Gene2"
        with self.assertRaises(ValueError):
            get_relative_abundance(df_multiple_genes)
        
        
        
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