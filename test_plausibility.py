"""
Plausibility Analysis for the results obtained.
"""
import pytest


from analysis import load_data
from config import DEFAULT_YEAR


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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
