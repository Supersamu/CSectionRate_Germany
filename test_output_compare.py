import os
import subprocess
from config import DEFAULT_YEAR

OUTPUT_DIR = "output"
OUTPUT_TEST_DIR = "output_test"
OUTPUT_FILES = [
    f"hospital_statistics_{DEFAULT_YEAR}.csv",
    f"full_list_{DEFAULT_YEAR}.txt",
    f"hospital_statistics_{DEFAULT_YEAR}.txt"
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
        output_path = os.path.join(OUTPUT_DIR, filename)
        test_path = os.path.join(OUTPUT_TEST_DIR, filename)
        assert os.path.exists(output_path), f"Missing output file: {output_path}"
        assert os.path.exists(test_path), f"Missing test file: {test_path}"
        assert compare_files(output_path, test_path), f"Files differ: {filename}"
