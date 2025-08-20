"""
config.py
Configuration constants for the C-section rate analysis project.
"""

# =========================
# Directory and File Paths
# =========================
DEFAULT_YEAR = 2022
DATA_DIR = "data"
OUTPUT_DIR = "output"

# =========================
# XML Processing Constants
# =========================
TARGET_TAG_STATISTIC = "Ergebnis_ID"
TARGET_VALUE = "52249"  # Number of C-sections

# =========================
# Output Column Names
# =========================
COLUMN_NAMES = {
    "hospital_name": "Name der Klinik",
    "city": "Ort", 
    "street_address": "Straße und Hausnummer",
    "postal_code": "PLZ",
    "total_births": "Geburten gesamt",
    "csections": "Anzahl Kaiserschnitte", 
    "csection_rate": "Kaiserschnitt %",
    "ik": "IK",
    "location_number": "Standortnummer"
}

# =========================
# File Extensions
# =========================
DAS_FILE_SUFFIX = "das.xml"
XML_FILE_SUFFIX = "xml.xml"

# =========================
# Logging Configuration
# =========================
LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'

# =========================
# Processing Configuration
# =========================
PROGRESS_INTERVAL = 100  # Log progress every N hospitals
PRIVACY_PROTECTION_VALUE = "Datenschutz"  # Placeholder for privacy-protected values in xml-files
