from pykml.factory import KML_ElementMaker as KML
from pykml.factory import ATOM_ElementMaker as ATOM
from pykml.factory import GX_ElementMaker as GX
from lxml import etree

import json

output = json.load(open("merged_output.json", "r"))

fld = KML.Folder()

counter = 0

for report in output:
    if report["confidence"] <= 0.1:
        continue

    #print(len(report["locations"]))
    if len(report["locations"]) > 0:
        locs2 = report["locations"]

        for locs1 in locs2:
            loc = locs1[0]
            
            if loc == 0:
                print(locs2)
                continue

            try:
                pm = KML.Placemark(KML.name(""),
                                    KML.Point(
                                        KML.coordinates(str(loc[0]) + "," + str(loc[1]))
                                    ))
            except Exception as e:
                print(loc)
                raise e

            fld.append(pm)
            counter += 1

fd = open("output.kml", "wb")
fd.write(etree.tostring(fld))
fd.close()

print(counter)