"""Correct a missed cross-domain duplicate without modifying another curator's ID."""

import copy
import json

from curation_support import ACCESS_DATE, RETURN_ROOT, write_batch

prior = json.loads((RETURN_ROOT / "waves-and-optics-codex-b02" / "bundle.json").read_text(encoding="utf-8"))
record = copy.deepcopy(next(item for item in prior["models"] if item["id"].endswith("--period-frequency-reciprocal")))
record["revision"] = "r2"
record["title"] = "Period-frequency reciprocal: overlap correction, not new coverage"
record["summary"] = "Corrects b02 period-frequency-reciprocal@r1's missed inventory overlap. The same full-cycle frequency/period reciprocity already appears as computer-science--clock-cycle-time@r1. Treat this record as evidence/metadata correction only and exclude it from new-model coverage/import; the existing catalog ID is not revised."
record["integration"]["duplicate_of"] = ["computer-science--clock-cycle-time@r1"]
record["integration"]["gaps"].append("KNOWN SCIENTIFIC OVERLAP: do not import as a new relationship. The catalog's processor-clock profile and this wave/oscillator profile share the same cycle-frequency reciprocal definition; a domain label or differently scoped quantity ID does not establish another law. Central review can consider broader quantity aliases/evidence, without automatically binding a processor instance to an acoustic wave.")
record["limitations"].append("This record is retained solely to correct the prior return's missed catalog overlap; numerical validity does not make it new scientific coverage.")
record["sources"].append({
    "id": "uvm-clock-reciprocity-overlap", "kind": "primary",
    "title": "Clayton Cafiero / University of Vermont: Basic performance metrics (duplicate confirmation only)",
    "url": "https://www.uvm.edu/~cbcafier/cs2210/content/02_basics_of_architecture/basic_performance_metrics.html",
    "version": "Published 2026-10-05 as displayed; official course HTML inspected 2026-11-03; adaptation credit to Patterson and Hennessy / Surya Malik and Clayton Cafiero recorded on page",
    "accessed": ACCESS_DATE, "locator": "Basic performance metrics: CPU time, CPI, MIPS; clock-cycle-time bullet after performance equation",
    "evidence": "The directly inspected course page defines clock-cycle duration as reciprocal clock frequency. It confirms the supplied inventory's computer-science--clock-cycle-time@r1 is the same full-cycle reciprocal definition under a processor-specific context.",
    "license": "Specific terms not inspected; page attribution/adaptation statement observed, no reuse license established. Terms unknown; page authorship and public access alone do not resolve textbook/adaptation rights.",
    "redistribution": "Only short original overlap paraphrase and source link, no copied course material. No permission or legal clearance claimed."
})

path = write_batch(7, [record], [
    dict(title="Withdraw period-frequency reciprocal from new coverage",
         reason="waves-and-optics--period-frequency-reciprocal@r1 in b02 should have been deferred as an overlap of supplied inventory computer-science--clock-cycle-time@r1 (1/f, cycles/s to duration of one complete cycle). This batch retains r2 under our own ID solely to make duplicate_of explicit and preserve the correction history. Do not import either wave-period revision as a new relationship. Additional OpenStax wave/oscillator evidence may inform a central generic scope/quantity-alias review; no other curator's ID/content is changed. Preferred new-coverage count is now eighteen, not nineteen.",
         source_urls=[record["sources"][0]["url"], record["sources"][1]["url"], record["sources"][2]["url"], "https://www.d.umn.edu/~gshute/arch/performance-equation.html"])
], "Duplicate correction only: mark the period-frequency definition as overlapping computer-science--clock-cycle-time@r1 and exclude it from new scientific coverage. All original archives remain intact. Eighteen nonduplicate relationships plus one explicitly flagged overlap ID remain, with two correction revisions across the session.",
"Corrected our b02 period-frequency-reciprocal@r1 after a full cross-domain inventory comparison, not just waves/optics title matching. Read the inventory's exact f/period quantity definitions and directly inspected its UVM clock-cycle bullet and UMN Clock Time section on 2026-11-03; both explicitly state the reciprocal. Existing ID and its source/content are not modified and no scientific approval is inferred from inventory intake. r2 changes evidence/overlap metadata, not arithmetic. UVM exact URL is in sources; additional directly inspected confirmation: https://www.d.umn.edu/~gshute/arch/performance-equation.html, Clock Time paragraph. Initial numerical validation results appended after execution. Review this correction together with b02; do not count domain-specific renaming as new coverage.")
print(path)
