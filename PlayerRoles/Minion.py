from PlayerRoles.RoleCard import RoleCard
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
                           "(and in turn the player holding the Minion card) assuming there are werewolves starting.\n"\
                           "However if there are no werewolves among players during start of night, the minion is" \
                           " now a werewolf."
        self.loses_to_tanner = True

    # Iterate through player_list, see who has a Werewolf role and send that as a dm.

    async def do_night_action(self, player, player_list, middle_cards, bot, client):
        if not isinstance(player, Player):
            raise Exception("Error: A person who drew the Minion role is not identified as of Player class.")

        # Todo in the future: Update this for other types of werewolves and doppleganger ofc.
        werewolf_list = [p for p in player_list if p.get_start_role().get_role_name() == "Werewolf"]
        if len(werewolf_list) > 0:
            werewolf_string = ""
            for w in werewolf_list:
                werewolf_string += w.get_player_name()
                if w != werewolf_list[-1]:
                    w += ", "
            await player.get_user().send("You wake up as minion during the night... You see the following "
                                         "players are werewolves:\n" + werewolf_string)
            await player.get_user().send("However, they do not know your identity.")
        else:
            # Well now there were no werewolves, so minion needs to just not die
            await player.get_user().send("You wake up as minion during the night... "
                                         "You see that there are no werewolves!!")
            await player.get_user().send("So now you are a Werewolf!")
            await player.get_user().send("Your new objective is to avoid dying.")