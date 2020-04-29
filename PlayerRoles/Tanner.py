from PlayerRoles import RoleCard
from Constants import Faction

"""This is the standard Tanner role in Neutral Faction which implements the RoleCard interface."""


class Tanner(RoleCard):

    # Initializing the faction, name and description of the Tanner role.
    # And setting loses_to_tanner to False since Tanner doesn't if Tanner dies.

    def __init__(self):
        self.faction = Faction.NEUTRAL
        self.name = "Tanner"
        self.description = "Tanner does not wake up during the night phase and has no special actions. \nTanner " \
                           "is technically part of the Village faction but is neutral, and Tanner wins " \
                           "only if Tanner himself is killed during the voting phase. If " \
                           "Tanner dies, all members of Werewolf faction lose. "
        self.loses_to_tanner = False
