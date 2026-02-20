from decimal import Decimal

from django.test import TestCase

from calculadora.services import calculate_compound_interest


class CompoundInterestServiceTests(TestCase):
    def test_zero_interest_rate(self):
        result = calculate_compound_interest(
            principal=Decimal("1000"),
            monthly_contribution=Decimal("100"),
            rate_percent=Decimal("0"),
            rate_period="mensal",
            duration=12,
            duration_period="meses",
        )
        self.assertEqual(result["months"], 12)
        self.assertEqual(result["future_value"], Decimal("2200"))
        self.assertEqual(result["total_invested"], Decimal("2200"))
        self.assertEqual(result["interest_earned"], Decimal("0"))

    def test_annual_rate_conversion(self):
        result = calculate_compound_interest(
            principal=Decimal("1000"),
            monthly_contribution=Decimal("0"),
            rate_percent=Decimal("12"),
            rate_period="anual",
            duration=12,
            duration_period="meses",
        )
        monthly_rate_expected = (Decimal("1.12") ** (Decimal("1") / Decimal("12"))) - Decimal("1")
        self.assertAlmostEqual(
            float(result["monthly_rate"]),
            float(monthly_rate_expected),
            places=12,
        )

    def test_years_duration_conversion(self):
        result = calculate_compound_interest(
            principal=Decimal("500"),
            monthly_contribution=Decimal("50"),
            rate_percent=Decimal("0"),
            rate_period="mensal",
            duration=2,
            duration_period="anos",
        )
        self.assertEqual(result["months"], 24)
        self.assertEqual(result["total_invested"], Decimal("1700"))
        self.assertEqual(result["future_value"], Decimal("1700"))

    def test_known_values(self):
        result = calculate_compound_interest(
            principal=Decimal("1000"),
            monthly_contribution=Decimal("0"),
            rate_percent=Decimal("10"),
            rate_period="anual",
            duration=1,
            duration_period="anos",
        )
        self.assertAlmostEqual(float(result["future_value"]), 1100.0, places=6)
        self.assertAlmostEqual(float(result["interest_earned"]), 100.0, places=6)
