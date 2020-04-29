from PlayerRoles import RoleCard
from Constants import Faction
from Player import Player

"""This is the standard Mason role in Village Faction which implements the RoleCard interface."""


class Mason(RoleCard):

    # Initializing the faction, name and description of the Mason role.
    # And setting loses_to_tanner to True since Mason loses if Tanner dies.

    def __init__(self):
        self.faction = Faction.VILLAGE
        self.name = "Mason"
        self.description = "During the night phase, the Mason will wake up and be informed of who the other Mason " \
                           "is in the game. If no one else has this role during the night phase, this means the " \
                           "other Mason card is in the center. \nAs part of the Village faction, the Mason's goal " \
                           "is to make sure a werewolf die during the voting phase. "
        self.loses_to_tanner = True

    # Iterate through player_list, see who else has a Mason role and send that as a dm.

    def do_night_action(self, player, player_list, middle_cards):
        if not isinstance(player, Player):
            raise Exception("Error: A person who drew the Mason role is not identified as of Player class.")
        other_masons = []
        # Todo in the future: Update this for doppelganger Mason.
        for p in player_list:
            if p.get_player_tag() != player.get_player_tag() and p.get_start_role().get_role_name() \
                    == player.get_start_role().get_role_name():
                other_masons.append(p.get_player_name())
        # First check if there are no masons besides that person.
        if len(other_masons) == 0:
            print("You wake up around to look for other Masons.... and no one else has woken up")
        else:
            print("You wake up around to look for other Masons.... you notice the following are awake: \n", other_masons)