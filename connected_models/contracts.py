"""Small scalar contracts; context belongs to each port, not to a whole node."""

from dataclasses import dataclass
import math

Dimensions = tuple[int, int, int, int]  # Mass, length, time, currency.
DIMENSIONLESS: Dimensions = (0, 0, 0, 0)
MASS: Dimensions = (1, 0, 0, 0)
LENGTH: Dimensions = (0, 1, 0, 0)
TIME: Dimensions = (0, 0, 1, 0)
VELOCITY: Dimensions = (0, 1, -1, 0)
ACCELERATION: Dimensions = (0, 1, -2, 0)
FORCE: Dimensions = (1, 1, -2, 0)
ENERGY: Dimensions = (1, 2, -2, 0)
MONEY: Dimensions = (0, 0, 0, 1)
PRICE: Dimensions = (-1, -2, 2, 1)
INVERSE_MONEY: Dimensions = (0, 0, 0, -1)
JOULES_PER_KWH = 3_600_000
VOCABULARY_PROFILE = "cm-vocabulary/mechanics-1+finance-1"
DIMENSION_AXES = ("mass", "length", "time", "currency")
NUMERICAL_BASIS = f"kWh, m, s, USD; mass base = {JOULES_PER_KWH} kg"


class ModelError(ValueError):
    """A user-actionable contract, binding, or calculation error."""


class NumericalError(ModelError):
    """The numerical backend cannot evaluate a value within its declared limits."""


@dataclass(frozen=True)
class Unit:
    """A ratio unit in the kWh, metre, second, USD numerical basis.

    Mass is measured internally in 3,600,000 kg so that energy remains in kWh.
    This preserves all legacy energy/currency scales while closing SI algebra.
    """

    dimensions: Dimensions
    scale: float


UNITS = {
    "1": Unit(DIMENSIONLESS, 1.0),
    "percent": Unit(DIMENSIONLESS, 0.01),
    "kWh": Unit(ENERGY, 1.0),
    "Wh": Unit(ENERGY, 0.001),
    "USD": Unit(MONEY, 1.0),
    "USD/kWh": Unit(PRICE, 1.0),
    "kg": Unit(MASS, 1 / JOULES_PER_KWH),
    "g": Unit(MASS, 0.001 / JOULES_PER_KWH),
    "m": Unit(LENGTH, 1.0),
    "cm": Unit(LENGTH, 0.01),
    "km": Unit(LENGTH, 1000.0),
    "s": Unit(TIME, 1.0),
    "min": Unit(TIME, 60.0),
    "h": Unit(TIME, 3600.0),
    "m/s": Unit(VELOCITY, 1.0),
    "km/h": Unit(VELOCITY, 1000 / 3600),
    "m/s^2": Unit(ACCELERATION, 1.0),
    "N": Unit(FORCE, 1 / JOULES_PER_KWH),
    "J": Unit(ENERGY, 1 / JOULES_PER_KWH),
    "kJ": Unit(ENERGY, 1000 / JOULES_PER_KWH),
    # Finance/economics batch (finance-1): period counts and abstract units are
    # dimensionless by design. Financial "years"/"periods" are discrete counts,
    # deliberately NOT physical time: they never convert to s/min/h.
    "periods": Unit(DIMENSIONLESS, 1.0),
    "periods/year": Unit(DIMENSIONLESS, 1.0),
    "years": Unit(DIMENSIONLESS, 1.0),
    "unit": Unit(DIMENSIONLESS, 1.0),
    "USD/unit": Unit(MONEY, 1.0),
    "unit^2/USD": Unit(INVERSE_MONEY, 1.0),
}

# Meaning is independent of dimension: heat and electricity cannot bind implicitly.
MEANINGS = {
    "delivered_heat": ENERGY,
    "electricity_consumption": ENERGY,
    "seasonal_performance": DIMENSIONLESS,
    "electricity_tariff": PRICE,
    "operating_cost": MONEY,
    "annual_saving": MONEY,
    "discount_rate": DIMENSIONLESS,
    "period_count": DIMENSIONLESS,
    "present_value": MONEY,
    "upfront_cost": MONEY,
    "net_present_value": MONEY,
    "mass": MASS,
    "position": LENGTH,
    "displacement": LENGTH,
    "vertical_displacement": LENGTH,
    "duration": TIME,
    "speed": VELOCITY,
    "velocity": VELOCITY,
    "acceleration": ACCELERATION,
    "gravitational_field_strength": ACCELERATION,
    "force": FORCE,
    "translational_kinetic_energy": ENERGY,
    "gravitational_potential_energy_change": ENERGY,
    "mechanical_work": ENERGY,
    # Finance/economics batch (finance-1): adopted curator quantity IDs verbatim
    # for the nine reviewed b01 records. Several are instance-level names that a
    # future canonicalization pass should consolidate; they bind conservatively
    # (exact meaning/context match) until then.
    "future_value": MONEY,
    "periodic_payment": MONEY,
    "effective_rate": DIMENSIONLESS,
    "nominal_rate": DIMENSIONLESS,
    "periodic_rate": DIMENSIONLESS,
    "real_rate": DIMENSIONLESS,
    "inflation_rate": DIMENSIONLESS,
    "required_return": DIMENSIONLESS,
    "growth_rate": DIMENSIONLESS,
    "annualized_geometric_growth_rate": DIMENSIONLESS,
    "compounding_frequency": DIMENSIONLESS,
    "periods_per_year": DIMENSIONLESS,
    "elapsed_time": DIMENSIONLESS,
    "expected_dividend": MONEY,
    "signed_point_price_elasticity": DIMENSIONLESS,
    "signed_arc_price_elasticity": DIMENSIONLESS,
    "quantity_price_derivative": INVERSE_MONEY,
    "unit_price": MONEY,
    "economic_quantity": DIMENSIONLESS,
    "economic_series_level": MONEY,
    "gross_domestic_product_current_price": MONEY,
    "personal_consumption_expenditure": MONEY,
    "gross_private_domestic_investment": MONEY,
    "government_consumption_and_gross_investment": MONEY,
    "exports_goods_services": MONEY,
    "imports_goods_services": MONEY,
}
ORIGINS = frozenset({"fixture", "user-scenario", "observation", "generated", "derived"})


def finite(value: float, label: str) -> float:
    """Reject booleans, non-numbers, infinities and NaNs before numerical use."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ModelError(f"{label}: expected a finite number.")
    try:
        result = float(value)
    except (ValueError, OverflowError) as exc:
        raise NumericalError(f"{label}: number is outside the supported range.") from exc
    if not math.isfinite(result):
        raise NumericalError(f"{label}: expected a finite number.")
    return result


@dataclass(frozen=True)
class Port:
    """An input/output meaning, ratio unit and exact bounded context role."""

    meaning: str
    unit: str
    context: str

    def validate(self) -> None:
        """Check a declaration even when it has no binding yet."""
        if self.meaning not in MEANINGS or self.unit not in UNITS:
            raise ModelError(f"Unsupported meaning/unit: {self.meaning}/{self.unit}.")
        if MEANINGS[self.meaning] != UNITS[self.unit].dimensions:
            raise ModelError(f"Meaning {self.meaning} cannot use unit {self.unit}.")
        if not isinstance(self.context, str) or not self.context:
            raise ModelError("Every port requires an explicit context.")

    def require_compatible(self, target: "Port") -> None:
        """Check port compatibility without inventing a numerical value during compilation."""
        self.validate()
        target.validate()
        if (self.meaning, self.context) != (target.meaning, target.context):
            raise ModelError(f"Cannot bind {self} to {target}: meaning/context mismatch.")


@dataclass(frozen=True)
class Value:
    """An attributed scalar value; context/evidence survive scenario reuse."""

    amount: float
    port: Port
    origin: str
    evidence: str

    def bind(self, target: Port) -> float:
        """Validate meaning/context and convert compatible ratio units explicitly."""
        self.port.require_compatible(target)
        if self.origin not in ORIGINS or not self.evidence:
            raise ModelError("Every value needs a supported origin and evidence.")
        amount = finite(self.amount, "Input value")
        converted = finite(amount * UNITS[self.port.unit].scale / UNITS[target.unit].scale, "Converted input")
        if target.meaning == "period_count" and not (converted * UNITS[target.unit].scale).is_integer():
            raise ModelError("Period count must be an integer number of annual periods.")
        return converted


@dataclass(frozen=True)
class Reference:
    """Explicit dependency on another node instance's sole output."""

    node: str


@dataclass(frozen=True)
class Model:
    """A revisioned scalar model with an allowlisted expression and evidence."""

    id: str
    version: str
    inputs: dict[str, Port]
    output: Port
    expression: str
    guards: tuple[str, ...]
    source: str
    assumptions: tuple[str, ...]
    status: str = "fixture"

    @property
    def key(self) -> str:
        """Return a revision-specific reference, never a latest-version alias."""
        return f"{self.id}@{self.version}"


@dataclass(frozen=True)
class Node:
    """An independent instance with explicit values or upstream bindings."""

    id: str
    model: str
    bindings: dict[str, Value | Reference]
    solve_for: str | None = None
    relation: str = "equal"


@dataclass(frozen=True)
class Composition:
    """A bounded scenario request, its instances, and its requested results."""

    id: str
    nodes: tuple[Node, ...]
    outputs: tuple[str, ...]
    purpose: str = "fixture"
