"""Review public preferred interfaces and refresh the session quantity index."""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import UTC, datetime
from typing import Any

from curation_support import RETURN_ROOT, checkpoint


def main() -> None:
    """Preserve definition variants and flag compatibility conditions for review."""
    session = json.loads((RETURN_ROOT / "SESSION.json").read_text(encoding="utf-8"))
    preferred: dict[str, dict[str, Any]] = {}
    for entry in session["completed_batches"]:
        batch = json.loads((RETURN_ROOT.parent / entry["bundle"]).read_text(encoding="utf-8-sig"))
        for record in batch["models"]:
            preferred[record["id"]] = record
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in preferred.values():
        for port in record["variables"]:
            grouped[port["quantity_id"]].append(dict(model_id=record["id"], revision=record["revision"], **port))
    quantities = []
    for quantity, ports in sorted(grouped.items()):
        units = sorted({port["unit"] for port in ports})
        if len(units) != 1:
            raise ValueError(f"Unexpected unit disagreement for {quantity}: {units}")
        quantities.append(dict(quantity_id=quantity, unit=units[0],
                               definitions=sorted({port["definition"] for port in ports}),
                               dimensions=sorted({port["dimensions"] for port in ports}),
                               uses=[dict(model_id=port["model_id"], revision=port["revision"], symbol=port["symbol"],
                                          role=port["role"], domain=port["domain"], context=port["context"]) for port in ports]))
    notes = [
        "Index rebuilt from preferred revisions. Historical observed_wave_frequency r1 said strictly positive; r2 explicitly permits the wave-comoving zero phase-crossing rate. No positive-only downstream wave_frequency binding is allowed at zero without checking its domain.",
        "wave_phase_speed identifies a phase feature, with medium/mode/state/frame compatibility required. pulse_propagation_speed is separate: echo timing cannot silently use phase speed in a dispersive medium.",
        "phase_refractive_index is wavelength/mode/state-specific. A shared quantity ID does not establish that two ports refer to the same actual material or wavelength. Ordinary n>=1 profiles are narrower than the positive-index homogeneous-path profile.",
        "focal_length is signed paraxial effective focal length. Telescope component identity, surrounding medium and wavelength must match; f-number excludes back focal length and a negative focal length. Thin-lens center and mirror vertex coincide with their ideal reference planes only under the stated approximations.",
        "object_distance and image_distance retain real-is-positive conventions. Refracting-interface image side and reflecting-mirror image side differ geometrically; component and side context must travel with a binding. Axial apparent depth is not transverse image height.",
        "signed_optical_surface_curvature is outgoing-center-positive for a transmitted surface, including zero for a plane. signed_spherical_mirror_radius uses concave-positive mirror convention. No raw equality binding between their sign conventions is authorized.",
        "Angular magnification uses the instrument-specific angular reference. Telescope incoming distant-field angle and magnifier unaided-near-point angle are different context instances; no direct equality binding follows from their common dimensionless quantity ID. Neither is transverse magnification.",
        "optical_power is reciprocal length, not watts. The contact-lens family contains signed powers at a common wavelength/medium and supports cancellation to zero; no finite focal length exists for an afocal total.",
        "geometric_ray_path_length, optical_path_length, object/image conjugate distances and acoustic_target_range all have length units but different meanings and signs. No unit-only aliases were introduced.",
        "wave_period is retained only as an overlap record, not new coverage. A period refers to one complete repeat; neither an arbitrary duration nor a zero-frequency observation supplies a finite cycle period.",
        "All quantity definitions remain proposals. This review finds no conflicting units within a proposed quantity; it does not instantiate systems, validate any real-world composition, or approve a central vocabulary extension."
    ]
    report = dict(checked_utc=datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
                  scope="Preferred local revisions including flagged duplicate for history; all variants retained, not silently merged.",
                  quantities=quantities, review_notes=notes)
    (RETURN_ROOT / "QUANTITY-REVIEW.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint(quantity_inventory=quantities,
               duplicate_check="Compared supplied 218-record inventory, runtime snapshot and own returns. Confirmed computer-science--clock-cycle-time@r1 overlap; period reciprocal r2 flags it. Inventory is a dated incomplete snapshot; no global uniqueness claimed.")
    print(json.dumps(dict(preferred_ids=len(preferred), quantities=len(quantities), review_file="returns/QUANTITY-REVIEW.json"), indent=2))


if __name__ == "__main__":
    main()
