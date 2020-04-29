from enum import Enum
from Player import Player
# This is an enum for the Faction which is used by the various classes implementing the RoleCard interface


class Faction(Enum):
    VILLAGE = 1
    WEREWOLF = 2
    NEUTRAL = 3

# This is a class for containing helper methods which will be used a lot


class HelperMethods:

    # Swaps the current_role attributes for 2 Players.

    def swap_roles(self, player_one, player_two):
        if not isinstance(player_one, Player) or not isinstance(player_two, Player):
            raise Exception("One of the Players passed in for swapping isn't of Player class")
        swapped_role = player_one.current_role
        player_one.set_current_role(player_two.current_role)
        player_two.set_current_role(swapped_role)
        return player_one, player_two