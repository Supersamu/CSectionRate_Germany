import xml.etree.ElementTree as ET
import os
import pandas as pd
from collections import defaultdict
year = 2023
mypath = os.path.join("data", f"xml_{year}")
all_files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
result_dict = defaultdict(list)

# Define the target tag and value
target_tag_statistic = "Ergebnis_ID"
target_value = "52249"  # Number of C-sections

IK_list = []
Standortnummer_list = []


def get_relevant_node(tree_of_interest, target_val, target_tag):
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
        #print(f"<{target_tag}> with value '{target_val}' not found.")
        return None, None


def get_hospital_statistic(IK, Standortnummer):
    quality_results_tree = ET.parse(source=os.path.join("data", f"xml_{year}", f"{IK}-{Standortnummer}-{year}-das.xml"))
    quality_results_root = quality_results_tree.getroot()
    Krankenhausstatistiken, _ = get_relevant_node(tree_of_interest=quality_results_root, target_val=target_value,
                                                  target_tag=target_tag_statistic)
    if Krankenhausstatistiken is not None:
        if len(Krankenhausstatistiken) != 1:
            print(f"special case 2 {IK}; {Standortnummer}")
        for Krankenhausstatistik in Krankenhausstatistiken:
            Fallzahl = Krankenhausstatistik.find('Fallzahl')
            if Fallzahl is None:
                Fallzahl_Datenschutz = Krankenhausstatistik.find('Fallzahl_Datenschutz')
                if Fallzahl_Datenschutz is not None:
                    return "Datenschutz", "Datenschutz", "Datenschutz"
                else:
                    print(f"special case 1 {IK}; {Standortnummer}")
                    return None, None, None
            Grundgesamtheit = Fallzahl.findtext('Grundgesamtheit')
            Beobachtete_Ereignisse = Fallzahl.findtext('Beobachtete_Ereignisse')
            return Grundgesamtheit, Beobachtete_Ereignisse, "{:.0%}".format(int(Beobachtete_Ereignisse)/int(Grundgesamtheit))
    else:
        return None, None, None


def get_clinic_data(IK, Standortnummer):
    clinic_data_tree = ET.parse(source=os.path.join("data", f"xml_{year}", f"{IK}-{Standortnummer}-{year}-xml.xml"))
    clinic_data_root = clinic_data_tree.getroot()
    Krankenhauskontaktdaten = clinic_data_root.find(".//Standortkontaktdaten")
    if Krankenhauskontaktdaten is None:
        Krankenhauskontaktdaten = clinic_data_root.find(".//Krankenhauskontaktdaten")
    Krankenhausname = Krankenhauskontaktdaten.findtext("Name")
    Addresse = Krankenhauskontaktdaten.find(f'Kontakt_Zugang')
    Ort = Addresse.findtext(f'Ort')
    Strasse_und_Hausnummer = Addresse.findtext(f'Strasse') + " " + Addresse.findtext(f'Hausnummer')
    PLZ = Addresse.findtext(f'Postleitzahl')
    return Krankenhausname, Ort, Strasse_und_Hausnummer, PLZ


for file in all_files:
    if file.endswith("das.xml"):
        IK_list.append(file.split("-")[0])
        Standortnummer_list.append(file.split("-")[1])

for idx, (IK, Standortnummer) in enumerate(zip(IK_list, Standortnummer_list)):
    if idx % 100 == 0:
        print(f" Working on {idx + 1} of {len(IK_list)}")
    total_births, num_csections, rate = get_hospital_statistic(IK, Standortnummer)
    if total_births is not None:
        if os.path.isfile(os.path.join("data", f"xml_{year}", f"{IK}-{Standortnummer}-{year}-xml.xml")):
            name_hospital, town, street, zip_code = get_clinic_data(IK, Standortnummer)

            result_dict["Name der Klinik"].append(name_hospital)
            result_dict["Ort"].append(town)
            result_dict["Straße und Hausnummer"].append(street)
            result_dict["PLZ"].append(zip_code)
            result_dict[f"Geburten gesamt {year}"].append(total_births)
            result_dict[f"Anzahl Kaiserschnitte {year}"].append(num_csections)
            result_dict[f"Kaiserschnitt % {year}"].append(rate)
            result_dict["IK"].append(IK)
            result_dict["Standortnummer"].append(Standortnummer)
        else:
            print(f"special case 3 {IK}; {Standortnummer}")

df = pd.DataFrame.from_dict(result_dict)
df.to_csv(f"data_{year}.csv")

keys = ["Name der Klinik", "Ort", "Straße und Hausnummer", "PLZ", f"Geburten gesamt {year}",
        f"Anzahl Kaiserschnitte {year}", f"Kaiserschnitt % {year}", "IK", "Standortnummer"]

num_hospitals = len(result_dict[keys[0]])
with open(f"full_list_{year}.txt", "w") as f:
    for hospital_num in range(num_hospitals):
        for key in keys:
            if key != "Standortnummer":
                f.write(f"{key}: {result_dict[key][hospital_num]}  -  ")
            else:
                f.write(f"{key}: {result_dict[key][hospital_num]}")
        f.write("\n")

with open(f"list_without_data_protected_{year}.txt", "w") as f:
    for hospital_num in range(num_hospitals):
        if not result_dict[f"Kaiserschnitt % {year}"] == "Datenschutz":
            for key in keys:
                if key != "Standortnummer":
                    f.write(f"{key}: {result_dict[key][hospital_num]}  -  ")
                else:
                    f.write(f"{key}: {result_dict[key][hospital_num]}")
            f.write("\n")

"""
special case 3 260500470; 772560000
special case 1 260820514; 773704000
special case 3 260841041; 772739000
special case 3 260971937; 773625000
special case 3 261101015; 773686000
special case 3 261101311; 772832000
special case 3 261101561; 773065000
special case 3 261500416; 773081000
special case 3 261500416; 773082000

"""