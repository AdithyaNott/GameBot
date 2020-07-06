from PlayerRoles.RoleCard import RoleCard
from Constants import Faction, HelperMethods
from Player import Player
import Constants
import random
import asyncio

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

    async def do_night_action(self, player, player_list, middle_cards, bot, client):
        # A check for seeing that the 1st player to "troublemake" is selected
        def first_card_check(reaction, user):
            return str(reaction.emoji) in Constants.DIGIT_EMOJIS[:len(other_players)]

        # A check for the second player to swap (by any valid reaction as the prev one except the one used
        def second_card_check(reaction, user):
            return Constants.DIGIT_EMOJIS.index(str(reaction.emoji)) in second_players_indices

        if not isinstance(player, Player):
            raise Exception("Error: A person who drew the Troublemaker role is not identified as of Player class.")
        other_players = [p for p in player_list if p.get_user() != player.get_user()]

        # Some user input to choose which 2 players the Troublemaker is swapping
        enquiry_str = "You wake up as Troublemaker. Which 2 players would you like to swap the roles of?\n"

        for i in range(len(other_players)):
            enquiry_str += Constants.DIGIT_EMOJIS[i] + " - " + other_players[i].get_player_name()
            if i is not len(other_players) - 1:
                enquiry_str += "\n"
        enquiry_msg = await player.get_user().send(enquiry_str)

        for i in range(len(other_players)):
            await enquiry_msg.add_reaction(Constants.DIGIT_EMOJIS[i])

        p1_index = -1
        p2_index = -1
        dm_channel = player.get_user().dm_channel

        # Check for time before first reaction is done
        try:
            await client.wait_for('reaction_add', timeout=30.0, check=first_card_check)
        except asyncio.TimeoutError:
            await player.get_user().send("You did not complete your action in time, so you are swapping the roles "
                                         "of 2 random players.")
            p1_index = random.randint(0, len(other_players) - 1)
            p2_index = random.choice([i for i in range(len(other_players)) if i is not p1_index])

        while p2_index == -1:
            enquiry_msg = await dm_channel.fetch_message(enquiry_msg.id)
            for reaction in [r for r in enquiry_msg.reactions if r.count > 1]:
                if p1_index == -1 and str(reaction) in Constants.DIGIT_EMOJIS[:len(other_players)]:
                    p1_index = Constants.DIGIT_EMOJIS.index(str(reaction))
                    second_players_indices = [i for i in range(3) if i is not p1_index]
                    try:
                        await client.wait_for('reaction_add', timeout=30.0, check=second_card_check)
                    except asyncio.TimeoutError:
                        await player.get_user().send("You did not pick a second player in time, so you are swapping "
                                                     "a random other player.")
                        p2_index = random.choice(second_players_indices)
                elif p2_index == -1 and \
                        str(reaction) in Constants.DIGIT_EMOJIS[:len(other_players)] and \
                        p1_index is not Constants.DIGIT_EMOJIS.index(str(reaction)):
                    p2_index = Constants.DIGIT_EMOJIS.index(str(reaction))
                    break

        player_one = other_players[p1_index]
        player_two = other_players[p2_index]
        HelperMethods.swap_roles(player_one=player_one, player_two=player_two)
        await player.get_user().send("You've swapped the roles of {} and {}".format
                                     (player_one.get_player_name(), player_two.get_player_name()))