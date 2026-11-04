"""Save a bounded, explicitly unfinished numerical investigation for the backlog."""

from __future__ import annotations

import json
from fractions import Fraction

from curation_support import RETURN_ROOT, checkpoint


def main() -> None:
    """Contrast focal definitions using independent exact paraxial ray steps."""
    height = Fraction(1, 1000)
    separation = Fraction(1, 20)
    first = Fraction(1, 10)
    second = Fraction(1, 5)
    cases = []
    for focal_one, focal_two in ((first, second), (second, first)):
        slope_after_first = -height / focal_one
        second_height = height + separation * slope_after_first
        slope_after_second = slope_after_first - second_height / focal_two
        back_focus = -second_height / slope_after_second
        effective_focus = -height / slope_after_second
        combined_focus = focal_one * focal_two / (focal_one + focal_two - separation)
        if effective_focus != combined_focus:
            raise ValueError("Ray-based effective focal comparison failed.")
        cases.append(dict(f1_m=float(focal_one), f2_m=float(focal_two), separation_m=float(separation),
                          incident_height_m=float(height), first_output_slope=str(slope_after_first),
                          second_height_m=str(second_height), exit_slope=str(slope_after_second),
                          back_focal_distance_m=str(back_focus), effective_focal_length_m=str(effective_focus)))
    report = dict(status="unfinished-research-not-a-curated-record", cases=cases,
                  source="https://wandell.github.io/FISE-git/chapters/optics-04-morelenses.html",
                  locator="Accessed 2026-11-03, section 11.2 Eqs. 11.1/11.2; 11.5.4 focal reference definitions",
                  method="Exact Fraction synthetic ray propagation: deflect at first thin lens, propagate to second, deflect again. Back focal distance uses outgoing height; effective focus uses incident height divided by net output slope for a parallel incident bundle. Independent construction is compared to the proposed focal equation, not treated as a published experiment.",
                  finding="Same 0.08 m effective focal length for either lens order, but 0.04 m versus 0.06 m back focal distance. Binding BFL to effective focal_length would therefore change the scientific meaning despite identical metre units.",
                  remaining="Before a complete record: verify source ambient-medium/sign conventions and rights, compare overlap with contact-family law, add source-grounded scope and exclusions, document all inverse singularities and independent second regime, then validate and pack a new bounded batch. No source or model approval claimed.")
    (RETURN_ROOT / "SEPARATED-LENS-FOLLOWUP.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    session = json.loads((RETURN_ROOT / "SESSION.json").read_text(encoding="utf-8"))
    deferred = session["attempted_or_deferred"]
    for item in deferred:
        if item.get("title", "").startswith("Separated thin-lens effective focal length and back focal distance:"):
            item["numerical_followup"] = "returns/SEPARATED-LENS-FOLLOWUP.json: exact ray-step order comparison; unfinished, not included as curated coverage."
    checkpoint(attempted_or_deferred=deferred)
    print("Saved two exact ray-step examples: EFL=0.08 m for both orders; BFL=0.04/0.06 m. Unfinished research only.")


if __name__ == "__main__":
    main()
