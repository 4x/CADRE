"""Guard/rejection coverage scan: guards never exercised by a domain case."""

import glob
import json

for path in sorted(
    glob.glob("from-offline-curation-workers/financial-analysis-cfa-l3-*/bundle.json")
):
    with open(path, encoding="utf-8", errors="replace") as fh:
        bundle = json.load(fh)
    for model in bundle["models"]:
        kinds = {c["kind"] for c in model["rejection_cases"]}
        if model["guards"] and "domain" not in kinds:
            print(f"{model['id']}: guards present, no domain case")
print("COVERAGE-DONE")
