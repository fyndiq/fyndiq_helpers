from decimal import Decimal

MINOR_UNIT_CONVERSION_FACTOR = 100
ROUNDING_PRECISION = Decimal('1.00')
VAT_RATE_CONVERSION_FACTOR = 10000


class UnitConverter:
    """
    Provides functionality to convert decimal values to minor units
    and vice versa.

    Example:
        >>> assert UnitConverter.to_minor_units(Decimal('1.0') == 100

        >>> assert UnitConverter.to_decimals(100) == Decimal('1.0')

    # TODO: make this class support all currencies.
    """

    @staticmethod
    def to_minor_units(amount: Decimal) -> int:
        if type(amount) not in (Decimal, str):
            raise TypeError("amount should be a string or a Decimal")
        return int(round((Decimal(amount) *
                          MINOR_UNIT_CONVERSION_FACTOR).quantize(ROUNDING_PRECISION), 0))

    @staticmethod
    def to_decimals(amount: int) -> Decimal:
        return (Decimal(amount) / Decimal("100.0")).quantize(ROUNDING_PRECISION)  # noqa

    @staticmethod
    def vat_rate_to_decimal(vat_rate: int) -> Decimal:
        return (Decimal(vat_rate) / Decimal("10000.0")).quantize(ROUNDING_PRECISION)

    @staticmethod
    def vat_rate_to_minor_units(vat_rate: Decimal) -> int:
        if type(vat_rate) not in (Decimal, str):
            raise TypeError("vat_rate should be a string or a Decimal")
        return int(round((Decimal(vat_rate) *
                          VAT_RATE_CONVERSION_FACTOR).quantize(ROUNDING_PRECISION), 0))
