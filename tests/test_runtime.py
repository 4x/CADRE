"""Reference, compatibility, topology and lineage checks for the scalar core."""

from dataclasses import replace
from decimal import Decimal
from fractions import Fraction
import json
from pathlib import Path
from test_support import scratch_directory
import unittest

from connected_models.contracts import ACCELERATION, AMOUNT, AREA, AREAL_DENSITY, CHARGE, CONDUCTANCE, CONDUCTIVITY, CURRENT, CURRENT_DENSITY, DIMENSIONLESS, ENERGY, GRAVITATIONAL_PARAMETER, INVERSE_LENGTH, INVERSE_MONEY, INVERSE_TEMPERATURE, INVERSE_TIME, LENGTH, MASS, MASS_DENSITY, MASS_FLOW, MASS_PER_MONEY, MEANINGS, MOLAR_MASS, MONEY, NUMBER_DENSITY, POWER, RESISTANCE, RESISTIVITY, SPECIFIC_ANGULAR_MOMENTUM_SQUARED, SPECIFIC_ENERGY, SPECIFIC_HEAT, TEMPERATURE, THERMAL_RESISTANCE_AREA, TIME, TIME_SQUARED, UNITS, VELOCITY, VELOCITY_SQUARED, VOLTAGE, VOLUME, VOLUME_FLOW, Composition, ModelError, Node, Port, Reference, Value
from connected_models.demo import ANNUAL, HEAT, RATE, SAVING, YEARS, catalog, composition, fixture
from connected_models.runtime import execute, save_run


class RuntimeTests(unittest.TestCase):
    """Exercise independent oracles and deliberately invalid compositions."""

    def test_cashflow_oracle_and_reuse(self) -> None:
        """Compare closed-form execution to a separately summed Decimal cash flow."""
        models = catalog()
        run = execute(composition(), models)
        expected = sum(Decimal(2400) / Decimal("1.05") ** year for year in range(1, 11)) - Decimal(10000)
        self.assertEqual(run["status"], "completed")
        self.assertAlmostEqual(run["outputs"]["investment-npv"]["amount"], float(expected), places=8)
        costs = execute(composition(operation="operating-cost"), models)
        self.assertEqual(costs["outputs"]["annual-savings"]["amount"], 2400)
        self.assertEqual(len(run["steps"]), 7)
        self.assertEqual(len(costs["steps"]), 5)
        self.assertEqual(costs["outputs"]["baseline-cost"]["amount"], 3600)
        self.assertEqual(costs["outputs"]["upgrade-cost"]["amount"], 1200)

    def test_nist_published_reference(self) -> None:
        """Reproduce NIST HB135 (2020), equation 3-7, printed page 29."""
        graph = Composition("nist-reference", (Node("pv", "uniform-present-value@1", {
            "annual": fixture(100, SAVING, "NIST reference annual amount"),
            "rate": fixture(0.03, RATE, "NIST reference discount rate"),
            "years": fixture(5, YEARS, "NIST reference horizon"),
        }),), ("pv",))
        run = execute(graph, catalog())
        self.assertEqual(run["status"], "completed")
        self.assertAlmostEqual(run["outputs"]["pv"]["amount"], 457.97, delta=0.005)

    def test_units_and_meanings(self) -> None:
        """Convert Wh to kWh but reject electricity bound to delivered heat."""
        value = Value(12000, Port("delivered_heat", "Wh", ANNUAL), "fixture", "conversion case")
        self.assertEqual(value.bind(HEAT), 12)
        with self.assertRaisesRegex(ModelError, "meaning/context"):
            Value(12, Port("electricity_consumption", "kWh", ANNUAL), "fixture", "wrong meaning").bind(HEAT)
        with self.assertRaisesRegex(ModelError, "cannot use unit"):
            Port("delivered_heat", "USD", ANNUAL).validate()
        with self.assertRaisesRegex(ModelError, "meaning/context"):
            Value(12, replace(HEAT, context="different-home"), "fixture", "wrong context").bind(HEAT)

    def test_invalid_domains_and_nonfinite(self) -> None:
        """Invalid performance, prices and nonfinite inputs yield saved rejections."""
        for graph in (composition(performance=0), composition(tariff=-1), composition(performance=float("nan"))):
            with self.subTest(graph=graph):
                run = execute(graph, catalog())
                self.assertEqual(run["status"], "rejected")
                self.assertIn("error", run)
                with scratch_directory() as folder:
                    saved = save_run(run, Path(folder))
                    self.assertEqual(json.loads(saved.read_text())["status"], "rejected")

    def test_cycle_and_missing_input(self) -> None:
        """Reject cycles and missing inputs before producing any numerical steps."""
        original = composition()
        first = original.nodes[0]
        missing = replace(first, bindings={"heat": first.bindings["heat"]})
        run = execute(replace(original, nodes=(missing,) + original.nodes[1:]), catalog())
        self.assertEqual(run["status"], "rejected")
        self.assertEqual(run["steps"], [])
        model = replace(catalog()["annual-saving@1"], id="identity", inputs={"annual": SAVING},
                        output=SAVING, expression="annual", guards=())
        cycle = Composition("cycle", (Node("a", model.key, {"annual": Reference("b")}),
                                      Node("b", model.key, {"annual": Reference("a")})), ("a",))
        run = execute(cycle, {model.key: model})
        self.assertIn("cycle", run["error"])

    def test_expression_boundary(self) -> None:
        """Reject arbitrary code and dimensionally incorrect arithmetic."""
        for expression in ("__import__('os').getcwd()", "heat + performance", "heat[0]"):
            models = catalog()
            models["heat-to-electricity@1"] = replace(models["heat-to-electricity@1"], expression=expression)
            run = execute(composition(), models)
            self.assertEqual(run["status"], "rejected")
            self.assertEqual(run["steps"], [])

    def test_finance_vocabulary_batch(self) -> None:
        """Finance-1 meanings validate with their units; financial years stay non-physical."""
        pairs = {"future_value": ("USD", MONEY), "periodic_payment": ("USD", MONEY),
                 "effective_rate": ("1", DIMENSIONLESS), "nominal_rate": ("1", DIMENSIONLESS),
                 "signed_point_price_elasticity": ("1", DIMENSIONLESS), "unit_price": ("USD/unit", MONEY),
                 "quantity_price_derivative": ("unit^2/USD", INVERSE_MONEY),
                 "gross_domestic_product_current_price": ("USD", MONEY),
                 "gradient_amount": ("USD", MONEY), "interest_payment": ("USD", MONEY),
                 "principal_payment": ("USD", MONEY), "payment_index": ("periods", DIMENSIONLESS),
                 "implicit_price_deflator": ("index-point", DIMENSIONLESS),
                 "midyear_resident_population": ("person", DIMENSIONLESS),
                 "gross_domestic_product_real": ("USD_ref", MONEY),
                 "real_gdp_per_capita": ("USD_ref/person", MONEY),
                 "economic_profit": ("USD", MONEY),
                 "produced_quantity": ("unit", DIMENSIONLESS),
                 "finite_increment_marginal_cost": ("USD/unit", MONEY),
                 "gross_domestic_income_current_price": ("USD", MONEY),
                 "personal_saving_fraction": ("1", DIMENSIONLESS),
                 "unit_contribution_margin": ("USD/unit", MONEY),
                 "degree_operating_leverage": ("1", DIMENSIONLESS),
                 "allele_frequency": ("1", DIMENSIONLESS),
                 "effective_size": ("count", DIMENSIONLESS),
                 "selection_response": ("trait-units", DIMENSIONLESS),
                 "mutation_rate": ("1/site/generation", DIMENSIONLESS),
                 "genotype_count": ("count", DIMENSIONLESS),
                 "individual_count": ("count", DIMENSIONLESS),
                 "break_even_quantity": ("unit", DIMENSIONLESS),
                 "unit_variable_cost": ("USD/unit", MONEY),
                 "initial_payment": ("USD", MONEY),
                 "parallel_availability": ("1", DIMENSIONLESS),
                 "execution_time": ("s", TIME),
                 "byte_count": ("B", DIMENSIONLESS),
                 "gigabyte_count": ("GB", DIMENSIONLESS),
                 "gibibyte_count": ("GiB", DIMENSIONLESS),
                 "parallel_fraction": ("1", DIMENSIONLESS),
                 "component_speedup": ("1", DIMENSIONLESS),
                 "data_size": ("B", DIMENSIONLESS),
                 "transfer_rate": ("B/s", INVERSE_TIME),
                 "transfer_time": ("s", TIME),
                 "record_count": ("1", DIMENSIONLESS),
                 "record_size": ("B", DIMENSIONLESS),
                 "storage_capacity": ("B", DIMENSIONLESS),
                 "series_availability": ("1", DIMENSIONLESS),
                 "measured_speedup": ("1", DIMENSIONLESS),
                 "experimental_serial_fraction": ("1", DIMENSIONLESS),
                 "mtbf": ("h", TIME),
                 "mttr": ("h", TIME),
                 "mttf": ("h", TIME),
                 "inherent_availability": ("1", DIMENSIONLESS),
                 "expected_uptime": ("h", TIME),
                 "expected_downtime": ("h", TIME),
                 "window_availability": ("1", DIMENSIONLESS),
                 "instruction_count": ("1", DIMENSIONLESS),
                 "effective_cpi": ("1", DIMENSIONLESS),
                 "cycle_time": ("s", TIME),
                 "cpu_time": ("s", TIME),
                 "clock_frequency": ("Hz", INVERSE_TIME),
                 "mips_rating": ("MIPS", INVERSE_TIME),
                 "redesign_performance_ratio": ("1", DIMENSIONLESS),
                 "mean_downtime": ("h", TIME),
                 "operational_availability": ("1", DIMENSIONLESS),
                 "leg_count": ("1", DIMENSIONLESS),
                 "disk_count": ("1", DIMENSIONLESS),
                 "member_capacity": ("GB", DIMENSIONLESS),
                 "striped_usable_capacity": ("GB", DIMENSIONLESS),
                 "parity_usable_capacity": ("GB", DIMENSIONLESS),
                 "double_parity_usable_capacity": ("GB", DIMENSIONLESS),
                 "module_reliability": ("1", DIMENSIONLESS),
                 "tmr_reliability": ("1", DIMENSIONLESS),
                 "voted_availability": ("1", DIMENSIONLESS),
                 "leg_mtbf": ("h", TIME),
                 "series_mtbf": ("h", TIME),
                 "leg_mdt": ("h", TIME),
                 "series_mdt": ("h", TIME),
                 "parallel_mtbf": ("h", TIME),
                 "parallel_mdt": ("h", TIME),
                 "constant_failure_rate": ("1/h", INVERSE_TIME),
                 "basal_metabolic_rate": ("kcal/day", POWER),
                 "body_mass": ("kg", MASS),
                 "metabolic_normalization": ("kcal/day per kg^0.75",
                                               (Fraction(1, 4), Fraction(2), Fraction(-3), Fraction(0),
                                                Fraction(0), Fraction(0), Fraction(0))),
                 "electrical_power": ("W", POWER),
                 "operating_duration": ("h", TIME),
                 "point_heating_cop": ("1", DIMENSIONLESS),
                 "point_heating_heat_delivery": ("J", ENERGY),
                 "point_work_input": ("J", ENERGY),
                 "point_cooling_cop": ("1", DIMENSIONLESS),
                 "point_cooling_heat_removal": ("J", ENERGY),
                 "seasonal_heating_performance_hspf": ("Btu/Wh", DIMENSIONLESS),
                 "seasonal_space_heating_delivered": ("Btu", ENERGY),
                 "seasonal_electricity_consumption_hp": ("Wh", ENERGY),
                 "mass_density": ("kg/m3", MASS_DENSITY),
                 "volume": ("m3", VOLUME),
                 "latent_heat_coefficient": ("J/kg", SPECIFIC_ENERGY),
                 "latent_heat_transfer": ("J", ENERGY),
                 "absolute_hot_reservoir_temperature": ("K", TEMPERATURE),
                 "absolute_cold_reservoir_temperature": ("K", TEMPERATURE),
                 "carnot_heating_cop_bound": ("1", DIMENSIONLESS),
                 "carnot_cooling_cop_bound": ("1", DIMENSIONLESS),
                 "sensible_heat_transfer": ("J", ENERGY),
                 "specific_heat_capacity": ("J/(kg*K)", SPECIFIC_HEAT),
                 "temperature_difference": ("K", TEMPERATURE),
                 "thermal_resistance_area_normalized": ("m2*K/W", THERMAL_RESISTANCE_AREA),
                 "terminal_voltage": ("V", VOLTAGE),
                 "electric_current": ("A", CURRENT),
                 "absorbed_electrical_power": ("W", POWER),
                 "electrical_resistance": ("ohm", RESISTANCE),
                 "cross_sectional_area": ("m^2", AREA),
                 "electrical_resistivity": ("ohm m", RESISTIVITY),
                 "length": ("m", LENGTH),
                 "electrical_conductivity": ("S/m", CONDUCTIVITY),
                 "resistance_temperature_coefficient": ("K^-1", INVERSE_TEMPERATURE),
                 "time_averaged_electric_current": ("A", CURRENT),
                 "net_transferred_electric_charge": ("C", CHARGE),
                 "constituent_mass": ("kg", MASS),
                 "solution_volume": ("m^3", VOLUME),
                 "mass_concentration": ("kg/m^3", MASS_DENSITY),
                 "postpartum_body_mass_retention": ("kg", MASS),
                 "fractional_body_mass_decrease": ("1", DIMENSIONLESS),
                 "mean_body_mass_change_rate": ("kg/s", MASS_FLOW),
                 "mean_constituent_mass_infusion_rate": ("kg/s", MASS_FLOW),
                 "mean_volumetric_infusion_rate": ("m^3/s", VOLUME_FLOW),
                 "prescribed_drug_mass_per_administration": ("kg", MASS),
                 "prescribed_drug_mass_per_body_surface_area": ("kg/m^2", AREAL_DENSITY),
                 "serum_bun_creatinine_mass_ratio": ("1", DIMENSIONLESS),
                 "serum_creatinine_mass_concentration": ("kg/m^3", MASS_DENSITY),
                 "serum_urea_nitrogen_mass_concentration": ("kg/m^3", MASS_DENSITY),
                 "body_surface_area": ("m^2", AREA),
                 "calculated_mid_upper_arm_muscle_circumference": ("m", LENGTH),
                 "mid_upper_arm_circumference": ("m", LENGTH),
                 "triceps_skinfold_thickness": ("m", LENGTH),
                 "central_mass": ("kg", MASS),
                 "circular_orbit_velocity_squared": ("m^2/s^2", VELOCITY_SQUARED),
                 "escape_reference_radius": ("m", LENGTH),
                 "escape_velocity_squared": ("m^2/s^2", VELOCITY_SQUARED),
                 "inner_sidereal_period": ("d", TIME),
                 "orbit_radius": ("m", LENGTH),
                 "orbital_period": ("s", TIME),
                 "orbital_period_squared": ("s^2", TIME_SQUARED),
                 "orbiting_mass": ("kg", MASS),
                 "outer_sidereal_period": ("d", TIME),
                 "parallax_angle": ("rad", DIMENSIONLESS),
                 "parallax_baseline": ("m", LENGTH),
                 "parallax_distance": ("m", LENGTH),
                 "semi_major_axis": ("m", LENGTH),
                 "standard_gravitational_parameter": ("m3/s2", GRAVITATIONAL_PARAMETER),
                 "synodic_period": ("d", TIME),
                 "total_orbital_energy": ("J", ENERGY),
                 "accountable_fossil_co2": ("kg", MASS),
                 "activity_amount": ("kg", MASS),
                 "analyzed_combustion_co2": ("kg", MASS),
                 "biomass_co2_memo": ("kg", MASS),
                 "carbon_dioxide_equivalent": ("kg", MASS),
                 "diversion_rate": ("1", DIMENSIONLESS),
                 "emission_factor": ("kg/kg", DIMENSIONLESS),
                 "emission_intensity": ("kg/unit", MASS),
                 "emission_mass": ("kg", MASS),
                 "fuel_burned_mass": ("t", MASS),
                 "fuel_combustion_analysis_mass": ("t", MASS),
                 "fuel_feedstock_mass": ("t", MASS),
                 "fuel_purchased_mass": ("t", MASS),
                 "fuel_stock_mass": ("t", MASS),
                 "global_warming_potential": ("1", DIMENSIONLESS),
                 "greenhouse_gas_mass": ("kg", MASS),
                 "per_capita_generation": ("t/person", MASS),
                 "production_output": ("unit", DIMENSIONLESS),
                 "recycling_rate": ("1", DIMENSIONLESS),
                 "revenue_emission_intensity": ("kg/USD", MASS_PER_MONEY),
                 "revenue_output": ("USD", MONEY),
                 "waste_combusted_mass": ("t", MASS),
                 "waste_composted_mass": ("t", MASS),
                 "waste_disposed_mass": ("t", MASS),
                 "waste_diverted_mass": ("t", MASS),
                 "waste_other_managed_mass": ("t", MASS),
                 "waste_recycled_mass": ("t", MASS),
                 "waste_total_mass": ("t", MASS),
                 "child_population_0_4_stock": ("1", DIMENSIONLESS),
                 "child_woman_ratio": ("1", DIMENSIONLESS),
                 "crude_birth_rate": ("1", DIMENSIONLESS),
                 "crude_death_rate": ("1", DIMENSIONLESS),
                 "crude_net_migration_rate": ("1", DIMENSIONLESS),
                 "death_period_count": ("person", DIMENSIONLESS),
                 "dependency_ratio": ("1", DIMENSIONLESS),
                 "elderly_dependent_population": ("person", DIMENSIONLESS),
                 "emigration_period_count": ("person", DIMENSIONLESS),
                 "female_population_15_49_stock": ("1", DIMENSIONLESS),
                 "female_population_stock": ("1", DIMENSIONLESS),
                 "final_period_population": ("person", DIMENSIONLESS),
                 "immigration_period_count": ("person", DIMENSIONLESS),
                 "initial_period_population": ("person", DIMENSIONLESS),
                 "live_birth_period_count": ("person", DIMENSIONLESS),
                 "male_population_stock": ("1", DIMENSIONLESS),
                 "midperiod_reference_population": ("person", DIMENSIONLESS),
                 "natural_increase_count": ("1", DIMENSIONLESS),
                 "natural_increase_rate": ("1", DIMENSIONLESS),
                 "net_migration_period_count": ("person", DIMENSIONLESS),
                 "old_age_dependency_ratio": ("1", DIMENSIONLESS),
                 "sex_ratio": ("1", DIMENSIONLESS),
                 "working_age_population": ("person", DIMENSIONLESS),
                 "youth_dependency_ratio": ("1", DIMENSIONLESS),
                 "youth_dependent_population": ("person", DIMENSIONLESS),
                 "barycenter_distance": ("m", LENGTH),
                 "binary_component_mass": ("kg", MASS),
                 "body_radius": ("m", LENGTH),
                 "body_separation": ("m", LENGTH),
                 "circular_orbit_kinetic_energy": ("J", ENERGY),
                 "departure_radius": ("m", LENGTH),
                 "departure_speed": ("m/s", VELOCITY),
                 "gravitational_potential_energy": ("J", ENERGY),
                 "hyperbolic_excess_velocity_squared": ("m^2/s^2", VELOCITY_SQUARED),
                 "mean_motion": ("rad/s", INVERSE_TIME),
                 "primary_mass": ("kg", MASS),
                 "reduced_mass": ("kg", MASS),
                 "secondary_mass": ("kg", MASS),
                 "specific_angular_momentum_squared": ("m4/s2", SPECIFIC_ANGULAR_MOMENTUM_SQUARED),
                 "surface_gravity": ("m/s^2", ACCELERATION),
                 "vis_viva_velocity_squared": ("m^2/s^2", VELOCITY_SQUARED),
                 "area_mean_normal_current_density": ("A/m^2", CURRENT_DENSITY),
                 "charge_carrier_number_density": ("m^-3", NUMBER_DENSITY),
                 "charge_per_carrier": ("C", CHARGE),
                 "electrical_conductance": ("S", CONDUCTANCE),
                 "electromotive_force": ("V", VOLTAGE),
                 "mobile_carriers_per_host_entity": ("1", DIMENSIONLESS),
                 "molar_mass": ("kg/mol", MOLAR_MASS),
                 "normal_carrier_drift_velocity": ("m/s", VELOCITY),
                 "relative_electrical_conductivity": ("1", DIMENSIONLESS),
                 "surface_area": ("m^2", AREA),
                 "acoustic_target_range": ("m", LENGTH),
                 "angular_magnification": ("1", DIMENSIONLESS),
                 "eye_to_lens_distance": ("m", LENGTH),
                 "eye_to_virtual_image_distance": ("m", LENGTH),
                 "focal_length": ("m", LENGTH),
                 "geometric_ray_path_length": ("m", LENGTH),
                 "image_distance": ("m", LENGTH),
                 "mach_number": ("1", DIMENSIONLESS),
                 "object_distance": ("m", LENGTH),
                 "observed_wave_frequency": ("Hz", INVERSE_TIME),
                 "observer_velocity_toward_source_in_medium": ("m/s", VELOCITY),
                 "optical_path_length": ("m", LENGTH),
                 "optical_power": ("1/m", INVERSE_LENGTH),
                 "phase_refractive_index": ("1", DIMENSIONLESS),
                 "pulse_propagation_speed": ("m/s", VELOCITY),
                 "round_trip_acoustic_time": ("s", TIME),
                 "signed_optical_surface_curvature": ("1/m", INVERSE_LENGTH),
                 "signed_optical_surface_radius": ("m", LENGTH),
                 "signed_spherical_mirror_radius": ("m", LENGTH),
                 "source_velocity_toward_observer_in_medium": ("m/s", VELOCITY),
                 "source_wave_frequency": ("Hz", INVERSE_TIME),
                 "speed": ("m/s", VELOCITY),
                 "transverse_magnification": ("1", DIMENSIONLESS),
                 "unaided_near_point_distance": ("m", LENGTH),
                 "wave_frequency": ("Hz", INVERSE_TIME),
                 "wave_period": ("s", TIME),
                 "wave_phase_speed": ("m/s", VELOCITY),
                 "wavelength": ("m", LENGTH),
                 "acoustic_beat_frequency": ("Hz", INVERSE_TIME),
                 "entrance_pupil_diameter": ("m", LENGTH),
                 "f_number": ("1", DIMENSIONLESS),
                 "administration_set_drop_factor": ("drops/m^3", NUMBER_DENSITY),
                 "body_mass_index": ("kg/m^2", AREAL_DENSITY),
                 "chronological_age_year_index": ("years", DIMENSIONLESS),
                 "cockcroft_gault_female_branch_indicator": ("1", DIMENSIONLESS),
                 "collected_urine_volume": ("m^3", VOLUME),
                 "creatinine_clearance": ("m^3/s", VOLUME_FLOW),
                 "glomerular_filtration_rate": ("m^3/s", VOLUME_FLOW),
                 "glomerular_filtration_rate_per_body_surface_area": ("m/s", VELOCITY),
                 "hip_circumference": ("m", LENGTH),
                 "infused_fluid_volume": ("m^3", VOLUME),
                 "labeled_active_drug_reference_mass": ("kg", MASS),
                 "labeled_liquid_reference_volume": ("m^3", VOLUME),
                 "linear_body_extent": ("m", LENGTH),
                 "mass_height_cubed_index": ("kg/m^3", MASS_DENSITY),
                 "mean_gravity_infusion_drop_rate": ("drops/s", INVERSE_TIME),
                 "prescribed_drug_mass_per_body_mass": ("1", DIMENSIONLESS),
                 "prescribed_liquid_medication_volume": ("m^3", VOLUME),
                 "standing_body_height": ("m", LENGTH),
                 "urine_creatinine_mass_concentration": ("kg/m^3", MASS_DENSITY),
                 "waist_circumference": ("m", LENGTH),
                 "waist_to_height_ratio": ("1", DIMENSIONLESS),
                 "waist_to_hip_ratio": ("1", DIMENSIONLESS),
                 "bit_rate": ("bit/s", INVERSE_TIME),
                 "byte_rate": ("B/s", INVERSE_TIME),
                 "exbibit_rate": ("Eibit/s", INVERSE_TIME),
                 "exbibyte_rate": ("EiB/s", INVERSE_TIME),
                 "gibibit_rate": ("Gibit/s", INVERSE_TIME),
                 "gibibyte_count": ("GiB", DIMENSIONLESS),
                 "gigabit_rate": ("Gbit/s", INVERSE_TIME),
                 "gigabyte_count": ("GB", DIMENSIONLESS),
                 "gigabyte_rate": ("GB/s", INVERSE_TIME),
                 "kibibit_rate": ("Kibit/s", INVERSE_TIME),
                 "kilobit_rate": ("kbit/s", INVERSE_TIME),
                 "mebibit_rate": ("Mibit/s", INVERSE_TIME),
                 "megabit_rate": ("Mbit/s", INVERSE_TIME),
                 "megabyte_rate": ("MB/s", INVERSE_TIME),
                 "pebibit_rate": ("Pibit/s", INVERSE_TIME),
                 "pebibyte_rate": ("PiB/s", INVERSE_TIME),
                 "petabit_rate": ("Pbit/s", INVERSE_TIME),
                 "petabyte_rate": ("PB/s", INVERSE_TIME),
                 "tebibit_rate": ("Tibit/s", INVERSE_TIME),
                 "tebibyte_rate": ("TiB/s", INVERSE_TIME),
                 "terabit_rate": ("Tbit/s", INVERSE_TIME),
                 "terabyte_rate": ("TB/s", INVERSE_TIME),
                 "mebibyte_rate": ("MiB/s", INVERSE_TIME),
                 "cockcroft_gault_divisor": ("s", TIME),
                 "distance": ("m", LENGTH),
                 "average_speed": ("m/s", VELOCITY),
                 "steady_unavailability": ("1", DIMENSIONLESS),
                 "annual_downtime": ("h", TIME),
                 "reference_year_hours": ("h", TIME),
                 "thermal_emissivity": ("1", DIMENSIONLESS),
                 "heat_transfer_area": ("m2", AREA),
                 "absolute_surroundings_temperature": ("K", TEMPERATURE),
                 "absolute_surface_temperature": ("K", TEMPERATURE),
                 "net_radiative_heat_rate": ("W", POWER),
                "sum_of_money": ("USD", MONEY),
                "scaled_money": ("USD", MONEY),
                "difference_of_money": ("USD", MONEY),
                "payback_period_count": ("1", DIMENSIONLESS)}
        for meaning, (unit, dimensions) in pairs.items():
            Port(meaning, unit, "test-context").validate()
            self.assertEqual(MEANINGS[meaning], dimensions)
        financial_year = Port("elapsed_time", "years", "test-context")
        financial_year.validate()
        with self.assertRaises(ModelError):
            Port("elapsed_time", "s", "test-context").validate()
        with self.assertRaises(ModelError):
            Port("duration", "years", "test-context").validate()

    def test_currency_units_never_convert_implicitly(self) -> None:
        """USD, CAD and reference-year dollars bind only to their own unit string."""
        usd = Port("future_value", "USD", "test-context")
        usd.require_compatible(Port("future_value", "USD", "test-context"))
        kwh = Port("delivered_heat", "kWh", "test-context")
        kwh.require_compatible(Port("delivered_heat", "Wh", "test-context"))
        with self.assertRaisesRegex(ModelError, "never convert implicitly"):
            Port("future_value", "USD", "test-context").require_compatible(Port("future_value", "CAD", "test-context"))
        with self.assertRaisesRegex(ModelError, "never convert implicitly"):
            Port("economic_series_current_price", "USD", "test-context").require_compatible(
                Port("economic_series_current_price", "USD_ref", "test-context"))

    def test_mips_scale_lives_in_registry(self) -> None:
        """MIPS ratings convert to per-second magnitude through the unit scale, never an inlined literal."""
        rating = Value(2000.0, Port("mips_rating", "MIPS", "test-context"), "observation", "test-evidence")
        self.assertAlmostEqual(rating.bind(Port("mips_rating", "MIPS", "test-context")), 2000.0)
        self.assertEqual(UNITS["MIPS"].scale, 1000000.0)
        self.assertEqual(UNITS["Hz"].scale, 1.0)

    def test_building_energy_scales_close_algebra(self) -> None:
        """Btu, W and Btu/Wh scales collapse seasonal ratings without inlined factors."""
        self.assertAlmostEqual(UNITS["W"].scale, 1 / 3600000)
        self.assertAlmostEqual(UNITS["Btu"].scale, 1055.05585262 / 3600000)
        self.assertAlmostEqual(UNITS["Btu/Wh"].scale, 1055.05585262 / 3600)
        self.assertEqual(UNITS["J/kg"].scale, 1.0)
        hspf = Value(10.0, Port("seasonal_heating_performance_hspf", "Btu/Wh", "test-context"),
                     "observation", "test-evidence")
        seasonal_wh = Value(1000.0, Port("seasonal_electricity_consumption_hp", "Wh", "test-context"),
                            "observation", "test-evidence")
        canonical_kwh = (hspf.amount * UNITS["Btu/Wh"].scale) * (seasonal_wh.amount * UNITS["Wh"].scale)
        self.assertAlmostEqual(canonical_kwh / UNITS["Btu"].scale, 10000.0, places=6)

    def test_electrical_scales_close_ohm_and_power_laws(self) -> None:
        """V, ohm, S, C and m2*K/W scales close their laws through registry scales alone."""
        self.assertAlmostEqual(UNITS["V"].scale, 1 / 3600000)
        self.assertAlmostEqual(UNITS["ohm"].scale, 1 / 3600000)
        self.assertAlmostEqual(UNITS["S"].scale, 3600000)
        self.assertEqual(UNITS["A"].scale, 1.0)
        self.assertEqual(UNITS["C"].scale, 1.0)
        self.assertEqual(UNITS["K"].scale, 1.0)
        self.assertEqual(UNITS["mol"].scale, 1.0)
        self.assertAlmostEqual(UNITS["ohm m"].scale, UNITS["ohm"].scale * UNITS["m"].scale)
        self.assertAlmostEqual(UNITS["S/m"].scale, UNITS["S"].scale / UNITS["m"].scale)
        self.assertAlmostEqual(UNITS["A"].scale * UNITS["ohm"].scale, UNITS["V"].scale)
        self.assertAlmostEqual(UNITS["V"].scale * UNITS["A"].scale, UNITS["W"].scale)
        self.assertAlmostEqual(UNITS["C"].scale / UNITS["s"].scale, UNITS["A"].scale)
        self.assertAlmostEqual(1 / UNITS["ohm"].scale, UNITS["S"].scale)
        self.assertAlmostEqual(1 / UNITS["S/m"].scale, UNITS["ohm m"].scale)
        self.assertAlmostEqual(UNITS["K"].scale / UNITS["W"].scale * UNITS["m^2"].scale,
                               UNITS["m2*K/W"].scale)
        self.assertAlmostEqual(UNITS["J"].scale / UNITS["kg"].scale / UNITS["K"].scale,
                               UNITS["J/(kg*K)"].scale)
        self.assertEqual(UNITS["S"].dimensions, CONDUCTANCE)
        self.assertEqual(UNITS["mol"].dimensions, AMOUNT)
        with self.assertRaises(ModelError):
            Port("elapsed_time", "s", "test-context").validate()

    def test_clinical_scales_close_concentration_and_infusion(self) -> None:
        """Caret-spelled SI units share scales with their plain twins; laws close."""
        self.assertEqual(UNITS["kg/m^3"].scale, UNITS["kg/m3"].scale)
        self.assertEqual(UNITS["m^3"].scale, UNITS["m3"].scale)
        self.assertAlmostEqual(UNITS["kg/m^3"].scale, UNITS["kg"].scale / UNITS["m^3"].scale)
        self.assertAlmostEqual(UNITS["kg/s"].scale, UNITS["kg"].scale / UNITS["s"].scale)
        self.assertAlmostEqual(UNITS["kg/m^2"].scale, UNITS["kg"].scale / UNITS["m^2"].scale)
        self.assertAlmostEqual(UNITS["m^3/s"].scale, UNITS["m^3"].scale / UNITS["s"].scale)
        self.assertAlmostEqual(UNITS["kg/m^3"].scale * UNITS["m^3/s"].scale, UNITS["kg/s"].scale)

    def test_orbital_scales_close_period_and_energy_laws(self) -> None:
        """Days, squared units and the gravitational parameter compose through scales."""
        self.assertEqual(UNITS["d"].scale, 86400)
        self.assertEqual(UNITS["rad"].scale, 1.0)
        self.assertEqual(UNITS["m^2/s^2"].scale, 1.0)
        self.assertEqual(UNITS["s^2"].scale, 1.0)
        self.assertEqual(UNITS["m3/s2"].scale, 1.0)
        self.assertAlmostEqual(UNITS["s"].scale ** 2, UNITS["s^2"].scale)
        self.assertAlmostEqual(UNITS["m"].scale ** 2 / UNITS["s"].scale ** 2, UNITS["m^2/s^2"].scale)

    def test_revision_and_old_run_preservation(self) -> None:
        """New inputs and a compatible model revision leave earlier runs intact."""
        models = catalog()
        old = execute(composition(), models)
        new_model = replace(models["heat-to-electricity@1"], version="2", expression="heat / performance * 1.0")
        models[new_model.key] = new_model
        graph = composition(performance=2)
        graph = replace(graph, nodes=tuple(replace(node, model=new_model.key) if node.id == "upgrade-energy" else node for node in graph.nodes))
        new = execute(graph, models)
        self.assertEqual(new["status"], "completed")
        self.assertNotEqual(old["model_snapshot_sha256"], new["model_snapshot_sha256"])
        self.assertEqual(old["outputs"]["annual-savings"]["amount"], 2400)
        self.assertEqual(new["outputs"]["annual-savings"]["amount"], 1800)
        with scratch_directory() as folder:
            first = save_run(old, Path(folder))
            contents = first.read_bytes()
            save_run(new, Path(folder))
            self.assertEqual(first.read_bytes(), contents)
            with self.assertRaises(FileExistsError):
                save_run(old, Path(folder))
