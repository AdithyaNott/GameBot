from PlayerRoles.RoleCard import RoleCard
from Constants import Faction
from Player import Player

"""This is the standard Seer role in Village Faction which implements the RoleCard interface."""


class Seer(RoleCard):

    # Initializing the faction, name and description of the Seer role.
    # And setting loses_to_tanner to True since Seer loses if Tanner dies.

    def __init__(self):
        self.faction = Faction.VILLAGE
        self.name = "Seer"
        self.description = "During the night phase, the Seer will wake up and look at either another player's card " \
                           "or 2 cards from the center of their choice. \nAs part of the Village faction, " \
                           "the Seer's goal is to ensure a werewolf dies during the voting phase. "
        self.loses_to_tanner = True

    # The seer chooses to look at the role of 1 other player or 2 center cards

    def do_night_action(self, player, player_list, middle_cards):
        if not isinstance(player, Player):
            raise Exception("Error: A person who drew the Seer role is not identified as of Player class.")
        # This is a boolean which is obviously set based on user input of whether they want to look at
        # another player's card or 2 from the center.
        check_player = True
        if check_player:
            other_players = [p for p in player_list if p.get_player_tag() != player.get_player_tag()]
            # Some input here to figure out which player the Seer wants to look at
            chosen_player = other_players[0]
            chosen_player_role = chosen_player.get_current_role().get_role_name()
            print("You look at the role of {}..... you see that their role is {}".format(chosen_player.get_player_name()
                                                                                         , chosen_player_role))
        else:
            # This is also chosen by input.... which will be updated
            first_card_index = 0
            second_card_index = 1
            first_card_name = middle_cards[first_card_index].get_role_name()
            second_card_name = middle_cards[second_card_index].get_role_name()
            print("You choose to look at the middle of cards of index {} and {}, "
                  "and you see the following 2 roles respectively: {} and {}".format(first_card_index,
                                                                                     second_card_index,
                                                                                     first_card_name, second_card_name))
