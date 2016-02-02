import xml.etree.ElementTree as ET
import csv
from collections import defaultdict


counts = defaultdict(lambda: defaultdict(lambda: 0))

name_mapping = {
    "Bahnhof": "Schopenhauerstraße"
}

with open('output.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=';', quotechar='|')

    for row in spamreader:
        street_name = row["street"]

        if street_name in name_mapping:
            street_name = name_mapping[street_name]

        street_counts = counts[street_name]
        category_counts = street_counts[row["category"]]
        street_counts[row["category"]] = category_counts + 1
        street_counts["foundInOSM"] = 0



tree = ET.parse('qgis_project/maplayer.osm')
root = tree.getroot()
# streets = tree.findall(".//way[tag[@k=\"highway\"] and tag[@k=\"name\" and @v != \"\"]]")
streets = tree.findall(".//tag[@k=\"highway\"]/..")

print(len(streets))

for street in streets:
    found_name_tags = street.findall("./tag[@k=\"name\"]")
    if len(found_name_tags) == 1:
        street_name = found_name_tags[0].get("v")
        street_counts = counts[street_name]
        street_counts["foundInOSM"] = 1

        tag_koerperverletzung = ET.SubElement(street, 'tag')
        count_koerperverletzung = str(street_counts["körperverletzung"])
        tag_koerperverletzung.set('k', 'countKoerperverletzung')
        tag_koerperverletzung.set('v', count_koerperverletzung)

        tag_unfaelle = ET.SubElement(street, 'tag')
        count_unfaelle = str(street_counts["unfall"])
        tag_unfaelle.set('k', 'countUnfaelle')
        tag_unfaelle.set('v', count_unfaelle)

        tag_einbruch = ET.SubElement(street, 'tag')
        count_einbruch = str(street_counts["einbruch"])
        tag_einbruch.set('k', 'countEinbruch')
        tag_einbruch.set('v', count_einbruch)

        tag_diebstahl = ET.SubElement(street, 'tag')
        count_diebstahl = str(street_counts["diebstahl"])
        tag_diebstahl.set('k', 'countDiebstahl')
        tag_diebstahl.set('v', count_diebstahl)

        street_counts["foundInOSM"] = 1
        tag_all_crimes = ET.SubElement(street, 'tag')

        sum_crimes = sum(street_counts.values())-1
        count_all_cimes = str(sum_crimes)
        tag_all_crimes.set('k', 'countAllCrimes')
        tag_all_crimes.set('v', count_all_cimes)



    # ET.dump(tag_koerperverletzung)
    # ET.dump(street)


for street_counts in counts:
    if counts[street_counts]["foundInOSM"] == 0:
        print( "didn't find " + street_counts)

print("writing result to file")

# usage:
# __for diagrams__
# use attribute based on expression for diagrams as follows:
# regexp_substr( "other_tags", '\\"countKoerperverletzung\\"=>\\"(\\d*)\\"')
#
# for coloring
#  color_rgba(111,0,111,regexp_substr( "other_tags", '\\"countKoerperverletzung\\"=>\\"(\\d*)\\"'))


tree.write('qgis_project/maplayer-weighted-streets.osm')

