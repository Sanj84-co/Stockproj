class DuplicateTickerError(Exception):
    pass
class TickerNotFoundError(Exception):
    pass
class EmptyTickerError(Exception):
    pass
watchlist =  {}
class TooLongTickerError(Exception):
    pass
class InavlidTickerFormatError(Exception):
    pass