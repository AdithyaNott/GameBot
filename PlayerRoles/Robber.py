from PlayerRoles import RoleCard
from Constants import Faction

"""This is the standard Robber role in Village Faction which implements the RoleCard interface."""


class Robber(RoleCard):

    # Initializing the faction, name and description of the Robber role.
    # And setting loses_to_tanner to True since Robber loses if Tanner dies.

    def __init__(self):
        self.faction = Faction.VILLAGE
        self.name = "Robber"
        self.description = "During the night phase, the Robber will wake up and swap their card for another" \
                           "player's card randomly. The Robber will get to see their new role. \nAs part of the " \
                           "Village faction, the Robber's goal is to ensure a werewolf dies during the voting phase. "
        self.loses_to_tanner = True

    # To be implemented

    def do_night_action(self):
        pass
