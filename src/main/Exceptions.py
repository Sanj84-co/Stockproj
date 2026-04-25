class DuplicateTickerError(Exception):
    pass
class TickerNotFoundError(Exception):
    pass
class EmptyTickerError(Exception):
    pass
class TooLongTickerError(Exception):
    pass
class InavlidTickerFormatError(Exception):
    pass
class InvalidPeriodError(Exception):
    pass
class AlertDoesNotExist(Exception):
    pass
class DuplicateAlertError(Exception):
    pass
class TransactionNotFoundError(Exception):
    pass 