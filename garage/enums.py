from enum import Enum


class JobStatus(Enum):
    INCOMING = "INCOMING"
    ACCEPTED = "ACCEPTED"
    STARTED = "STARTED"
    COMPLETED = "COMPLETED"


class QuoteStatus(Enum):
    OPEN = "OPEN"
    EXPIRED = "EXPIRED"
    CLOSED = "CLOSED"
