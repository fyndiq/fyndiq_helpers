
class ExtendedException(Exception):

    def __init__(self, details: dict) -> None:
        self.details = details

    def __str__(self):
        return self.details

    def __repr__(self):
        return self.details


class ValidationFailedException(ExtendedException):
    pass
