import csv
import json

def generate_aliases(name, depth=1):
    name = name.lower()
    aliases = [name]

    if "-" in name:
        aliases.append(name.replace("-", " "))

    if " " in name:
        aliases.append(name.replace(" ", ""))
        aliases.append(name.replace(" ", "-"))

    if "ß" in name:
        aliases.append(name.replace("ß", "ss"))

    if "ss" in name:
        aliases.append(name.replace("ss", "ß"))

    if "straße" in name or "strasse" in name:
        aliases.append(name.replace("straße", "str"))
        aliases.append(name.replace("strasse", "str"))
        aliases.append(name.replace("straße", "-straße"))
        aliases.append(name.replace("strasse", "-strasse"))

    merger = []
    if depth > 0:
        for alias in aliases:
            merger.extend(generate_aliases(alias, depth=depth-1))
    else:
        merger = aliases

    return list(set(merger))

container = {}

with open("streets.csv", "r") as csvfile:
    streetreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    for row in streetreader:
        name = row[6]
        lat = row[2] 
        lon = row[3]

        # streetname 'markt' results in problems
        if name is "markt" or name is "Markt":
            continue

        if name not in container:
            container[name] = {}
            container[name]["coordinates"] = [(lat, lon)]
            container[name]["aliases"] = generate_aliases(name)
        else:
            container[name]["coordinates"].append((lat, lon))

json.dump(container, open("streets.json", "w"))