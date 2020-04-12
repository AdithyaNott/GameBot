from PlayerRoles import RoleCard
from Constants import Faction

"""This is the standard Mason role in Village Faction which implements the RoleCard interface."""


class Mason(RoleCard):

    # Initializing the faction, name and description of the Mason role.
    # And setting loses_to_tanner to True since Mason loses if Tanner dies.

    def __init__(self):
        self.faction = Faction.VILLAGE
        self.name = "Mason"
        self.description = "During the night phase, the Mason will wake up and be informed of who the other Mason " \
                           "is in the game. If no one else has this role during the night phase, this means the " \
                           "other Mason card is in the center. \nAs part of the Village faction, the Mason's goal " \
                           "is to make sure a werewolf die during the voting phase. "
        self.loses_to_tanner = True

    # To be implemented

    def do_night_action(self):
        pass
