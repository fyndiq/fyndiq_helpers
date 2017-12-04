from decimal import Decimal

from fyndiq_helpers.unit_converter import UnitConverter


class MoneyField:
    """
    Represents the composite amount field for money values.
    Used by both events and commands.
    Avro will serialize it as follows:
    >>> {'amount': 1000, 'currency': 'SEK'}

    Examples:
        >>> from typing import Dict, NamedTuple
        >>> from eventsourcing_helpers.message import Event
        >>>
        >>> @Event
        >>> class CheckoutStarted(NamedTuple):
        >>>     total_amount = Dict[str, MoneyField]

    """

    @staticmethod
    def get_amount_from_decimal(decimal_amount: Decimal) -> int:
        return UnitConverter.to_minor_units(decimal_amount)

    def to_decimals(self) -> Decimal:
        return UnitConverter.to_decimals(self.amount)

    def set_amount_from_decimal(self, decimal_amount: Decimal) -> None:
        self.amount = self.get_amount_from_decimal(decimal_amount)

    def __init__(self, amount: int, currency: str) -> None:
        self.amount = amount
        self.currency = currency

    def to_dict(self):
        return {'amount': self.amount, 'currency': self.currency}
