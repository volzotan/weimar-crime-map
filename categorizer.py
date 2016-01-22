import json
import pprint

CATEGORIES = {
    "unfall":       [   "unfall", "unfälle", "verkehrsteilnehmer",
                        "radfahrer", "fahrerin", 
                        "pkw", "lkw",
                        "renault", "audi", "opel", "mercedes", 
                        "ford", "golf", "toyota", "nissan", "mazda", 
                        "honda"
                    ],
    "verkehrskontrolle": [
                        "verkehrskontrolle"
                    ],
    "körperverletzung": [
                        "körperverletzung", "faustschlag", "einzuschlagen",
                        "gesichtsverletzungen", "jack russel mischling",
                        "schlägerei", "geschlagen", "körperlichen auseinandersetzung",
                        "angerempelt"
                    ],
    "belästigung":  [   "klapser", "sexuelle handlungen", "sexuell belästigt"
                    ],
    "diebstahl":    [   "dieb", "laden", "gestellt", "gestohlen",
                        "entwendeten", "verkäuferin",
                        "entwendet", "entwenden",
                        "zielgerichtet", "betrüger", "handtasche",
                        "einkaufsmarkt", "hobelbank", "geldbörse",
                        "kraftstoff", "küchenmesser", "umhängtasche"
                    ],
    "einbruch":     [   "einbruch", "einbrecher", "wohnung", "eingebrochen",
                        "wühlen", "drangen", "einzudringen", "aufbruch"
                    ],
    "vandalismus":  [   "vandalismus", "bauwalze", "graffiti", "besprüht", "getränkebecher", "müllcontainer",
                        "außenputz", "zerstachen", "zerstörten", "sachbeschädigung", "randale", "zerbrochen",
                        "abgerissen", "sachschaden", "beschädigt", "gesamtschaden", "schadenshöhe", 
                        "geschädigte", "gerissen", "fassade"
                    ],
    "waffengesetz": [   "waffengesetz", "schreckschusswaffen"
                    ],
    "drogenmissbrauch": [
                        "promille", "alcomat", "alkomat", "bierflasche", "cannabis", "marihuana",
                        "drogen"
                    ],
    "exhibitionismus": ["exhibitionist", "exhibitionismus", "erregung"],
    "brandstiftung":[   "brandstiftung"
                    ],
    "unkategorisiert": ["fahrradcodierung", "ehrlichenfinder", "rollator",
                        "rückstau", "langer esel", "brandursache", "bedeutende veranstaltung",
                        "kampfmittel", "mutti", "fraktur"
                    ]

}

reports = json.load(open("merged_output.json", "r"))
pp = pprint.PrettyPrinter(indent=4)

keywordcheck = {}
todo = 0
done = 0

def add(cat, word):
    if cat in keywordcheck:
        if word in keywordcheck[cat]:
            keywordcheck[cat][word] += 1
        else:
            keywordcheck[cat][word] = 1
    else:
        keywordcheck[cat] = {}
        add(cat, word)


for report in reports:
    text = report["text"].lower()
    identified_categories = {}
    for category in CATEGORIES:
        keywords = CATEGORIES[category]
        for keyword in keywords:
            if keyword in text:
                add(category, keyword) # debug
                if category in identified_categories:
                    identified_categories[category] += 1
                else:
                    identified_categories[category] = 1

    report["category"] = identified_categories

for report in reports:
    if(len(report["streets"]) > 0 and report["confidence"] > 0):
        if(len(report["category"]) < 1):
            print(report)
            print("\n\n\n")
            todo += 1
        else:
            done += 1

json.dump(reports, open("merged_output.json", "w"))

print("{} unkategorisiert | {} kategorisiert".format(todo, done))

pp.pprint(keywordcheck)