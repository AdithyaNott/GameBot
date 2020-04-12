from PlayerRoles import RoleCard
from Constants import Faction

"""This is the standard Seer role in Village Faction which implements the RoleCard interface."""


class Seer(RoleCard):

    # Initializing the faction, name and description of the Seer role.
    # And setting loses_to_tanner to True since Seer loses if Tanner dies.

    def __init__(self):
        self.faction = Faction.VILLAGE
        self.name = "Seer"
        self.description = "During the night phase, the Seer will wake up and look at either another player's card " \
                           "or 2 cards from the center of their choice. \nAs part of the Village faction, " \
                           "the Seer's goal is to ensure a werewolf dies during the voting phase. "
        self.loses_to_tanner = True

    # To be implemented

    def do_night_action(self):
        pass
