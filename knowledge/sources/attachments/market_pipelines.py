#!/usr/bin/env python3
"""Ten illustrative prediction-market forecast pipelines; Python 3.9+ stdlib only.

Run `python market_pipelines.py --demo` for SYNTHETIC examples, or
`python market_pipelines.py input.json --draws 20000 --seed 1` where input.json is
{"market": "cpi", "data": {...}}.  See demo_inputs() for all 10 input schemas.
The arrays in those schemas must be replaced with real, point-in-time inputs.

Each `forecast_*` function connects distinct model stages.  Residual arrays must
be out-of-sample, same-horizon errors defined as FIRST PUBLISHED value minus the
then-available point forecast, in the units specified.  Bootstrap draws are not
necessarily independent or representative of the future.  Forecasts exclude
cancellation, source failure, rule disputes, missing reports, fees and fair-price
settlement unless explicitly stated.  Read the current contract rules first.
"""
import argparse
import json
import math
import random
from decimal import Decimal, ROUND_HALF_UP
from statistics import mean, stdev


def require_nonempty(values, name):
    if not values:
        raise ValueError(f"{name} must not be empty")


def probability(value, name):
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0, 1]")
    return value


def quantize(value, increment):
    """Illustrative nearest-increment, ties-away-from-zero reporting rule.

    Confirm each source/exchange's actual rounding before production use.
    """
    step = Decimal(str(increment))
    if step <= 0:
        raise ValueError("rounding increment must be positive")
    return float((Decimal(str(value)) / step).quantize(
        Decimal('1'), rounding=ROUND_HALF_UP) * step)


class EmpiricalErrorModel:
    """Point prediction + a resampled, out-of-sample first-release error."""
    def __init__(self, errors):
        require_nonempty(errors, "historical forecast errors")
        self.errors = list(errors)

    def sample(self, point, rng):
        return point + rng.choice(self.errors)


class EmpiricalScenarioModel:
    """Resample complete joint scenarios without breaking within-scenario dependence."""
    def __init__(self, scenarios):
        require_nonempty(scenarios, "scenarios")
        self.scenarios = list(scenarios)

    def sample(self, rng):
        return rng.choice(self.scenarios)


class Settlement:
    """Apply the exact supplied predicate to a simulated reported measurement."""
    def __init__(self, predicate):
        self.predicate = predicate

    def payout(self, reported):
        return float(self.predicate(reported))


class MonteCarlo:
    """Sample the entire connected pipeline and summarize payout uncertainty.

    Standard error is conditional Monte Carlo simulation error only: it excludes
    uncertainty in the estimated inputs, bias, model choice, and rule ambiguity.
    """
    def __init__(self, draws=10000, seed=1):
        if draws < 2:
            raise ValueError("draws must be at least 2")
        self.draws = draws
        self.rng = random.Random(seed)

    def run(self, sample_payout):
        samples = [float(sample_payout(self.rng)) for _ in range(self.draws)]
        if any(not 0 <= x <= 1 or not math.isfinite(x) for x in samples):
            raise ValueError("payouts must be finite values in [0, 1]")
        return {"expected_payout": mean(samples),
                "mc_standard_error": stdev(samples) / math.sqrt(self.draws),
                "draws": self.draws}


# 1. Rain: atmospheric scenarios -> rain codes at real observation times -> payout.
class StationObservationModel:
    """Each scenario supplies P(qualifying code) for each real observation time.

    For example use p_rain*detection + (1-p_rain)*false_positive, separately
    fitted at the station and conditioned on rain type.  Scenarios capture common
    weather uncertainty.  Observation codes are independent CONDITIONAL on the
    selected scenario; model spell dependence with richer scenarios if needed.
    Input probabilities must already encode METAR/SPECI weather-code semantics,
    station local-standard-time selection and qualifying observations only.
    """
    def sample_any_qualifying(self, per_observation_probabilities, rng):
        require_nonempty(per_observation_probabilities, "station observations")
        for p in per_observation_probabilities:
            probability(p, "station code probability")
        return any(rng.random() < p for p in per_observation_probabilities)


def forecast_rain(data, draws=10000, seed=1):
    scenarios = EmpiricalScenarioModel(data["code_prob_scenarios"])
    station = StationObservationModel()
    settle = Settlement(lambda observed: observed)
    return MonteCarlo(draws, seed).run(
        lambda rng: settle.payout(station.sample_any_qualifying(scenarios.sample(rng), rng)))


# 2, 3 and 5. Real-time point forecasts -> first-publication error -> reporting -> rule.
class PublishedEstimateModel:
    def __init__(self, forecast, first_release_errors, increment):
        self.forecast = forecast
        self.errors = EmpiricalErrorModel(first_release_errors)
        self.increment = increment

    def sample(self, rng):
        return quantize(self.errors.sample(self.forecast, rng), self.increment)


def forecast_cpi(data, draws=10000, seed=1):
    # All values in percentage points; the rounded release must be strictly above.
    release = PublishedEstimateModel(data["nowcast_pct"], data["errors_pct"], 0.1)
    settle = Settlement(lambda value: value > data["threshold_pct"])
    return MonteCarlo(draws, seed).run(lambda rng: settle.payout(release.sample(rng)))


def forecast_sofr(data, draws=10000, seed=1):
    # All values in percent, not basis points; publication increments of 0.01%.
    release = PublishedEstimateModel(data["nowcast_pct"], data["errors_pct"], 0.01)
    settle = Settlement(lambda value: value <= data["threshold_pct"])
    return MonteCarlo(draws, seed).run(lambda rng: settle.payout(release.sample(rng)))


def forecast_payrolls(data, draws=10000, seed=1):
    # Values are numbers of jobs, not thousands of jobs.
    release = PublishedEstimateModel(data["nowcast_jobs"], data["errors_jobs"], 1000)
    settle = Settlement(lambda value: value > data["threshold_jobs"])
    return MonteCarlo(draws, seed).run(lambda rng: settle.payout(release.sample(rng)))


# 4. Joint quarterly real GDP levels -> annual growth -> first release -> range.
class AnnualGDPModel:
    @staticmethod
    def growth_pct(prior_year_levels, current_year_levels):
        if len(prior_year_levels) != 4 or len(current_year_levels) != 4:
            raise ValueError("each GDP scenario needs exactly four quarterly levels")
        if any(x <= 0 for x in prior_year_levels + current_year_levels):
            raise ValueError("GDP levels must be positive")
        return 100.0 * (mean(current_year_levels) / mean(prior_year_levels) - 1.0)


def forecast_gdp(data, draws=10000, seed=1):
    # Levels must be consistent real GDP index/levels, same scale and vintage.
    scenarios = EmpiricalScenarioModel(data["quarterly_scenarios"])
    release_error = EmpiricalErrorModel(data["errors_pct"])
    settle = Settlement(lambda g: data["lower_pct"] <= g <= data["upper_pct"])
    def sample(rng):
        growth = AnnualGDPModel.growth_pct(data["prior_year_levels"], scenarios.sample(rng))
        return settle.payout(quantize(release_error.sample(growth, rng), 0.1))
    return MonteCarlo(draws, seed).run(sample)


# 6. Current global-temperature nowcast -> NCEI published anomaly -> record test.
def forecast_hottest_october(data, draws=10000, seed=1):
    # Same NCEI product, baseline and anomaly units for nowcast, errors and record.
    release = PublishedEstimateModel(data["nowcast_anomaly_c"], data["errors_c"],
                                     data["report_increment_c"])
    record = data["previous_october_record_c"]
    ties = data["tie_policy"]  # Explicitly chosen after checking the product rules.
    if ties not in ("yes", "no", "error"):
        raise ValueError("tie_policy must be yes, no or error")
    def payoff(value):
        if value == record:
            if ties == "error":
                raise ValueError("tie encountered; verify NCEI/exchange tie rules")
            return ties == "yes"
        return value > record
    settle = Settlement(payoff)
    return MonteCarlo(draws, seed).run(lambda rng: settle.payout(release.sample(rng)))


# 7 and 8. Elo strengths -> game outcomes -> game or season contract.
class EloGameModel:
    """Elo logistic win probability conditional on non-tie; external tie rate."""
    @staticmethod
    def sample(home_elo, away_elo, home_advantage, tie_probability, rng):
        probability(tie_probability, "tie_probability")
        if rng.random() < tie_probability:
            return "tie"
        p_home = 1.0 / (1.0 + 10.0 ** (-(home_elo + home_advantage - away_elo) / 400.0))
        return "home" if rng.random() < p_home else "away"


def forecast_nfl_game(data, draws=10000, seed=1):
    # game['selected'] identifies the team that receives $1 if it wins.
    game = data["game"]
    if game["selected"] not in ("home", "away"):
        raise ValueError("selected must be home or away")
    def sample(rng):
        outcome = EloGameModel.sample(game["home_elo"], game["away_elo"],
                                      game["home_advantage"], game["tie_probability"], rng)
        return 0.5 if outcome == "tie" else float(outcome == game["selected"])
    return MonteCarlo(draws, seed).run(sample)


def forecast_nfl_season(data, draws=10000, seed=1):
    # A single shared season shock affects every remaining game, introducing
    # dependence. Inputs specify each opponent and whether the target is at home.
    schedule = data["remaining_games"]
    if data["wins_so_far"] < 0 or data["team_elo_shock_sd"] < 0:
        raise ValueError("wins and shock SD must be nonnegative")
    def sample(rng):
        wins = data["wins_so_far"]
        team_elo = data["team_elo"] + rng.gauss(0, data["team_elo_shock_sd"])
        for game in schedule:
            if game["team_location"] == "home":
                home, away, selected = team_elo, game["opponent_elo"], "home"
            elif game["team_location"] == "away":
                home, away, selected = game["opponent_elo"], team_elo, "away"
            else:
                raise ValueError("team_location must be home or away")
            outcome = EloGameModel.sample(home, away, data["home_advantage"],
                                          data["tie_probability"], rng)
            wins += int(outcome == selected)
        return float(wins > data["threshold_wins"])
    return MonteCarlo(draws, seed).run(sample)


# 9. Joint first-release wage/CPI scenarios -> published real earnings -> payout.
class RealEarningsModel:
    @staticmethod
    def change_pct(wage_index, cpi_index):
        # Scenario inputs are December current/prior index RATIOS, same seasonal
        # adjustment. Real earnings growth = wage-ratio / CPI-ratio - 1.
        if wage_index <= 0 or cpi_index <= 0:
            raise ValueError("wage and CPI ratios must be positive")
        return 100.0 * (wage_index / cpi_index - 1.0)


def forecast_real_wages(data, draws=10000, seed=1):
    # Joint scenarios have wage_ratio and cpi_ratio in each dict. Do not
    # independently shuffle the two components, which would destroy correlation.
    scenarios = EmpiricalScenarioModel(data["joint_scenarios"])
    errors = EmpiricalErrorModel(data["errors_pct"])
    settle = Settlement(lambda value: value > 0.0)
    def sample(rng):
        path = scenarios.sample(rng)
        value = RealEarningsModel.change_pct(path["wage_ratio"], path["cpi_ratio"])
        return settle.payout(quantize(errors.sample(value, rng), 0.1))
    return MonteCarlo(draws, seed).run(sample)


# 10. Player availability -> passing-yard outcome -> season-total settlement.
class PlayerAvailabilityModel:
    @staticmethod
    def plays(p_active, rng):
        return rng.random() < probability(p_active, "active probability")


class PassingYardsModel:
    """Positive gross per-game yards: Gamma(shape, mean/shape).

    This simplified baseline excludes negative passing-yard totals. For exact
    accounting use an empirical/signed game-yard distribution instead.
    """
    @staticmethod
    def sample(expected_yards, shape, rng):
        if expected_yards < 0 or shape <= 0:
            raise ValueError("yards mean must be nonnegative and gamma shape positive")
        return rng.gammavariate(shape, expected_yards / shape) if expected_yards else 0.0


def forecast_passing_yards(data, draws=10000, seed=1):
    # Each joint scenario is a whole remaining schedule with game-level active
    # probability, expected yards conditional on playing, and gamma shape.
    # Scenario dependence can represent a persistent injury. Conditional game
    # participation and per-game yardage are independent in this baseline.
    scenarios = EmpiricalScenarioModel(data["remaining_scenarios"])
    def sample(rng):
        total = data["yards_so_far"]
        for game in scenarios.sample(rng):
            if PlayerAvailabilityModel.plays(game["p_active"], rng):
                total += PassingYardsModel.sample(game["yards_if_active"], game["shape"], rng)
        return float(total > data["threshold_yards"])
    return MonteCarlo(draws, seed).run(sample)


PIPELINES = {
    "rain": forecast_rain,
    "cpi": forecast_cpi,
    "sofr": forecast_sofr,
    "gdp": forecast_gdp,
    "payrolls": forecast_payrolls,
    "hottest_october": forecast_hottest_october,
    "nfl_game": forecast_nfl_game,
    "nfl_season": forecast_nfl_season,
    "real_wages": forecast_real_wages,
    "passing_yards": forecast_passing_yards,
}


def demo_inputs():
    """All numbers below are fictional and used ONLY to demonstrate interfaces."""
    return {
        "rain": {"code_prob_scenarios": [[.01, .02, .1, .05], [.05, .3, .4, .1]]},
        "cpi": {"nowcast_pct": .2, "errors_pct": [-.2, -.1, 0, .1, .2], "threshold_pct": -.2},
        "sofr": {"nowcast_pct": 3.88, "errors_pct": [-.03, -.02, 0, .01, .02], "threshold_pct": 3.85},
        "gdp": {"prior_year_levels": [100, 100.2, 100.4, 100.6],
                "quarterly_scenarios": [[101.3, 101.8, 102.1, 102.4], [101.2, 101.7, 102.0, 102.2]],
                "errors_pct": [-.1, 0, .1], "lower_pct": 1.6, "upper_pct": 2.0},
        "payrolls": {"nowcast_jobs": 90000, "errors_jobs": [-80000, -30000, 0, 30000, 80000],
                     "threshold_jobs": 50000},
        "hottest_october": {"nowcast_anomaly_c": 1.25, "errors_c": [-.1, -.02, 0, .03, .1],
                            "report_increment_c": .01, "previous_october_record_c": 1.21,
                            "tie_policy": "no"},
        "nfl_game": {"game": {"home_elo": 1550, "away_elo": 1500, "home_advantage": 50,
                              "tie_probability": .01, "selected": "home"}},
        "nfl_season": {"wins_so_far": 6, "team_elo": 1550, "team_elo_shock_sd": 50,
                       "home_advantage": 50, "tie_probability": .01, "threshold_wins": 8.5,
                       "remaining_games": [{"team_location": "home", "opponent_elo": 1500},
                                           {"team_location": "away", "opponent_elo": 1550},
                                           {"team_location": "home", "opponent_elo": 1600},
                                           {"team_location": "away", "opponent_elo": 1450}]},
        "real_wages": {"joint_scenarios": [{"wage_ratio": 1.04, "cpi_ratio": 1.03},
                                           {"wage_ratio": 1.03, "cpi_ratio": 1.04}],
                       "errors_pct": [-.1, 0, .1]},
        "passing_yards": {"yards_so_far": 2200, "threshold_yards": 3250.5,
                          "remaining_scenarios": [[{"p_active": .95, "yards_if_active": 240, "shape": 8} for _ in range(7)],
                                                  [{"p_active": .45, "yards_if_active": 210, "shape": 8} for _ in range(7)]]},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", help="local JSON file with market and data keys")
    parser.add_argument("--demo", action="store_true", help="use fictional inputs for all pipelines")
    parser.add_argument("--draws", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    if args.demo == bool(args.input):
        parser.error("provide exactly one of --demo or input JSON")
    if args.demo:
        result = {name: fn(demo_inputs()[name], args.draws, args.seed)
                  for name, fn in PIPELINES.items()}
        print(json.dumps({"warning": "Fictional inputs; not forecasts", "results": result}, indent=2))
    else:
        with open(args.input, encoding="utf-8") as handle:
            payload = json.load(handle)
        name = payload["market"]
        if name not in PIPELINES:
            parser.error("unknown market; choose from " + ", ".join(PIPELINES))
        print(json.dumps(PIPELINES[name](payload["data"], args.draws, args.seed), indent=2))


if __name__ == "__main__":
    main()
