from PlayerRoles import RoleCard
from Constants import Faction

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

    # To be implemented

    def do_night_action(self):
        pass
