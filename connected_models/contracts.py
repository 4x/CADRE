"""Small scalar contracts; context belongs to each port, not to a whole node."""

from dataclasses import dataclass, field
from fractions import Fraction
import math

Dimensions = tuple[Fraction, Fraction, Fraction, Fraction]  # Mass, length, time, currency.


def _dims(mass: int | Fraction, length: int | Fraction, time: int | Fraction, currency: int | Fraction) -> Dimensions:
    """Build an exact dimension vector; rational powers need exact rationals, never floats."""
    return (Fraction(mass), Fraction(length), Fraction(time), Fraction(currency))


DIMENSIONLESS: Dimensions = _dims(0, 0, 0, 0)
MASS: Dimensions = _dims(1, 0, 0, 0)
LENGTH: Dimensions = _dims(0, 1, 0, 0)
TIME: Dimensions = _dims(0, 0, 1, 0)
VELOCITY: Dimensions = _dims(0, 1, -1, 0)
ACCELERATION: Dimensions = _dims(0, 1, -2, 0)
FORCE: Dimensions = _dims(1, 1, -2, 0)
ENERGY: Dimensions = _dims(1, 2, -2, 0)
POWER: Dimensions = _dims(1, 2, -3, 0)
MONEY: Dimensions = _dims(0, 0, 0, 1)
PRICE: Dimensions = _dims(-1, -2, 2, 1)
INVERSE_MONEY: Dimensions = _dims(0, 0, 0, -1)
INVERSE_TIME: Dimensions = _dims(0, 0, -1, 0)
JOULES_PER_KWH = 3_600_000
KCAL_IN_JOULES = 4_184
SECONDS_PER_DAY = 86_400
KLEIBER_MASS_EXPONENT = Fraction(3, 4)
VOCABULARY_PROFILE = "cm-vocabulary/mechanics-1+finance-2+economics-5+biology-3+cs-4"
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


def encode_dimensions(dims: Dimensions) -> list[object]:
    """Encode a dimension vector for JSON; whole powers stay ints, fractional powers become [num, den] pairs."""
    return [power.numerator if power.denominator == 1 else [power.numerator, power.denominator] for power in dims]


def unit_json(unit: Unit) -> dict[str, object]:
    """Encode a unit for JSON manifests with exact dimension powers."""
    return {"dimensions": encode_dimensions(unit.dimensions), "scale": unit.scale}


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
    # Economics batch (economics-1): reference-year dollars are still currency;
    # the base-year distinction lives in meaning/context, not dimensions. Counts
    # (persons) and index points are dimensionless.
    "USD_ref": Unit(MONEY, 1.0),
    "USD_ref/person": Unit(MONEY, 1.0),
    "person": Unit(DIMENSIONLESS, 1.0),
    "index-point": Unit(DIMENSIONLESS, 1.0),
    # Economics-3: second currency identity. Currency units never convert
    # implicitly (see Value.bind): CAD and USD amounts mix only through an
    # explicit rate model, never at assumed parity.
    "CAD": Unit(MONEY, 1.0),
    "CAD/unit": Unit(MONEY, 1.0),
    "CAD_ref": Unit(MONEY, 1.0),
    # Biology batch (biology-1): organism/site counts and abstract trait units
    # are dimensionless. Concrete units (cm, kg) cannot bind abstract trait
    # ports: the meaning/unit dimension check rejects them fail-closed.
    "count": Unit(DIMENSIONLESS, 1.0),
    "trait-units": Unit(DIMENSIONLESS, 1.0),
    "1/site/generation": Unit(DIMENSIONLESS, 1.0),
    # CS batch (cs-1): byte counts with fixed decimal/binary ratios; abstract
    # activity units are dimensionless.
    "B": Unit(DIMENSIONLESS, 1.0),
    "GB": Unit(DIMENSIONLESS, 1000000000.0),
    "GiB": Unit(DIMENSIONLESS, 1073741824.0),
    "activity-unit": Unit(DIMENSIONLESS, 1.0),
    "USD/activity-unit": Unit(MONEY, 1.0),
    # CS batch (cs-2): byte-rates carry explicit 1/time dimensions so that
    # data-size / transfer-rate yields physical time; bytes themselves stay
    # dimensionless and no rate ever converts implicitly to a time instant.
    "B/s": Unit(INVERSE_TIME, 1.0),
    # CS batch (cs-3): clock frequencies in Hz; MIPS ratings in an explicit
    # MIPS unit (millions of instructions per second) so the 1e6 factor lives
    # in the registry scale, never inlined in an expression.
    "Hz": Unit(INVERSE_TIME, 1.0),
    "MIPS": Unit(INVERSE_TIME, 1000000.0),
    # CS batch (cs-4): per-hour failure rates against the per-second base.
    "1/h": Unit(INVERSE_TIME, 1 / 3600),
    # Biology batch (biology-3): metabolic power in kcal/day (thermochemical
    # kcal) and its Kleiber normalization per kg^0.75. The normalization unit
    # carries fractional mass power 1 - 3/4; its scale divides the kcal/day
    # scale by the canonical-kg scale raised to the Kleiber exponent.
    "kcal/day": Unit(POWER, (KCAL_IN_JOULES / JOULES_PER_KWH) / SECONDS_PER_DAY),
    "kcal/day per kg^0.75": Unit(_dims(Fraction(1) - KLEIBER_MASS_EXPONENT, 2, -3, 0),
                                 ((KCAL_IN_JOULES / JOULES_PER_KWH) / SECONDS_PER_DAY)
                                 / ((1 / JOULES_PER_KWH) ** float(KLEIBER_MASS_EXPONENT))),
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
    # Finance-2: second reviewed batch (amortization schedule and gradient meanings).
    "gradient_amount": MONEY,
    "interest_payment": MONEY,
    "principal_payment": MONEY,
    "payment_index": DIMENSIONLESS,
    # Economics-1: national-accounts and price-index meanings for reviewed b03/b04.
    "gross_national_product_current_price": MONEY,
    "net_domestic_product_current_price": MONEY,
    "consumption_fixed_capital_current_price": MONEY,
    "income_receipts_rest_of_world": MONEY,
    "income_payments_rest_of_world": MONEY,
    "personal_income_current_price": MONEY,
    "personal_outlays_current_price": MONEY,
    "personal_current_taxes": MONEY,
    "personal_saving_current_price": MONEY,
    "implicit_price_deflator": DIMENSIONLESS,
    "economic_series_current_price": MONEY,
    "economic_series_chained_price": MONEY,
    "fixed_basket_value_current_prices": MONEY,
    "fixed_basket_value_reference_prices": MONEY,
    "fixed_basket_price_relative": DIMENSIONLESS,
    "laspeyres_price_relative": DIMENSIONLESS,
    "paasche_price_relative": DIMENSIONLESS,
    "fisher_price_relative": DIMENSIONLESS,
    "gross_domestic_product_real": MONEY,
    "midyear_resident_population": DIMENSIONLESS,
    "real_gdp_per_capita": MONEY,
    # Economics-2: profit and marginal-cost meanings for reviewed b06 admittables.
    "total_revenue": MONEY,
    "explicit_cost_amount": MONEY,
    "implicit_opportunity_cost_amount": MONEY,
    "economic_profit": MONEY,
    "total_production_cost": MONEY,
    "produced_quantity": DIMENSIONLESS,
    "finite_increment_marginal_cost": MONEY,
    # Economics-3: value-added, capital-stock and transaction-price meanings.
    "gross_value_added_current_price": MONEY,
    "industry_gross_output_current_price": MONEY,
    "industry_intermediate_inputs_current_price": MONEY,
    "fixed_capital_net_stock_reference_price": MONEY,
    "fixed_capital_investment_reference_price": MONEY,
    "fixed_capital_consumption_reference_price": MONEY,
    "fixed_capital_other_disappearance_reference_price": MONEY,
    "identical_product_transaction_value": MONEY,
    "identical_product_transacted_quantity": DIMENSIONLESS,
    "quantity_weighted_mean_transaction_price": MONEY,
    # Economics-4: income-side aggregates and cost-volume-profit meanings.
    "gross_domestic_income_current_price": MONEY,
    "gdp_gdi_statistical_discrepancy": MONEY,
    "final_sales_domestic_product_current_price": MONEY,
    "gross_domestic_purchases_current_price": MONEY,
    "private_inventory_change_current_price": MONEY,
    "net_exports_goods_services_current_price": MONEY,
    "disposable_personal_income_current_price": MONEY,
    "personal_saving_fraction": DIMENSIONLESS,
    "unit_contribution_margin": MONEY,
    "unit_contribution_margin_ratio": DIMENSIONLESS,
    "total_contribution_margin": MONEY,
    "actual_sales_revenue": MONEY,
    "break_even_sales_revenue": MONEY,
    "sales_margin_of_safety_fraction": DIMENSIONLESS,
    "degree_operating_leverage": DIMENSIONLESS,
    "net_operating_income": MONEY,
    # Biology-1: population-genetics frequencies, counts and trait meanings.
    "allele_frequency": DIMENSIONLESS,
    "genotype_frequency": DIMENSIONLESS,
    "narrow_heritability": DIMENSIONLESS,
    "selection_differential": DIMENSIONLESS,
    "selection_response": DIMENSIONLESS,
    "breeding_males": DIMENSIONLESS,
    "breeding_females": DIMENSIONLESS,
    "census_size": DIMENSIONLESS,
    "effective_size": DIMENSIONLESS,
    "ideal_population_size": DIMENSIONLESS,
    "drift_variance": DIMENSIONLESS,
    "mutation_rate": DIMENSIONLESS,
    "nucleotide_diversity": DIMENSIONLESS,
    # Biology-2: count meanings for genotype-frequency r2.
    "genotype_count": DIMENSIONLESS,
    "individual_count": DIMENSIONLESS,
    # Biology-3: Kleiber metabolic scaling (power, mass, fractional normalization).
    "basal_metabolic_rate": POWER,
    "body_mass": MASS,
    "metabolic_normalization": _dims(Fraction(1) - KLEIBER_MASS_EXPONENT, 2, -3, 0),
    # Economics-5: break-even, mixed-cost and average-cost meanings.
    "break_even_quantity": DIMENSIONLESS,
    "unit_variable_cost": MONEY,
    "fixed_cost": MONEY,
    "cost_driver_quantity": DIMENSIONLESS,
    "cost_per_activity_unit": MONEY,
    "fixed_cost_pool_amount": MONEY,
    "mixed_cost_pool_amount": MONEY,
    "average_total_production_cost": MONEY,
    # Finance-3 straggler: growing-annuity initial payment.
    "initial_payment": MONEY,
    # CS-1: availability, speedup, execution-time and byte-count meanings.
    "component_availability": DIMENSIONLESS,
    "parallel_availability": DIMENSIONLESS,
    "unavailability": DIMENSIONLESS,
    "execution_time": TIME,
    "overall_speedup": DIMENSIONLESS,
    "scaled_speedup": DIMENSIONLESS,
    "parallel_efficiency": DIMENSIONLESS,
    "serial_fraction": DIMENSIONLESS,
    "parallel_fraction_scaled": DIMENSIONLESS,
    "processor_count": DIMENSIONLESS,
    "byte_count": DIMENSIONLESS,
    "gigabyte_count": DIMENSIONLESS,
    "gibibyte_count": DIMENSIONLESS,
    # CS-2: Amdahl fractions, transfer sizing, record capacity, series systems.
    "parallel_fraction": DIMENSIONLESS,
    "component_speedup": DIMENSIONLESS,
    "data_size": DIMENSIONLESS,
    "transfer_rate": INVERSE_TIME,
    "transfer_time": TIME,
    "record_count": DIMENSIONLESS,
    "record_size": DIMENSIONLESS,
    "storage_capacity": DIMENSIONLESS,
    "series_availability": DIMENSIONLESS,
    # CS-3: Karp-Flatt, MTBF/MTTR/MTTF availability family, CPU-performance
    # equation, clock/cycle quantities, operational availability, leg counts.
    "measured_speedup": DIMENSIONLESS,
    "experimental_serial_fraction": DIMENSIONLESS,
    "mtbf": TIME,
    "mttr": TIME,
    "mttf": TIME,
    "inherent_availability": DIMENSIONLESS,
    "expected_uptime": TIME,
    "expected_downtime": TIME,
    "window_availability": DIMENSIONLESS,
    "instruction_count": DIMENSIONLESS,
    "effective_cpi": DIMENSIONLESS,
    "cycle_time": TIME,
    "cpu_time": TIME,
    "clock_frequency": INVERSE_TIME,
    "mips_rating": INVERSE_TIME,
    "redesign_performance_ratio": DIMENSIONLESS,
    "mean_downtime": TIME,
    "operational_availability": DIMENSIONLESS,
    "leg_count": DIMENSIONLESS,
    # CS-4: RAID usable-capacity family (disk counts and member capacities).
    "disk_count": DIMENSIONLESS,
    "member_capacity": DIMENSIONLESS,
    "striped_usable_capacity": DIMENSIONLESS,
    "parity_usable_capacity": DIMENSIONLESS,
    "double_parity_usable_capacity": DIMENSIONLESS,
    # CS-4 continued: voting/TMR reliability and series/parallel MTBF/MDT pairs.
    "module_reliability": DIMENSIONLESS,
    "tmr_reliability": DIMENSIONLESS,
    "voted_availability": DIMENSIONLESS,
    "leg_mtbf": TIME,
    "series_mtbf": TIME,
    "leg_mdt": TIME,
    "series_mdt": TIME,
    "parallel_mtbf": TIME,
    "parallel_mdt": TIME,
    "constant_failure_rate": INVERSE_TIME,
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
        if self.unit != target.unit and (UNITS[self.unit].dimensions[3] != 0 or UNITS[target.unit].dimensions[3] != 0):
            raise ModelError(f"Cannot bind {self.unit} to {target.unit}: currency units never convert implicitly; "
                             "route through an explicit rate model instead of assuming parity.")


MAX_FAMILY_SIZE = 256


@dataclass(frozen=True)
class Family:
    """An index-family input: one shared port plus a declared maximum element count."""

    meaning: str
    unit: str
    context: str
    max_size: int

    @property
    def port(self) -> "Port":
        """Return the shared element port without copying declarations."""
        return Port(self.meaning, self.unit, self.context)

    def validate(self) -> None:
        """Check the shared element declaration and the size bound."""
        self.port.validate()
        if type(self.max_size) is not int or not 1 <= self.max_size <= MAX_FAMILY_SIZE:
            raise ModelError(f"Family size bound must be an integer from 1 to {MAX_FAMILY_SIZE}.")


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
    families: dict[str, Family] = field(default_factory=dict)

    @property
    def key(self) -> str:
        """Return a revision-specific reference, never a latest-version alias."""
        return f"{self.id}@{self.version}"


@dataclass(frozen=True)
class Node:
    """An independent instance with explicit values or upstream bindings."""

    id: str
    model: str
    bindings: dict[str, Value | Reference | tuple[Value | Reference, ...]]
    solve_for: str | None = None
    relation: str = "equal"


@dataclass(frozen=True)
class Composition:
    """A bounded scenario request, its instances, and its requested results."""

    id: str
    nodes: tuple[Node, ...]
    outputs: tuple[str, ...]
    purpose: str = "fixture"
