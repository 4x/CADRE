"""Small scalar contracts; context belongs to each port, not to a whole node."""

import math
import re
from dataclasses import dataclass, field
from fractions import Fraction

Dimensions = tuple[
    Fraction, Fraction, Fraction, Fraction, Fraction, Fraction, Fraction
]  # Mass, length, time, currency, temperature, current, amount.


def _dims(
    mass: int | Fraction,
    length: int | Fraction,
    time: int | Fraction,
    currency: int | Fraction,
    temperature: int | Fraction = 0,
    current: int | Fraction = 0,
    amount: int | Fraction = 0,
) -> Dimensions:
    """Build an exact dimension vector; rational powers need exact rationals, never floats."""
    return (
        Fraction(mass),
        Fraction(length),
        Fraction(time),
        Fraction(currency),
        Fraction(temperature),
        Fraction(current),
        Fraction(amount),
    )


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
VOLUME: Dimensions = _dims(0, 3, 0, 0)
MASS_DENSITY: Dimensions = _dims(1, -3, 0, 0)
SPECIFIC_ENERGY: Dimensions = _dims(0, 2, -2, 0)
AREA: Dimensions = _dims(0, 2, 0, 0)
TEMPERATURE: Dimensions = _dims(0, 0, 0, 0, 1, 0, 0)
INVERSE_TEMPERATURE: Dimensions = _dims(0, 0, 0, 0, -1, 0, 0)
CURRENT: Dimensions = _dims(0, 0, 0, 0, 0, 1, 0)
AMOUNT: Dimensions = _dims(0, 0, 0, 0, 0, 0, 1)
VOLTAGE: Dimensions = _dims(1, 2, -3, 0, 0, -1, 0)
RESISTANCE: Dimensions = _dims(1, 2, -3, 0, 0, -2, 0)
CHARGE: Dimensions = _dims(0, 0, 1, 0, 0, 1, 0)
CONDUCTANCE: Dimensions = _dims(-1, -2, 3, 0, 0, 2, 0)
RESISTIVITY: Dimensions = _dims(1, 3, -3, 0, 0, -2, 0)
CONDUCTIVITY: Dimensions = _dims(-1, -3, 3, 0, 0, 2, 0)
SPECIFIC_HEAT: Dimensions = _dims(0, 2, -2, 0, -1, 0, 0)
THERMAL_RESISTANCE_AREA: Dimensions = _dims(-1, 0, 3, 0, 1, 0, 0)
THERMAL_RESISTANCE: Dimensions = _dims(-1, -2, 3, 0, 1, 0, 0)
THERMAL_CONDUCTIVITY: Dimensions = _dims(1, 1, -3, 0, -1, 0, 0)
STEFAN_BOLTZMANN: Dimensions = _dims(1, 0, -3, 0, -4, 0, 0)
GRAVITATION: Dimensions = _dims(-1, 3, -2, 0, 0, 0, 0)
PER_AMOUNT: Dimensions = _dims(0, 0, 0, 0, 0, 0, -1)
AREAL_DENSITY: Dimensions = _dims(1, -2, 0, 0, 0, 0, 0)
MASS_FLOW: Dimensions = _dims(1, 0, -1, 0, 0, 0, 0)
VOLUME_FLOW: Dimensions = _dims(0, 3, -1, 0, 0, 0, 0)
VELOCITY_SQUARED: Dimensions = _dims(0, 2, -2, 0, 0, 0, 0)
TIME_SQUARED: Dimensions = _dims(0, 0, 2, 0, 0, 0, 0)
GRAVITATIONAL_PARAMETER: Dimensions = _dims(0, 3, -2, 0, 0, 0, 0)
MASS_PER_MONEY: Dimensions = _dims(1, 0, 0, -1, 0, 0, 0)
# CFA-L1 batch: money per selling area for retail intensity records.
MONEY_PER_AREA: Dimensions = _dims(0, -2, 0, 1)
SPECIFIC_ANGULAR_MOMENTUM_SQUARED: Dimensions = _dims(0, 4, -2, 0, 0, 0, 0)
CURRENT_DENSITY: Dimensions = _dims(0, -2, 0, 0, 0, 1, 0)
NUMBER_DENSITY: Dimensions = _dims(0, -3, 0, 0, 0, 0, 0)
MOLAR_MASS: Dimensions = _dims(1, 0, 0, 0, 0, 0, -1)
INVERSE_LENGTH: Dimensions = _dims(0, -1, 0, 0, 0, 0, 0)
# Lane intake (fuel-b01, dctco-b01, water-b01): per-volume, per-length,
# per-energy and per-time ratios for economy, tariff, intensity and cost.
LENGTH_PER_VOLUME: Dimensions = _dims(0, -2, 0, 0)
MONEY_PER_VOLUME: Dimensions = _dims(0, -3, 0, 1)
MONEY_PER_LENGTH: Dimensions = _dims(0, -1, 0, 1)
VOLUME_PER_ENERGY: Dimensions = _dims(-1, 1, 2, 0)
MASS_PER_ENERGY: Dimensions = _dims(0, -2, 2, 0)
MONEY_PER_TIME: Dimensions = _dims(0, 0, -1, 1)
# Data-quantity convention: byte counts and byte rates are the canonical base
# (B and B/s at scale 1); one bit is one eighth of a byte everywhere, so every
# bit-denominated scale carries the /8 explicitly.
BITS_PER_BYTE = 8
JOULES_PER_KWH = 3_600_000
KCAL_IN_JOULES = 4_184
SECONDS_PER_DAY = 86_400
BTU_IN_JOULES = 1055.05585262
# Exact imperial/US-customary definitions (query-3): the inch is exactly
# 25.4 mm and every other unit below derives from exact definitions.
METERS_PER_INCH = 0.0254
METERS_PER_FOOT = 0.3048
METERS_PER_YARD = 0.9144
METERS_PER_MILE = 1609.344
METERS_PER_NAUTICAL_MILE = 1852
CUBIC_METERS_PER_LITER = 0.001
CUBIC_METERS_PER_GALLON = 3.785411784e-3  # US liquid gallon, exactly 231 in^3.
KG_PER_POUND = 0.45359237
KG_PER_MILLIGRAM = 1e-6
CUBIC_METERS_PER_DECILITER = 1e-4
NEWTONS_PER_POUND_FORCE = 4.4482216152605
WATTS_PER_HORSEPOWER = 550 * METERS_PER_FOOT * NEWTONS_PER_POUND_FORCE  # Mechanical hp.
KLEIBER_MASS_EXPONENT = Fraction(3, 4)
VOCABULARY_PROFILE = "cm-vocabulary/mechanics-1+finance-2+economics-5+biology-3+cs-4+be-1+be-2+circuits-1+clinical-1+orbital-1+envacct-1+demography-1+orbital-2+circuits-2+waves-1+waves-2+clinical-2+cs-5+clinical-3+mechanics-2+cs-6+be-3+query-2+query-3+query-4+glue-1+economics-6+query-5+glue-2+envacct-2+cs-7+water-1+economics-7+cs-8+cfa-l1-1"
DIMENSION_AXES = (
    "mass",
    "length",
    "time",
    "currency",
    "temperature",
    "current",
    "amount",
)
NUMERICAL_BASIS = f"kWh, m, s, USD, K, A, mol; mass base = {JOULES_PER_KWH} kg"


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
    return [
        power.numerator
        if power.denominator == 1
        else [power.numerator, power.denominator]
        for power in dims
    ]


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
    # Building-energy batch (be-3): square metres in the curator spelling
    # for heat-transfer areas (m^2 stays the sibling spelling elsewhere).
    "m2": Unit(AREA, 1.0),
    # CS batch (cs-4): per-hour failure rates against the per-second base.
    "1/h": Unit(INVERSE_TIME, 1 / 3600),
    # CS batch (cs-5): bit counts and decimal/binary bit- and byte-rate units
    # in curator spellings. Bytes stay the base (B, B/s at 1.0); every bit
    # scale divides by BITS_PER_BYTE. Decimal kilo..peta are powers of 1000,
    # binary kibi..exbi powers of 1024, matching the curated r1 factors.
    "bit": Unit(DIMENSIONLESS, 1 / BITS_PER_BYTE),
    "bit/s": Unit(INVERSE_TIME, 1 / BITS_PER_BYTE),
    "kbit/s": Unit(INVERSE_TIME, 1000 / BITS_PER_BYTE),
    "Kibit/s": Unit(INVERSE_TIME, 1024 / BITS_PER_BYTE),
    "Mbit/s": Unit(INVERSE_TIME, 1000000 / BITS_PER_BYTE),
    "Mibit/s": Unit(INVERSE_TIME, 1048576 / BITS_PER_BYTE),
    "Gbit/s": Unit(INVERSE_TIME, 1000000000 / BITS_PER_BYTE),
    "Gibit/s": Unit(INVERSE_TIME, 1073741824 / BITS_PER_BYTE),
    "Tbit/s": Unit(INVERSE_TIME, 1000000000000 / BITS_PER_BYTE),
    "Tibit/s": Unit(INVERSE_TIME, 1099511627776 / BITS_PER_BYTE),
    "Pbit/s": Unit(INVERSE_TIME, 1000000000000000 / BITS_PER_BYTE),
    "Pibit/s": Unit(INVERSE_TIME, 1125899906842624 / BITS_PER_BYTE),
    "Eibit/s": Unit(INVERSE_TIME, 1152921504606846976 / BITS_PER_BYTE),
    "MB/s": Unit(INVERSE_TIME, 1000000.0),
    "MiB/s": Unit(INVERSE_TIME, 1048576.0),
    "GB/s": Unit(INVERSE_TIME, 1000000000.0),
    "TB/s": Unit(INVERSE_TIME, 1000000000000.0),
    "TiB/s": Unit(INVERSE_TIME, 1099511627776.0),
    "PB/s": Unit(INVERSE_TIME, 1000000000000000.0),
    "PiB/s": Unit(INVERSE_TIME, 1125899906842624.0),
    "EiB/s": Unit(INVERSE_TIME, 1152921504606846976.0),
    # Biology batch (biology-3): metabolic power in kcal/day (thermochemical
    # kcal) and its Kleiber normalization per kg^0.75. The normalization unit
    # carries fractional mass power 1 - 3/4; its scale divides the kcal/day
    # scale by the canonical-kg scale raised to the Kleiber exponent.
    "kcal/day": Unit(POWER, (KCAL_IN_JOULES / JOULES_PER_KWH) / SECONDS_PER_DAY),
    "kcal/day per kg^0.75": Unit(
        _dims(Fraction(1) - KLEIBER_MASS_EXPONENT, 2, -3, 0),
        ((KCAL_IN_JOULES / JOULES_PER_KWH) / SECONDS_PER_DAY)
        / ((1 / JOULES_PER_KWH) ** float(KLEIBER_MASS_EXPONENT)),
    ),
    # Building-energy batch (be-1): SI power, volume, mass density and specific
    # energy plus the International Table Btu used by ENERGY STAR seasonal
    # ratings. Btu/Wh is a dimensionless scale ratio: (Btu/Wh)*Wh collapses to
    # Btu through the registry scales, never through an inlined factor.
    "W": Unit(POWER, 1 / JOULES_PER_KWH),
    "Btu": Unit(ENERGY, BTU_IN_JOULES / JOULES_PER_KWH),
    "Btu/Wh": Unit(DIMENSIONLESS, BTU_IN_JOULES / 3600),
    "m3": Unit(VOLUME, 1.0),
    "kg/m3": Unit(MASS_DENSITY, 1 / JOULES_PER_KWH),
    "J/kg": Unit(SPECIFIC_ENERGY, 1.0),
    # Temperature/current/amount axes (7-axis migration): SI base units K, A,
    # mol at scale 1; electrical units derive from the kWh energy base so that
    # V=IR and P=IV close through registry scales (V and ohm carry 1/3.6e6,
    # S carries 3.6e6). Curator unit strings adopted verbatim (m^2, ohm m,
    # K^-1, S/m); K serves both absolute temperatures and differences — the
    # distinction lives in guards and review scope, not in the engine.
    "K": Unit(TEMPERATURE, 1.0),
    "V": Unit(VOLTAGE, 1 / JOULES_PER_KWH),
    "A": Unit(CURRENT, 1.0),
    "ohm": Unit(RESISTANCE, 1 / JOULES_PER_KWH),
    "C": Unit(CHARGE, 1.0),
    "S": Unit(CONDUCTANCE, JOULES_PER_KWH),
    "m^2": Unit(AREA, 1.0),
    "ohm m": Unit(RESISTIVITY, 1 / JOULES_PER_KWH),
    "S/m": Unit(CONDUCTIVITY, JOULES_PER_KWH),
    "K^-1": Unit(INVERSE_TEMPERATURE, 1.0),
    "mol": Unit(AMOUNT, 1.0),
    "m2*K/W": Unit(THERMAL_RESISTANCE_AREA, JOULES_PER_KWH),
    "J/(kg*K)": Unit(SPECIFIC_HEAT, 1.0),
    # Registry-constant units: sigma per area per K^4, Newtonian gravitation,
    # and per-mole counts for Avogadro-scale conversions.
    "W/(m2*K^4)": Unit(STEFAN_BOLTZMANN, 1 / JOULES_PER_KWH),
    "m3/(kg*s^2)": Unit(GRAVITATION, JOULES_PER_KWH),
    "1/mol": Unit(PER_AMOUNT, 1.0),
    # Clinical batch (clinical-1): concentration, dosing and infusion units in
    # curator SI spellings. kg/m^3 and m^3 duplicate canonical kg/m3 and m3
    # (the latter pinned by an admitted record); machine spellings are all
    # canonical, query aliases serve natural language only.
    "kg/m^3": Unit(MASS_DENSITY, 1 / JOULES_PER_KWH),
    "m^3": Unit(VOLUME, 1.0),
    "m^3/s": Unit(VOLUME_FLOW, 1.0),
    "kg/m^2": Unit(AREAL_DENSITY, 1 / JOULES_PER_KWH),
    "kg/s": Unit(MASS_FLOW, 1 / JOULES_PER_KWH),
    # Orbital batch (orbital-1): SI radian (dimensionless angle), calendar
    # days, and squared/parameter combinations for Kepler and energy records.
    "rad": Unit(DIMENSIONLESS, 1.0),
    "d": Unit(TIME, 86400),
    "m^2/s^2": Unit(VELOCITY_SQUARED, 1.0),
    "s^2": Unit(TIME_SQUARED, 1.0),
    "m3/s2": Unit(GRAVITATIONAL_PARAMETER, 1.0),
    # Environmental-accounting batch (envacct-1): metric tonne (SI symbol t),
    # mass ratios, and per-output / per-revenue / per-capita intensities in
    # curator spellings. Person, output-unit and currency denominators are
    # dimensionless/registry-scaled, so t/person and kg/unit stay MASS while
    # kg/USD carries the mass-per-money dimension.
    "t": Unit(MASS, 1000 / JOULES_PER_KWH),
    "kg/kg": Unit(DIMENSIONLESS, 1.0),
    "kg/unit": Unit(MASS, 1 / JOULES_PER_KWH),
    "kg/USD": Unit(MASS_PER_MONEY, 1 / JOULES_PER_KWH),
    "t/person": Unit(MASS, 1000 / JOULES_PER_KWH),
    # Orbital batch (orbital-2): mean motion in rad/s and squared specific
    # angular momentum. Radian measure keeps rad/s at scale 1 against the
    # per-second base.
    "rad/s": Unit(INVERSE_TIME, 1.0),
    "m4/s2": Unit(SPECIFIC_ANGULAR_MOMENTUM_SQUARED, 1.0),
    # Circuits batch (circuits-2): current density, number density and molar
    # mass in curator spellings. Molar mass rides the kg/mol scale off the
    # canonical-kg base; mol itself stays scale 1.
    "A/m^2": Unit(CURRENT_DENSITY, 1.0),
    "m^-3": Unit(NUMBER_DENSITY, 1.0),
    "kg/mol": Unit(MOLAR_MASS, 1 / JOULES_PER_KWH),
    # Waves batch (waves-1): reciprocal length for optical power and surface
    # curvature in the curator spelling.
    "1/m": Unit(INVERSE_LENGTH, 1.0),
    # Clinical batch (clinical-2): drop counts are dimensionless, so the
    # administration-set drop factor is a number density and the gravity
    # drop rate is a reciprocal time, in curator spellings.
    "drops/m^3": Unit(NUMBER_DENSITY, 1.0),
    "drops/s": Unit(INVERSE_TIME, 1.0),
    # Query batch (query-2): international mile and miles-per-hour so
    # faithful query facts ("30 mph", "100 miles") bind for execution.
    "mi": Unit(LENGTH, METERS_PER_MILE),
    "mph": Unit(VELOCITY, METERS_PER_MILE / 3600),
    # Query batch (query-3): imperial/US-customary lengths, volumes, masses
    # and their derived rates plus SI liter and thermochemical calories, so
    # everyday query facts ("12 ft", "2 gal", "150 lb") bind for execution.
    # All scales derive from the exact constants above; KCAL_IN_JOULES is
    # the thermochemical calorie already used by kcal/day. Fahrenheit and
    # Celsius are deliberately absent: absolute readings need an offset
    # conversion and Unit is ratio-only, so admitting them would silently
    # misread e.g. 68 degF as a ratio quantity.
    "in": Unit(LENGTH, METERS_PER_INCH),
    "ft": Unit(LENGTH, METERS_PER_FOOT),
    "yd": Unit(LENGTH, METERS_PER_YARD),
    "nmi": Unit(LENGTH, METERS_PER_NAUTICAL_MILE),
    "ft/s": Unit(VELOCITY, METERS_PER_FOOT),
    "kn": Unit(VELOCITY, METERS_PER_NAUTICAL_MILE / 3600),
    "L": Unit(VOLUME, CUBIC_METERS_PER_LITER),
    "mL": Unit(VOLUME, CUBIC_METERS_PER_LITER / 1000),
    "gal": Unit(VOLUME, CUBIC_METERS_PER_GALLON),
    "qt": Unit(VOLUME, CUBIC_METERS_PER_GALLON / 4),
    "lb": Unit(MASS, KG_PER_POUND / JOULES_PER_KWH),
    "oz": Unit(MASS, KG_PER_POUND / 16 / JOULES_PER_KWH),
    "lbf": Unit(FORCE, NEWTONS_PER_POUND_FORCE / JOULES_PER_KWH),
    "cal": Unit(ENERGY, (KCAL_IN_JOULES / 1000) / JOULES_PER_KWH),
    "kcal": Unit(ENERGY, KCAL_IN_JOULES / JOULES_PER_KWH),
    "hp": Unit(POWER, WATTS_PER_HORSEPOWER / JOULES_PER_KWH),
    # Query batch (query-4): clinical mass and concentration spellings so
    # dosing facts ("250 mg", "15 mg per kg", "1.2 mg/dL") bind for
    # execution. mg/dL is exactly 0.01 kg/m^3.
    "mg": Unit(MASS, KG_PER_MILLIGRAM / JOULES_PER_KWH),
    "mg/kg": Unit(DIMENSIONLESS, KG_PER_MILLIGRAM),
    "dL": Unit(VOLUME, CUBIC_METERS_PER_DECILITER),
    "mg/dL": Unit(
        MASS_DENSITY, (KG_PER_MILLIGRAM / CUBIC_METERS_PER_DECILITER) / JOULES_PER_KWH
    ),
    # Lane intake (fuel-b01, dctco-b01, water-b01): composite scales are the
    # numerator scale over the denominator scale, as with J/kg and USD/kWh.
    "mi/gal": Unit(LENGTH_PER_VOLUME, METERS_PER_MILE / CUBIC_METERS_PER_GALLON),
    "USD/gal": Unit(MONEY_PER_VOLUME, 1.0 / CUBIC_METERS_PER_GALLON),
    "USD/mi": Unit(MONEY_PER_LENGTH, 1.0 / METERS_PER_MILE),
    "L/kWh": Unit(VOLUME_PER_ENERGY, CUBIC_METERS_PER_LITER),
    "kg/kWh": Unit(MASS_PER_ENERGY, 1.0 / JOULES_PER_KWH),
    "USD/h": Unit(MONEY_PER_TIME, 1.0 / 3600.0),
    "m3/person": Unit(VOLUME, 1.0),
    "USD/m3": Unit(MONEY_PER_VOLUME, 1.0),
    "m3/unit": Unit(VOLUME, 1.0),
    # R2 intake (computer-science-dctco-b02): per-period money spells the
    # rate/amount distinction at the unit level; periods are dimensionless
    # counts, so the dimension stays currency with scale 1.
    "USD/periods": Unit(MONEY, 1.0),
    # CFA-L1 batch (cfa-l1-1): currency identities, abstract count/service
    # units, FX ratio quotes, per-unit money, demand slopes, selling area.
    # EUR/GBP/CNY join USD/CAD as MONEY identities; they never convert
    # implicitly (see Port.require_compatible). The generic `currency` unit
    # covers currency-agnostic statement amounts. Abstract data, quantity,
    # service and count units are dimensionless by design (unit/count/person
    # precedent); labor-hour and machine-hour are SERVICE quantities (curator
    # labor_service/capital_service), never physical time, so they never
    # convert to s/min/h. FX quotes are dimensionless money/money ratios:
    # the 7-axis system has one currency axis, so a pair quote cannot be
    # MONEY; exact meaning/context binding still applies.
    "EUR": Unit(MONEY, 1.0),
    "GBP": Unit(MONEY, 1.0),
    "CNY": Unit(MONEY, 1.0),
    "currency": Unit(MONEY, 1.0),
    "data-unit": Unit(DIMENSIONLESS, 1.0),
    "data-unit^2": Unit(DIMENSIONLESS, 1.0),
    "data-unit^3": Unit(DIMENSIONLESS, 1.0),
    "data-unit^4": Unit(DIMENSIONLESS, 1.0),
    "data-unit-x*data-unit-y": Unit(DIMENSIONLESS, 1.0),
    "1/data-unit": Unit(DIMENSIONLESS, 1.0),
    "predictor-unit": Unit(DIMENSIONLESS, 1.0),
    "1/predictor-unit": Unit(DIMENSIONLESS, 1.0),
    "response-unit": Unit(DIMENSIONLESS, 1.0),
    "response-unit^2": Unit(DIMENSIONLESS, 1.0),
    "good-unit": Unit(DIMENSIONLESS, 1.0),
    "input-service-unit": Unit(DIMENSIONLESS, 1.0),
    "good-unit/input-service-unit": Unit(DIMENSIONLESS, 1.0),
    "good-unit/labor-hour": Unit(DIMENSIONLESS, 1.0),
    "labor-hour": Unit(DIMENSIONLESS, 1.0),
    "machine-hour": Unit(DIMENSIONLESS, 1.0),
    "employee": Unit(DIMENSIONLESS, 1.0),
    "persons": Unit(DIMENSIONLESS, 1.0),
    "room_night": Unit(DIMENSIONLESS, 1.0),
    "share": Unit(DIMENSIONLESS, 1.0),
    "unit^2": Unit(DIMENSIONLESS, 1.0),
    "price_currency_per_base_currency": Unit(DIMENSIONLESS, 1.0),
    "base_currency_per_price_currency": Unit(DIMENSIONLESS, 1.0),
    "currency_a_per_currency_b": Unit(DIMENSIONLESS, 1.0),
    "currency_a_per_currency_c": Unit(DIMENSIONLESS, 1.0),
    "currency_b_per_currency_c": Unit(DIMENSIONLESS, 1.0),
    "USD per EUR": Unit(DIMENSIONLESS, 1.0),
    # Per-unit money follows the USD/unit lane-A convention (MONEY, since
    # every denominator is a dimensionless count); demand slopes dQ/dP are
    # INVERSE_MONEY (unit^2/USD precedent) while inverse-demand slopes
    # dP/dQ stay MONEY. square_foot adopts the curator-declared area
    # dimension with the exact ft^2 scale; USD_per_square_foot carries
    # MONEY_PER_AREA with the numerator-over-denominator scale (USD/gal
    # precedent).
    "EUR/good-unit": Unit(MONEY, 1.0),
    "EUR/good-unit**2": Unit(MONEY, 1.0),
    "EUR/labor-hour": Unit(MONEY, 1.0),
    "EUR/machine-hour": Unit(MONEY, 1.0),
    "EUR/person": Unit(MONEY, 1.0),
    "USD_per_unit": Unit(MONEY, 1.0),
    "USD_per_employee": Unit(MONEY, 1.0),
    "USD_per_room_night": Unit(MONEY, 1.0),
    "good-unit/(EUR/good-unit)": Unit(INVERSE_MONEY, 1.0),
    "good-unit/(EUR)": Unit(INVERSE_MONEY, 1.0),
    "good-unit**2/EUR": Unit(INVERSE_MONEY, 1.0),
    "square_foot": Unit(AREA, METERS_PER_FOOT**2),
    "USD_per_square_foot": Unit(MONEY_PER_AREA, 1.0 / METERS_PER_FOOT**2),
}


def normalize_unit_spelling(unit: str) -> str:
    """Lowercase and squeeze a lexical unit spelling before alias lookup."""
    if not isinstance(unit, str):
        raise ModelError("Unit spellings must be strings.")
    return re.sub(r"\s+per\s+", "/", unit.strip().lower()).replace(" ", "")


# Lexical aliases live with the vocabulary they resolve against, not in the
# query layer: every target is validated at import, and curation kits ship
# this map so curators see it offline. Grandfathered duplicate canonicals
# (m^2/m2) stay canonical because admitted ports pin those exact strings;
# all future spelling variants enter here, never as parallel canonicals.
UNIT_ALIASES = {
    # Query batch 1 (moved from the query layer, minus self-maps now served
    # by canonical passthrough, plus year folds from the retired YEAR_UNITS).
    "dimensionless": "1",
    "ratio": "1",
    "percentage": "percent",
    "usd": "USD",
    "$": "USD",
    "dollar": "USD",
    "dollars": "USD",
    "usd/kwh": "USD/kWh",
    "$/kwh": "USD/kWh",
    "dollar/kwh": "USD/kWh",
    "dollars/kwh": "USD/kWh",
    "kwh": "kWh",
    "wh": "Wh",
    "kilogram": "kg",
    "kilograms": "kg",
    "grams": "g",
    "metre": "m",
    "metres": "m",
    "meter": "m",
    "meters": "m",
    "second": "s",
    "seconds": "s",
    "minute": "min",
    "minutes": "min",
    "hour": "h",
    "hours": "h",
    "m/s²": "m/s^2",
    "n": "N",
    "newton": "N",
    "newtons": "N",
    "j": "J",
    "joule": "J",
    "joules": "J",
    "kj": "kJ",
    "year": "years",
    "annual-period": "years",
    "annual-periods": "years",
    # Query batch (query-2): natural spellings for the mile units. Lookup
    # normalizes first, so "miles per hour" also reaches "miles/hour".
    "mile": "mi",
    "miles": "mi",
    "miles/hour": "mph",
    "mi/h": "mph",
    # Query batch (query-3): natural spellings for the imperial batch.
    # Multiword forms normalize (spaces removed) before lookup, so e.g.
    # "nautical miles" reaches "nauticalmiles" and "feet per second"
    # reaches "feet/second".
    "inch": "in",
    "inches": "in",
    "foot": "ft",
    "feet": "ft",
    "feet/second": "ft/s",
    "yard": "yd",
    "yards": "yd",
    "nauticalmile": "nmi",
    "nauticalmiles": "nmi",
    "knot": "kn",
    "knots": "kn",
    "liter": "L",
    "liters": "L",
    "litre": "L",
    "litres": "L",
    "milliliter": "mL",
    "milliliters": "mL",
    "millilitre": "mL",
    "millilitres": "mL",
    "ml": "mL",
    "cc": "mL",
    "gallon": "gal",
    "gallons": "gal",
    "quart": "qt",
    "quarts": "qt",
    "pound": "lb",
    "pounds": "lb",
    "lbs": "lb",
    "ounce": "oz",
    "ounces": "oz",
    "calorie": "cal",
    "calories": "cal",
    "kilocalorie": "kcal",
    "kilocalories": "kcal",
    "horsepower": "hp",
    # Query batch (query-4): clinical spellings. Lookup normalizes first,
    # so "mg per kg" reaches "mg/kg" and "mg per dl" reaches "mg/dl".
    "milligram": "mg",
    "milligrams": "mg",
    "deciliter": "dL",
    "deciliters": "dL",
    "decilitre": "dL",
    "decilitres": "dL",
    "dl": "dL",
    "mg/dl": "mg/dL",
    # Query batch (query-5): per-unit money phrasing. "800 units" must read
    # as the canonical count, and "$50"/"50 dollars" per unit as USD/unit.
    "units": "unit",
    "dollar/unit": "USD/unit",
    "dollars/unit": "USD/unit",
}


def _validate_unit_aliases() -> None:
    """Reject alias misconfiguration at import: unknown targets, chains, dead entries."""
    normalized_canonical: dict[str, str] = {}
    for unit in UNITS:
        # SI case pairs (S/s) share a normalized form; exact-first lookup
        # keeps both usable, so canonical collisions are allowed here.
        normalized_canonical.setdefault(normalize_unit_spelling(unit), unit)
    seen: dict[str, str] = {}
    for alias, canonical in UNIT_ALIASES.items():
        if canonical not in UNITS:
            raise ModelError(
                f"Unit alias {alias!r} targets unknown unit {canonical!r}."
            )
        if alias in UNITS:
            raise ModelError(
                f"Unit alias {alias!r} shadows a canonical unit; remove it."
            )
        if canonical in UNIT_ALIASES:
            raise ModelError(
                f"Unit alias {alias!r} targets another alias; point at a canonical unit."
            )
        key = normalize_unit_spelling(alias)
        if key in seen:
            raise ModelError(
                f"Unit aliases {seen[key]!r} and {alias!r} normalize identically; one is dead."
            )
        seen[key] = alias
        if key in normalized_canonical and canonical != normalized_canonical[key]:
            raise ModelError(
                f"Unit alias {alias!r} shadows canonical {normalized_canonical[key]!r} but points elsewhere."
            )


_validate_unit_aliases()


def describe_units(filter: str = "") -> str:
    """Render canonical units with dimensions, scales, and aliases for inspection."""
    needle = filter.strip().lower()
    grouped: dict[str, list[str]] = {}
    for alias, canonical in UNIT_ALIASES.items():
        grouped.setdefault(canonical, []).append(alias)
    lines = []
    for unit in sorted(UNITS):
        aliases = sorted(grouped.get(unit, []))
        if (
            needle
            and needle not in unit.lower()
            and not any(needle in item.lower() for item in aliases)
        ):
            continue
        powers = " ".join(
            f"{axis}^{power}"
            for axis, power in zip(DIMENSION_AXES, UNITS[unit].dimensions)
            if power != 0
        )
        line = f"{unit} | {powers or 'dimensionless'} | scale {UNITS[unit].scale!r}"
        if aliases:
            line += f" | aliases: {', '.join(aliases)}"
        lines.append(line)
    return "\n".join(lines)


# Meaning is independent of dimension: heat and electricity cannot bind implicitly.
MEANINGS = {
    "delivered_heat": ENERGY,
    "electricity_consumption": ENERGY,
    "seasonal_performance": DIMENSIONLESS,
    "electricity_tariff": PRICE,
    "operating_cost": MONEY,
    "annual_saving": MONEY,
    # Glue batch: outputs-only comparison/scaling vocabulary. difference_of_money
    # carries sign for answer-layer reading (no engine comparison operators).
    "sum_of_money": MONEY,
    "scaled_money": MONEY,
    "difference_of_money": MONEY,
    # Glue batch intake (economics-glue-b01): generic input-side vocabulary.
    # Counts are dimensionless per the lane-B convention.
    "named_money_amount": MONEY,
    "plain_multiplier": DIMENSIONLESS,
    "counted_unit_quantity": DIMENSIONLESS,
    # Lane intake (environmental-accounting-fuel-b01): trip economy, cost,
    # fuel energy and conversion efficiency vocabulary.
    "trip_distance": LENGTH,
    "trip_fuel_volume": VOLUME,
    "fuel_economy": LENGTH_PER_VOLUME,
    "fuel_unit_price": MONEY_PER_VOLUME,
    "trip_fuel_cost": MONEY,
    "fuel_mass": MASS,
    "lower_heating_value": SPECIFIC_ENERGY,
    "fuel_chemical_energy": ENERGY,
    "useful_work_output": ENERGY,
    "heat_input": ENERGY,
    "thermal_efficiency": DIMENSIONLESS,
    "tank_fuel_volume": VOLUME,
    "vehicle_range": LENGTH,
    "driving_fuel_cost_per_distance": MONEY_PER_LENGTH,
    # Lane intake (computer-science-dctco-b01): xUE efficiency, overhead,
    # downtime cost and depreciation vocabulary.
    "total_facility_energy": ENERGY,
    "it_equipment_energy": ENERGY,
    "power_usage_effectiveness": DIMENSIONLESS,
    "site_water_consumption": VOLUME,
    "water_usage_effectiveness": VOLUME_PER_ENERGY,
    "attributable_carbon_emissions": MASS,
    "carbon_usage_effectiveness": MASS_PER_ENERGY,
    "overhead_energy": ENERGY,
    "outage_cost_rate": MONEY_PER_TIME,
    "annual_downtime_cost": MONEY,
    "asset_cost": MONEY,
    "salvage_value": MONEY,
    "recovery_periods": DIMENSIONLESS,
    "annual_depreciation": MONEY,
    # Lane intake (water-hydraulics-use-b01): flow, use, cost, harvest and
    # intensity vocabulary. Counts are dimensionless by convention.
    "volumetric_flow": VOLUME_FLOW,
    "flow_duration": TIME,
    "water_volume": VOLUME,
    "served_population": DIMENSIONLESS,
    "per_capita_daily_water_use": VOLUME,
    "water_tariff": MONEY_PER_VOLUME,
    "water_cost": MONEY,
    "catchment_area": AREA,
    "rainfall_depth": LENGTH,
    "collection_efficiency": DIMENSIONLESS,
    "harvested_rainwater": VOLUME,
    "product_output": DIMENSIONLESS,
    "water_intensity": VOLUME,
    # Lane intake (engineering-finance-retire-b01): nest-egg, replacement,
    # benefit, distribution and coverage vocabulary.
    "annual_withdrawal": MONEY,
    "safe_withdrawal_rate": DIMENSIONLESS,
    "required_nest_egg": MONEY,
    "retirement_income": MONEY,
    "preretirement_income": MONEY,
    "replacement_ratio": DIMENSIONLESS,
    "primary_insurance_amount": MONEY,
    "delayed_retirement_years": DIMENSIONLESS,
    "delayed_benefit": MONEY,
    "prior_year_balance": MONEY,
    "rmd_distribution_period": DIMENSIONLESS,
    "required_minimum_distribution": MONEY,
    "retirement_savings": MONEY,
    "annual_expenses": MONEY,
    "expense_coverage_multiple": DIMENSIONLESS,
    "discount_rate": DIMENSIONLESS,
    "period_count": DIMENSIONLESS,
    "present_value": MONEY,
    "upfront_cost": MONEY,
    "payback_period_count": DIMENSIONLESS,
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
    # BE-1: point and seasonal heat-pump, density and latent-heat meanings for
    # reviewed wave-2 b01/b02/b03 admittables. Curator quantity IDs adopted
    # verbatim; temperature-carrying records stay out until the engine gains a
    # temperature axis (no silent remaps onto existing axes).
    "electrical_power": POWER,
    "operating_duration": TIME,
    "point_heating_cop": DIMENSIONLESS,
    "point_heating_heat_delivery": ENERGY,
    "point_work_input": ENERGY,
    "point_cooling_cop": DIMENSIONLESS,
    "point_cooling_heat_removal": ENERGY,
    "seasonal_heating_performance_hspf": DIMENSIONLESS,
    "seasonal_space_heating_delivered": ENERGY,
    "seasonal_electricity_consumption_hp": ENERGY,
    "mass_density": MASS_DENSITY,
    "volume": VOLUME,
    "latent_heat_coefficient": SPECIFIC_ENERGY,
    "latent_heat_transfer": ENERGY,
    # BE-2: thermal meanings for reviewed wave-2 b01/b03/b04 admittables.
    # Absolute temperatures and differences share K by curator convention;
    # guards (T > 0) and review scope carry the absolute-side constraint.
    "absolute_hot_reservoir_temperature": TEMPERATURE,
    "absolute_cold_reservoir_temperature": TEMPERATURE,
    "carnot_heating_cop_bound": DIMENSIONLESS,
    "carnot_cooling_cop_bound": DIMENSIONLESS,
    "sensible_heat_transfer": ENERGY,
    "specific_heat_capacity": SPECIFIC_HEAT,
    "temperature_difference": TEMPERATURE,
    "thermal_resistance_area_normalized": THERMAL_RESISTANCE_AREA,
    # Circuits-1: electrical meanings for reviewed codex b01/b02 admittables.
    # Finance-owned elapsed_time stays dimensionless (period counts); physical
    # durations use duration (average-signed-current needs a rename r2).
    "terminal_voltage": VOLTAGE,
    "electric_current": CURRENT,
    "absorbed_electrical_power": POWER,
    "electrical_resistance": RESISTANCE,
    "cross_sectional_area": AREA,
    "electrical_resistivity": RESISTIVITY,
    "length": LENGTH,
    "electrical_conductivity": CONDUCTIVITY,
    "resistance_temperature_coefficient": INVERSE_TEMPERATURE,
    "time_averaged_electric_current": CURRENT,
    "net_transferred_electric_charge": CHARGE,
    # Clinical-1: concentration, infusion, dosing and anthropometric meanings
    # for reviewed codex b04/b05/b06 admittables. Curator quantity IDs adopted
    # verbatim.
    "constituent_mass": MASS,
    "solution_volume": VOLUME,
    "mass_concentration": MASS_DENSITY,
    "postpartum_body_mass_retention": MASS,
    "fractional_body_mass_decrease": DIMENSIONLESS,
    "mean_body_mass_change_rate": MASS_FLOW,
    "mean_constituent_mass_infusion_rate": MASS_FLOW,
    "mean_volumetric_infusion_rate": VOLUME_FLOW,
    "prescribed_drug_mass_per_administration": MASS,
    "prescribed_drug_mass_per_body_surface_area": AREAL_DENSITY,
    "serum_bun_creatinine_mass_ratio": DIMENSIONLESS,
    "serum_creatinine_mass_concentration": MASS_DENSITY,
    "serum_urea_nitrogen_mass_concentration": MASS_DENSITY,
    "body_surface_area": AREA,
    "calculated_mid_upper_arm_muscle_circumference": LENGTH,
    "mid_upper_arm_circumference": LENGTH,
    "triceps_skinfold_thickness": LENGTH,
    # Orbital-1: Kepler, energy, parallax and synodic meanings for reviewed
    # a-b01/a-b02 records. Day-counted periods are TIME (the engine models
    # periods as physical time); parallax angles are dimensionless radians.
    "central_mass": MASS,
    "circular_orbit_velocity_squared": VELOCITY_SQUARED,
    "escape_reference_radius": LENGTH,
    "escape_velocity_squared": VELOCITY_SQUARED,
    "inner_sidereal_period": TIME,
    "orbit_radius": LENGTH,
    "orbital_period": TIME,
    "orbital_period_squared": TIME_SQUARED,
    "orbiting_mass": MASS,
    "outer_sidereal_period": TIME,
    "parallax_angle": DIMENSIONLESS,
    "parallax_baseline": LENGTH,
    "parallax_distance": LENGTH,
    "semi_major_axis": LENGTH,
    "standard_gravitational_parameter": GRAVITATIONAL_PARAMETER,
    "synodic_period": TIME,
    "total_orbital_energy": ENERGY,
    # Environmental-accounting batch (envacct-1): factor-accounting, GWP
    # conversion, intensity, waste-ledger, fuel-inventory and biomass-memo
    # meanings for reviewed a-b01..b05 records. Curator quantity IDs adopted
    # verbatim.
    "accountable_fossil_co2": MASS,
    "activity_amount": MASS,
    "analyzed_combustion_co2": MASS,
    "biomass_co2_memo": MASS,
    "carbon_dioxide_equivalent": MASS,
    "diversion_rate": DIMENSIONLESS,
    "emission_factor": DIMENSIONLESS,
    "emission_intensity": MASS,
    "emission_mass": MASS,
    "fuel_burned_mass": MASS,
    "fuel_combustion_analysis_mass": MASS,
    "fuel_feedstock_mass": MASS,
    "fuel_purchased_mass": MASS,
    "fuel_stock_mass": MASS,
    "global_warming_potential": DIMENSIONLESS,
    "greenhouse_gas_mass": MASS,
    "per_capita_generation": MASS,
    "production_output": DIMENSIONLESS,
    "recycling_rate": DIMENSIONLESS,
    "revenue_emission_intensity": MASS_PER_MONEY,
    "revenue_output": MONEY,
    "waste_combusted_mass": MASS,
    "waste_composted_mass": MASS,
    "waste_disposed_mass": MASS,
    "waste_diverted_mass": MASS,
    "waste_other_managed_mass": MASS,
    "waste_recycled_mass": MASS,
    "waste_total_mass": MASS,
    # Demography batch (demography-1): vital rates, dependency ratios,
    # population-balance and migration meanings for reviewed a-b01..b03
    # records. Counts, stocks and rates are dimensionless by design: persons
    # never convert to other units, and per-1000/per-100 rate scales live in
    # the record expressions, not in unit scales.
    "child_population_0_4_stock": DIMENSIONLESS,
    "child_woman_ratio": DIMENSIONLESS,
    "crude_birth_rate": DIMENSIONLESS,
    "crude_death_rate": DIMENSIONLESS,
    "crude_net_migration_rate": DIMENSIONLESS,
    "death_period_count": DIMENSIONLESS,
    "dependency_ratio": DIMENSIONLESS,
    "elderly_dependent_population": DIMENSIONLESS,
    "emigration_period_count": DIMENSIONLESS,
    "female_population_15_49_stock": DIMENSIONLESS,
    "female_population_stock": DIMENSIONLESS,
    "final_period_population": DIMENSIONLESS,
    "immigration_period_count": DIMENSIONLESS,
    "initial_period_population": DIMENSIONLESS,
    "live_birth_period_count": DIMENSIONLESS,
    "male_population_stock": DIMENSIONLESS,
    "midperiod_reference_population": DIMENSIONLESS,
    "natural_increase_count": DIMENSIONLESS,
    "natural_increase_rate": DIMENSIONLESS,
    "net_migration_period_count": DIMENSIONLESS,
    "old_age_dependency_ratio": DIMENSIONLESS,
    "sex_ratio": DIMENSIONLESS,
    "working_age_population": DIMENSIONLESS,
    "youth_dependency_ratio": DIMENSIONLESS,
    "youth_dependent_population": DIMENSIONLESS,
    # Orbital batch (orbital-2): mean motion, two-body energies, vis-viva,
    # barycenter and reduced-mass meanings for reviewed a-b03..b05 records.
    # Includes meanings for G/pi-inlining records whose r2s reuse them.
    "barycenter_distance": LENGTH,
    "binary_component_mass": MASS,
    "body_radius": LENGTH,
    "body_separation": LENGTH,
    "circular_orbit_kinetic_energy": ENERGY,
    "departure_radius": LENGTH,
    "departure_speed": VELOCITY,
    "gravitational_potential_energy": ENERGY,
    "hyperbolic_excess_velocity_squared": VELOCITY_SQUARED,
    "mean_motion": INVERSE_TIME,
    "primary_mass": MASS,
    "reduced_mass": MASS,
    "secondary_mass": MASS,
    "specific_angular_momentum_squared": SPECIFIC_ANGULAR_MOMENTUM_SQUARED,
    "surface_gravity": ACCELERATION,
    "vis_viva_velocity_squared": VELOCITY_SQUARED,
    # Circuits batch (circuits-2): conductance, current-density, drift,
    # source-characteristic, carrier-content and calibration meanings for
    # reviewed codex b03/b04 records. Includes meanings for the two
    # dimensional-literal records whose r2s reuse them.
    "area_mean_normal_current_density": CURRENT_DENSITY,
    "charge_carrier_number_density": NUMBER_DENSITY,
    "charge_per_carrier": CHARGE,
    "electrical_conductance": CONDUCTANCE,
    "electromotive_force": VOLTAGE,
    "mobile_carriers_per_host_entity": DIMENSIONLESS,
    "molar_mass": MOLAR_MASS,
    "normal_carrier_drift_velocity": VELOCITY,
    "relative_electrical_conductivity": DIMENSIONLESS,
    "surface_area": AREA,
    # Waves batch (waves-1): propagation, imaging, magnification, acoustic
    # and ranging meanings for reviewed codex b01/b02/b03/b04 records.
    # Curator quantity IDs adopted verbatim.
    "acoustic_target_range": LENGTH,
    "angular_magnification": DIMENSIONLESS,
    "eye_to_lens_distance": LENGTH,
    "eye_to_virtual_image_distance": LENGTH,
    "focal_length": LENGTH,
    "geometric_ray_path_length": LENGTH,
    "image_distance": LENGTH,
    "mach_number": DIMENSIONLESS,
    "object_distance": LENGTH,
    "observed_wave_frequency": INVERSE_TIME,
    "observer_velocity_toward_source_in_medium": VELOCITY,
    "optical_path_length": LENGTH,
    "optical_power": INVERSE_LENGTH,
    "phase_refractive_index": DIMENSIONLESS,
    "pulse_propagation_speed": VELOCITY,
    "round_trip_acoustic_time": TIME,
    "signed_optical_surface_curvature": INVERSE_LENGTH,
    "signed_optical_surface_radius": LENGTH,
    "signed_spherical_mirror_radius": LENGTH,
    "source_velocity_toward_observer_in_medium": VELOCITY,
    "source_wave_frequency": INVERSE_TIME,
    "transverse_magnification": DIMENSIONLESS,
    "unaided_near_point_distance": LENGTH,
    "wave_frequency": INVERSE_TIME,
    "wave_period": TIME,
    "wave_phase_speed": VELOCITY,
    "wavelength": LENGTH,
    # Waves batch (waves-2): beat, pupil and f-number meanings for reviewed
    # codex b05 records. The b06/b07/b08 r2s reuse waves-1 meanings.
    "acoustic_beat_frequency": INVERSE_TIME,
    "entrance_pupil_diameter": LENGTH,
    "f_number": DIMENSIONLESS,
    # Clinical batch (clinical-2): anthropometric, dosing, infusion,
    # clearance and filtration meanings for reviewed codex b01/b02/b03
    # records. Includes the Cockcroft-Gault meanings whose r3 reuses them.
    "administration_set_drop_factor": NUMBER_DENSITY,
    "body_mass_index": AREAL_DENSITY,
    "chronological_age_year_index": DIMENSIONLESS,
    "cockcroft_gault_female_branch_indicator": DIMENSIONLESS,
    "collected_urine_volume": VOLUME,
    "creatinine_clearance": VOLUME_FLOW,
    "glomerular_filtration_rate": VOLUME_FLOW,
    "glomerular_filtration_rate_per_body_surface_area": VELOCITY,
    "hip_circumference": LENGTH,
    "infused_fluid_volume": VOLUME,
    "labeled_active_drug_reference_mass": MASS,
    "labeled_liquid_reference_volume": VOLUME,
    "linear_body_extent": LENGTH,
    "mass_height_cubed_index": MASS_DENSITY,
    "mean_gravity_infusion_drop_rate": INVERSE_TIME,
    "prescribed_drug_mass_per_body_mass": DIMENSIONLESS,
    "prescribed_liquid_medication_volume": VOLUME,
    "standing_body_height": LENGTH,
    "urine_creatinine_mass_concentration": MASS_DENSITY,
    "waist_circumference": LENGTH,
    "waist_to_height_ratio": DIMENSIONLESS,
    "waist_to_hip_ratio": DIMENSIONLESS,
    # CS batch (cs-5): bit/byte rate and count meanings for the briefed
    # canonical-identity r2s. Curator quantity IDs adopted verbatim.
    "bit_rate": INVERSE_TIME,
    "byte_rate": INVERSE_TIME,
    "exbibit_rate": INVERSE_TIME,
    "exbibyte_rate": INVERSE_TIME,
    "gibibit_rate": INVERSE_TIME,
    "gigabit_rate": INVERSE_TIME,
    "gigabyte_rate": INVERSE_TIME,
    "kibibit_rate": INVERSE_TIME,
    "kilobit_rate": INVERSE_TIME,
    "mebibit_rate": INVERSE_TIME,
    "megabit_rate": INVERSE_TIME,
    "megabyte_rate": INVERSE_TIME,
    "pebibit_rate": INVERSE_TIME,
    "pebibyte_rate": INVERSE_TIME,
    "petabit_rate": INVERSE_TIME,
    "petabyte_rate": INVERSE_TIME,
    "tebibit_rate": INVERSE_TIME,
    "tebibyte_rate": INVERSE_TIME,
    "terabit_rate": INVERSE_TIME,
    "terabyte_rate": INVERSE_TIME,
    "mebibyte_rate": INVERSE_TIME,
    # Clinical batch (clinical-3): the Cockcroft-Gault divisor input meaning
    # for the r3 (empirical time-valued coefficient, seconds).
    "cockcroft_gault_divisor": TIME,
    # Mechanics batch (mechanics-2): path length is unsigned distance, not
    # signed displacement; averaged rate is average speed, not instantaneous
    # speed. Curator quantity IDs adopted verbatim.
    "distance": LENGTH,
    "average_speed": VELOCITY,
    # CS batch (cs-6): downtime and reference-year meanings for the
    # annual-downtime-hours r2.
    "steady_unavailability": DIMENSIONLESS,
    "annual_downtime": TIME,
    "reference_year_hours": TIME,
    # Building-energy batch (be-3): gray-surface radiative exchange meanings
    # for the stefan_boltzmann-naming r2. Curator quantity IDs adopted verbatim.
    "thermal_emissivity": DIMENSIONLESS,
    "heat_transfer_area": AREA,
    "absolute_surroundings_temperature": TEMPERATURE,
    "absolute_surface_temperature": TEMPERATURE,
    "net_radiative_heat_rate": POWER,
    # Economics batch (economics-cvp-b01): lane-B CVP unit-margin, volume,
    # fixed-cost, target-profit and adapter meanings. Per-unit money follows
    # the lane-A convention (MONEY, matching the currency^1 USD/unit axis);
    # unit counts and ratios are dimensionless. Curator quantity IDs adopted
    # verbatim.
    "selling_price_per_unit": MONEY,
    "variable_cost_per_unit": MONEY,
    "contribution_margin_per_unit": MONEY,
    "units_sold_or_produced": DIMENSIONLESS,
    "contribution_margin_income": MONEY,
    "fixed_operating_cost": MONEY,
    "break_even_unit_quantity": DIMENSIONLESS,
    "target_operating_profit": MONEY,
    "required_unit_sales_for_target_profit": DIMENSIONLESS,
    "operating_leverage_ratio": DIMENSIONLESS,
    "price_elasticity_of_demand": DIMENSIONLESS,
    # CFA-L1 batch, book-1 statistics/probability/regression (cfa-l1-1):
    # descriptive statistics, probability, distributions, inference,
    # regression and SEC income-statement money meanings for the reviewed
    # cfa-l1-b1 b25-b55 admittables. Curator quantity IDs adopted verbatim;
    # abstract data/response/predictor units keep every statistical meaning
    # dimensionless while statement amounts are MONEY. contingency_row_count
    # and contingency_column_count serve two dimensionless count roles
    # (marginal counts vs category counts) separated by context, never by
    # meaning alone; a future canonicalization may split the IDs.
    "absolute_mean_deviation": DIMENSIONLESS,
    "bernoulli_success_probability": DIMENSIONLESS,
    "bernoulli_trial_count": DIMENSIONLESS,
    "binomial_coefficient": DIMENSIONLESS,
    "binomial_mean_success_count": DIMENSIONLESS,
    "binomial_success_count": DIMENSIONLESS,
    "binomial_success_count_variance": DIMENSIONLESS,
    "categorical_independence_chi_square_statistic": DIMENSIONLESS,
    "centered_cross_product": DIMENSIONLESS,
    "combinatorial_outcome_count": DIMENSIONLESS,
    "confidence_bound_side": DIMENSIONLESS,
    "contingency_column_count": DIMENSIONLESS,
    "contingency_independence_degrees_of_freedom": DIMENSIONLESS,
    "contingency_row_count": DIMENSIONLESS,
    "cost_of_sales": MONEY,
    "cubed_mean_deviation": DIMENSIONLESS,
    "cumulative_distribution_probability": DIMENSIONLESS,
    "data_range": DIMENSIONLESS,
    "expected_cell_frequency": DIMENSIONLESS,
    "explained_response_sum_of_squares": DIMENSIONLESS,
    "first_quartile": DIMENSIONLESS,
    "fitted_regression_response": DIMENSIONLESS,
    "fourth_power_mean_deviation": DIMENSIONLESS,
    "geometric_mean": DIMENSIONLESS,
    "geometric_mean_periodic_return": DIMENSIONLESS,
    "gross_profit_amount": MONEY,
    "hypothesized_population_mean": DIMENSIONLESS,
    "income_before_income_taxes": MONEY,
    "interpolated_quantile": DIMENSIONLESS,
    "interquartile_range": DIMENSIONLESS,
    "large_sample_excess_kurtosis_approximation": DIMENSIONLESS,
    "large_sample_skewness_approximation": DIMENSIONLESS,
    "linear_response_logpredictor_intercept": DIMENSIONLESS,
    "linear_response_logpredictor_slope": DIMENSIONLESS,
    "linearlog_fitted_response": DIMENSIONLESS,
    "log_response_linear_predictor_slope": DIMENSIONLESS,
    "log_response_regression_intercept": DIMENSIONLESS,
    "loglog_regression_elasticity": DIMENSIONLESS,
    "loglog_regression_intercept": DIMENSIONLESS,
    "lower_adjacent_order_statistic": DIMENSIONLESS,
    "mean_absolute_deviation": DIMENSIONLESS,
    "net_income_amount": MONEY,
    "nonnegative_numerical_observation": DIMENSIONLESS,
    "normalized_backtransformed_loglinear_response": DIMENSIONLESS,
    "normalized_backtransformed_loglog_response": DIMENSIONLESS,
    "normalized_regression_predictor": DIMENSIONLESS,
    "observed_regression_response": DIMENSIONLESS,
    "one_sample_mean_test_statistic": DIMENSIONLESS,
    "operating_income_amount": MONEY,
    "order_location_fraction": DIMENSIONLESS,
    "pearson_cell_chi_square_contributions": DIMENSIONLESS,
    "periodic_gross_return_factor": DIMENSIONLESS,
    "population_mean_confidence_bound": DIMENSIONLESS,
    "positive_mean_interval_critical_value": DIMENSIONLESS,
    "probability_density": DIMENSIONLESS,
    "probability_mass": DIMENSIONLESS,
    "quantile_fraction": DIMENSIONLESS,
    "quantile_order_location": DIMENSIONLESS,
    "random_variable_threshold": DIMENSIONLESS,
    "regression_coefficient_of_determination": DIMENSIONLESS,
    "regression_predictor_value": DIMENSIONLESS,
    "regression_residual_standard_error": DIMENSIONLESS,
    "regression_response_residual": DIMENSIONLESS,
    "regression_sample_count": DIMENSIONLESS,
    "regression_sum_of_squares": DIMENSIONLESS,
    "residual_response_sum_of_squares": DIMENSIONLESS,
    "sample_covariance": DIMENSIONLESS,
    "sample_maximum": DIMENSIONLESS,
    "sample_mean": DIMENSIONLESS,
    "sample_mean_standard_error": DIMENSIONLESS,
    "sample_minimum": DIMENSIONLESS,
    "sample_observation_count": DIMENSIONLESS,
    "sample_standard_deviation": DIMENSIONLESS,
    "sample_variance": DIMENSIONLESS,
    "sampling_population_standard_deviation_or_estimate": DIMENSIONLESS,
    "separately_reported_operating_expenses": MONEY,
    "squared_mean_deviation": DIMENSIONLESS,
    "squared_response_deviation_terms": DIMENSIONLESS,
    "stage_choice_count": DIMENSIONLESS,
    "third_quartile": DIMENSIONLESS,
    "total_response_sum_of_squares": DIMENSIONLESS,
    "uniform_distribution_mean": DIMENSIONLESS,
    "uniform_distribution_variance": DIMENSIONLESS,
    "uniform_lower_support": DIMENSIONLESS,
    "uniform_upper_support": DIMENSIONLESS,
    "upper_adjacent_order_statistic": DIMENSIONLESS,
    # CFA-L1 batch, book-2 micro/macro/FX/trade economics (cfa-l1-1):
    # demand/supply/elasticities, production/cost, market structure,
    # national accounts, labor/price measurement, money/banking and
    # exchange-rate meanings for the reviewed cfa-l1-b2 b19-b42
    # admittables. Curator quantity IDs adopted verbatim. Good, service,
    # labor and population quantities are dimensionless counts; currency
    # amounts are MONEY in the record's stated currency; FX quotes are
    # dimensionless pair ratios; demand slopes dQ/dP are INVERSE_MONEY.
    "acquired_unit_marginal_valuation": MONEY,
    "actual_industry_output_index": DIMENSIONLESS,
    "actual_real_output": MONEY,
    "aggregate_employee_compensation": MONEY,
    "aggregate_gross_mixed_income": MONEY,
    "aggregate_gross_operating_surplus": MONEY,
    "aggregate_labor_hours": DIMENSIONLESS,
    "aggregate_price_inflation_rate": DIMENSIONLESS,
    "average_fixed_production_cost": MONEY,
    "average_input_product": DIMENSIONLESS,
    "average_sales_revenue": MONEY,
    "average_variable_production_cost": MONEY,
    "base_period_basket_base_price_value_terms": MONEY,
    "base_period_basket_current_price_value_terms": MONEY,
    "bilateral_fisher_price_index": DIMENSIONLESS,
    "bilateral_laspeyres_price_index": DIMENSIONLESS,
    "bilateral_paasche_price_index": DIMENSIONLESS,
    "capital_input_growth": DIMENSIONLESS,
    "capital_service_quantity": DIMENSIONLESS,
    "capital_service_rental_rate": MONEY,
    "change_in_autonomous_spending": MONEY,
    "change_in_equilibrium_output": MONEY,
    "closed_economy_spending_multiplier": DIMENSIONLESS,
    "closing_saleable_inventory_value": MONEY,
    "competitive_equilibrium_quantity": DIMENSIONLESS,
    "constant_marginal_production_cost": MONEY,
    "constant_price_gross_domestic_product": MONEY,
    "consumer_income": MONEY,
    "consumer_purchase_expenditure": MONEY,
    "consumer_surplus": MONEY,
    "cross_price_demand_elasticity": DIMENSIONLESS,
    "current_aggregate_price_index": DIMENSIONLESS,
    "current_period_basket_base_price_value_terms": MONEY,
    "current_period_basket_current_price_value_terms": MONEY,
    "demand_price_elasticity_magnitude": DIMENSIONLESS,
    "demand_slope_wrt_consumer_income": INVERSE_MONEY,
    "demand_slope_wrt_other_good_unit_price": INVERSE_MONEY,
    "demand_slope_wrt_own_good_unit_price": INVERSE_MONEY,
    "domestic_investment": MONEY,
    "domestic_price_level_fractional_change": DIMENSIONLESS,
    "economic_component_diffusion_fraction": DIMENSIONLESS,
    "economic_indicator_direction_score": DIMENSIONLESS,
    "employed_population": DIMENSIONLESS,
    "expected_future_spot_exchange_rate": DIMENSIONLESS,
    "expected_inflation_rate": DIMENSIONLESS,
    "export_demand_price_elasticity_magnitude": DIMENSIONLESS,
    "export_price_index": DIMENSIONLESS,
    "exports_share_of_total_trade": DIMENSIONLESS,
    "final_production_input": DIMENSIONLESS,
    "final_real_gdp": MONEY,
    "final_single_product_sales_revenue": MONEY,
    "final_total_economic_cost": MONEY,
    "final_total_product": DIMENSIONLESS,
    "first_order_revenue_fractional_change": DIMENSIONLESS,
    "fiscal_expenditure_multiplier": DIMENSIONLESS,
    "fixed_capital_consumption": MONEY,
    "foreign_price_level_fractional_change": DIMENSIONLESS,
    "forward_foreign_exchange_rate": DIMENSIONLESS,
    "fx_base_currency_annual_simple_rate": DIMENSIONLESS,
    "fx_covered_parity_forward_quote_price_per_base": DIMENSIONLESS,
    "fx_forward_interest_year_fraction": DIMENSIONLESS,
    "fx_forward_minus_spot_quote_difference": DIMENSIONLESS,
    "fx_forward_quote_price_per_base": DIMENSIONLESS,
    "fx_inverse_pair_ask": DIMENSIONLESS,
    "fx_inverse_pair_bid": DIMENSIONLESS,
    "fx_original_pair_ask": DIMENSIONLESS,
    "fx_original_pair_bid": DIMENSIONLESS,
    "fx_price_currency_annual_simple_rate": DIMENSIONLESS,
    "fx_rate_a_per_b": DIMENSIONLESS,
    "fx_rate_a_per_c": DIMENSIONLESS,
    "fx_rate_b_per_c": DIMENSIONLESS,
    "fx_spot_quote_price_per_base": DIMENSIONLESS,
    "fx_unannualized_forward_premium": DIMENSIONLESS,
    "gdp_price_deflator_ratio": DIMENSIONLESS,
    "goods_services_exports": MONEY,
    "goods_services_imports": MONEY,
    "government_budget_deficit": MONEY,
    "government_debt_gdp_ratio": DIMENSIONLESS,
    "government_debt_stock": MONEY,
    "government_final_purchases": MONEY,
    "government_purchases": MONEY,
    "government_saving": MONEY,
    "government_tax_revenue": MONEY,
    "government_transfer_payments": MONEY,
    "government_transfers_and_net_interest": MONEY,
    "gross_domestic_product": MONEY,
    "gross_fixed_capital_formation": MONEY,
    "gross_private_saving": MONEY,
    "gross_taxes": MONEY,
    "herfindahl_hirschman_fraction": DIMENSIONLESS,
    "hourly_labor_compensation": MONEY,
    "household_current_transfers_paid": MONEY,
    "household_current_transfers_received": MONEY,
    "household_disposable_income": MONEY,
    "household_employee_compensation": MONEY,
    "household_final_consumption": MONEY,
    "household_net_mixed_income": MONEY,
    "household_net_property_income": MONEY,
    "household_net_saving": MONEY,
    "household_pension_entitlement_adjustment": MONEY,
    "household_primary_income": MONEY,
    "household_saving_rate": DIMENSIONLESS,
    "import_demand_price_elasticity_magnitude": DIMENSIONLESS,
    "import_price_index": DIMENSIONLESS,
    "import_tariff_per_unit": MONEY,
    "import_tariff_revenue": MONEY,
    "income_demand_elasticity": DIMENSIONLESS,
    "income_gdp_statistical_discrepancy": MONEY,
    "income_velocity_money": DIMENSIONLESS,
    "incremental_household_consumption": MONEY,
    "incremental_household_disposable_income": MONEY,
    "incremental_input_product": DIMENSIONLESS,
    "incremental_production_cost": MONEY,
    "incremental_sales_revenue": MONEY,
    "industrial_capacity_utilization": DIMENSIONLESS,
    "industry_capacity_index": DIMENSIONLESS,
    "inflation_target_rate": DIMENSIONLESS,
    "initial_production_input": DIMENSIONLESS,
    "initial_real_gdp": MONEY,
    "initial_reserve_backed_deposit_injection": MONEY,
    "initial_single_product_sales_revenue": MONEY,
    "initial_total_economic_cost": MONEY,
    "initial_total_product": DIMENSIONLESS,
    "inventory_sales_ratio": DIMENSIONLESS,
    "inverse_demand_local_slope": MONEY,
    "inverse_demand_price_intercept": MONEY,
    "inverse_demand_slope_magnitude": MONEY,
    "inverse_supply_price_intercept": MONEY,
    "inverse_supply_slope": MONEY,
    "labor_factor_income_share": DIMENSIONLESS,
    "labor_force_participation_rate": DIMENSIONLESS,
    "labor_force_population": DIMENSIONLESS,
    "labor_input_growth": DIMENSIONLESS,
    "labor_service_quantity": DIMENSIONLESS,
    "labor_wage_rate": MONEY,
    "largest_firm_concentration_ratio": DIMENSIONLESS,
    "largest_firm_market_share": DIMENSIONLESS,
    "limiting_total_deposit_expansion": MONEY,
    "linear_demand_price_coefficient_magnitude": INVERSE_MONEY,
    "linear_demand_quantity_intercept": DIMENSIONLESS,
    "local_marginal_production_cost": MONEY,
    "local_marginal_sales_revenue": MONEY,
    "marginal_propensity_to_consume": DIMENSIONLESS,
    "marginal_propensity_to_consume_after_tax": DIMENSIONLESS,
    "matched_inflation_linked_bond_yield": DIMENSIONLESS,
    "matched_nominal_bond_yield": DIMENSIONLESS,
    "monopoly_stationary_price": MONEY,
    "net_barter_terms_of_trade_index": DIMENSIONLESS,
    "net_current_taxes": MONEY,
    "net_exports": MONEY,
    "net_fixed_capital_formation": MONEY,
    "net_production_product_import_taxes": MONEY,
    "nominal_exchange_rate_fractional_change": DIMENSIONLESS,
    "nominal_gross_domestic_product": MONEY,
    "nominal_interest_rate": DIMENSIONLESS,
    "nominal_money_stock": MONEY,
    "nominal_neutral_interest_rate_estimate": DIMENSIONLESS,
    "observed_breakeven_inflation_spread": DIMENSIONLESS,
    "operating_revenue": MONEY,
    "other_good_unit_price": MONEY,
    "other_income_and_gains": MONEY,
    "own_good_unit_price": MONEY,
    "own_price_demand_elasticity": DIMENSIONLESS,
    "own_price_demand_elasticity_magnitude": DIMENSIONLESS,
    "period_net_sales_value": MONEY,
    "physical_labor_productivity": DIMENSIONLESS,
    "post_tariff_domestic_demand": DIMENSIONLESS,
    "post_tariff_domestic_supply": DIMENSIONLESS,
    "post_tariff_import_quantity": DIMENSIONLESS,
    "potential_output_growth": DIMENSIONLESS,
    "potential_real_output": MONEY,
    "pre_tariff_domestic_demand": DIMENSIONLESS,
    "pre_tariff_domestic_supply": DIMENSIONLESS,
    "previous_aggregate_price_index": DIMENSIONLESS,
    "private_disposable_national_income": MONEY,
    "private_saving": MONEY,
    "product_price_fractional_change": DIMENSIONLESS,
    "production_input_service_quantity": DIMENSIONLESS,
    "proportional_net_tax_rate": DIMENSIONLESS,
    "quantity_demanded": DIMENSIONLESS,
    "quantity_sold": DIMENSIONLESS,
    "real_exchange_rate_fractional_change": DIMENSIONLESS,
    "real_interest_rate": DIMENSIONLESS,
    "real_output_per_labor_hour": MONEY,
    "real_output_simple_growth": DIMENSIONLESS,
    "required_bank_reserve_amount": MONEY,
    "required_bank_reserve_fraction": DIMENSIONLESS,
    "reserve_eligible_deposit_liabilities": MONEY,
    "resident_population": DIMENSIONLESS,
    "signed_real_output_level_gap": MONEY,
    "simple_reserve_deposit_multiplier": DIMENSIONLESS,
    "single_product_sales_revenue": MONEY,
    "squared_firm_market_share": DIMENSIONLESS,
    "stage_gross_output_value": MONEY,
    "stage_gross_value_added": MONEY,
    "stage_intermediate_consumption_value": MONEY,
    "symmetric_cournot_firm_output": DIMENSIONLESS,
    "tariff_consumer_surplus_loss": MONEY,
    "tariff_deadweight_loss": MONEY,
    "tariff_domestic_demand_decrease": DIMENSIONLESS,
    "tariff_domestic_supply_increase": DIMENSIONLESS,
    "tariff_producer_surplus_gain": MONEY,
    "total_consumption_willingness_to_pay": MONEY,
    "total_economic_cost": MONEY,
    "total_expenses_and_losses": MONEY,
    "total_factor_productivity_growth": DIMENSIONLESS,
    "total_fixed_production_cost": MONEY,
    "total_product_quantity": DIMENSIONLESS,
    "total_variable_production_cost": MONEY,
    "trade_export_value": MONEY,
    "trade_import_value": MONEY,
    "trend_real_output_growth_rate": DIMENSIONLESS,
    "unemployed_population": DIMENSIONLESS,
    "unemployment_rate": DIMENSIONLESS,
    "unit_labor_production_cost": MONEY,
    "weighted_marshall_lerner_response_expression": DIMENSIONLESS,
    # CFA-L1 batch, book-3 financial reporting and analysis (cfa-l1-1):
    # statements, inventories, depreciation, taxes, debt, leases, cash
    # flows, ratios, credit and operating metrics for the reviewed
    # cfa-l1-b3 b04-b101 admittables. Curator quantity IDs adopted
    # verbatim. Statement and position amounts are MONEY; ratios, rates,
    # counts and shares are dimensionless; activity durations use TIME
    # (curator-declared elapsed durations in days); selling area is AREA
    # and retail intensity MONEY_PER_AREA.
    "accounts_receivable_change": MONEY,
    "accrual_sales_revenue": MONEY,
    "accrued_period_expense": MONEY,
    "accumulated_depreciation": MONEY,
    "accumulated_depreciation_removed_on_disposal": MONEY,
    "accumulated_depreciation_to_gross_ppe": DIMENSIONLESS,
    "acquired_identifiable_net_assets": MONEY,
    "acquisition_consideration_fair_value": MONEY,
    "acquisition_goodwill": MONEY,
    "after_tax_operating_profit": MONEY,
    "after_tax_return_on_invested_capital": DIMENSIONLESS,
    "after_tax_shareholder_distribution": MONEY,
    "aggregate_net_deferred_tax_asset_position": MONEY,
    "aggregate_same_store_sales_growth": DIMENSIONLESS,
    "allowance_doubtful_accounts": MONEY,
    "allowance_for_doubtful_accounts": MONEY,
    "altman_original_z_score": DIMENSIONLESS,
    "amortization_expense": MONEY,
    "annualized_inventory_turnover": DIMENSIONLESS,
    "applicable_interest_tax_rate": DIMENSIONLESS,
    "asset_accumulated_depreciation": MONEY,
    "asset_beginning_book_value": MONEY,
    "asset_carrying_amount": MONEY,
    "asset_cumulative_tax_deductions": MONEY,
    "asset_deferred_tax_asset": MONEY,
    "asset_deferred_tax_liability": MONEY,
    "asset_disposal_costs": MONEY,
    "asset_estimated_residual_value": MONEY,
    "asset_fair_value": MONEY,
    "asset_fair_value_less_disposal_costs": MONEY,
    "asset_historical_cost": MONEY,
    "asset_original_tax_cost": MONEY,
    "asset_sale_proceeds": MONEY,
    "asset_tax_base": MONEY,
    "average_book_invested_capital": MONEY,
    "average_common_shareholders_equity": MONEY,
    "average_interest_bearing_debt": MONEY,
    "average_inventory": MONEY,
    "average_net_fixed_assets": MONEY,
    "average_shareholders_equity": MONEY,
    "average_total_assets": MONEY,
    "average_trade_payables": MONEY,
    "average_trade_receivables": MONEY,
    "average_working_capital": MONEY,
    "balance_sheet_common_size_fraction": DIMENSIONLESS,
    "balance_sheet_financial_leverage": DIMENSIONLESS,
    "balance_sheet_line_item": MONEY,
    "balance_sheet_total_assets": MONEY,
    "bank_approved_liquid_securities": MONEY,
    "bank_approved_liquid_securities_to_deposits": DIMENSIONLESS,
    "bank_average_interest_earning_assets": MONEY,
    "bank_central_bank_reserves": MONEY,
    "bank_net_interest_income": MONEY,
    "bank_net_interest_margin": DIMENSIONLESS,
    "bank_reserve_eligible_deposits": MONEY,
    "bank_reserves_to_eligible_deposits": DIMENSIONLESS,
    "bank_specified_deposit_liabilities": MONEY,
    "base_project_net_present_value": MONEY,
    "basic_earnings_per_common_share": MONEY,
    "beginning_accumulated_depreciation": MONEY,
    "beginning_cash_and_equivalents": MONEY,
    "beginning_depreciable_asset_book_value": MONEY,
    "beginning_gross_equipment_cost": MONEY,
    "beginning_retained_earnings": MONEY,
    "beginning_shareholders_equity": MONEY,
    "bond_amortization_period_count": DIMENSIONLESS,
    "bond_coupon_payment": MONEY,
    "bond_coupon_payment_per_period": MONEY,
    "bond_discount_premium_amortization_per_period": MONEY,
    "bond_face_amount": MONEY,
    "bond_interest_expense": MONEY,
    "bond_periodic_discount_rate": DIMENSIONLESS,
    "bond_remaining_coupon_periods": DIMENSIONLESS,
    "capex_share_gross_ppe_plus_capex": DIMENSIONLESS,
    "capital_expenditure": MONEY,
    "cash_and_cash_equivalents": MONEY,
    "cash_balance": MONEY,
    "cash_collected_from_customers": MONEY,
    "cash_conversion_cycle": TIME,
    "cash_flow_directional_common_size_fraction": DIMENSIONLESS,
    "cash_flow_directional_total": MONEY,
    "cash_flow_from_operating_activities": MONEY,
    "cash_flow_line_magnitude": MONEY,
    "cash_flow_line_to_net_revenue": DIMENSIONLESS,
    "cash_flow_statement_line": MONEY,
    "cash_flow_to_operating_income": DIMENSIONLESS,
    "cash_flow_to_revenue_ratio": DIMENSIONLESS,
    "cash_liquidity_ratio": DIMENSIONLESS,
    "cash_paid_accrued_expense": MONEY,
    "cash_paid_for_long_term_assets": MONEY,
    "cash_paid_inventory_suppliers": MONEY,
    "cash_paid_other_operating_expenses": MONEY,
    "cash_return_on_average_assets": DIMENSIONLESS,
    "cash_return_on_average_equity": DIMENSIONLESS,
    "change_in_accrued_operating_expenses": MONEY,
    "change_in_prepaid_operating_expenses": MONEY,
    "closing_bond_carrying_amount": MONEY,
    "closing_finance_lease_liability": MONEY,
    "combined_corporate_dividend_tax_rate": DIMENSIONLESS,
    "common_dividend_payout_ratio": DIMENSIONLESS,
    "common_share_dividends": MONEY,
    "common_share_market_price": MONEY,
    "common_shares_outstanding": DIMENSIONLESS,
    "company_sales_in_defined_market": MONEY,
    "company_sales_market_share": DIMENSIONLESS,
    "consignment_agent_commission_revenue": MONEY,
    "consignment_commission_rate": DIMENSIONLESS,
    "contract_allocated_transaction_price": MONEY,
    "contract_cost_based_progress": DIMENSIONLESS,
    "contract_cumulative_revenue": MONEY,
    "contract_eligible_costs_incurred": MONEY,
    "contract_previously_recognized_revenue": MONEY,
    "contract_progress": DIMENSIONLESS,
    "contract_revenue_catch_up_adjustment": MONEY,
    "contract_revised_cumulative_revenue": MONEY,
    "contract_total_expected_eligible_costs": MONEY,
    "convatec_adjusted_ebit_net_adjustments": MONEY,
    "convatec_adjusted_ebitda": MONEY,
    "convatec_depreciation_excluding_accelerated": MONEY,
    "convatec_post_ipo_share_compensation": MONEY,
    "convatec_software_and_rd_amortization": MONEY,
    "convertible_debt_after_tax_interest": MONEY,
    "corporate_income_tax_rate": DIMENSIONLESS,
    "cost_based_markup_fraction": DIMENSIONLESS,
    "cost_of_goods_sold": MONEY,
    "cost_plus_pricing_cost_basis": MONEY,
    "cost_plus_selling_price": MONEY,
    "cost_volume_profit_operating_income": MONEY,
    "credit_rating_adjusted_cfo": MONEY,
    "credit_rating_adjusted_debt": MONEY,
    "credit_rating_adjusted_ebitda": MONEY,
    "credit_rating_beginning_capital": MONEY,
    "credit_rating_capital": MONEY,
    "credit_rating_capital_expenditures": MONEY,
    "credit_rating_capital_other_adjustments": MONEY,
    "credit_rating_current_tax_expense": MONEY,
    "credit_rating_ebit": MONEY,
    "credit_rating_ending_capital": MONEY,
    "credit_rating_equity": MONEY,
    "credit_rating_ffo_other_adjustments": MONEY,
    "credit_rating_ffo_to_debt": DIMENSIONLESS,
    "credit_rating_focf_other_adjustments": MONEY,
    "credit_rating_focf_to_debt": DIMENSIONLESS,
    "credit_rating_free_operating_cash_flow": MONEY,
    "credit_rating_funds_from_operations": MONEY,
    "credit_rating_net_interest_expense": MONEY,
    "credit_rating_noncurrent_deferred_taxes": MONEY,
    "credit_rating_return_on_average_capital": DIMENSIONLESS,
    "credit_sales_receivables_turnover": DIMENSIONLESS,
    "current_assets": MONEY,
    "current_comparable_store_sales": MONEY,
    "current_income_tax_expense": MONEY,
    "current_income_tax_rate": DIMENSIONLESS,
    "current_liabilities": MONEY,
    "current_liquidity_ratio": DIMENSIONLESS,
    "current_revenue_at_prior_exchange_rates": MONEY,
    "current_trade_receivables": MONEY,
    "days_of_inventory_on_hand": TIME,
    "days_of_sales_outstanding": TIME,
    "days_of_trade_payables": TIME,
    "debt_extinguishment_consideration": MONEY,
    "debt_extinguishment_gain": MONEY,
    "debt_market_value": MONEY,
    "declining_balance_depreciation_rate": DIMENSIONLESS,
    "defensive_interval_duration": TIME,
    "deferred_income_tax_expense": MONEY,
    "deferred_revenue_future_nontaxable_amount": MONEY,
    "deferred_revenue_liability_carrying_amount": MONEY,
    "deferred_revenue_liability_tax_base": MONEY,
    "deferred_tax_asset_net_of_valuation_allowance": MONEY,
    "deferred_tax_asset_valuation_allowance": MONEY,
    "deferred_tax_liabilities": MONEY,
    "deferred_tax_liability_rate_change": MONEY,
    "deferred_tax_reversal_rate": DIMENSIONLESS,
    "defined_benefit_obligation_present_value": MONEY,
    "defined_benefit_plan_assets_fair_value": MONEY,
    "defined_benefit_plan_deficit": MONEY,
    "degree_combined_leverage": DIMENSIONLESS,
    "degree_financial_leverage": DIMENSIONLESS,
    "depreciable_asset_book_value": MONEY,
    "depreciable_asset_cost": MONEY,
    "depreciable_asset_residual_value": MONEY,
    "depreciation_expense": MONEY,
    "dividends_charged_to_retained_earnings": MONEY,
    "dividends_declared": MONEY,
    "dividends_paid": MONEY,
    "doubtful_accounts_allowance_to_gross_receivables": DIMENSIONLESS,
    "dupont_ebit_margin": DIMENSIONLESS,
    "dupont_interest_burden": DIMENSIONLESS,
    "dupont_tax_burden": DIMENSIONLESS,
    "early_payment_discount_fraction": DIMENSIONLESS,
    "earnings_before_interest_and_taxes": MONEY,
    "earnings_before_interest_taxes_depreciation_amortization": MONEY,
    "earnings_before_tax": MONEY,
    "earnings_retention_fraction": DIMENSIONLESS,
    "ebit_interest_coverage": DIMENSIONLESS,
    "ebit_to_total_assets": DIMENSIONLESS,
    "elapsed_depreciation_periods": DIMENSIONLESS,
    "eligible_consignment_sales": MONEY,
    "eligible_specific_borrowing_costs": MONEY,
    "ending_accumulated_depreciation": MONEY,
    "ending_cash_and_equivalents": MONEY,
    "ending_gross_equipment_cost": MONEY,
    "ending_retained_earnings": MONEY,
    "ending_shareholders_equity": MONEY,
    "enterprise_value": MONEY,
    "enterprise_value_equity_debt_cash": MONEY,
    "enterprise_value_to_ebitda": DIMENSIONLESS,
    "equity_market_value": MONEY,
    "estimated_lifetime_production_units": DIMENSIONLESS,
    "exchange_effect_cash_equivalents": MONEY,
    "extinguished_debt_carrying_amount": MONEY,
    "fifo_basis_net_income": MONEY,
    "fifo_cost_of_sales": MONEY,
    "fifo_cost_of_sales_excluding_writedown": MONEY,
    "fifo_inventory_carrying_amount": MONEY,
    "fifo_retained_earnings": MONEY,
    "final_period_depreciation_expense": MONEY,
    "finance_lease_liability_interest": MONEY,
    "financial_leverage_ratio": DIMENSIONLESS,
    "fixed_asset_turnover_ratio": DIMENSIONLESS,
    "fixed_capital_investment": MONEY,
    "fixed_charge_coverage_ratio": DIMENSIONLESS,
    "fixed_coupon_bond_price": MONEY,
    "fixed_operating_costs": MONEY,
    "free_cash_flow_to_equity": MONEY,
    "free_cash_flow_to_firm": MONEY,
    "goodwill_carrying_amount": MONEY,
    "gross_accounts_receivable": MONEY,
    "gross_asset_liquidation_value": MONEY,
    "gross_deferred_tax_asset": MONEY,
    "gross_equipment_cost_additions": MONEY,
    "gross_equipment_cost_removed_on_disposal": MONEY,
    "gross_operating_cash_payments": MONEY,
    "gross_operating_cash_receipts": MONEY,
    "gross_ppe_before_measured_capex": MONEY,
    "gross_profit": MONEY,
    "gross_profit_margin": DIMENSIONLESS,
    "gross_property_plant_and_equipment": MONEY,
    "gross_sales": MONEY,
    "hotel_average_daily_room_rate": MONEY,
    "hotel_room_nights_available": DIMENSIONLESS,
    "hotel_room_nights_sold": DIMENSIONLESS,
    "hotel_room_occupancy_rate": DIMENSIONLESS,
    "hotel_room_revenue": MONEY,
    "if_converted_debt_eps": MONEY,
    "if_converted_preferred_eps": MONEY,
    "income_statement_common_size_fraction": DIMENSIONLESS,
    "income_statement_line_item": MONEY,
    "income_statement_revenue": MONEY,
    "industry_sales": MONEY,
    "initial_bond_carrying_amount": MONEY,
    "initial_depreciable_asset_carrying_amount": MONEY,
    "insurance_combined_ratio": DIMENSIONLESS,
    "insurance_incurred_losses": MONEY,
    "insurance_net_premiums_earned": MONEY,
    "insurance_underwriting_expenses": MONEY,
    "interest_bearing_debt_to_assets": DIMENSIONLESS,
    "interest_bearing_debt_to_capital": DIMENSIONLESS,
    "interest_bearing_debt_to_ebitda": DIMENSIONLESS,
    "interest_expense": MONEY,
    "interest_paid_or_expense_matching_cfo": MONEY,
    "interest_tax_shield_rate": DIMENSIONLESS,
    "inventory_adjustment_tax_rate": DIMENSIONLESS,
    "inventory_balance_change": MONEY,
    "inventory_completion_cost": MONEY,
    "inventory_current_cost_per_unit": MONEY,
    "inventory_estimated_selling_price": MONEY,
    "inventory_layer_cost_per_unit": MONEY,
    "inventory_net_realisable_value": MONEY,
    "inventory_purchases": MONEY,
    "inventory_selling_cost": MONEY,
    "inventory_supplier_payables_change": MONEY,
    "inventory_turnover_annual_comparison_length": DIMENSIONLESS,
    "inventory_turnover_observed_period_length": DIMENSIONLESS,
    "inventory_turnover_ratio": DIMENSIONLESS,
    "inventory_writedown_charge": MONEY,
    "inventory_writedown_charge_in_cost_of_sales": MONEY,
    "issued_common_shares": DIMENSIONLESS,
    "issuer_defined_adjusted_ebit": MONEY,
    "lease_liability_payments": MONEY,
    "liability_carrying_amount": MONEY,
    "liability_deferred_tax_asset": MONEY,
    "liability_deferred_tax_liability": MONEY,
    "liability_future_tax_deduction": MONEY,
    "liability_tax_base": MONEY,
    "lifo_basis_net_income": MONEY,
    "lifo_cost_of_sales": MONEY,
    "lifo_inventory_carrying_amount": MONEY,
    "lifo_inventory_reserve": MONEY,
    "lifo_liquidation_gross_profit_effect": MONEY,
    "lifo_reserve_change": MONEY,
    "lifo_retained_earnings": MONEY,
    "liquidated_inventory_unit_count": DIMENSIONLESS,
    "liquidation_cost_fraction": DIMENSIONLESS,
    "long_lived_asset_sale_gain_loss": MONEY,
    "long_term_debt": MONEY,
    "long_term_debt_to_equity_ratio": DIMENSIONLESS,
    "market_capitalization_common_equity": MONEY,
    "market_equity_to_book_liabilities": DIMENSIONLESS,
    "market_to_tangible_book_equity_multiple": DIMENSIONLESS,
    "net_accounts_receivable": MONEY,
    "net_asset_liquidation_proceeds": MONEY,
    "net_borrowing": MONEY,
    "net_credit_sales": MONEY,
    "net_financing_cash_flow": MONEY,
    "net_income_attributable_to_common": MONEY,
    "net_income_attributable_to_parent": MONEY,
    "net_income_available_to_common": MONEY,
    "net_income_excluding_inventory_writedown": MONEY,
    "net_income_return_on_average_assets": DIMENSIONLESS,
    "net_investing_cash_flow": MONEY,
    "net_noncash_charges": MONEY,
    "net_noncash_income_adjustment": MONEY,
    "net_nonoperating_gains_in_income": MONEY,
    "net_operating_cash_flow": MONEY,
    "net_owner_capital_contributions": MONEY,
    "net_period_revenue": MONEY,
    "net_profit_margin": DIMENSIONLESS,
    "net_revenue": MONEY,
    "new_deferred_tax_rate": DIMENSIONLESS,
    "noncash_charges": MONEY,
    "noncash_working_capital_balance": MONEY,
    "noncash_working_capital_to_sales_fraction": DIMENSIONLESS,
    "old_deferred_tax_rate": DIMENSIONLESS,
    "opening_bond_carrying_amount": MONEY,
    "opening_finance_lease_liability": MONEY,
    "operating_cash_flow_debt_coverage": DIMENSIONLESS,
    "operating_cash_flow_dividend_coverage": DIMENSIONLESS,
    "operating_cash_flow_per_common_share": MONEY,
    "operating_cash_flow_reinvestment_coverage": DIMENSIONLESS,
    "operating_current_assets_change": MONEY,
    "operating_current_liabilities_change": MONEY,
    "operating_income": MONEY,
    "operating_lease_liability_interest_accretion": MONEY,
    "operating_lease_rou_amortization": MONEY,
    "operating_lease_single_cost": MONEY,
    "operating_profit": MONEY,
    "operating_profit_margin": DIMENSIONLESS,
    "operating_return_on_average_assets": DIMENSIONLESS,
    "option_outstanding_period_fraction": DIMENSIONLESS,
    "other_comprehensive_income": MONEY,
    "other_intangible_assets_carrying_amount": MONEY,
    "other_operating_expense": MONEY,
    "partial_period_inventory_turnover": DIMENSIONLESS,
    "period_cash_operating_expenditures": MONEY,
    "period_depreciation_expense": MONEY,
    "period_interest_payments": MONEY,
    "period_lease_payments": MONEY,
    "period_production_units": DIMENSIONLESS,
    "period_sales": MONEY,
    "preferred_dividends_for_eps": MONEY,
    "preferred_dividends_paid": MONEY,
    "pretax_corporate_profit": MONEY,
    "pretax_income": MONEY,
    "pretax_profit_margin": DIMENSIONLESS,
    "pretax_return_on_total_capital": DIMENSIONLESS,
    "prior_comparable_store_sales": MONEY,
    "prior_period_revenue": MONEY,
    "prior_rate_constant_currency_revenue_growth": DIMENSIONLESS,
    "profit_before_income_tax": MONEY,
    "project_net_present_value_with_real_option": MONEY,
    "project_npv_value_change_per_share": MONEY,
    "quick_liquidity_ratio": DIMENSIONLESS,
    "real_option_obtaining_cost": MONEY,
    "real_option_value": MONEY,
    "receivables_turnover_ratio": DIMENSIONLESS,
    "related_accrued_payable_change": MONEY,
    "reported_effective_income_tax_rate": DIMENSIONLESS,
    "reported_net_income": MONEY,
    "reported_operating_profit": MONEY,
    "reporting_period_duration": TIME,
    "retail_floor_area_square_feet": AREA,
    "retail_sales": MONEY,
    "retail_sales_per_square_foot": MONEY_PER_AREA,
    "retained_earnings_to_total_assets": DIMENSIONLESS,
    "retention_based_sustainable_growth_rate": DIMENSIONLESS,
    "return_on_average_common_equity": DIMENSIONLESS,
    "return_on_average_equity": DIMENSIONLESS,
    "sales_returns_and_allowances": MONEY,
    "sales_revenue": MONEY,
    "sales_to_total_assets": DIMENSIONLESS,
    "service_company_employee_count": DIMENSIONLESS,
    "service_company_net_income": MONEY,
    "service_company_revenue": MONEY,
    "service_net_income_per_employee": MONEY,
    "service_revenue_per_employee": MONEY,
    "shareholder_dividend_tax_rate": DIMENSIONLESS,
    "shares_assumed_issued_on_option_exercise": DIMENSIONLESS,
    "shares_assumed_repurchased_with_option_proceeds": DIMENSIONLESS,
    "short_term_marketable_securities": MONEY,
    "specific_borrowing_costs": MONEY,
    "tangible_book_value_equity": MONEY,
    "taxable_profit": MONEY,
    "taxable_temporary_difference": MONEY,
    "temporary_investment_income_specific_borrowing": MONEY,
    "total_asset_turnover_ratio": DIMENSIONLESS,
    "total_assets": MONEY,
    "total_comprehensive_income": MONEY,
    "total_debt_to_equity_ratio": DIMENSIONLESS,
    "total_interest_bearing_debt": MONEY,
    "total_liabilities": MONEY,
    "total_shareholders_equity": MONEY,
    "total_variable_costs": MONEY,
    "trade_credit_periodic_cost": DIMENSIONLESS,
    "trade_payables_turnover_ratio": DIMENSIONLESS,
    "trailing_earnings_per_common_share": MONEY,
    "trailing_price_earnings_ratio": DIMENSIONLESS,
    "treasury_common_shares": DIMENSIONLESS,
    "treasury_stock_method_eps": MONEY,
    "unanticipated_project_net_present_value": MONEY,
    "uncapped_declining_balance_depreciation": MONEY,
    "unit_selling_price": MONEY,
    "units_of_production_depreciation_expense": MONEY,
    "warrant_bond_lot_principal": MONEY,
    "warrant_linked_bond_principal": MONEY,
    "warrant_shares_per_bond_lot": DIMENSIONLESS,
    "warrant_subscribed_shares": DIMENSIONLESS,
    "weighted_average_common_shares": DIMENSIONLESS,
    "weighted_average_debt_conversion_shares": DIMENSIONLESS,
    "weighted_average_preferred_conversion_shares": DIMENSIONLESS,
    "working_capital_investment": MONEY,
    "working_capital_to_total_assets": DIMENSIONLESS,
    "working_capital_turnover_ratio": DIMENSIONLESS,
    # CFA-L1 batch, cross-slice statement meanings (cfa-l1-1): income,
    # tax and revenue meanings shared by book-1 and book-3 admittables.
    "income_tax_expense": MONEY,
    "net_income": MONEY,
    "net_sales_revenue": MONEY,
}
ORIGINS = frozenset({"fixture", "user-scenario", "observation", "generated", "derived"})


def finite(value: object, label: str) -> float:
    """Reject booleans, non-numbers, infinities and NaNs before numerical use."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ModelError(f"{label}: expected a finite number.")
    try:
        result = float(value)
    except (ValueError, OverflowError) as exc:
        raise NumericalError(
            f"{label}: number is outside the supported range."
        ) from exc
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
            raise ModelError(
                f"Cannot bind {self} to {target}: meaning/context mismatch."
            )
        if self.unit != target.unit and (
            UNITS[self.unit].dimensions[3] != 0 or UNITS[target.unit].dimensions[3] != 0
        ):
            raise ModelError(
                f"Cannot bind {self.unit} to {target.unit}: currency units never convert implicitly; "
                "route through an explicit rate model instead of assuming parity."
            )


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
            raise ModelError(
                f"Family size bound must be an integer from 1 to {MAX_FAMILY_SIZE}."
            )


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
        converted = finite(
            amount * UNITS[self.port.unit].scale / UNITS[target.unit].scale,
            "Converted input",
        )
        if (
            target.meaning == "period_count"
            and not (converted * UNITS[target.unit].scale).is_integer()
        ):
            raise ModelError(
                "Period count must be an integer number of annual periods."
            )
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
    branch: str | None = None


@dataclass(frozen=True)
class Composition:
    """A bounded scenario request, its instances, and its requested results."""

    id: str
    nodes: tuple[Node, ...]
    outputs: tuple[str, ...]
    purpose: str = "fixture"
