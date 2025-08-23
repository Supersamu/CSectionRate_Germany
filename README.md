# C-Section Rate Analysis - German Hospitals

## Project Overview

This project analyzes cesarean section (C-section) rates across German hospitals using structured XML data from publically available hospital quality reports. The analysis extracts, processes, and transforms hospital statistics into actionable insights for mothers and parents that want to make an informed choice about their preferred location of delivery.
C-section map for 2023: [Link](https://www.google.com/maps/d/u/0/edit?mid=1WXZwVSqyD3cogWQ6pkaoDNaeN_GhZN4&usp=sharing)
C-section map for 2022: [Link](https://www.google.com/maps/d/u/0/edit?mid=1DFZHtyN63QHYThzrG3YtIJKUQQH8U24&usp=sharing)

## Why this project?
There is a worldwide increase in caesarean section rates, without significant benefit to the health of women or their babies. The World Health Organization (WHO) aims to reduce this rate and has published [recommendations](https://www.who.int/publications/i/item/9789241550338) on non-clinical interventions to reduce unnecessary caesarean sections.

The Federal Statistical Office of Germany (Statistisches Bundesamt) [reported](https://www.destatis.de/DE/Presse/Pressemitteilungen/2023/02/PD23_N009_231.html) that, compared to 1991, the C-section rates in 2021 doubled from 15.3% to 30.9%. Meanwhile, the WHO [reported in 2015](https://www.who.int/publications/i/item/WHO-RHR-15.02) that >there is no evidence that increasing the C-section rate above 10% improves maternal or newborn mortality. 
If 30% of births are a C-section and 10% are enough to reduce the maternal and perinatal mortality rates, then two out of three C-sections in Germany are potentially being performed without medical necessity. 

However, mortality is not the only concern.
Nevertheless, [medically unnecessary C-sections are a public health concern and their rate should be diminished](https://onlinelibrary.wiley.com/doi/full/10.1002/hsr2.1274). 
C-section deliveries have been linked to placentation problems and higher rates of hysterectomies. There are also negative health implications for the babies born by C-section. This C-section map is created to give people a choice and to inform them about the health care situation in Germany.

If you are interested in giving birth outside of a hospital and want to know more about the safety of this option, read the [QUAG report on home and birth center deliveries](https://www.quag.de/downloads/Quag-Zu_Hause_und_im_Geburtshaus.pdf).

## Project Structure

```
CSectionRate_Germany/
├── analysis.py                     # Data analysis and visualization functions
├── config.py                       # Configuration constants and settings
├── create_kml.py                   # KML files generation for Google Maps
├── extract_from_xml.py             # XML parsing and data extraction functions
├── get_gps_coordinates.py          # Retrieval of location data for hospitals
├── process_hospital_data.py        # Main processing pipeline
├── requirements.txt                # Python dependencies
├── run_complete_analysis.py        # Entry point for running the analysis
├── test_ci_cd.py                   # Compatibility testing
├── test_plausibility.py            # Data Integrity testing
└── output/$year$/
   ├── analysis_report.md           # Short overview of findings
   ├── complete_analysis.log        # Detailed log of analysis run
   ├── hospital_csection_rates.kml  # Map file for Google Maps
   ├── full_list.txt                # Complete hospital listing
   ├── hospital_statistics.csv      # Main analysis results
   ├── hospital_statistics.txt      # Public data only
   └── visualizations/
      ├── rate_distribution.png     # Comparison of Csection rates across hospitals
      └── size_vs_rate.png          # Correlation between hospital size and Csection rate
```

## How to Download the Hospital Data yourself:
- Go to https://qb-datenportal.g-ba.de
- Scroll down towards "Zum Auftragsformular" under the header "Qualitätsberichte"
- Follow further instructions on the website
---

## Quick Start

### Prerequisites
- Python 3.11+
- pandas
- pytest (for testing)
- matplotlib and numpy for plotting

### Installation
1. Clone the repository
2. Set up virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
Download the XML data (see [here](How to Download the Hospital Data yourself)) and organize it as follows:
1. Create a folder named `data` in your project directory.
2. Inside `data`, create a subfolder named `xml_$year$` (replace `$year$` with the relevant year, e.g., `xml_2023`).
3. Place the downloaded XML files into the `data/xml_$year$/` folder.

```bash
python run_complete_analysis.py --year 2023
```

## Attributions
Location Data from OpenStreetMap, available under the Open Database License. 
Hospital Statistics from www.g-ba.de/qualitaetsberichte (Qualitätsberichte der Krankenhäuser)

## License
[MIT](LICENSE)
