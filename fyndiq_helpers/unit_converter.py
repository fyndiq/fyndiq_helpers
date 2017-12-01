from decimal import Decimal

MINOR_UNIT_CONVERSION_FACTOR = 100
ROUNDING_PRECISION = Decimal('1.00')


class UnitConverter:
    """
    Since Klarna uses minor units for payment amounts, we convert decimals to
    this format.
    1.0 -> 100

    When we send data back, we convert back to decimals.
    100 -> 1.0

    # TODO: make this class support all currencies.
    """

    @staticmethod
    def to_minor_units(amount: Decimal) -> int:
        assert type(amount) is Decimal, \
            "The input amount should be in string format."
        return int((Decimal(amount) *
                    MINOR_UNIT_CONVERSION_FACTOR).quantize(ROUNDING_PRECISION))

    @staticmethod
    def to_decimals(amount: int) -> Decimal:
        assert type(amount) is int, \
            "The input amount should be in integer format."
        return (Decimal(amount) / Decimal("100.0")).quantize(ROUNDING_PRECISION)  # noqa
