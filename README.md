# C-Section Rate Analysis - German Hospitals

## Project Overview

This project analyzes cesarean section (C-section) rates across German hospitals using structured XML data from publically available hospital quality reports. The analysis extracts, processes, and transforms hospital statistics into actionable insights for mothers and parents that want to make an informed choice about their preferred location of delivery.

## Project Structure

```
CSectionRate_Germany/
├── config.py              # Configuration constants and settings
├── extract.py              # XML parsing and data extraction functions
├── process_hospital_data.py # Main processing pipeline
├── test_output_compare.py  # Automated testing suite
├── data/
│   └── xml_2023/          # Input XML files (hospital data)
└── output/
    ├── hospital_statistics_2023.csv      # Main analysis results
    ├── full_list_2023.txt # Complete hospital listing
    └── hospital_statistics_2023.txt # Public data only
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

```bash
python run_complete_analysis.py --year 2023
```

## Attributions
Location Data from OpenStreetMap, available under the Open Database License. 
Hospital Statistics from www.g-ba.de/qualitaetsberichte (Qualitätsberichte der Krankenhäuser)

## Why this project?
There is a worldwide increase in caesarean section rates, without significant benefit to the health of women or their babies. The World Health Organization (WHO) aims to reduce this rate and has published [recommendations](https://www.who.int/publications/i/item/9789241550338) on non-clinical interventions to reduce unnecessary caesarean sections.

The Federal Statistical Office of Germany (Statistisches Bundesamt) [reported](https://www.destatis.de/DE/Presse/Pressemitteilungen/2023/02/PD23_N009_231.html)that, compared to 1991, the C-section rates in 2021 doubled from 15.3% to 30.9%. Meanwhile, the WHO [reported in 2015](https://www.who.int/publications/i/item/WHO-RHR-15.02) that >there is no evidence that increasing the C-section rate above 10% improves maternal or newborn mortality. 
If 30% of births are a C-section and 10% are enough to reduce the maternal and perinatal mortality rates, then two out of three C-sections in Germany are potentially being performed without medical necessity. 

However, mortality is not the only concern.
Nevertheless, [> medically unnecessary C-sections are a public health concern and their rate should be diminished](https://onlinelibrary.wiley.com/doi/full/10.1002/hsr2.1274). 
C-section deliveries have been linked to placentation problems and higher rates of hysterectomies. There are also negative health implications for the babies born by C-section. This C-section map is created to give people a choice and to inform them about the health care situation in Germany.

If you are interested in giving birth outside of a hospital and want to know more about the safety of this option, read the [QUAG report on home and birth center deliveries](https://www.quag.de/downloads/Quag-Zu_Hause_und_im_Geburtshaus.pdf).

## License
[LICENSE](MIT)
