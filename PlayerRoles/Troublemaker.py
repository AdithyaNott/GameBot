from PlayerRoles import RoleCard
from Constants import Faction

"""This is the standard Troublemaker role in Village Faction which implements the RoleCard interface."""


class Troublemaker(RoleCard):

    # Initializing the faction, name and description of the Troublemaker role.
    # And setting loses_to_tanner to True since Troublemaker loses if Tanner dies.

    def __init__(self):
        self.faction = Faction.VILLAGE
        self.name = "Troublemaker"
        self.description = "During the night phase, the Troublemaker will wake up and swap 2 player's " \
                           "cards of their choosing without looking at either of them (and while not being " \
                           "able to swap their own). \nAs part of the Village faction, the Troublemaker's goal " \
                           "is to make sure a Werewolf dies during the night phase. "
        self.loses_to_tanner = True

    # To be implemented

    def do_night_action(self):
        pass
