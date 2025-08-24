# Analyse der Kaiserschnitt-Rate - Deutsche Krankenhäuser

## Projektübersicht

Dieses Projekt analysiert die Raten von Kaiserschnitten (C-Section) in deutschen Krankenhäusern anhand strukturierter XML-Daten aus öffentlich verfügbaren Qualitätsberichten der Krankenhäuser. Die Analyse extrahiert, verarbeitet und transformiert Krankenhausstatistiken in umsetzbare Erkenntnisse für Mütter und Eltern, die eine informierte Entscheidung über ihren bevorzugten Geburtsort treffen möchten.

Kaiserschnitt-Karte für 2023: [Link](https://www.google.com/maps/d/u/0/edit?mid=1WXZwVSqyD3cogWQ6pkaoDNaeN_GhZN4&usp=sharing)

Kaiserschnitt-Karte für 2022: [Link](https://www.google.com/maps/d/u/0/edit?mid=1DFZHtyN63QHYThzrG3YtIJKUQQH8U24&usp=sharing)


## Warum dieses Projekt?
Weltweit nehmen die Raten von Kaiserschnitten zu, ohne dass ein signifikanter Nutzen für die Gesundheit der Frauen oder ihrer Kinder erkennbar wäre. Die Weltgesundheitsorganisation (WHO) zielt darauf ab, diese Rate zu senken, und hat [Empfehlungen](https://www.who.int/publications/i/item/9789241550338) zu nicht-klinischen Interventionen veröffentlicht, um unnötige Kaiserschnitte zu reduzieren.

Das Statistische Bundesamt [berichtete](https://www.destatis.de/DE/Presse/Pressemitteilungen/2023/02/PD23_N009_231.html), dass sich im Vergleich zu 1991 die Kaiserschnittrate im Jahr 2021 von 15,3 % auf 30,9 % verdoppelte. Die WHO [berichtete 2015](https://www.who.int/publications/i/item/WHO-RHR-15.02), dass es keine Hinweise darauf gibt, dass eine Erhöhung der Kaiserschnittrate über 10 % hinaus die mütterliche oder die Neugeborenensterblichkeit verbessert. 
Wenn 30 % der Geburten ein Kaiserschnitt sind und 10 % ausreichen, um die maternale und perinatale Sterblichkeit zu senken, dann werden zwei von drei Kaiserschnitten in Deutschland potenziell ohne medizinische Notwendigkeit durchgeführt. Meine Analysen der Jahre 2022 und 2023 zeigen einen Anstieg der Kaiserschnittraten in Krankenhäusern von 32,3 % im Jahr 2022 auf 33,0 % im Jahr 2023.

Allerdings ist die Sterblichkeit nicht das einzige Anliegen.
Nichtsdestotrotz sind [medizinisch nicht notwendige Kaiserschnitte ein Problem der öffentlichen Gesundheit und ihre Rate sollte verringert werden](https://onlinelibrary.wiley.com/doi/full/10.1002/hsr2.1274). 
Kaiserschnittgeburten wurden mit Plazentationsproblemen und höheren Raten an Hysterektomien in Verbindung gebracht. Es gibt auch negative gesundheitliche Auswirkungen für die per Kaiserschnitt geborenen Kinder. Diese Kaiserschnitt-Karte wurde erstellt, um Menschen eine Wahl zu geben und sie über die gesundheitliche Versorgungssituation in Deutschland zu informieren.

Wenn du dich für eine Geburt außerhalb eines Krankenhauses interessierst und mehr über die Sicherheit dieser Option erfahren möchtest, lies den [QUAG-Bericht zu Haus- und Geburtshausgeburten](https://www.quag.de/downloads/Quag-Zu_Hause_und_im_Geburtshaus.pdf).

## Projektstruktur

```
CSectionRate_Germany/
├── analysis.py                     # Funktionen zur Datenanalyse und Visualisierung
├── config.py                       # Konfigurationskonstanten und -einstellungen
├── create_kml.py                   # Erstellung von KML-Dateien für Google Maps
├── extract_from_xml.py             # XML-Parsing und Datenextraktion
├── get_gps_coordinates.py          # Abruf von Standortdaten für Krankenhäuser
├── process_hospital_data.py        # Hauptverarbeitungspipeline
├── requirements.txt                # Python-Abhängigkeiten
├── run_complete_analysis.py        # Einstiegspunkt zum Ausführen der Analyse
├── test_ci_cd.py                   # Kompatibilitätstests
├── test_plausibility.py            # Tests der Datenintegrität
└── output/$year$/
   ├── analysis_report.md           # Kurzer Überblick über die Ergebnisse
   ├── complete_analysis.log        # Detailliertes Protokoll des Analyse-Laufs
   ├── hospital_csection_rates.kml  # Kartendatei für Google Maps
   ├── full_list.txt                # Vollständige Krankenhausliste
   ├── hospital_statistics.csv      # Zentrale Analyseergebnisse
   ├── hospital_statistics.txt      # Nur öffentliche Daten
   └── visualizations/
      ├── rate_distribution.png     # Vergleich der Kaiserschnittraten zwischen Krankenhäusern
      └── size_vs_rate.png          # Zusammenhang zwischen Krankenhausgröße und Kaiserschnittrate
```

## Wie du die Krankenhausdaten selbst herunterlädst:
- Gehe zu https://qb-datenportal.g-ba.de
- Scrolle nach unten zu „Zum Auftragsformular“ unter der Überschrift „Qualitätsberichte“
- Folge den weiteren Anweisungen auf der Website
---

## Schnellstart

### Voraussetzungen
- Python 3.11+
- pandas
- pytest (für Tests)
- matplotlib und numpy für Grafiken

### Installation
1. Repository klonen
2. Virtuelle Umgebung einrichten:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```
3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

### Verwendung
Lade die XML-Daten herunter (siehe [hier](Wie du die Krankenhausdaten selbst herunterlädst)) und organisiere sie wie folgt:
1. Erstelle einen Ordner namens `data` in deinem Projektverzeichnis.
2. Lege darin einen Unterordner namens `xml_$year$` an (ersetze `$year$` durch das relevante Jahr, z. B. `xml_2023`).
3. Lege die heruntergeladenen XML-Dateien im Ordner `data/xml_$year$/` ab.

```bash
python run_complete_analysis.py --year 2023
```

## Quellenhinweise
Standortdaten von OpenStreetMap, verfügbar unter der Open Database License. 
Krankenhausstatistiken von www.g-ba.de/qualitaetsberichte (Qualitätsberichte der Krankenhäuser)

## Lizenz
[MIT](LICENSE)

## Zukünftige Schritte
- Ausreißer-Krankenhäuser (mit zu wenigen Geburten) aus den Grafiken entfernen, da sie das Histogramm und die Korrelationsgrafik verzerren.
- Statistische Signifikanz dafür berechnen, dass Krankenhäuser über der durchschnittlichen deutschen Kaiserschnittrate liegen
- Karte erstellen, die Risiken eines Kaiserschnitts in einer Region zeigt
- Individualisierte Karten in Betracht ziehen, z. B. für VBACs (Vaginalgeburt nach Kaiserschnitt)
- Veränderungen von Krankenhäusern im Zeitverlauf nachverfolgen (Es werden mehr Daten benötigt, da gemäß Qualitätsberichten die während Covid erhobenen Daten nicht vergleichbar sind)

## Hinweise
- Da nur Krankenhäuser mit geburtshilflichen Abteilungen analysiert wurden, die die genaue Anzahl der Geburten und Kaiserschnitte gemeldet haben (bei einer geringen Anzahl von Geburten muss das Krankenhaus die Daten aus Gründen der Patient*innenvertraulichkeit nicht melden), ist der folgende Hinweis erforderlich:
Die Qualitätsberichte der Krankenhäuser werden vorliegend nur teilweise bzw. auszugsweise genutzt. Eine vollständige unveränderte Darstellung der Qualitätsberichte der Krankenhäuser erhalten Sie unter www.g-ba.de/qualitaetsberichte.
- Da die (GPS-)Standortdaten nicht aus den Qualitätsberichten, sondern aus einer externen Quelle (OpenStreetMap) stammen, ist der folgende Hinweis erforderlich:
Die Qualitätsberichte der Krankenhäuser werden vorliegend in Verbindung mit anderen Erkenntnisquellen genutzt. Die angegebenen Empfehlungen und Ergebnisse stellen daher keine authentische Wiedergabe der Qualitätsberichte dar. Eine vollständige Darstellung der Qualitätsberichte der Krankenhäuser erhalten Sie unter www.g-ba.de/qualitaetsberichte.
