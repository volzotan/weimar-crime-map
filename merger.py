import json, pickle
import sys

example = {     "heading": None,
                "date": None,
                "text": None,
                "streets": [],
                "locations": [],    
                "confidence": 0.5
            }

SPECIAL_LOCATIONS = [   ("atrium"       , "Friedensstraße", 11.328813, 50.984910),
                        ("herderplatz"  , "Kaufstraße",     11.329757, 50.981215),
                        ("theaterplatz" , "Wielandstraße",  11.325680, 50.979871)
                    ]            

picklelist  = pickle.load(open("weighted.pickle", "rb"))
streets     = json.load(open("streets.json", "r"))

changed_streets = 0
changed_speciallocations = 0

for report in picklelist:
    if report["confidence"] <= 0.1:
        #continue
        pass
    for street_tuple in streets.items():
        streetname = street_tuple[0]
        aliases = street_tuple[1]["aliases"]
        match = False
        for alias in aliases:
            if alias in report["text"].lower():
                match = True
                break

        if match:
            report["streets"].append(streetname)
            report["locations"].append(street_tuple[1]["coordinates"])
            changed_streets += 1
    for speciallocation in SPECIAL_LOCATIONS:
        if speciallocation[0] in report["text"].lower():
            report["streets"].append(speciallocation[1])
            report["locations"].append([[speciallocation[2], speciallocation[3]]])
            changed_speciallocations += 1

print(changed_streets)
print(changed_speciallocations)

json.dump(picklelist, open("merged_output.json", "w"))

# for report in picklelist:
#     if len(report["streets"]) > 0:
#         print(report["streets"])