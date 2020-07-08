from PlayerRoles.RoleCard import RoleCard
from Constants import Faction
from Player import Player
import Constants
import random
import asyncio

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

    async def do_night_action(self, player, player_list, middle_cards, bot, client, summary_msg):

        # This is a check which sees that the reaction added is of 1 of the below types.
        def check(reaction, user):
            return str(reaction.emoji) in Constants.DIGIT_EMOJIS[:3]

        if not isinstance(player, Player):
            raise Exception("Error: A person who drew the Werewolf role is not identified as of Player class.")
        other_werewolf_list = [p for p in player_list if p.get_user() != player.get_user()
                               and p.get_start_role().get_role_name() == player.get_start_role().get_role_name()]
        # Todo in the future: Update this for other types of werewolves and doppelganger ofc.
        if len(other_werewolf_list) > 0:
            werewolf_str = "You wake up during the night... you see that the other werewolves are the following: "
            for w in other_werewolf_list:
                werewolf_str += w.get_player_name()
                if w is not other_werewolf_list[-1]:
                    werewolf_str += ", "
            await player.get_user().send(werewolf_str)
        else:
            await player.get_user().send("You wake up during the night... you see that "
                                         "there are no other werewolves. You are now allowed to look at "
                                         "one card from the center of your choice.")
            choice_str = "Which card would you like to look at?\n"
            choice_str += Constants.DIGIT_EMOJIS[0] + " - Left Card\n"
            choice_str += Constants.DIGIT_EMOJIS[1] + " - Middle Card\n"
            choice_str += Constants.DIGIT_EMOJIS[2] + " - Right Card"

            choice_msg = await player.get_user().send(choice_str)
            for i in range(3):
                await choice_msg.add_reaction(Constants.DIGIT_EMOJIS[i])

            card_index = -1
            dm_channel = player.get_user().dm_channel

            # Making sure that the player reacts within 60 seconds, else a card is randomly picked from the center for
            # them.
            try:
                await client.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await player.get_user().send(
                    "You did not complete your action in time, so you are randomly looking at a card "
                    "from the center.")
                card_index = random.randint(0, 2)
                if card_index == 0:
                    await player.get_user().send(
                        "By random chance, you look at the left card from the center.")
                elif card_index == 1:
                    await player.get_user().send("By random chance, you look at the middle card from the center.")
                else:
                    await player.get_user().send("By random chance, you look at the right card from the center.")

            while card_index == -1:
                choice_msg = await dm_channel.fetch_message(choice_msg.id)
                for reaction in [r for r in choice_msg.reactions if r.count > 1]:
                    if str(reaction) == Constants.DIGIT_EMOJIS[0]:
                        card_index = 0
                        await player.get_user().send("You look at the left card from the center.")
                        break
                    elif str(reaction) == Constants.DIGIT_EMOJIS[1]:
                        card_index = 1
                        await player.get_user().send("You look at the middle card from the center.")
                        break
                    elif str(reaction) == Constants.DIGIT_EMOJIS[2]:
                        card_index = 2
                        await player.get_user().send("You look at the right card from the center.")
                        break

            card_name = middle_cards[card_index].get_role_name()
            if card_index == 0:
                summary_msg += "{} woke up and saw no other werewolves. " \
                               "They looked at the left center card and saw {} role.\n".format(player.get_player_name(), card_name)
            elif card_index == 1:
                summary_msg += "{} woke up and saw no other werewolves. " \
                               "They looked at the middle center card and saw {} role.\n".format(player.get_player_name(),
                                                                                               card_name)
            else:
                summary_msg += "{} woke up and saw no other werewolves. " \
                               "They looked at the right center card and saw {} role.\n".format(player.get_player_name(),
                                                                                               card_name)
            await player.get_user().send("You see the role of the {}".format(card_name))
        return summary_msg