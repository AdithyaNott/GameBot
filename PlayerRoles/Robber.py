from PlayerRoles import RoleCard
from Constants import Faction, HelperMethods
from Player import Player

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

    # Swaps current_role with that of another player per choosing

    def do_night_action(self, player, player_list, middle_cards):
        if not isinstance(player, Player):
            raise Exception("Error: A person who drew the Robber role is not identified as of Player class.")
        other_players = [p for p in player_list if p.get_player_tag() != player.get_player_tag()]
        # Some input here to generate which player the Robber Player decides to rob from.

        # Swap the roles of the 2 players
        chosen_player = other_players[0]
        HelperMethods.swap_roles(chosen_player, player)

        # And now the Robber is informed of their new role
        print("You now look at your new role.... and you see that you have drawn the role of", player.get_current_role().get_role_name())
