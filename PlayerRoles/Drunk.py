from PlayerRoles import RoleCard
from Constants import Faction
from Player import Player

"""This is the standard Drunk role in Village Faction which implements the RoleCard interface."""


class Drunk(RoleCard):

    # Initializing the faction, name and description of the Drunk role.
    # And setting loses_to_tanner to True since Drunk loses if Tanner dies.

    def __init__(self):
        self.faction = Faction.VILLAGE
        self.name = "Drunk"
        self.description = "During the night phase, the Drunk will wake up and swap their card for a card in the " \
                           "center of their choosing, but will not be able to see their new role.\n As part of the " \
                           "Village faction, the Drunk's goal is to make sure a werewolf dies during the voting phase. "
        self.loses_to_tanner = True

    # This action will be swapping the Player's current role with 1 from the middle (chosen by the Player).

    def do_night_action(self, player, player_list, middle_cards):
        # Some user input over here to decide which middle card to take. Basically index within
        # middle_cards array
        if not isinstance(player, Player):
            raise Exception("Error: A person who drew the Drunk role is not identified as of Player class.")
        middle_role = 0  # can also be 1 or 2 since 3 middle roles are present.
        new_middle_role = player.get_current_role()
        player.set_current_role(middle_cards[middle_role])
        middle_cards[middle_role] = new_middle_role
