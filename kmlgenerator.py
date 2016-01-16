from pykml.factory import KML_ElementMaker as KML
from pykml.factory import ATOM_ElementMaker as ATOM
from pykml.factory import GX_ElementMaker as GX
from lxml import etree

import json

output = json.load(open("merged_output.json", "r"))

fld = KML.Folder()


for report in output:
    if report["confidence"] <= 0.1:
        continue

    #print(len(report["locations"]))
    if len(report["locations"]) > 0:
        loc = report["locations"][0][0]

        if loc == 0:
            #print(loc)
            continue

        pm = KML.Placemark(KML.name(""),
                            KML.Point(
                                KML.coordinates(str(loc[0]) + "," + str(loc[1]))
                            ))

        #print(etree.tostring(pm, pretty_print=True))

        fld.append(pm)
        # print("narf")

fd = open("output.kml", "wb")
fd.write(etree.tostring(fld))
fd.close()