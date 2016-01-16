#/bin/sh

python3 scraper.py              #                   --> raw.pickle
python3 weighter.py             # raw.pickle        --> weighted.pickle
sh ./extract_streets.sh         # xapi_export.osm   --> streets.csv
python3 streetconverter.py      # streets.csv       --> streets.json
python3 merger.py               # weighted.pickle / streets.json --> merged_output.json