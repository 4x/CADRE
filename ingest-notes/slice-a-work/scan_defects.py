"""Scan CFA-L3 records for placeholder markers and phantom guard citations."""

import glob
import json
import re

for path in sorted(
    glob.glob("from-offline-curation-workers/financial-analysis-cfa-l3-*/bundle.json")
):
    with open(path, encoding="utf-8", errors="replace") as fh:
        bundle = json.load(fh)
    for model in bundle["models"]:
        blob = json.dumps(model)
        if re.search(r"laceholder|TODO|FIXME|\bTBD\b|\bXXX\b", blob):
            print(f"{model['id']}: SUSPICIOUS-MARKER")
        guards = " | ".join(model["guards"])
        for case in model["rejection_cases"]:
            for cited in re.findall(
                r"[Gg]uard ([A-Za-z0-9_+*/<>=! .()-]+?) violated", case["reason"]
            ):
                cited = cited.strip()
                if cited and cited not in guards:
                    print(f"{model['id']}: cites [{cited}] not in guards [{guards}]")
print("SCAN-DONE")
