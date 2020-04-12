from PlayerRoles import RoleCard
from Constants import Faction

"""This is the standard Werewolf role in Werewolf Faction which implements the RoleCard interface."""


class Werewolf(RoleCard):

    # Initializing the faction, name and description of the Werewolf role. Also setting is_lose_condition to True
    # where is_lose_condition is whether the Werewolf faction loss occurs based on this role dying.
    # And setting loses_to_tanner to True since Werewolf loses if Tanner dies.

    def __init__(self):
        self.faction = Faction.WEREWOLF
        self.name = "Werewolf"
        self.is_lose_condition = True
        self.description = "During the night phase, a Werewolf will wake up and be able to see other werewolves. " \
                           "If there are no other werewolves who wake up, the werewolf will be able to look at " \
                           "a card in the center of their choosing. \nAs part of the Werewolf faction, the " \
                           "Werewolf's goal is to make sure no werewolf dies during the voting phase. "
        self.loses_to_tanner = True
