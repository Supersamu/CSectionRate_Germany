"""
create_kml.py
Create KML files from hospital statistics CSV data
"""
import os
import pandas as pd
import argparse
from config import DEFAULT_YEAR, OUTPUT_DIR, COLUMN_NAMES, NOT_ENOUGH_BIRTHS_MARKER


def create_kml_from_csv(df, year):
    """Create a KML file from CSV data with hospitals categorized by C-section rates.
    The KML file can be uploaded to Google Maps to create a custom map."""
        
    kml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>C-Section Rates in German Hospitals</name>
    <description>Hospitals are grouped by the percentage of C-Sections that are performed. Location Data from OpenStreetMap, available under the Open Database License. Hospital Statistics from www.g-ba.de/qualitaetsberichte (Qualitätsberichte der Krankenhäuser, {year})/</description>
    <Style id="icon-1899-558B2F-nodesc-normal">
      <IconStyle>
        <color>ff2f8b55</color>
        <scale>1</scale>
        <Icon>
          <href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
        <hotSpot x="32" xunits="pixels" y="64" yunits="insetPixels"/>
      </IconStyle>
      <LabelStyle>
        <scale>0</scale>
      </LabelStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <Style id="icon-1899-558B2F-nodesc-highlight">
      <IconStyle>
        <color>ff2f8b55</color>
        <scale>1</scale>
        <Icon>
          <href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
        <hotSpot x="32" xunits="pixels" y="64" yunits="insetPixels"/>
      </IconStyle>
      <LabelStyle>
        <scale>1</scale>
      </LabelStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <StyleMap id="icon-1899-558B2F-nodesc">
      <Pair>
        <key>normal</key>
        <styleUrl>#icon-1899-558B2F-nodesc-normal</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#icon-1899-558B2F-nodesc-highlight</styleUrl>
      </Pair>
    </StyleMap>
    <Style id="icon-1899-A52714-nodesc-normal">
      <IconStyle>
        <color>ff1427a5</color>
        <scale>1</scale>
        <Icon>
          <href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
        <hotSpot x="32" xunits="pixels" y="64" yunits="insetPixels"/>
      </IconStyle>
      <LabelStyle>
        <scale>0</scale>
      </LabelStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <Style id="icon-1899-A52714-nodesc-highlight">
      <IconStyle>
        <color>ff1427a5</color>
        <scale>1</scale>
        <Icon>
          <href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
        <hotSpot x="32" xunits="pixels" y="64" yunits="insetPixels"/>
      </IconStyle>
      <LabelStyle>
        <scale>1</scale>
      </LabelStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <StyleMap id="icon-1899-A52714-nodesc">
      <Pair>
        <key>normal</key>
        <styleUrl>#icon-1899-A52714-nodesc-normal</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#icon-1899-A52714-nodesc-highlight</styleUrl>
      </Pair>
    </StyleMap>
    <Style id="icon-1899-F9A825-nodesc-normal">
      <IconStyle>
        <color>ff25a8f9</color>
        <scale>1</scale>
        <Icon>
          <href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
        <hotSpot x="32" xunits="pixels" y="64" yunits="insetPixels"/>
      </IconStyle>
      <LabelStyle>
        <scale>0</scale>
      </LabelStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <Style id="icon-1899-F9A825-nodesc-highlight">
      <IconStyle>
        <color>ff25a8f9</color>
        <scale>1</scale>
        <Icon>
          <href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
        <hotSpot x="32" xunits="pixels" y="64" yunits="insetPixels"/>
      </IconStyle>
      <LabelStyle>
        <scale>1</scale>
      </LabelStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <StyleMap id="icon-1899-F9A825-nodesc">
      <Pair>
        <key>normal</key>
        <styleUrl>#icon-1899-F9A825-nodesc-normal</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#icon-1899-F9A825-nodesc-highlight</styleUrl>
      </Pair>
    </StyleMap>
    <Style id="icon-1899-FFEA00-nodesc-normal">
      <IconStyle>
        <color>ff00eaff</color>
        <scale>1</scale>
        <Icon>
          <href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
        <hotSpot x="32" xunits="pixels" y="64" yunits="insetPixels"/>
      </IconStyle>
      <LabelStyle>
        <scale>0</scale>
      </LabelStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <Style id="icon-1899-FFEA00-nodesc-highlight">
      <IconStyle>
        <color>ff00eaff</color>
        <scale>1</scale>
        <Icon>
          <href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
        <hotSpot x="32" xunits="pixels" y="64" yunits="insetPixels"/>
      </IconStyle>
      <LabelStyle>
        <scale>1</scale>
      </LabelStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <StyleMap id="icon-1899-FFEA00-nodesc">
      <Pair>
        <key>normal</key>
        <styleUrl>#icon-1899-FFEA00-nodesc-normal</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#icon-1899-FFEA00-nodesc-highlight</styleUrl>
      </Pair>
    </StyleMap>'''

    # Create folders for each category
    categories = [
        ("<20%", "558B2F", lambda rate: rate < 20),
        ("20-30%", "FFEA00", lambda rate: 20 <= rate < 30),
        ("30-40%", "F9A825", lambda rate: 30 <= rate < 40),
        (">40%", "A52714", lambda rate: rate >= 40)
    ]
    
    rate_column = f"{COLUMN_NAMES['csection_rate']} {year}"
    
    for category_name, style_id, rate_filter in categories:
        kml_content += f'''
    <Folder>
      <name><![CDATA[{category_name}]]></name>'''
        
        # Filter hospitals for this category
        for idx, row in df.iterrows():
            try:
                # Skip privacy protected entries
                if row[rate_column] == NOT_ENOUGH_BIRTHS_MARKER:
                    continue
                    
                rate = row[rate_column]
                
                # Check if coordinates are available
                latitude = row.get('Latitude', None)
                longitude = row.get('Longitude', None)
                if latitude is not None and longitude is not None:
                    lat = float(latitude)
                    lon = float(longitude)
                    if rate_filter(rate) and lat and lon:
                        hospital_name = str(row[COLUMN_NAMES["hospital_name"]])
                        city = str(row[COLUMN_NAMES["city"]])
                        street = str(row[COLUMN_NAMES["street_address"]])
                        postal_code = str(row[COLUMN_NAMES["postal_code"]])
                        total_births = row[f"{COLUMN_NAMES['total_births']} {year}"]
                        csections = row[f"{COLUMN_NAMES['csections']} {year}"]
                        
                        # Escape XML characters
                        hospital_name = hospital_name.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        city = city.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        street = street.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        
                        description = f"""
                        <![CDATA[
                        <b>Address:</b> {street}, {postal_code} {city}<br/>
                        <b>Total Births:</b> {total_births}<br/>
                        <b>C-sections:</b> {csections}<br/>
                        <b>C-section Rate:</b> {rate}%
                        ]]>
                        """
                        
                        kml_content += f'''
      <Placemark>
        <name>{hospital_name}</name>
        <styleUrl>#icon-1899-{style_id}-nodesc</styleUrl>
        <Point>
          <coordinates>
            {lon},{lat},0
          </coordinates>
        </Point>
      </Placemark>'''
            except (ValueError, TypeError, KeyError) as e:
                # Skip rows with invalid data
                continue
        
        kml_content += '''
    </Folder>'''
    
    kml_content += '''
  </Document>
</kml>'''
    
    # Write KML file
    kml_filename = os.path.join(OUTPUT_DIR, str(year), f"hospital_csection_rates.kml")
    try:
        with open(kml_filename, 'w', encoding='utf-8') as f:
            f.write(kml_content)
        print(f"KML file created: {kml_filename}")
        return kml_filename
    except Exception as e:
        print(f"Error creating KML file: {e}")
        return None


def main(year):
    csv_file = os.path.join(OUTPUT_DIR, str(year), f"hospital_statistics.csv")

    if not os.path.exists(csv_file):
        print(f"CSV file not found: {csv_file}")
        print("Please run process_hospital_data.py first or specify a valid CSV file")
        return
    
    df = pd.read_csv(csv_file)
    os.makedirs(os.path.join(OUTPUT_DIR, str(year)), exist_ok=True)

    kml_file = create_kml_from_csv(df, year, OUTPUT_DIR)
    if kml_file:
        print(f"Success! KML file created at: {kml_file}")
    else:
        print("Failed to create KML file")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create KML from hospital statistics CSV")
    parser.add_argument("--year", type=int, default=DEFAULT_YEAR, help="Year to process")
    args = parser.parse_args()
    
    year = args.year
    main(year)
