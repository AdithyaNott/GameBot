from PlayerRoles.RoleCard import RoleCard
from Constants import Faction
from Player import Player
import Constants
import asyncio
import random

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

    async def do_night_action(self, player, player_list, middle_cards, bot, client):
        # A check for reaction 1 or 2, for whether user wishes to see 2 center cards or another player's card
        def check_choice(reaction, user):
            return str(reaction.emoji) in Constants.DIGIT_EMOJIS[:2]

        # A check for in event of another player's card, adds an appropriate reaction for selecting one of them
        def other_player_check(reaction, user):
            return str(reaction.emoji) in Constants.DIGIT_EMOJIS[:len(other_players)]

        # A check for in event of 2 center cards, picks an emoji reaction of 1 to 3
        def first_card_check(reaction, user):
            return str(reaction.emoji) in Constants.DIGIT_EMOJIS[:3]

        # A check for in event of 2 center cards and 1 is already picked, picks an emoji 1 to 3 that isn't
        # already picked
        def second_card_check(reaction, user):
            return Constants.DIGIT_EMOJIS.index(str(reaction.emoji)) in other_cards_indices

        if not isinstance(player, Player):
            raise Exception("Error: A person who drew the Seer role is not identified as of Player class.")

        # First gather whether they want to see 2 cards from center or another player's role
        enquiry_str = "You now wake up as the seer. What would you like to do?"
        enquiry_str += "\n" + Constants.DIGIT_EMOJIS[0] + " - Look at 2 cards from the center"
        enquiry_str += "\n" + Constants.DIGIT_EMOJIS[1] + " - Look at another player's card"
        enquiry_msg = await player.get_user().send(enquiry_str)
        # Adding relevant emojis
        for i in range(2):
            await enquiry_msg.add_reaction(Constants.DIGIT_EMOJIS[i])

        # This boolean is to make sure we loop until an emoji has been added (or player timed out)
        automated_check = False
        # This is whether seer wishes to see another player's role or not
        check_player = True

        # Give 60 seconds to complete the action, else just time out
        try:
            await client.wait_for('reaction_add', timeout=60.0, check=check_choice)
        except asyncio.TimeoutError:
            await player.get_user().send("You did not complete your action in time, so you are robbing a "
                                         "random player.")
            check_player = random.choice([True, False])
            if check_player:
                await player.get_user().send("You did not make your decision in time, so you randomly choose "
                                             "to check a player.")
            else:
                await player.get_user().send("You did not make your decision in time, so you randomly choose "
                                             "to look at 2 cards from the center.")
            automated_check = True

        # Looping and seeing when we get a reaction matching the relevant criteria. Update check_player accordingly.
        dm_channel = player.get_user().dm_channel
        while not automated_check:
            enquiry_msg = await dm_channel.fetch_message(enquiry_msg.id)
            for reaction in [r for r in enquiry_msg.reactions if r.count > 1]:
                if str(reaction) in Constants.DIGIT_EMOJIS[:2]:
                    check_player = Constants.DIGIT_EMOJIS.index(str(reaction)) == 1
                    automated_check = True
                    break

        # Part 2 - Now we figure out which player to see the role of or which 2 cards from the center (1 at a time)
        # Very fun :D. HELP ME I'M GOING INSANE.
        if check_player:
            other_players = [p for p in player_list if p.get_user() is not player.get_user()]

            # Some code here to figure out which player the Seer wants to look at
            enquiry_str = "Which player do you wish to see the role of?\n"
            for i in range(len(other_players)):
                enquiry_str += Constants.DIGIT_EMOJIS[i] + " - " + other_players[i].get_player_name()
                if i is not len(other_players) - 1:
                    enquiry_str += "\n"
            enquiry_msg = await player.get_user().send(enquiry_str)
            for i in range(len(other_players)):
                await enquiry_msg.add_reaction(Constants.DIGIT_EMOJIS[i])

            seen_role = -1
            # Give 60 seconds to complete the action, else just time out
            try:
                await client.wait_for('reaction_add', timeout=60.0, check=other_player_check)
            except asyncio.TimeoutError:
                await player.get_user().send("You did not complete your action in time, so you are viewing "
                                             "the role of a random player.")
                seen_role = random.randint(0, len(other_players) - 1)

            # Looping while the seer hasn't chosen (or been assigned) a player whose role to look at
            while seen_role == -1:
                enquiry_msg = await dm_channel.fetch_message(enquiry_msg.id)
                for reaction in [r for r in enquiry_msg.reactions if r.count > 1]:
                    if str(reaction) in Constants.DIGIT_EMOJIS[:len(other_players)]:
                        seen_role = Constants.DIGIT_EMOJIS.index(str(reaction))
                        break

            chosen_player = other_players[seen_role]
            chosen_player_role = chosen_player.get_current_role().get_role_name()
            await player.get_user().send("You look at the role of {}..... you see that their role is "
                                         "{}".format(chosen_player.get_player_name(), chosen_player_role))
        else:
            enquiry_str = "Which 2 cards do you wish to look at?\n"
            enquiry_str += Constants.DIGIT_EMOJIS[0] + " - Left Card\n"
            enquiry_str += Constants.DIGIT_EMOJIS[1] + " - Middle Card\n"
            enquiry_str += Constants.DIGIT_EMOJIS[2] + " - Right Card"
            enquiry_msg = await player.get_user().send(enquiry_str)
            for i in range(3):
                await enquiry_msg.add_reaction(Constants.DIGIT_EMOJIS[i])

            first_card_index = -1
            second_card_index = -1

            # Check for time before first reaction is done
            try:
                await client.wait_for('reaction_add', timeout=30.0, check=first_card_check)
            except asyncio.TimeoutError:
                await player.get_user().send("You did not complete your action in time, so you are viewing "
                                             "2 random cards from the center.")
                first_card_index = random.randint(0, 2)
                second_card_index = random.choice([i for i in range(3) if i is not first_card_index])

            # Waiting for second reaction to be done too
            while second_card_index == -1:
                enquiry_msg = await dm_channel.fetch_message(enquiry_msg.id)
                for reaction in [r for r in enquiry_msg.reactions if r.count > 1]:
                    if first_card_index == -1 and str(reaction) in Constants.DIGIT_EMOJIS[:3]:
                        first_card_index = Constants.DIGIT_EMOJIS.index(str(reaction))
                        other_cards_indices = [i for i in range(3) if i is not first_card_index]
                        try:
                            await client.wait_for('reaction_add', timeout=30.0, check=second_card_check)
                        except asyncio.TimeoutError:
                            await player.get_user().send("You did not pick a second card in time, so you are viewing "
                                                         "a different random card from the center.")
                            second_card_index = random.choice(other_cards_indices)
                    elif second_card_index == -1 and \
                            str(reaction) in Constants.DIGIT_EMOJIS[:3] and \
                            first_card_index is not Constants.DIGIT_EMOJIS.index(str(reaction)):
                        second_card_index = Constants.DIGIT_EMOJIS.index(str(reaction))
                        break

            final_str1 = "You look at the following 2 cards from the center: "
            final_str2 = "You see the following roles respectively: "
            if first_card_index == 0 or second_card_index == 0:
                final_str1 += "Left Card "
                final_str2 += middle_cards[0].get_role_name() + " "
            if first_card_index == 1 or second_card_index == 1:
                final_str1 += "Middle Card "
                final_str2 += middle_cards[1].get_role_name() + " "
            if first_card_index == 2 or second_card_index == 2:
                final_str1 += "Right Card"
                final_str2 += middle_cards[2].get_role_name()
            await player.get_user().send(final_str1 + "\n" + final_str2)

