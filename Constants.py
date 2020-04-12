from enum import Enum

# This is an enum for the Faction which is used by the various classes implementing the RoleCard interface


class Faction(Enum):
    VILLAGE = 1
    WEREWOLF = 2
    NEUTRAL = 3
