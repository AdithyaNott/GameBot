from PlayerRoles import RoleCard
from Constants import Faction

"""This is the standard Minion role in Werewolf Faction which implements the RoleCard interface."""


class Minion(RoleCard):

    # Initializing the faction, name, and description of the Minion role. Also setting is_lose_condition to False
    # where is_lose_condition is whether the Werewolf faction loss occurs based on this role dying.
    # And setting loses_to_tanner to True since minion loses if Tanner dies.

    def __init__(self):
        self.faction = Faction.WEREWOLF
        self.name = "Minion"
        self.is_lose_condition = False
        self.description = "During the night phase, the Minion will wake up and be able to see who the " \
                           "werewolves are, but the werewolves will not know the Minion's identity. \nAs part " \
                           "of the Werewolf faction, the Minion's goal is to make sure a werewolf does not die " \
                           "during the night phase. The Minion dying would also be a win for the Werewolf faction " \
                           "(and in turn the player holding the Minion card). "
        self.loses_to_tanner = True

    # To be implemented

    def do_night_action(self):
        pass
