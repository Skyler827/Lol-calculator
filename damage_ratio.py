from enum import Enum, auto

class DamageRatio(Enum):
    FLAT = auto()
    PERCENT_MAX_HP = auto()
    PERCENT_CURRENT_HP = auto()
    PERCENT_BONUS_HP = auto()
    PERCENT_MISSING_HP = auto()
