from PlayerRoles.RoleCard import RoleCard
from Constants import Faction, HelperMethods
import Constants
from Player import Player
import random
import asyncio

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

    async def do_night_action(self, player, player_list, middle_cards, bot, client):
        # This is a check which sees that the reaction added is of 1 of the below types.
        def check(reaction, user):
            return str(reaction.emoji) in Constants.DIGIT_EMOJIS[:len(other_players)]

        if not isinstance(player, Player):
            raise Exception("Error: A person who drew the Robber role is not identified as of Player class.")

        # Compiling list of players that can be stolen from
        other_players = [p for p in player_list if p.get_user() is not player.get_user()]

        # Some input here to generate which player the Robber Player decides to rob from.
        enquiry_str = "You now wake up as the robber during the night. Pick which player you would like to rob from.\n"
        # Adding options of which players to steal from and the reactions corresponding to them.
        for i in range(len(other_players)):
            enquiry_str += Constants.DIGIT_EMOJIS[i] + " - " + other_players[i].get_player_name()
            if i is not len(other_players) - 1:
                enquiry_str += "\n"
        enquiry_msg = await player.get_user().send(enquiry_str)
        for i in range(len(other_players)):
            await enquiry_msg.add_reaction(Constants.DIGIT_EMOJIS[i])

        automated_check = False
        stolen_role = -1
        # Give 60 seconds to complete the action, else just time out
        try:
            await client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await player.get_user().send("You did not complete your action in time, so you are robbing a "
                                         "random player.")
            stolen_role = random.randint(0, len(other_players) - 1)
            automated_check = True

        dm_channel = player.get_user().dm_channel
        while not automated_check:
            enquiry_msg = await dm_channel.fetch_message(enquiry_msg.id)
            for reaction in [r for r in enquiry_msg.reactions if r.count > 1]:
                if str(reaction) in Constants.DIGIT_EMOJIS[:len(other_players)]:
                    stolen_role = Constants.DIGIT_EMOJIS.index(str(reaction))
                    automated_check = True
                    break

        chosen_player = other_players[stolen_role]

        # Swap the roles of the 2 players
        HelperMethods.swap_roles(player_one=chosen_player, player_two=player)

        await player.get_user().send("You steal the role of " +
                                     chosen_player.get_player_name() +
                                     " and see your new role is " + chosen_player.get_current_role())
