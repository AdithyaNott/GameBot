from PlayerRoles import RoleCard
from Constants import Faction
from Player import Player

"""This is the standard Insomniac role in Village Faction which implements the RoleCard interface."""


class Insomniac(RoleCard):

    # Initializing the faction, name and description of the Insomniac role.
    # And setting loses_to_tanner to True since Insomniac loses if Tanner dies.

    def __init__(self):
        self.faction = Faction.VILLAGE
        self.name = "Insomniac"
        self.description = "During the night phase (at the end), the Insomniac will eventually wake up " \
                           "and look at their role. \nAs part of the Village faction, the Insomniac's goal " \
                           "is to make sure a werewolf die during the voting phase. "
        self.loses_to_tanner = True

    # Gets to look at their current role during the night

    def do_night_action(self, player, player_list, middle_cards):
        if not isinstance(player, Player):
            raise Exception("Error: A person who drew the Insomniac role is not identified as of Player class.")
        current_role = player.get_current_role()
        # This will be sent as a dm obviously and such
        print("Your look at your role.....\nYou see that your new role is", current_role.get_role_name())
