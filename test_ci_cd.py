"""
CI/CD-style tests for C-section rate analysis project. 
The tests cannot run on Github, as the raw data cannot be uploaded for license reasons.
"""

import os
import subprocess
from config import DEFAULT_YEAR
import pytest

OUTPUT_DIR = "output"
OUTPUT_TEST_DIR = "output_test"
OUTPUT_FILES = [
    f"hospital_statistics.csv",
    f"full_list.txt",
    f"hospital_statistics.txt"
]

def run_main_script():
    """
    Run process_hospital_data.py to generate output files for the year specified in the config.
    """
    python_exe = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")

    subprocess.run(
        [python_exe, "process_hospital_data.py", "--year", f"{DEFAULT_YEAR}"],
        check=True
    )

def compare_files(file1: str, file2: str) -> bool:
    """
    Compare the contents of two files.
    """
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        return f1.read() == f2.read()

def test_outputs_match():
    """
    Generate output files and compare them to output_test files.
    """
    run_main_script()
    for filename in OUTPUT_FILES:
        output_path = os.path.join(OUTPUT_DIR, str(DEFAULT_YEAR), filename)
        test_path = os.path.join(OUTPUT_TEST_DIR, str(DEFAULT_YEAR), filename)
        assert os.path.exists(output_path), f"Missing output file: {output_path}"
        assert os.path.exists(test_path), f"Missing test file: {test_path}"
        assert compare_files(output_path, test_path), f"Files differ: {filename}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
