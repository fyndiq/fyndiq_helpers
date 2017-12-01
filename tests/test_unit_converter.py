
import pytest
from decimal import Decimal

from fyndiq_helpers.unit_converter import UnitConverter


class TestConverter:

    # To minor units

    def test_to_minor_units(self):
        result = UnitConverter.to_minor_units("12.10")
        expected = 1210
        assert result == expected

    def test_to_minor_units_round_up(self):
        result = UnitConverter.to_minor_units("0.09999999999")
        expected = 10
        assert result == expected

    def test_to_minor_units_round_down(self):
        result = UnitConverter.to_minor_units("0.011")
        expected = 1
        assert result == expected

    def test_to_minor_units_from_float_assertion_error(self):
        with pytest.raises(AssertionError):
            UnitConverter.to_minor_units(12.1)

    # To decimals

    def test_to_decimals_success(self):
        result = UnitConverter.to_decimals(1210)
        expected = Decimal("12.10")
        assert result == expected

    def test_to_decimals_fraction(self):
        result = UnitConverter.to_decimals(9)
        expected = Decimal("0.09")
        assert result == expected

    def test_to_decimals_from_float_assertion_error(self):
        with pytest.raises(AssertionError):
            UnitConverter.to_decimals(12.10)

    def test_to_decimals_zero(self):
        result = UnitConverter.to_decimals(0)
        expected = Decimal("0.00")
        assert result == expected
