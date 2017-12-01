from decimal import Decimal

from fyndiq_helpers.message_fields import MoneyField


class TestMoneyField():

    def test_init(self):
        amount = 1
        currency = 'SEK'

        mf = MoneyField(amount=amount, currency=currency)

        assert mf.amount == amount
        assert mf.currency == currency

    def test_to_decimals_should_return_decimal(self):
        amount = 1000
        currency = 'SEK'

        mf = MoneyField(amount=amount, currency=currency)
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

        new_amount_decimal = Decimal("20.00")
        expected_amount = 2000

        mf = MoneyField(amount=amount, currency=currency)

        mf.set_amount_from_decimal(new_amount_decimal)

        assert mf.amount == expected_amount
