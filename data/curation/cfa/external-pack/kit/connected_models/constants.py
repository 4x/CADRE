"""Named physical constants resolved inside expressions.

Universal fixed values live here, versioned with the runtime: expressions name
them instead of inlining magic literals, and the engine converts them through
the registry unit scales like any other quantity. Case- or material-specific
fitted values stay input variables; only universal constants belong here.
"""

from dataclasses import dataclass

from .contracts import UNITS, ModelError, finite


@dataclass(frozen=True)
class Constant:
    """One registry constant: SI value, unit key, provenance, and stability."""

    value: float
    unit: str
    source: str
    exact: bool  # True when the value is definitive and never changes on CODATA updates.


CONSTANTS = {
    # Mathematical, nearest double.
    "pi": Constant(3.141592653589793, "1", "math.pi", True),
    # Universal physical constants, CODATA 2022. Sigma and Avogadro are exact
    # via the SI defining constants; G is measured.
    "stefan_boltzmann": Constant(5.670374419e-8, "W/(m2*K^4)", "CODATA 2022", True),
    "gravitational_constant": Constant(6.67430e-11, "m3/(kg*s^2)", "CODATA 2022", False),
    "avogadro": Constant(6.02214076e23, "1/mol", "SI defining constant", True),
    "speed_of_light": Constant(299792458, "m/s", "SI defining constant", True),
}


def validate_constants(table: dict[str, Constant]) -> None:
    """Reject unusable constant entries: non-identifiers, unknown units, bad values."""
    for name, constant in table.items():
        if not name.isidentifier():
            raise ModelError(f"Constant name {name!r} is not a valid expression identifier.")
        if constant.unit not in UNITS:
            raise ModelError(f"Constant {name!r} uses unknown unit {constant.unit!r}.")
        finite(constant.value, f"Constant {name}")
        if not isinstance(constant.source, str) or not constant.source.strip():
            raise ModelError(f"Constant {name!r} needs a provenance source.")


validate_constants(CONSTANTS)

CONSTANT_DIMENSIONS = {name: UNITS[constant.unit].dimensions for name, constant in CONSTANTS.items()}
CONSTANT_VALUES = {name: constant.value * UNITS[constant.unit].scale for name, constant in CONSTANTS.items()}
# Raw SI values for display-unit curation checks: reference/rejection cases are
# stated in display units, so they resolve constants without canonical scaling.
CONSTANT_DISPLAY_VALUES = {name: constant.value for name, constant in CONSTANTS.items()}


def constants_json() -> dict[str, dict[str, object]]:
    """Project the table for kits and inspection without engine internals."""
    return {name: {"value": constant.value, "unit": constant.unit, "source": constant.source, "exact": constant.exact}
            for name, constant in CONSTANTS.items()}
