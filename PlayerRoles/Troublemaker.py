from PlayerRoles.RoleCard import RoleCard
from Constants import Faction, HelperMethods
from Player import Player

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

    # The Troublemaker will select 2 other players of their choosing, and swap their current_roles

    def do_night_action(self, player, player_list, middle_cards):
        if not isinstance(player, Player):
            raise Exception("Error: A person who drew the Troublemaker role is not identified as of Player class.")
        other_players = [p for p in player_list if p.get_player_tag() != player.get_player_tag()]
        # Some user input to choose which 2 players the Troublemaker is swapping
        player_one = other_players[0]
        player_two = other_players[1]
        helper = HelperMethods()
        helper.swap_roles(player_one=player_one, player_two=player_two)
        print("You've swapped the roles of {} and {}".format(player_one.get_player_name(), player_two.get_player_name()))