import pickle
import sys

KILLLIST = [    "apolda",
                "bad berka",
                "possendorf",
                "blankenhain",
                "auerstedt",
                "ettersburg",
                "heusdorf",
                "stobra",
                "bad sulza",
                "weimarer land",
                "pfiffelbach",
                "obernissa",
                "landstrasse",
                "landstraße"
            ]

WEIMARLIST = [  "in weimar.",
                "in weimar,",
                "von weimar"
            ]

killdict = {}
for killer in KILLLIST:
    killdict[killer] = 0
    #killdict[killer + "er"] = 0

picklelist = pickle.load(open("raw.pickle", "rb"))

for item in picklelist:
    report = item["text"].lower()
    for killer in KILLLIST:
        if killer in report:
            if not "weimar" in report:  # apoldaer strasse in weimar
                killdict[killer] += 1
                item["confidence"] = 0
            else:
                item["confidence"] = 0.1
            #     print(report)
            #     print("\n\n\n")

    for weimarword in WEIMARLIST:
        if weimarword in report:
            item["confidence"] = 0.9
            #print(report)
            #print("\n\n\n")
                
pickle.dump(picklelist, open("weighted.pickle", "wb"))
print(killdict)
