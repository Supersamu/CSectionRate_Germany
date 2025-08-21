"""
run_complete_analysis.py
Complete analysis pipeline that runs all components.
"""
import os
import argparse
from pathlib import Path
import time
import logging
from config import DEFAULT_YEAR, LOG_FORMAT
from analysis import load_data, create_visualizations, generate_analysis_report, generate_summary_statistics


def setup_logger(logfile):
    """Setup logging configuration"""
    logging.basicConfig(
        filename=logfile,
        filemode='w',
        format=LOG_FORMAT,
        level=logging.INFO
    )

def main(year: int):
    start_time = time.time()
    
    # Import here to avoid circular imports
    from process_hospital_data import main as process_hospital_data

    print(f"Starting complete C-section rate analysis for {year}")
    print("=" * 60)
    
    # Step 1: Data Extraction and Processing
    print("Step 1: Data Extraction and Processing")
    process_hospital_data(year=year)
    
    
    # Step 2: Statistical Analysis and Visualizations
    print("\nStep 2: Statistical Analysis and Visualizations")
    df = load_data(year)
    viz_path = create_visualizations(df, year)
    report_path = generate_analysis_report(df, year)
    
    print(f"Analysis completed - {len(df)} hospitals analyzed")
    print(f"   Visualizations: {viz_path}")
    print(f"   Report: {report_path}")
    
    
    # Summary
    elapsed_time = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"Analysis completed in {elapsed_time:.1f} seconds")
    print(f"All outputs saved to: {Path('output').absolute()}")
    
    # Generate final summary
    try:
        df = load_data(year)
        stats = generate_summary_statistics(df, year)
        
        print(f"\nFinal Results Summary:")
        print(f"   • {stats['total_hospitals']} hospitals analyzed")
        print(f"   • {stats['total_births']:,} total births")
        print(f"   • {stats['overall_rate']:.1%} national C-section rate")
        print(f"   • Range: {stats['min_rate']:.1%} - {stats['max_rate']:.1%}")
    except Exception as e:
        print(f"Note: Could not generate final summary: {e}")
    
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run complete C-section rate analysis")
    parser.add_argument("--year", type=int, default=DEFAULT_YEAR, help="Year to analyze")
    parser.add_argument("--include-analysis", action="store_true", default=True, 
                       help="Include statistical analysis and visualizations")
    args = parser.parse_args()
    
    year = args.year
    os.makedirs(f'output/{year}', exist_ok=True)
    setup_logger(f'output/{year}/complete_analysis.log')
    main(year)
