from PlayerRoles.RoleCard import RoleCard
from Constants import Faction
from Player import Player

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

    # The Werewolf player is informed of the other Werewolf players in the game. If there is only one Werewolf player,
    # they will get to look at a card from the center of their choosing.

    async def do_night_action(self, player, player_list, middle_cards, bot, client):
        if not isinstance(player, Player):
            raise Exception("Error: A person who drew the Werewolf role is not identified as of Player class.")
        other_werewolf_list = []
        # Todo in the future: Update this for other types of werewolves and doppelganger ofc.
        for p in player_list:
            if p.get_start_role().get_role_name() == player.get_start_role().get_role_name() and \
                    p.get_player_tag() != player.get_player_tag():
                other_werewolf_list.append(p.get_player_name())
        if len(other_werewolf_list) > 0:
            print("You wake up during the night... you see that the other werewolves are the following: ",
                  other_werewolf_list)
        else:
            print("You wake up during the night... you see that there are no other werewolves. You are now"
                  "allowed to look at one card from the center of your choice.")
            card_index = 0
            card_name = middle_cards[card_index].get_role_name()
            print("You choose to look at the middle of cards of index {} and you see the following role: {}"
                  .format(card_index, card_name))
