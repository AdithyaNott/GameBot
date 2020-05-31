from PlayerRoles import RoleCard
from Constants import Faction
from Player import Player

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
                           "(and in turn the player holding the Minion card) assuming there are werewolves starting."
        self.loses_to_tanner = True

    # Iterate through player_list, see who has a Werewolf role and send that as a dm.

    def do_night_action(self, player, player_list, middle_cards):
        if not isinstance(player, Player):
            raise Exception("Error: A person who drew the Minion role is not identified as of Player class.")
        werewolf_list = []
        # Todo in the future: Update this for other types of werewolves and doppleganger ofc.
        for p in player_list:
            if p.get_start_role().get_role_name() == "Werewolf":
                werewolf_list.append(p.get_player_name())
        if len(werewolf_list) > 0:
            print("You wake up as minion during the night... You see the following players are werewolves:\n",
                  werewolf_list)
            print("However, they do not know your identity.")
        else:
            # Well now there were no werewolves, so minion needs to just not die
            print("You wake up as minion during the night... You see that there are no werewolves!!")
            print("So now you are a Werewolf!")
            print("Your new objective is to avoid dying.")