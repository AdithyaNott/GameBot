from PlayerRoles.RoleCard import RoleCard
from Constants import Faction

"""This is the standard Hunter role in Village Faction which implements the RoleCard interface."""


class Hunter(RoleCard):

    # Initializing the faction, name and description of the Insomniac role.
    # And setting loses_to_tanner to True since Hunter loses if Tanner dies.

    def __init__(self):
        self.faction = Faction.VILLAGE
        self.name = "Hunter"
        self.description = "The Hunter does not have any special actions to perform during the night, and so " \
                           "doesn't wake up during the night phase. However, if the Hunter is killed during the " \
                           "voting phase, the Hunter dies and in addition the person the Hunter voted for dies. " \
                           "\nAs part of the Village faction, the Hunter's goal is to make sure a werewolf dies " \
                           "during the voting phase."
        self.loses_to_tanner = True
