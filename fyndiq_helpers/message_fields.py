
from typing import NamedTumple


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
