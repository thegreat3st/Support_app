from enum import IntEnum


class TicketStatus(IntEnum):
    NOT_STARTED = 1
    PENDING = 2
    CLOSED = 3