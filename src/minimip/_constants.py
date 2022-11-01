from enum import Enum, auto


class ConstraintSense(Enum):
    LT = auto()
    EQ = auto()
    GT = auto()


class ObjectiveSense(Enum):
    MIN = auto()
    MAX = auto()
