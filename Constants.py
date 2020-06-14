from enum import Enum
from Player import Player
import time

# List of roles that are currently supported by the Werewolf Bot.
# Might be useful to use this list to prompt the user for which roles to use in the game based
# on some reaction~ish input.
POSSIBLE_ROLES = ["Drunk", "Hunter", "Insomniac", "Mason", "Minion",
                  "Robber", "Seer", "Tanner", "Troublemaker", "Villager", "Werewolf"]

DIGIT_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "0️⃣"]

# This contains the list of roles for which there can be more than 1 present in the game.
# Villager (for which there are at most 3)
# Werewolf (for which there are at most 2)
# Mason (for which there are exactly 2 or 0)
SPECIAL_ROLES_MULTIPLE_COUNT = ["Mason", "Villager", "Werewolf"]

# Priority of order for night actions for each role (assuming they have a night role)
PRIORITY = ["Werewolf", "Minion", "Mason", "Seer", "Robber", "Troublemaker", "Drunk", "Insomniac"]

ONUWSTRINGS = ["werewolf", "werewolves", "onuw"]


# This is an enum for the Faction which is used by the various classes implementing the RoleCard interface


class Faction(Enum):
    VILLAGE = 0
    WEREWOLF = 1
    NEUTRAL = 2


WEREWOLF_FACTION_LIST = ["Village", "Werewolf", "Neutral"]

# This is a class for containing helper methods which will be used a lot


class HelperMethods:

    # This is a method to simulate a countdown via Discord message being edited.
    # t = time to countdown from. ctx = Discord Context.
    @staticmethod
    async def countdown(t, ctx):
        if t < 0:
            raise Exception("Can't have negative amount of time. ")
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        msg = await ctx.send("Time remaining: " + timeformat)
        time.sleep(1)
        t -= 1
        while t>0:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            await msg.edit(content=("Time remaining: " + timeformat))
            time.sleep(1)
            t -= 1
        if t == 0:
            msg.edit(content="Time's up!")

    # Swaps the current_role attributes for 2 Players.
    # Input: player_one and player_two are two instances of the Player Object
    @staticmethod
    def swap_roles(player_one, player_two):
        if not isinstance(player_one, Player) or not isinstance(player_two, Player):
            raise Exception("One of the Players passed in for swapping isn't of Player class")
        swapped_role = player_one.get_current_role()
        player_one.set_current_role(player_two.get_current_role())
        player_two.set_current_role(swapped_role)
        return player_one, player_two

    # Converts dictionary to list version, where each (k,v) in the dict is the element and number of times
    # it would appear in the list respectively.
    @staticmethod
    def convert_dict_to_list(role_dict):
        role_list = []
        for i in role_dict.keys():
            for j in range(role_dict[i]):
                role_list.append(i)
        return role_list

    # Gets a list of players who have reacted with '👍' to a message by the bot asking who's playing
    # Input is message of type Message in the Discordpy API, and user of type User based on the same API.
    @staticmethod
    async def get_players(message, user):
        player_list = []

        #for reaction in message.reactions:
        #    if reaction == "👍":
        #        async for player in reaction.users():
        #            player_list.append(player)
        for r in range(len(message.reactions)):
            if str(message.reactions[r]) == "👍":
                players = await message.reactions[r].users().flatten()
                for p in players:
                    if p != user:
                        player_list.append(p)
                return player_list

    @staticmethod
    def thumbs_up_check(reaction, user):
        return str(reaction.emoji) == '👍'
