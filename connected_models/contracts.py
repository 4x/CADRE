"""Small scalar contracts; context belongs to each port, not to a whole node."""

from dataclasses import dataclass
import math

Dimensions = tuple[int, int]  # Energy, currency; annual totals carry time in context.
DIMENSIONLESS: Dimensions = (0, 0)
ENERGY: Dimensions = (1, 0)
MONEY: Dimensions = (0, 1)
PRICE: Dimensions = (-1, 1)


class ModelError(ValueError):
    """A user-actionable contract, binding, or calculation error."""


@dataclass(frozen=True)
class Unit:
    """A pinned ratio unit and its scale to kWh/USD base units."""

    dimensions: Dimensions
    scale: float


UNITS = {
    "1": Unit(DIMENSIONLESS, 1.0),
    "percent": Unit(DIMENSIONLESS, 0.01),
    "kWh": Unit(ENERGY, 1.0),
    "Wh": Unit(ENERGY, 0.001),
    "USD": Unit(MONEY, 1.0),
    "USD/kWh": Unit(PRICE, 1.0),
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
}
ORIGINS = frozenset({"fixture", "user-scenario", "observation", "generated", "derived"})


def finite(value: float, label: str) -> float:
    """Reject booleans, non-numbers, infinities and NaNs before numerical use."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ModelError(f"{label}: expected a finite number.")
    try:
        result = float(value)
    except (ValueError, OverflowError) as exc:
        raise ModelError(f"{label}: number is outside the supported range.") from exc
    if not math.isfinite(result):
        raise ModelError(f"{label}: expected a finite number.")
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


@dataclass(frozen=True)
class Value:
    """An attributed scalar value; context/evidence survive scenario reuse."""

    amount: float
    port: Port
    origin: str
    evidence: str

    def bind(self, target: Port) -> float:
        """Validate meaning/context and convert compatible ratio units explicitly."""
        self.port.validate()
        target.validate()
        if self.origin not in ORIGINS or not self.evidence:
            raise ModelError("Every value needs a supported origin and evidence.")
        if (self.port.meaning, self.port.context) != (target.meaning, target.context):
            raise ModelError(f"Cannot bind {self.port} to {target}: meaning/context mismatch.")
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


@dataclass(frozen=True)
class Composition:
    """A bounded scenario request, its instances, and its requested results."""

    id: str
    nodes: tuple[Node, ...]
    outputs: tuple[str, ...]
    purpose: str = "fixture"
