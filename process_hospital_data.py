import os
import pandas as pd
from collections import defaultdict
import argparse
import logging
from extract_from_xml import get_hospital_statistic, get_clinic_data
from config import (
    DEFAULT_YEAR, DATA_DIR, OUTPUT_DIR, COLUMN_NAMES, 
    DAS_FILE_SUFFIX, XML_FILE_SUFFIX, PROGRESS_INTERVAL, NOT_ENOUGH_BIRTHS_MARKER, LOG_FORMAT
)
from get_gps_coordinates import get_coordinates_from_clinic_data
from create_kml import create_kml_from_csv

def setup_logger(logfile):
    """Setup logging configuration"""
    logging.basicConfig(
        filename=logfile,
        filemode='w',
        format=LOG_FORMAT,
        level=logging.INFO
    )


# =========================
# Argument Parsing
# =========================

def main(year:int) -> None:
    # =========================
    # Paths & Data Structures
    # =========================
    mypath = os.path.join(DATA_DIR, f"xml_{year}")
    os.makedirs(os.path.join(OUTPUT_DIR, str(year)), exist_ok=True)
    

    try:
        all_files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    except FileNotFoundError:
        logging.error(f"Data directory for year {year} not found: {mypath}")
        return
    except Exception as e:
        logging.error(f"Error reading files from {mypath}: {e}")
        return
    result_dict = defaultdict(list)
    IK_list = []
    Standortnummer_list = []

    ###############################
    # Main Data Extraction Process
    ###############################
    # Collect IK and Standortnummer from filenames
    for file in all_files:
        if file.endswith(DAS_FILE_SUFFIX):
            IK_list.append(file.split("-")[0])
            Standortnummer_list.append(file.split("-")[1])

    # Process each hospital
    for idx, (IK, Standortnummer) in enumerate(zip(IK_list, Standortnummer_list)):
        if idx % PROGRESS_INTERVAL == 0:
            print(f"Working on Hospital {idx + 1} of {len(IK_list)}")
        total_births, num_csections, rate = get_hospital_statistic(IK, Standortnummer, year)
        if total_births is not None:  # Enough births occured to report statistics 
            xml_path = os.path.join(DATA_DIR, f"xml_{year}", f"{IK}-{Standortnummer}-{year}-{XML_FILE_SUFFIX}")
            if os.path.isfile(xml_path):
                name_hospital, town, street, zip_code = get_clinic_data(IK, Standortnummer, year)
                coordinates = get_coordinates_from_clinic_data({
                    "city": town,
                    "street": street,
                    "postalcode": zip_code
                })
                result_dict[COLUMN_NAMES["hospital_name"]].append(name_hospital)
                result_dict[COLUMN_NAMES["city"]].append(town)
                result_dict[COLUMN_NAMES["street_address"]].append(street)
                result_dict[COLUMN_NAMES["postal_code"]].append(zip_code)
                result_dict[f"{COLUMN_NAMES['total_births']} {year}"].append(total_births)
                result_dict[f"{COLUMN_NAMES['csections']} {year}"].append(num_csections)
                result_dict[f"{COLUMN_NAMES['csection_rate']} {year}"].append(rate)
                result_dict[COLUMN_NAMES["ik"]].append(IK)
                result_dict[COLUMN_NAMES["location_number"]].append(Standortnummer)
                result_dict["Latitude"].append(coordinates[0])
                result_dict["Longitude"].append(coordinates[1])
            else:
                logging.warning(f"No corresponding file ending in {XML_FILE_SUFFIX} found for hospital "
                                f"with IK {IK} and Standortnummer {Standortnummer}")

    ###############################
    # Output Results
    ###############################
    try:
        df = pd.DataFrame.from_dict(result_dict)
        df.to_csv(os.path.join(OUTPUT_DIR, str(year), f"hospital_statistics.csv"))
        
        # Create KML file
        create_kml_from_csv(df, year)
        
    except Exception as e:
        logging.error(f"Error writing CSV file: {e}")
        return

    keys = [COLUMN_NAMES["hospital_name"], COLUMN_NAMES["city"], COLUMN_NAMES["street_address"], 
            COLUMN_NAMES["postal_code"], f"{COLUMN_NAMES['total_births']} {year}",
            f"{COLUMN_NAMES['csections']} {year}", f"{COLUMN_NAMES['csection_rate']} {year}", 
            COLUMN_NAMES["ik"], COLUMN_NAMES["location_number"]]

    num_hospitals = len(result_dict[keys[0]])
    try:
        with open(os.path.join(OUTPUT_DIR, str(year), f"full_list.txt"), "w") as f:
            for hospital_num in range(num_hospitals):
                line = "  -  ".join([f"{key}: {result_dict[key][hospital_num]}" for key in keys])
                f.write(line + "\n")
    except Exception as e:
        logging.error(f"Error writing full_list file: {e}")
        return

    try:
        with open(os.path.join(OUTPUT_DIR, str(year), f"hospital_statistics.txt"), "w") as f:
            for hospital_num in range(num_hospitals):
                if not result_dict[f"{COLUMN_NAMES['csection_rate']} {year}"][hospital_num] == NOT_ENOUGH_BIRTHS_MARKER:
                    line = "  -  ".join([f"{key}: {result_dict[key][hospital_num]}" for key in keys])
                    f.write(line + "\n")
    except Exception as e:
        logging.error(f"Error writing hospital_statistics file: {e}")
        return
    
    # Log final statistics
    total_processed = len(result_dict[COLUMN_NAMES["hospital_name"]])
    privacy_protected = sum(1 for rate in result_dict[f"{COLUMN_NAMES['csection_rate']} {year}"] 
                           if rate == NOT_ENOUGH_BIRTHS_MARKER)
    logging.info(f"Processing completed: {total_processed} hospitals total, {privacy_protected} hospitals of those with not enough births to report statistics")
    print(f"Processing completed successfully!")
    print(f"   {total_processed} hospitals processed")
    print(f"   {privacy_protected} hospitals with not enough births to report statistics")
    print(f"   Output saved to: {OUTPUT_DIR}/{year}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process C-section rates by year.")
    parser.add_argument("--year", type=int, default=DEFAULT_YEAR, help="Year to process")
    args = parser.parse_args()
    year = args.year
    os.makedirs(f'output/{year}', exist_ok=True)
    setup_logger(f'output/{year}/process_hospital_data.log')
    main(year)
