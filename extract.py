"""
extract.py
Module for extracting statistics and clinic data from XML files.
"""
import xml.etree.ElementTree as ET
import os
from typing import Tuple, Optional
from config import TARGET_TAG_STATISTIC, TARGET_VALUE, DATA_DIR, PRIVACY_PROTECTION_VALUE, XML_FILE_SUFFIX
import logging

def get_relevant_node(tree_of_interest: ET.ElementTree, target_val: str, target_tag: str) -> Tuple[list, list]:
    """
    Find all elements with a specific tag and value, and return their parents and the elements themselves.
    """
    target_elem_list = []
    parent_map = {child: parent for parent in tree_of_interest.iter() for child in parent}
    for elem in tree_of_interest.iter():
        if elem.tag == target_tag:
            if (elem.text or "").strip() == target_val:
                target_elem_list.append(elem)
    if len(target_elem_list) != 0:
        parent_list = [parent_map.get(target_elem) for target_elem in target_elem_list]
        return parent_list, target_elem_list
    else:
        return [], []

def get_hospital_statistic(IK: str, Standortnummer: str, year: int) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Extract birth statistics for a hospital from its XML file.
    Returns (total births, number of C-sections, C-section rate) or Datenschutz if protected.
    Handles file and XML errors gracefully.
    """
    path = os.path.join(DATA_DIR, f"xml_{year}", f"{IK}-{Standortnummer}-{year}-das.xml")
    try:
        quality_results_tree = ET.parse(source=path)
        quality_results_root = quality_results_tree.getroot()
    except (FileNotFoundError, ET.ParseError) as e:
        logging.error(f"Error reading/parsing {path}: {e}")
        return None, None, None
    Krankenhausstatistiken, _ = get_relevant_node(tree_of_interest=quality_results_root, target_val=TARGET_VALUE,
                                                  target_tag=TARGET_TAG_STATISTIC)
    if Krankenhausstatistiken:
        if len(Krankenhausstatistiken) != 1:
            logging.error(f"There are multiple instances of Krankenhausstatistik for the hospital "
                            f"with IK {IK} and Standortnummer {Standortnummer}")
        for Krankenhausstatistik in Krankenhausstatistiken:
            Fallzahl = Krankenhausstatistik.find('Fallzahl')
            if Fallzahl is None:
                Fallzahl_Datenschutz = Krankenhausstatistik.find('Fallzahl_Datenschutz')
                if Fallzahl_Datenschutz is not None:
                    return PRIVACY_PROTECTION_VALUE, PRIVACY_PROTECTION_VALUE, PRIVACY_PROTECTION_VALUE
                else:  # There were not enough births in the hospital to report the number of births
                    logging.info(f"Not enough births in hospital with IK {IK} and Standortnummer {Standortnummer} to report statistics.")
                    return None, None, None
            Grundgesamtheit = Fallzahl.findtext('Grundgesamtheit')
            Beobachtete_Ereignisse = Fallzahl.findtext('Beobachtete_Ereignisse')
            try:
                rate = 100 * round(int(Beobachtete_Ereignisse) / int(Grundgesamtheit), 2)
            except (TypeError, ValueError, ZeroDivisionError):
                rate = None
            return Grundgesamtheit, Beobachtete_Ereignisse, rate
    else:
        logging.info(f"The hospital with IK {IK} and Standortnummer {Standortnummer} does not have an obstetrics department.")
        return None, None, None

def get_clinic_data(IK: str, Standortnummer: str, year: int) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    """
    Extract clinic contact data from its XML file.
    Returns (name, town, street name, house number, zip code).
    Handles file and XML errors gracefully.
    """
    path = os.path.join(DATA_DIR, f"xml_{year}", f"{IK}-{Standortnummer}-{year}-{XML_FILE_SUFFIX}")
    try:
        clinic_data_tree = ET.parse(source=path)
        clinic_data_root = clinic_data_tree.getroot()
    except (FileNotFoundError, ET.ParseError) as e:
        logging.error(f"Error reading/parsing {path}: {e}")
        return None, None, None, None
    Krankenhauskontaktdaten = clinic_data_root.find(".//Standortkontaktdaten")
    if Krankenhauskontaktdaten is None:
        Krankenhauskontaktdaten = clinic_data_root.find(".//Krankenhauskontaktdaten")
    if Krankenhauskontaktdaten is None:
        logging.error(f"No Krankenhauskontaktdaten found for hospital with IK {IK} and Standortnummer {Standortnummer}")
        return None, None, None, None
    Krankenhausname = Krankenhauskontaktdaten.findtext("Name")
    Addresse = Krankenhauskontaktdaten.find('Kontakt_Zugang')
    if Addresse is None:
        logging.error(f"No Kontakt_Zugang found for hospital with IK {IK} and Standortnummer {Standortnummer}")
        return Krankenhausname, None, None, None
    Ort = Addresse.findtext('Ort')
    strasse = Addresse.findtext('Strasse')
    hausnummer = Addresse.findtext('Hausnummer')
    
    PLZ = Addresse.findtext('Postleitzahl')
    return clean_clinic_data(IK, Standortnummer, Krankenhausname, Ort, strasse, hausnummer, PLZ)


def clean_clinic_data(ik: str, standortnummer: str, krankenhausname: str, ort: str, strasse: str, hausnummer: str, plz: str):
    """
    Clean the contact data, as some fields may contain extraneous information.
    This function was created through an iterative process because the data in the xml files was not always consistent,
    therefore this might need to be repeated for future years.
    For this reason, logging has been put in place.
    """
    if "(" in strasse:
        logging.info(f"For the hospital with IK {ik} and Standortnummer {standortnummer}, the street name was "
                     f"changed from : {strasse} to {strasse.split("(")[0].strip()}")
        strasse = strasse.split("(")[0].strip()
    if any(char.isdigit() for char in strasse):
        # get the index of the first digit
        index = next(i for i, char in enumerate(strasse) if char.isdigit())
        logging.info(f"For the hospital with IK {ik} and Standortnummer {standortnummer}, the street name was "
                     f"changed from : {strasse} to {strasse[:index].strip()}")
        strasse = strasse[:index].strip()
    Strasse_und_Hausnummer = None
    if strasse and hausnummer:
        Strasse_und_Hausnummer = strasse + " " + hausnummer
    if "/" in ort:
        logging.info(f"For the hospital with IK {ik} and Standortnummer {standortnummer}, the city name was "
                     f"changed from : {ort} to {ort.split('/')[0].strip()}")
        ort = ort.split("/")[0].strip()

    return krankenhausname, ort, Strasse_und_Hausnummer, plz
        