"""Independent research audit of dimensions, inverse identities and archive fidelity.

This reads only this curator's public artifacts and the supplied vocabulary. It
does not alter the toolkit, registry, packed batches or any scientific record.
The inverse checks establish algebraic consistency, not source/physical approval.
"""

from __future__ import annotations

import ast
import hashlib
import json
from datetime import UTC, datetime
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Any
from zipfile import ZipFile

from curation_support import RETURN_ROOT

Dim = tuple[Fraction, ...]
DIMENSION_COUNT = 4
ZERO_DIM: Dim = (Fraction(0),) * DIMENSION_COUNT
INVERSE_LENGTH_DIM: Dim = (Fraction(0), Fraction(-1), Fraction(0), Fraction(0))
SMALL_GRID = tuple(Fraction(value) for value in ("0.05", "0.1", "0.2", "0.4", "0.75", "2"))


def require(condition: bool, message: str) -> None:
    """Fail a research audit explicitly with enough context to diagnose it."""
    if not condition:
        raise ValueError(message)


def unit_dimension(unit: str, vocabulary: dict[str, Any]) -> Dim:
    """Use snapshot dimensions, plus the explicitly proposed coherent 1/m unit."""
    if unit == "1/m":
        return INVERSE_LENGTH_DIM
    entry = vocabulary["units"][unit]
    require(entry["scale"] == 1, f"Non-base unit needs explicit canonical review: {unit}")
    return tuple(Fraction(value) for value in entry["dimensions"])


def expression_dimension(node: ast.AST, bindings: dict[str, Dim], literals: dict[Fraction, Dim]) -> Dim:
    """Compute dimensions independently for the arithmetic used by these returns."""
    if isinstance(node, ast.Expression):
        return expression_dimension(node.body, bindings, literals)
    if isinstance(node, ast.Name):
        return bindings[node.id]
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return literals.get(Fraction(str(node.value)), ZERO_DIM)
    if isinstance(node, ast.UnaryOp):
        return expression_dimension(node.operand, bindings, literals)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.func.id == "sum":
            dimensions = [expression_dimension(arg, bindings, literals) for arg in node.args]
            require(all(item == dimensions[0] for item in dimensions), "sum dimensions disagree")
            return dimensions[0]
        if node.func.id == "len":
            return ZERO_DIM
    if isinstance(node, ast.BinOp):
        left = expression_dimension(node.left, bindings, literals)
        right = expression_dimension(node.right, bindings, literals)
        if isinstance(node.op, (ast.Add, ast.Sub)):
            require(left == right, f"Addition mixes dimensions: {ast.unparse(node)}")
            return left
        if isinstance(node.op, ast.Mult):
            return tuple(a + b for a, b in zip(left, right, strict=True))
        if isinstance(node.op, ast.Div):
            return tuple(a - b for a, b in zip(left, right, strict=True))
        if isinstance(node.op, ast.Pow) and isinstance(node.right, ast.Constant):
            require(right == ZERO_DIM, "Dimensional exponent")
            return tuple(value * Fraction(str(node.right.value)) for value in left)
    raise ValueError(f"Unreviewed dimensional notation: {ast.dump(node)}")


def audit_dimensions(record: dict[str, Any], vocabulary: dict[str, Any]) -> dict[str, Any]:
    """Check one research expression and its physical-constant dimensions."""
    bindings = {port["symbol"]: unit_dimension(port["unit"], vocabulary) for port in record["variables"]}
    literals = {Fraction(str(item["literal"])): unit_dimension(item["unit"], vocabulary) for item in record["constants"]}
    rhs = expression_dimension(ast.parse(record["relationship"]["expression"], mode="eval"), bindings, literals)
    output = bindings[record["relationship"]["output_symbol"]]
    require(rhs == output, f"Output dimension mismatch: {record['id']}@{record['revision']}")
    for guard in record["guards"]:
        tree = ast.parse(guard, mode="eval").body
        require(isinstance(tree, ast.Compare), f"Unexpected guard form: {guard}")
        left = expression_dimension(tree.left, bindings, literals)
        right_node = tree.comparators[0]
        right = expression_dimension(right_node, bindings, literals)
        is_zero = isinstance(right_node, ast.Constant) and right_node.value == 0
        require(left == right or is_zero, f"Guard mixes dimensions: {record['id']} {guard}")
    return dict(identity=f"{record['id']}@{record['revision']}", rhs_dimensions=[str(value) for value in rhs],
                output_dimensions=[str(value) for value in output], guard_dimensions="checked; zero comparison treated dimensionally polymorphic",
                numerical_basis="All returned length/time/dimensionless units have scale 1; proposed 1/m is coherent research notation, not an installed registry edit.")


def audit_imaging_inverses() -> dict[str, Any]:
    """Verify original reciprocal equations and both conjugate/focal inverses exactly."""
    count = 0
    for focal, distance in product((*SMALL_GRID, *(-value for value in SMALL_GRID)), SMALL_GRID):
        if focal == distance:
            continue
        image = focal * distance / (distance - focal)
        require(1 / distance + 1 / image == 1 / focal, "Gaussian source residual")
        require(focal * image / (image - focal) == distance, "Gaussian object inverse")
        require(distance * image / (distance + image) == focal, "Gaussian focal inverse")
        magnification = -image / distance
        require(-magnification * distance == image, "Image inverse from magnification")
        require(-image / magnification == distance, "Object inverse from magnification")
        count += 1
    return dict(cases=count, arithmetic="exact Fraction; both focal signs and real/virtual images", singularities=[
        "d_o=f: parallel rays, no finite image; not an unphysical optical system",
        "d_i=f: object at infinity; d_i=-d_o: infinite f / zero power",
        "zero conjugates/focal lengths excluded before simplification",
        "m=0 with finite nonzero conjugates: no finite solution; m=d_i=0 is outside the profile"
    ])


def audit_doppler_inverses() -> dict[str, Any]:
    """Derive observer frequencies from two emission/intersection events, then invert."""
    count = 0
    singular = 0
    speed = Fraction(300)
    emitted = Fraction(100)
    initial_separation = Fraction(3000)
    for source_velocity, observer_velocity in product((Fraction(-120), Fraction(0), Fraction(60)),
                                                       (Fraction(-300), Fraction(-150), Fraction(0), Fraction(60), Fraction(450))):
        if observer_velocity == -speed:
            observed = Fraction(0)
            require(observed * (speed - source_velocity) / emitted - speed == observer_velocity, "Zero-rate observer inverse")
            reconstructed_speed = (observed * source_velocity + emitted * observer_velocity) / (observed - emitted)
            require(reconstructed_speed == speed, "Zero-rate medium speed inverse")
            singular += 1
        else:
            first_arrival = initial_separation / (speed + observer_velocity)
            second_arrival = (initial_separation + (speed - source_velocity) / emitted) / (speed + observer_velocity)
            observed = 1 / (second_arrival - first_arrival)
            require(observed == emitted * (speed + observer_velocity) / (speed - source_velocity), "Doppler event-derived source residual")
            require(observed * (speed - source_velocity) / (speed + observer_velocity) == emitted, "Source frequency inverse")
            require(speed - emitted * (speed + observer_velocity) / observed == source_velocity, "Source velocity inverse")
            require(observed * (speed - source_velocity) / emitted - speed == observer_velocity, "Observer velocity inverse")
            if observed != emitted:
                reconstructed_speed = (observed * source_velocity + emitted * observer_velocity) / (observed - emitted)
                require(reconstructed_speed == speed, "Medium-speed inverse")
            else:
                require(observer_velocity == -source_velocity, "Equal frequencies must be comoving in this geometry")
                singular += 1
        count += 1
    return dict(cases=count, arithmetic="exact event intersections, not only frequency-formula replay", special_or_ambiguous_cases=singular,
                finding="r1 observer subsonic cap unnecessary; r2 includes approaching u_o=450>v=300 and u_o=-v zero-rate limit. Source remains subsonic.",
                singularities=["u_s=v excluded denominator", "u_o=-v: f_o=0, f_s and u_s individually underdetermined",
                               "f_o=f_s and u_o=-u_s: v undetermined; otherwise inconsistent",
                               "u_o inverse permits f_o=0 and uniquely gives -v"])


def audit_refracting_inverses() -> dict[str, Any]:
    """Verify spherical-interface and lens-maker inverse notes using rational grids."""
    surface_count = 0
    matched_count = 0
    for first, second, radius, distance in product((Fraction(1), Fraction(3, 2)),
                                                  (Fraction(1), Fraction(3, 2)),
                                                  (Fraction(-1, 10), Fraction(1, 10)), SMALL_GRID):
        denominator = (second - first) * distance - first * radius
        if denominator == 0:
            continue
        image = second * radius * distance / denominator
        require(first / distance + second / image == (second - first) / radius, "Interface source residual")
        require(first * radius * image / ((second - first) * image - second * radius) == distance, "Interface object inverse")
        radius_denominator = first * image + second * distance
        if first == second:
            require(image == -distance and radius_denominator == 0, "Index-match radius degeneracy")
            matched_count += 1
        else:
            require((second - first) * distance * image / radius_denominator == radius, "Interface radius inverse")
        surface_count += 1
    curvature_count = 0
    plane_count = 0
    for first, second, curvature, distance in product((Fraction(1), Fraction(3, 2)),
                                                     (Fraction(1), Fraction(3, 2)),
                                                     (Fraction(-10), Fraction(0), Fraction(10)), SMALL_GRID):
        denominator = (second - first) * curvature * distance - first
        if denominator == 0:
            continue
        image = second * distance / denominator
        require(first / distance + second / image == (second - first) * curvature, "Curvature source residual")
        require(first * image / ((second - first) * curvature * image - second) == distance,
                "Curvature-form object inverse")
        if first != second:
            recovered = (first * image + second * distance) / ((second - first) * distance * image)
            require(recovered == curvature, "Curvature inverse including the plane surface")
        else:
            require(image == -distance, "Matched-index curvature degeneracy")
        if curvature == 0:
            require(image == -second * distance / first, "Signed normal-view apparent-depth relation")
            plane_count += 1
        curvature_count += 1
    lens_count = 0
    for lens_index, medium_index, first_curve, second_curve in product((Fraction(3, 2), Fraction(2)),
                                                                     (Fraction(1), Fraction(3, 2)),
                                                                     (Fraction(-4), Fraction(0), Fraction(4)),
                                                                     (Fraction(-3), Fraction(0), Fraction(3))):
        contrast = lens_index / medium_index - 1
        if contrast == 0 or first_curve == second_curve:
            continue
        focal = 1 / (contrast * (first_curve - second_curve))
        require(second_curve + 1 / (focal * contrast) == first_curve, "Lens first-curvature inverse")
        require(first_curve - 1 / (focal * contrast) == second_curve, "Lens second-curvature inverse")
        require(medium_index * (1 + 1 / (focal * (first_curve - second_curve))) == lens_index, "Lens-index inverse")
        lens_count += 1
    return dict(surface_cases=surface_count, matched_index_degeneracies=matched_count, lens_maker_cases=lens_count,
                curvature_form_cases=curvature_count, plane_cases_in_curvature_grid=plane_count,
                arithmetic="exact Fraction; both radius/focal signs, index orderings, individually plane surfaces",
                singularities=["Interface object focus: no finite d_i", "Matched indices: radius not identifiable from d_i=-d_o",
                               "Lens index match or equal curvatures: zero power/infinite f", "A single zero curvature is permitted, not a zero radius"])


def audit_magnifier_inverses() -> dict[str, Any]:
    """Check finite-view magnifier inverse denominators and the ell=f degeneracy."""
    count = 0
    degenerate = 0
    for near, focal, separation, viewing in product((Fraction(1, 4), Fraction(3, 10)),
                                                    (Fraction(1, 10), Fraction(1, 5)),
                                                    (Fraction(0), Fraction(1, 50), Fraction(1, 10), Fraction(1, 5)),
                                                    (Fraction(3, 10), Fraction(1, 2), Fraction(1))):
        if viewing < near or viewing <= separation:
            continue
        magnification = near / viewing * (1 + (viewing - separation) / focal)
        require((viewing - separation) / (magnification * viewing / near - 1) == focal, "Magnifier focal inverse")
        if separation == focal:
            require(magnification == near / focal, "Magnifier viewing-distance degeneracy")
            degenerate += 1
        else:
            require(near * (focal - separation) / (magnification * focal - near) == viewing, "Magnifier viewing-distance inverse")
        count += 1
    return dict(cases=count, ell_equals_f_degeneracies=degenerate, arithmetic="exact Fraction",
                source_review="Source's near-point image-distance sign slip not propagated; near point supplied as N rather than hard-coded 25 cm. General eye spacing does not obey the close-eye magnification bound.")


def audit_archives(paths: list[Path]) -> list[dict[str, Any]]:
    """Verify two-member ZIPs and semantic agreement after pack normalization."""
    reports = []
    for path in paths:
        archive_path = RETURN_ROOT / f"{path.parent.name}-return.zip"
        with ZipFile(archive_path) as archive:
            require(sorted(archive.namelist()) == ["bundle.json", "manifest.json"], f"Unexpected archive members: {archive_path}")
            packed_bundle = archive.read("bundle.json")
            require(json.loads(packed_bundle) == json.loads(path.read_text(encoding="utf-8-sig")), f"Packed scientific content differs: {path}")
            manifest = json.loads(archive.read("manifest.json"))
            require(isinstance(manifest, dict), "Invalid manifest structure")
        reports.append(dict(batch_id=path.parent.name, zip=str(archive_path.relative_to(RETURN_ROOT.parent)),
                            members=["bundle.json", "manifest.json"], bundle_bytes=path.stat().st_size,
                            sha256=hashlib.sha256(archive_path.read_bytes()).hexdigest(), local_bundle_semantically_matches_zip=True,
                            byte_identical=packed_bundle == path.read_bytes(),
                            normalization_note="Pack emits normalized JSON; whitespace/key order/line endings may differ from local authoring JSON. Toolkit ZIP validator checks the packed manifest integrity."))
    return reports


def main() -> None:
    """Save a reproducible, compact research audit without asserting approval."""
    vocabulary = json.loads((RETURN_ROOT.parent / "data" / "curation" / "runtime-vocabulary.json").read_text(encoding="utf-8"))
    paths = sorted(RETURN_ROOT.glob("waves-and-optics-codex-b*/bundle.json"))
    dimension_reports = []
    preferred: dict[str, dict[str, Any]] = {}
    for path in paths:
        batch = json.loads(path.read_text(encoding="utf-8-sig"))
        for record in batch["models"]:
            dimension_reports.append(audit_dimensions(record, vocabulary))
            preferred[record["id"]] = record
    report = dict(
        checked_utc=datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        status="algebraic-and-transfer-checks-passed; source/scientific/rights review still pending",
        command="uv --cache-dir .uv-cache run --no-env-file returns/numerical_review.py",
        dimension_checks=dimension_reports,
        gaussian_and_magnification=audit_imaging_inverses(), doppler=audit_doppler_inverses(),
        refracting_elements=audit_refracting_inverses(), simple_magnifier=audit_magnifier_inverses(),
        archives=audit_archives(paths),
        preferred_candidates=[dict(id=record["id"], revision=record["revision"], duplicate_of=record["integration"]["duplicate_of"],
                                   new_coverage=not record["integration"]["duplicate_of"]) for record in preferred.values()],
        limitations=["Dimension checker uses mass,length,time,currency axes and treats pure zero as dimensionally polymorphic in inequalities.",
                     "Coherent research 1/m is checked locally; this does not extend the installed registry or make records runtime-ready.",
                     "Grid checks verify the documented inverse algebra and singularities, not source truth, optical approximation error, actual parameter measurements or physical instance compatibility.",
                     "Published rounded numerical evidence remains as reported in the data; these rational checks do not replace it with recomputed expected values."])
    destination = RETURN_ROOT / "NUMERICAL-REVIEW.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(report=str(destination), dimension_checks=len(dimension_reports), archives=len(paths),
                          distinct_ids=len(preferred), new_coverage=sum(not item["integration"]["duplicate_of"] for item in preferred.values()),
                          inverse_case_groups={"imaging": report["gaussian_and_magnification"]["cases"], "doppler": report["doppler"]["cases"],
                                               "interface_r1": report["refracting_elements"]["surface_cases"],
                                               "interface_r2": report["refracting_elements"]["curvature_form_cases"],
                                               "lens_maker": report["refracting_elements"]["lens_maker_cases"],
                                               "magnifier": report["simple_magnifier"]["cases"]}), indent=2))


if __name__ == "__main__":
    main()
