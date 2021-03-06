from decimal import Decimal

from fyndiq_helpers.message_fields import DecimalMoneyField, MoneyField


class TestMoneyField():

    def test_init(self):
        amount = 100
        currency = 'SEK'
        vat_amount = 25
        vat_rate = 2500

        mf = MoneyField(
            amount=amount,
            currency=currency,
            vat_amount=vat_amount,
            vat_rate=vat_rate
        )

        assert mf.amount == amount
        assert mf.currency == currency
        assert mf.vat_amount == vat_amount
        assert mf.vat_rate == vat_rate

    def test_to_decimals_should_return_decimal(self):
        amount = 1000
        currency = 'SEK'
        vat_amount = 250
        vat_rate = 2500

        mf = MoneyField(
            amount=amount,
            currency=currency,
            vat_amount=vat_amount,
            vat_rate=vat_rate
        )
        expected_decimal_amount = Decimal("10.00")

        assert mf.to_decimals() == expected_decimal_amount

    def test_get_amount_from_decimal_should_return_minor_units(self):
        expected_result = 1000
        decimal_amount = Decimal("10.00")

        result = MoneyField.get_amount_from_decimal(decimal_amount)
        assert result == expected_result

    def test_set_amount_from_decimal_should_update_amount(self):
        amount = 1000
        currency = 'SEK'
        vat_amount = 250
        vat_rate = 2500

        mf = MoneyField(
            amount=amount,
            currency=currency,
            vat_amount=vat_amount,
            vat_rate=vat_rate
        )

        new_amount_decimal = Decimal("20.00")
        expected_amount = 2000

        mf.set_amount_from_decimal(new_amount_decimal)

        assert mf.amount == expected_amount

    def test_to_dict_method(self):
        amount = 1000
        currency = 'SEK'
        vat_amount = 250
        vat_rate = 2500

        mf = MoneyField(
            amount=amount,
            currency=currency,
            vat_amount=vat_amount,
            vat_rate=vat_rate
        )

        expected_response = {
            'amount': amount,
            'currency': currency,
            'vat_amount': vat_amount,
            'vat_rate': vat_rate,
        }

        response = mf.to_dict()
        assert response == expected_response


class TestDecimalMoneyField:
    def test_init(self):
        amount = Decimal("10.0")
        currency = 'SEK'
        vat_amount = Decimal("2")
        vat_rate = Decimal("0.25")

        expected_amount = 1000
        expected_vat_amount = 200
        expected_vat_rate = 2500

        mf = DecimalMoneyField(
            decimal_amount=amount,
            currency=currency,
            decimal_vat_amount=vat_amount,
            decimal_vat_rate=vat_rate
        )

        assert mf.amount == expected_amount
        assert mf.currency == currency
        assert mf.vat_amount == expected_vat_amount
        assert mf.vat_rate == expected_vat_rate
