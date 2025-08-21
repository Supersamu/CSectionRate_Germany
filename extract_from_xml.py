"""
extract.py
Module for extracting statistics and clinic data from XML files.
"""
import xml.etree.ElementTree as ET
import os
from typing import Tuple, Optional
from config import TARGET_TAG_STATISTIC, TARGET_VALUE, DATA_DIR, NOT_ENOUGH_BIRTHS_MARKER, XML_FILE_SUFFIX, DAS_FILE_SUFFIX
import logging

def get_relevant_node(tree_of_interest: ET.ElementTree, target_val: str, target_tag: str) -> list:
    """
    Find all elements with a specific tag and value, and return their parents and the elements themselves.
    """
    target_elem_list = []
    parent_map = {child: parent for parent in tree_of_interest.iter() for child in parent}
    for elem in tree_of_interest.iter():
        if elem.tag == target_tag:
            if (elem.text or "").strip() == target_val:
                target_elem_list.append(elem)
    parent_list = [parent_map.get(target_elem) for target_elem in target_elem_list]
    return parent_list
    

def get_hospital_statistic(IK: str, site_identifier: str, year: int) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Extract birth statistics for a hospital from its XML file.
    Returns (total births, number of C-sections, C-section rate) or Datenschutz if protected.
    Handles file and XML errors gracefully.
    """
    path = os.path.join(DATA_DIR, f"xml_{year}", f"{IK}-{site_identifier}-{year}-{DAS_FILE_SUFFIX}")
    try:
        quality_xml_tree = ET.parse(source=path)
        quality_xml_root = quality_xml_tree.getroot()
    except (FileNotFoundError, ET.ParseError) as e:
        logging.error(f"Error reading/parsing {path}: {e}")
        return None, None, None
    HospitalStatistics = get_relevant_node(tree_of_interest=quality_xml_root, target_val=TARGET_VALUE,
                                                  target_tag=TARGET_TAG_STATISTIC)
    if HospitalStatistics:
        if len(HospitalStatistics) != 1:
            logging.error(f"There are multiple instances of HospitalStatistics for the hospital "
                            f"with IK {IK} and Standortnummer {site_identifier}")
        for HospitalStatistic in HospitalStatistics:
            CaseCount = HospitalStatistic.find('Fallzahl')
            if CaseCount is None:
                CaseCountNoData = HospitalStatistic.find('Fallzahl_Datenschutz')
                if CaseCountNoData is not None:
                    logging.info(f"Not enough births in hospital with IK {IK} and Standortnummer {site_identifier} to report statistics.")
                    return NOT_ENOUGH_BIRTHS_MARKER, NOT_ENOUGH_BIRTHS_MARKER, NOT_ENOUGH_BIRTHS_MARKER
                else:
                    logging.info(f"The xml file for the hospital with IK {IK} and Standortnummer {site_identifier} does not follow the expected structure.")
                    return None, None, None
            OverallCount = CaseCount.findtext('Grundgesamtheit')
            ObservedEvents = CaseCount.findtext('Beobachtete_Ereignisse')
            try:
                rate = int(round(100* int(ObservedEvents) / int(OverallCount)))
            except (TypeError, ValueError, ZeroDivisionError) as e:
                logging.error(f"Error calculating rate for hospital with IK {IK} and Standortnummer {site_identifier}. "
                              f"ObservedEvents: {ObservedEvents}, OverallCount: {OverallCount}, Error: {e}")
                rate = None
            return OverallCount, ObservedEvents, rate
    else:
        logging.info(f"The hospital with IK {IK} and Standortnummer {site_identifier} does not have an obstetrics department.")
        return None, None, None

def get_clinic_data(IK: str, site_identifier: str, year: int) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    """
    Extract clinic contact data from its XML file.
    Returns (name, town, street name, house number, zip code).
    Handles file and XML errors gracefully.
    """
    path = os.path.join(DATA_DIR, f"xml_{year}", f"{IK}-{site_identifier}-{year}-{XML_FILE_SUFFIX}")
    try:
        hospital_xml_tree = ET.parse(source=path)
        hospital_xml_root = hospital_xml_tree.getroot()
    except (FileNotFoundError, ET.ParseError) as e:
        logging.error(f"Error reading/parsing {path}: {e}")
        return None, None, None, None
    hospital_contact_data = hospital_xml_root.find(".//Standortkontaktdaten")
    if hospital_contact_data is None:
        hospital_contact_data = hospital_xml_root.find(".//Krankenhauskontaktdaten")
    if hospital_contact_data is None:
        logging.error(f"No Krankenhauskontaktdaten found for hospital with IK {IK} and Standortnummer {site_identifier}")
        return None, None, None, None
    hospital_name = hospital_contact_data.findtext("Name")
    adress = hospital_contact_data.find('Kontakt_Zugang')
    if adress is None:
        logging.error(f"No Kontakt_Zugang found for hospital with IK {IK} and Standortnummer {site_identifier}")
        return hospital_name, None, None, None
    city = adress.findtext('Ort')
    street = adress.findtext('Strasse')
    street_number = adress.findtext('Hausnummer')
    
    postal_code = adress.findtext('Postleitzahl')
    return clean_clinic_data(IK, site_identifier, hospital_name, city, street, street_number, postal_code)


def clean_clinic_data(ik: str, site_identifier: str, hospital_name: str, city: str, street: str, street_number: str, postal_code: str):
    """
    Clean the contact data, as some fields may contain extraneous information.
    This function was created through an iterative process because the data in the xml files was not always consistent,
    therefore this might need to be repeated for future years.
    For this reason, logging has been put in place.
    """
    if "(" in street:
        logging.warning(f"For the hospital with IK {ik} and Standortnummer {site_identifier}, the street name was "
                     f"changed from : [[{street}]] to [[{street.split("(")[0].strip()}]]")
        street = street.split("(")[0].strip()
    if any(char.isdigit() for char in street):
        # get the index of the first digit
        index = next(i for i, char in enumerate(street) if char.isdigit())
        logging.warning(f"For the hospital with IK {ik} and Standortnummer {site_identifier}, the street name was "
                     f"changed from : [[{street}]] to [[{street[:index].strip()}]]")
        street = street[:index].strip()
    street_and_street_number = None
    if street and street_number:
        street_and_street_number = street + " " + street_number
    if "/" in city:
        logging.warning(f"For the hospital with IK {ik} and Standortnummer {site_identifier}, the city name was "
                     f"changed from : [[{city}]] to [[{city.split('/')[0].strip()}]]")
        city = city.split("/")[0].strip()

    return hospital_name, city, street_and_street_number, postal_code
        