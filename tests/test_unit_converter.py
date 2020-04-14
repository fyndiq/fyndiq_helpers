from decimal import Decimal

import pytest

from fyndiq_helpers.unit_converter import UnitConverter, UnitConverterPriceField


class TestConverter:

    # To minor units

    def test_to_minor_units(self):
        result = UnitConverter.to_minor_units(Decimal("12.10"))
        expected = 1210
        assert result == expected

    def test_to_minor_units_round_up(self):
        result = UnitConverter.to_minor_units(Decimal("0.095"))
        expected = 10
        assert result == expected

    def test_to_minor_units_round_down(self):
        result = UnitConverter.to_minor_units(Decimal("0.011"))
        expected = 1
        assert result == expected

    def test_to_minor_units_from_float_assertion_error(self):
        with pytest.raises(TypeError):
            UnitConverter.to_minor_units(12.1)

    def test_vat_rate_to_minor_units(self):
        assert UnitConverter.vat_rate_to_minor_units(Decimal("0.06")) == 600

    def test_vat_rate_to_minor_units_rounding(self):
        assert UnitConverter.vat_rate_to_minor_units(Decimal("0.06555555")) == 656

    # To decimals

    def test_to_decimals_success(self):
        result = UnitConverter.to_decimals(1210)
        expected = Decimal("12.10")
        assert result == expected

    def test_to_decimals_fraction(self):
        result = UnitConverter.to_decimals(9)
        expected = Decimal("0.09")
        assert result == expected

    def test_to_decimals_zero(self):
        result = UnitConverter.to_decimals(0)
        expected = Decimal("0.00")
        assert result == expected

    def test_vat_rate_to_decimal(self):
        assert UnitConverter.vat_rate_to_decimal(2500) == Decimal('0.25')

    def test_price_field_to_decimals(self):
        price_field = dict(
            amount=1000,
            vat_amount=250,
            vat_rate=2500,
            currency="SEK"
        )

        expected_result = dict(
            amount=10.0,
            vat_amount=2.5,
            vat_rate=0.25,
            currency="SEK"
        )

        assert expected_result == UnitConverterPriceField.convert_price_field_to_decimal(price_field)

