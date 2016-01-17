import requests
import re

import xlsxwriter
import pickle, sys

URL = "http://www.weimar-in.de/01news/01news.php?site={0}&searchstring=&newscat=#01jumpnews"

REGEX_HEADING = r"<h2>([\s\S]*?)<\/h2>"
REGEX_REPORTS = r"</b>([\s\S]*?)<b>"


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def replaceUmlauts(data):
    data = data.replace("&auml;", "ä")
    data = data.replace("&ouml;", "ö")
    data = data.replace("&uuml;", "ü")
    data = data.replace("&szlig;", "ß")
    data = data.replace("&Auml;", "Ä")
    data = data.replace("&Ouml;", "Ö")
    data = data.replace("&Uuml;", "U")

    data = data.replace("\r", "")
    data = data.replace("\n", "")

    return data

picklelist = []


for i in range(1, 662):
    r = requests.get(URL.format(i))
    
    heading = re.findall(REGEX_HEADING, r.text)
    reports = re.findall(REGEX_REPORTS, r.text)

    try:
        heading = ''.join(e for e in heading[0] if e.isalnum())
    except:
        heading = "EMPTY"

    for report in reports:
        content = replaceUmlauts(striphtml(report))

        pickledict = {  "heading": heading,
                        "date": None,
                        "text": content,
                        "streets": [],
                        "locations": [],    
                        "confidence": 0.5
                    }

        picklelist.append(pickledict)

fd = open("raw.pickle", "wb")
pickle.dump(picklelist, fd)

