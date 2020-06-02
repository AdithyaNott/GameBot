from PlayerRoles.RoleCard import RoleCard
from Constants import Faction

"""This is the standard Villager role in Village faction which implements the RoleCard interface."""


class Villager(RoleCard):

    # Initializing the faction, name and description of the Villager role.
    # And setting loses_to_tanner to True since Villager loses if Tanner dies.

    def __init__(self):
        self.faction = Faction.VILLAGE
        self.name = "Villager"
        self.description = "A Villager does not make up during the night phase and does not have any special " \
                           "actions. \nAs part of the Village faction, the Villager's goal is to ensure a Werewolf " \
                           "dies during the voting phase. "
        self.loses_to_tanner = True
