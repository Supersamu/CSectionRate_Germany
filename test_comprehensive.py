"""
test_comprehensive.py
Comprehensive test suite for C-section rate analysis project.
"""
import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import patch

from process_hospital_data import main
from analysis import load_data, generate_summary_statistics
from config import OUTPUT_DIR, PRIVACY_PROTECTION_VALUE, DEFAULT_YEAR


class TestDataAnalysis:
    """Test analysis functions."""
    
    def test_summary_statistics(self):
        """Test summary statistics generation."""
        try:
            df = load_data(DEFAULT_YEAR)
            stats = generate_summary_statistics(df, DEFAULT_YEAR)
                
            # Verify logical constraints
            assert stats['total_csections'] <= stats['total_births']
            assert 0 <= stats['overall_rate'] <= 1
            assert stats['total_hospitals'] > 0
            
        except FileNotFoundError:
            pytest.skip("Data file not available for testing")

class TestDataQuality:
    """Test data quality and validation."""
    
    def test_data_consistency(self):
        """Test that data is internally consistent."""
        try:
            df = load_data(DEFAULT_YEAR)
            
            # Check that numeric columns are properly converted
            births_col = f"Geburten gesamt {DEFAULT_YEAR}"
            csections_col = f"Anzahl Kaiserschnitte {DEFAULT_YEAR}"

            assert df[births_col].dtype in ['int64', 'float64']
            assert df[csections_col].dtype in ['int64', 'float64']
            
            # Check that C-sections don't exceed births
            assert (df[csections_col] <= df[births_col]).all()
            
            # Check rate calculations
            calculated_rates = df[csections_col] / df[births_col]
            assert (abs(calculated_rates - df['csection_rate_numeric']) < 0.01).all()
            
        except FileNotFoundError:
            pytest.skip("Data file not available for testing")
    
    def test_privacy_protection_handling(self):
        """Test that privacy protection is properly handled."""
        try:
            # Load original data with privacy protection
            filepath = Path(OUTPUT_DIR) / f"hospital_statistics_{DEFAULT_YEAR}.csv"
            df_original = pd.read_csv(filepath, index_col=0)
            
            # Load cleaned data
            df_clean = load_data(DEFAULT_YEAR)

            # Verify privacy-protected records are filtered out
            privacy_records = df_original[df_original[f'Kaiserschnitt % {DEFAULT_YEAR}'] == PRIVACY_PROTECTION_VALUE]
            assert len(privacy_records) > 0, "Expected some privacy-protected records"
            assert PRIVACY_PROTECTION_VALUE not in df_clean[f'Kaiserschnitt % {DEFAULT_YEAR}'].values

        except FileNotFoundError:
            pytest.skip("Data file not available for testing")


def test_integration_full_pipeline():
    """Integration test for the complete pipeline."""
    # Test that the full pipeline runs without errors
    # This is essentially what test_output_compare.py does
    try:
        # Run main processing
        main()
        
        # Verify outputs exist and are valid
        df = load_data(DEFAULT_YEAR)
        assert len(df) > 0

        stats = generate_summary_statistics(df, DEFAULT_YEAR)
        assert stats['total_hospitals'] > 0
        assert 0 < stats['overall_rate'] < 1
        
    except Exception as e:
        pytest.fail(f"Integration test failed: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
