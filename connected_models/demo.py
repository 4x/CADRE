"""Explicit synthetic heating-upgrade fixtures, not agent-curated model evidence."""

from .contracts import Composition, Model, Node, Port, Reference, Value

ANNUAL = "home-A:representative-year:constant-real-prices"
PERFORMANCE = "home-A:representative-year:whole-system-performance"
VALUATION = "home-A:valuation-date:constant-real-prices"
DISCOUNT = "annual-effective-real:year-end-cashflows"
HEAT = Port("delivered_heat", "kWh", ANNUAL)
ELECTRICITY = Port("electricity_consumption", "kWh", ANNUAL)
COP = Port("seasonal_performance", "1", PERFORMANCE)
TARIFF = Port("electricity_tariff", "USD/kWh", ANNUAL)
COST = Port("operating_cost", "USD", ANNUAL)
SAVING = Port("annual_saving", "USD", ANNUAL)
RATE = Port("discount_rate", "1", DISCOUNT)
YEARS = Port("period_count", "1", "annual-period-count")
PV = Port("present_value", "USD", VALUATION)
CAPEX = Port("upfront_cost", "USD", VALUATION)
NPV = Port("net_present_value", "USD", VALUATION)

DEFAULT_HEAT = 12_000.0
DEFAULT_COP = 3.0
DEFAULT_TARIFF = 0.30
DEFAULT_CAPEX = 10_000.0
DEFAULT_RATE = 0.05
DEFAULT_YEARS = 10


def catalog() -> dict[str, Model]:
    """Return source-informed but manually authored fixture model definitions."""
    energy_source = "https://www.extension.umd.edu/resource/home-energy-heat-pump"
    nist_source = "https://nvlpubs.nist.gov/nistpubs/hb/2020/NIST.HB.135-2020.pdf#page=61"
    models = [
        Model("heat-to-electricity", "1", {"heat": HEAT, "performance": COP}, ELECTRICITY,
              "heat / performance", ("heat >= 0", "performance > 0"), energy_source,
              ("Performance is effective seasonal delivered heat / whole-system electricity, not a point COP rating.",
               "Same delivered heat and comfort; auxiliaries/losses must already be included in the supplied performance.")),
        Model("electricity-cost", "1", {"energy": ELECTRICITY, "tariff": TARIFF}, COST,
              "energy * tariff", ("energy >= 0", "tariff >= 0"), "project-derived accounting identity: electricity times flat unit tariff",
              ("Flat real electricity price; unchanged fixed charges; excludes maintenance and cooling benefits.",)),
        Model("annual-saving", "1", {"baseline": COST, "alternative": COST}, SAVING,
              "baseline - alternative", (), "project-derived comparison: baseline cost minus alternative cost",
              ("Costs cover the same annual service and price basis.",)),
        Model("uniform-present-value", "1", {"annual": SAVING, "rate": RATE, "years": YEARS}, PV,
              "annual * (1 - (1 + rate) ** (-years)) / rate",
              ("rate > 0", "rate <= 1", "years > 0", "years <= 100"), nist_source,
              ("Constant real annual amount at each year end; positive annual effective real discount rate.",
               "No replacements, residual value, tariff escalation or degradation; horizon is a scenario, not a lifetime claim.")),
        Model("net-present-value", "1", {"benefit": PV, "investment": CAPEX}, NPV,
              "benefit - investment", ("investment >= 0",), "project-derived incremental investment accounting identity",
              ("Investment is incremental upfront cost relative to the baseline; no rebates or financing modeled.",)),
    ]
    return {model.key: model for model in models}


def fixture(amount: float, port: Port, label: str) -> Value:
    """Label every example input as a synthetic scenario, never an observation."""
    return Value(amount, port, "fixture", f"Synthetic example: {label}; not a measured household input.")


def composition(performance: float = DEFAULT_COP, investment: float = DEFAULT_CAPEX,
                tariff: float = DEFAULT_TARIFF, operation: str = "investment") -> Composition:
    """Build either an operating-cost or investment question through shared models."""
    heat = fixture(DEFAULT_HEAT, HEAT, "annual delivered heat")
    price = fixture(tariff, TARIFF, "flat real electricity tariff")
    nodes = [
        Node("baseline-energy", "heat-to-electricity@1", {"heat": heat, "performance": fixture(1.0, COP, "ideal resistance reference")}),
        Node("upgrade-energy", "heat-to-electricity@1", {"heat": heat, "performance": fixture(performance, COP, "effective seasonal performance")}),
        Node("baseline-cost", "electricity-cost@1", {"energy": Reference("baseline-energy"), "tariff": price}),
        Node("upgrade-cost", "electricity-cost@1", {"energy": Reference("upgrade-energy"), "tariff": price}),
        Node("annual-savings", "annual-saving@1", {"baseline": Reference("baseline-cost"), "alternative": Reference("upgrade-cost")}),
    ]
    outputs = ("baseline-cost", "upgrade-cost", "annual-savings")
    if operation == "investment":
        nodes.extend([
            Node("savings-present-value", "uniform-present-value@1", {"annual": Reference("annual-savings"),
                 "rate": fixture(DEFAULT_RATE, RATE, "annual real discount rate"), "years": fixture(DEFAULT_YEARS, YEARS, "study horizon")}),
            Node("investment-npv", "net-present-value@1", {"benefit": Reference("savings-present-value"), "investment": fixture(investment, CAPEX, "incremental installation cost")}),
        ])
        outputs += ("investment-npv",)
    return Composition(f"heating-{operation}", tuple(nodes), outputs)
