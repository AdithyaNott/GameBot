from PlayerRoles.RoleCard import RoleCard
from Constants import Faction
import Constants
from Player import Player
import asyncio
import random

"""This is the standard Drunk role in Village Faction which implements the RoleCard interface."""


class Drunk(RoleCard):

    # Initializing the faction, name and description of the Drunk role.
    # And setting loses_to_tanner to True since Drunk loses if Tanner dies.

    def __init__(self):
        self.faction = Faction.VILLAGE
        self.name = "Drunk"
        self.description = "During the night phase, the Drunk will wake up and swap their card for a card in the " \
                           "center of their choosing, but will not be able to see their new role.\n As part of the " \
                           "Village faction, the Drunk's goal is to make sure a werewolf dies during the voting phase. "
        self.loses_to_tanner = True

    # This action will be swapping the Player's current role with 1 from the middle (chosen by the Player).

    async def do_night_action(self, player, player_list, middle_cards, bot, client, summary_msg):

        # This is a check which sees that the reaction added is of 1 of the below types.
        def check(reaction, user):
            return str(reaction.emoji) in Constants.DIGIT_EMOJIS[:3] and user != client.user

        # First validate that the player is correct format
        if not isinstance(player, Player):
            raise Exception("Error: A person who drew the Drunk role is not identified as of Player class.")

        # Sending message which would gather input about which role the Drunk "drunks"
        dm_channel = player.get_user().dm_channel
        enquiry = await player.get_user().send("As the drunk, you now must exchange one of your cards with the center. "
                                               "Which center card would you like to select?\n"
                                               "1️⃣ - Left Card\n2️⃣ - Middle Card\n3️⃣ - Right Card")
        for i in range(3):
            await enquiry.add_reaction(Constants.DIGIT_EMOJIS[i])
        middle_role = -1

        # Making sure that the player reacts within 60 seconds, else a card is randomly picked from the center for them.
        try:
            await client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await player.get_user().send("You did not complete your action in time, so you are randomly drawing a card "
                                         "from the center.")
            summary_msg += player.get_player_name() + " did not drunk a card in time, and randomly was given a card. "
            middle_role = random.randint(0, 2)
            if middle_role == 0:
                await player.get_user().send("By random chance, you draw the left card from the center and place your "
                                             "role there.")
                summary_msg += player.get_player_name() + " drunk the left middle card of role " + middle_cards[0].get_role_name()
            elif middle_role == 1:
                await player.get_user().send("By random chance, you draw the middle card from the center and "
                                             "place your role there.")
                summary_msg += player.get_player_name() + " drunk the center middle card of role " + middle_cards[
                    1].get_role_name()
            else:
                await player.get_user().send("By random chance, you draw the right card from the center and place "
                                             "your role there.")
                summary_msg += player.get_player_name() + " drunk the right middle card of role " + middle_cards[
                    2].get_role_name()

        # This code is run to "wait" for a reaction to be added for 60 seconds.
        while middle_role == -1:
            enquiry = await dm_channel.fetch_message(enquiry.id)
            for reaction in [r for r in enquiry.reactions if r.count > 1]:
                if str(reaction) == Constants.DIGIT_EMOJIS[0]:
                    middle_role = 0
                    await player.get_user().send("You now draw the left center card and place your role there.")
                    summary_msg += player.get_player_name() + " drunk the left middle card of role " + middle_cards[
                        0].get_role_name()
                    break
                elif str(reaction) == Constants.DIGIT_EMOJIS[1]:
                    middle_role = 1
                    await player.get_user().send("You now draw the middle center card and place your role there.")
                    summary_msg += player.get_player_name() + " drunk the center middle card of role " + middle_cards[
                        1].get_role_name()
                    break
                elif str(reaction) == Constants.DIGIT_EMOJIS[2]:
                    middle_role = 2
                    await player.get_user().send("You now draw the right center card and place your role there.")
                    summary_msg += player.get_player_name() + " drunk the right middle card of role " + middle_cards[
                        2].get_role_name()
                    break

        # The main part of the code. Current role swapped with center role without revealing information to the player.
        summary_msg += "\n"
        new_middle_role = player.get_current_role()
        player.set_current_role(middle_cards[middle_role])
        middle_cards[middle_role] = new_middle_role
        return summary_msg
