"""
analysis.py
Data analysis and visualization functions for C-section rate analysis.
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from config import OUTPUT_DIR, PRIVACY_PROTECTION_VALUE, COLUMN_NAMES, DEFAULT_YEAR

def load_data(year: int) -> pd.DataFrame:
    """Load and clean the processed hospital data."""
    filepath = Path(OUTPUT_DIR) / f"hospital_statistics_{year}.csv"
    df = pd.read_csv(filepath, index_col=0)
    
    # Clean and convert data types
    births_col = f"{COLUMN_NAMES['total_births']} {year}"
    csections_col = f"{COLUMN_NAMES['csections']} {year}"
    rate_col = f"{COLUMN_NAMES['csection_rate']} {year}"
    
    # Filter out privacy-protected data for analysis
    df_clean = df[df[rate_col] != PRIVACY_PROTECTION_VALUE].copy()
    
    # Convert numeric columns
    df_clean[births_col] = pd.to_numeric(df_clean[births_col], errors='coerce')
    df_clean[csections_col] = pd.to_numeric(df_clean[csections_col], errors='coerce')
    
    # Extract numeric rate from percentage string
    df_clean['csection_rate_numeric'] = df_clean[rate_col].str.rstrip('%').astype(float) / 100
    
    return df_clean

def generate_summary_statistics(df: pd.DataFrame, year: int) -> dict:
    """Generate comprehensive summary statistics."""
    births_col = f"{COLUMN_NAMES['total_births']} {year}"
    csections_col = f"{COLUMN_NAMES['csections']} {year}"
    
    stats = {
        'total_hospitals': len(df),
        'total_births': df[births_col].sum(),
        'total_csections': df[csections_col].sum(),
        'overall_rate': df[csections_col].sum() / df[births_col].sum(),
        'mean_rate': df['csection_rate_numeric'].mean(),
        'median_rate': df['csection_rate_numeric'].median(),
        'std_rate': df['csection_rate_numeric'].std(),
        'min_rate': df['csection_rate_numeric'].min(),
        'max_rate': df['csection_rate_numeric'].max(),
    }
    
    return stats

def create_visualizations(df: pd.DataFrame, year: int, output_dir: str = None):
    """Create comprehensive visualizations of the data."""
    if output_dir is None:
        output_dir = Path(OUTPUT_DIR) / "visualizations"
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Set style
    plt.style.use('seaborn-v0_8')
    
    # 1. Distribution of C-section rates
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.hist(df['csection_rate_numeric'] * 100, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    plt.axvline(df['csection_rate_numeric'].mean() * 100, color='red', linestyle='--', 
                label=f'Mean: {df["csection_rate_numeric"].mean()*100:.1f}%')
    plt.xlabel('C-section Rate (%)')
    plt.ylabel('Number of Hospitals')
    plt.title(f'Distribution of C-section Rates ({year})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 2. Box plot of rates
    plt.subplot(1, 2, 2)
    plt.boxplot(df['csection_rate_numeric'] * 100, patch_artist=True, 
                boxprops=dict(facecolor='lightblue', alpha=0.7))
    plt.ylabel('C-section Rate (%)')
    plt.title(f'C-section Rate Distribution ({year})')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path / f'csection_rate_distribution_{year}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Hospital size vs C-section rate
    births_col = f"Geburten gesamt {year}"
    plt.figure(figsize=(10, 6))
    plt.scatter(df[births_col], df['csection_rate_numeric'] * 100, alpha=0.6, s=50)
    plt.xlabel('Total Births')
    plt.ylabel('C-section Rate (%)')
    plt.title(f'Hospital Size vs C-section Rate ({year})')
    
    # Add trend line
    z = np.polyfit(df[births_col], df['csection_rate_numeric'] * 100, 1)
    p = np.poly1d(z)
    plt.plot(df[births_col], p(df[births_col]), "r--", alpha=0.8, 
             label=f'Trend: slope={z[0]:.4f}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(output_path / f'size_vs_rate_{year}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    
    return output_path

def generate_analysis_report(df: pd.DataFrame, year: int, output_file: str = None):
    """Generate a comprehensive analysis report."""
    if output_file is None:
        output_file = Path(OUTPUT_DIR) / f"analysis_report_{year}.md"
    
    stats = generate_summary_statistics(df, year)
    
    report = f"""# C-Section Rate Analysis Report - {year}

## Executive Summary

This analysis examined C-section rates across **{stats['total_hospitals']} German hospitals** in {year}, 
covering **{stats['total_births']:,} total births** and **{stats['total_csections']:,} C-sections**.

## Overall Statistics
- **National C-section Rate**: {stats['overall_rate']:.1%} ({stats['total_csections']:,} out of {stats['total_births']:,} births)
- **Average Hospital Rate**: {stats['mean_rate']:.1%} (± {stats['std_rate']:.1%})
- **Median Hospital Rate**: {stats['median_rate']:.1%}
- **Range**: {stats['min_rate']:.1%} - {stats['max_rate']:.1%}

## Recommendations

1. **Regional Analysis**: Investigate state-level variations for policy implications  
2. **Trend Monitoring**: Track changes over time to measure improvement initiatives

---
*Report generated automatically from hospital quality data*
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return output_file

if __name__ == "__main__":
    # Example usage
    year = DEFAULT_YEAR
    df = load_data(year)
    
    # Generate visualizations
    viz_path = create_visualizations(df, year)
    print(f"Visualizations saved to: {viz_path}")
    
    # Generate analysis report
    report_path = generate_analysis_report(df, year)
    print(f"Analysis report saved to: {report_path}")
    
    # Print summary statistics
    stats = generate_summary_statistics(df, year)
    print(f"\n📊 Quick Summary for {year}:")
    print(f"   • {stats['total_hospitals']} hospitals analyzed")
    print(f"   • {stats['overall_rate']:.1%} national C-section rate")
    print(f"   • {stats['min_rate']:.1%} - {stats['max_rate']:.1%} range across hospitals")
