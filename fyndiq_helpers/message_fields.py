from decimal import Decimal
from typing import NamedTuple

MINOR_UNIT_CONVERSION_FACTOR = 100


class MoneyField(NamedTuple):
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
    amount: int
    currency: str

    def to_decimals(self):
        return Decimal(amount / MINOR_UNIT_CONVERSION_FACTOR)

    def get_amount_from_decimal(self, decimal_amount: Decimal) -> int:
        return int(decimal_amount * Decimal(MINOR_UNIT_CONVERSION_FACTOR))

    def set_amount_from_decimal(self, decimal_amount: Decimal) -> None:
        self.amount = self.get_amount_from_decimal(decimal_amount: Decimal)
