import json

reports = json.load(open("merged_output.json", "r"))

confidence_levels   = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
streets           = [0, 0, 0, 0, 0, 0, 0, 0]

for report in reports:
    confidence_levels[int(report["confidence"] * 10)] += 1

    if report["confidence"] < 0.2:
        continue

    streets[int(len(report["streets"]))] += 1

    if len(report["streets"]) > 0:
        print(report["text"])
        print("\n")
        print(report["streets"])
        print("\n\n\n")

print("confidence_levels : {}".format(confidence_levels))
print("streets : {}".format(streets))
