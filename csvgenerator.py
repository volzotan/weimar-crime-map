import json

output = json.load(open("merged_output.json", "r"))

print("X;Y;street;category")

for report in output: #[:10]:
    if report["confidence"] <= 0.1:
        continue

    #print(len(report["locations"]))
    if len(report["locations"]) > 0:
        locs2 = report["locations"]

        category = report["category"]
        category = max(category, key=category.get) # category with most hits

        street = ""

        try: 
            street = report["streets"][0]
        except:
            pass

        for locs1 in locs2:
            loc = locs1[0]
            
            if loc == 0:
                print(locs2)
                continue

            try:
                print("{0};{1};{2};{3}".format(loc[0], loc[1], street, category))
                pass
            except Exception as e:
                print(loc)
                raise e

#fd = open("output.kml", "wb")
#fd.write(etree.tostring(fld))
#fd.close()