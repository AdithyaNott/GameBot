from Player import Player
from collections import Counter
import Constants
import discord
import asyncio
import random
from PlayerRoles.Drunk import Drunk
from PlayerRoles.Hunter import Hunter
from PlayerRoles.Insomniac import Insomniac
from PlayerRoles.Mason import Mason
from PlayerRoles.Minion import Minion
from PlayerRoles.Robber import Robber
from PlayerRoles.Seer import Seer
from PlayerRoles.Tanner import Tanner
from PlayerRoles.Troublemaker import Troublemaker
from PlayerRoles.Villager import Villager
from PlayerRoles.Werewolf import Werewolf


# Code to verify that Discord tags and Discord names are read correctly, and sizes of input are functional for game
# Input: roles = list of the roles used. ex: ["Werewolf", "Minion", "Villager"]
# Input: user_list = the list of players for the game
# Output: count = number of players in the game
def validate_player_role_sizes(roles, user_list):
    # Validation check to see that the length of tags == length of names which it should be since this is automatically
    # picked up via discord.py
    count = len(user_list)

    # Need to verify that there are at least 3 players and at most 10 players (for now) for a functional game.
    # Commenting out the below code for now, should uncomment later.
    #if count < 3:
    #    raise Exception("Error. Need at least 3 players to play One Night Ultimate Werewolf.")
    #if count > 10:
    #    raise Exception("Error. One Night Ultimate Werewolf supports at most 10 players")

    # Validation check that there are 3 more roles than there are players
    if len(roles) != count + 3:
        raise Exception("Error in number of roles. There should be 3 more roles than there are players "
                        "(1 role per player and 3 roles in the middle).")

    return count


# Code for verifying that there aren't more roles of a certain type inputted than supported by Werewolves.
# And that there are no invalid roles sent. Amount of roles which have more than 1 possible are mentioned
# in Constants by special_roles_for_count
def verify_role_counts(roles):
    role_count = Counter(roles)
    for role in role_count.keys():
        if role not in Constants.POSSIBLE_ROLES:
            raise Exception("{} role is currently not supported by our bot or does not exist".format(role))
        if role_count[role] > 1 and role not in Constants.SPECIAL_ROLES_MULTIPLE_COUNT:
            raise Exception("There can only be at most 1 {} role".format(role))
    if role_count["Mason"] > 2:
        raise Exception("There can only be at most 2 Mason roles")
    if role_count["Villager"] > 3:
        raise Exception("There can only be at most 3 Villager roles")
    if role_count["Werewolf"] > 2:
        raise Exception("There can only be at most 2 Werewolf roles")
    return True


# Code for checking if tanner is in the game.
# Input: roles = list of roles
# Output. Boolean for whether Tanner is in the game or not (which changes win conditions for various roles)
def check_for_tanner(roles):
    return "Tanner" in roles


# Code for checking if the starting minion might be a werewolf
# Input: 2 booleans containing whether a minion is in the game and werewolf is in the game
# Output: boolean of whether minion acts as werewolf (if there is a minion but no werewolf in starting roles
def check_minion_is_werewolf(minion, werewolf):
    return minion and not werewolf


# This is code for returning a list of players who have been killed, by input of a list of tuples
# containing votes where (PlayerOne, PlayerTwo) means PlayerOne voted to kill PlayerTwo.
def get_killed_players(vote_list):
    vote_map = {}
    for vote in vote_list:
        # Below line would be triggered if player voted for center in my current thoughts.
        if vote[1] is None:
            continue
        if vote[1] in vote_map:
            vote_map[vote[1]] += 1
        else:
            vote_map[vote[1]] = 1

    # Computing list of killed players
    dead = []
    if len(vote_map) > 0:
        dead = [key for (key, count) in vote_map.items() if count == max(vote_map.values())]

    return dead


# This is code for getting the roles to be used in One Night Ultimate Werewolf based on reactions added
# to a message by the bot by the users.
# If only switch case existed in Python :(
def getRoleCounts(reactions):
    roles = {}
    for reaction in [r for r in reactions if r.count > 1]:
        if str(reaction) == "🧍":
            roles["Villager"] = 1
        if str(reaction) == "👨":
            if "Villager" in roles:
                roles["Villager"] += 1
            else:
                roles["Villager"] = 1
        if str(reaction) == "👩":
            if "Villager" in roles:
                roles["Villager"] += 1
            else:
                roles["Villager"] = 1
        if str(reaction) == "🐺":
            roles["Werewolf"] = 1
        if str(reaction) == "☠":
            if "Werewolf" in roles:
                roles["Werewolf"] += 1
            else:
                roles["Werewolf"] = 1
        if str(reaction) == "🍺":
            roles["Drunk"] = 1
        if str(reaction) == "🔫":
            roles["Hunter"] = 1
        if str(reaction) == "😴":
            roles["Insomniac"] = 1
        if str(reaction) == "⬅":
            roles["Mason"] = 1
        if str(reaction) == "➡":
            if "Mason" in roles:
                roles["Mason"] += 1
            else:
                roles["Mason"] = 1
        if str(reaction) == "💁":
            roles["Minion"] = 1
        if str(reaction) == "💰":
            roles["Robber"] = 1
        if str(reaction) == "🧠":
            roles["Seer"] = 1
        if str(reaction) == "😐":
            roles["Tanner"] = 1
        if str(reaction) == "😲":
            roles["Troublemaker"] = 1
    return roles


# This method takes in a role as string, and accordingly returns its corresponding class
def getClass(role_string):
    if role_string == "Drunk":
        return Drunk()
    elif role_string == "Hunter":
        return Hunter()
    elif role_string == "Insomniac":
        return Insomniac()
    elif role_string == "Mason":
        return Mason()
    elif role_string == "Minion":
        return Minion()
    elif role_string == "Robber":
        return Robber()
    elif role_string == "Seer":
        return Seer()
    elif role_string == "Tanner":
        return Tanner()
    elif role_string == "Troublemaker":
        return Troublemaker()
    elif role_string == "Villager":
        return Villager()
    elif role_string == "Werewolf":
        return Werewolf()


async def main(bot, roles_list, users, client):
    # This is probably the roles they input they want. Below is an example I just have for now
    roles_input = roles_list

    # Let's assume that the following are the list of discord tags and discord nicknames respectively.

    player_count = validate_player_role_sizes(roles_input, users)

    verify_role_counts(roles_input)

    # Shuffle the roles for randomization (which will accordingly then be distributed)
    random.shuffle(roles_input)

    # Boolean to see if there is a Tanner in the game.
    tanner_check = check_for_tanner(roles_input)

    await bot.send("Now sending the role information to each player in their dms, one at a time.")

    # Initializing the players classes for everyone. Will contain discord tag, name, game,
    # and starting role in that order.
    # Important Note: For the Player Class, we expect that the start role is a class type (ex: Drunk() instance), but
    # current role will be saved as a string as that makes it easier to swap.
    player_list = []
    starting_roles = []
    werewolf_check = False
    minion_check = False
    for i in range(player_count):
        starting_roles.append(roles_input[i])
        start_role = getClass(roles_input[i])

        # for updating the Tanner clause if Tanner is in the game
        if tanner_check:
            start_role.update_description_tanner_clause()

        # for checking whether a Werewolf and Minion started. If a minion started but no
        # werewolf, then the minion is a werewolf
        if start_role.get_faction() == Constants.Faction.WEREWOLF:
            if start_role.get_role_name() == "Minion":
                minion_check = True
            else:
                werewolf_check = True

        player_list.append(Player(users[i], "One Night Ultimate Werewolf", start_role))

    # Calculate whether the minion starting out is a werewolf (aka has to avoid being killed by village)
    minion_is_werewolf = check_minion_is_werewolf(minion_check, werewolf_check)

    # message the players about their role

    msgs_not_accepted = []

    for p in player_list:
        role_msg = await p.get_user().send("Your Role: " + p.get_start_role().get_role_name() + "\n" + "Description: " +
                                           p.get_start_role().get_description() + "\n" + "Faction: " +
                                           Constants.WEREWOLF_FACTION_LIST[p.get_start_role().get_faction().value]
                                           + "\nReact with 👍 to continue (and if you understand).")
        await role_msg.add_reaction("👍")
        msgs_not_accepted.append((role_msg.id, p.get_user().dm_channel))
        # If any player doesn't confirm that they got their role in 120 seconds, the game is cancelled and remade.
        try:
            await client.wait_for('reaction_add', timeout=120.0, check=Constants.HelperMethods.thumbs_up_check)
        except asyncio.TimeoutError:
            raise Exception(p.get_player_name() + " did not accept their role in time.")

        # A courtesy message
        if p is not player_list[-1]:
            await p.get_user().send("Waiting for other people to accept their roles")

    # This while loop is to "wait" for everyone to accept their role
    while len(msgs_not_accepted) > 0:
        dmtuple = msgs_not_accepted[0]
        try:
            dm_msg = await dmtuple[1].fetch_message(dmtuple[0])
            for reaction in [r for r in dm_msg.reactions if r.count > 1]:
                if str(reaction) == "👍":
                    del msgs_not_accepted[0]
        except Exception:
            raise Exception("Could not retrieve role message with player: ", str(dmtuple[1].recipient))

    await bot.send("All players have accepted their starting role.")
    await bot.send("Now the night phase begins")

    if len(player_list) == 1:
        return

    # Storing the middle classes/roles (there will be 3 exactly)
    middle_cards = roles_input[-3:].copy()
    middle_roles = []
    for card in middle_cards:
        middle_role = getClass(card)
        if tanner_check:
            middle_role.update_description_tanner_clause()
        middle_roles.append(middle_role)

    # Now to code each person doing their one night action
    for role in Constants.PRIORITY:
        if role in starting_roles:
            for player in player_list:
                if player.get_start_role().get_role_name() == role:
                    await player.get_start_role().do_night_action(player, player_list, middle_roles, bot, client)

    # Some code here to set a timer for 5 minutes after each person doing action
    await Constants.HelperMethods.countdown(300, bot)

    # Now we need to handle the voting phase. Probably a list of tuples for each vote of type (Player, Player)
    votes = [[player_list[1], player_list[0]]]
    killed_players = get_killed_players(votes)

    result_message = ""
    if len(killed_players) == 0:
        result_message = "After the night phase, it seems that everyone voted for the center....."
        villager_list = []
        werewolf_list = []
        werewolf_win = False
        for player in player_list:
            if player.get_current_role().get_faction() == Constants.Faction.WEREWOLF:
                if player.get_current_role().get_role_name() != "Minion" or minion_is_werewolf:
                    werewolf_win = True
                werewolf_list.append(player)
            elif player.get_current_role().get_faction() == Constants.Faction.VILLAGE:
                villager_list.append(player)
        if not werewolf_win:
            result_message += "\nAnd there were no werewolves among you! The Village faction has won!!"
        else:
            result_message += "\nThere were werewolves to be killed amongst you! The Werewolf faction has won!!"
    else:
        result_message = "After the night phase, some players did die. The following players died: \n"
        werewolf_win = True
        tanner_win = False
        for killed in killed_players:
            if killed != killed_players[-1]:
                result_message += killed.get_player_name() + ", "
            else:
                result_message+= killed.get_player_name() + "\n"
            if killed.get_current_role().get_faction() == Constants.Faction.WEREWOLF:
                if killed.get_current_role().get_role_name() != "Minion":
                    werewolf_win = False
            elif killed.get_current_role().get_faction() == Constants.Faction.NEUTRAL:
                if killed.get_current_role().get_role_name() == "Tanner":
                    tanner_win = True
        if tanner_win:
            if werewolf_win:
                result_message += "Tanner did die, and no werewolves died. So Tanner has won the game, " \
                                  "while the rest of the village and werewolves lose!"
            else:
                result_message += "Tanner did die, so Tanner has won! However, a werewolf also died, " \
                                  "so the village faction has won!"
        else:
            if werewolf_win:
                if tanner_check:
                    result_message += "No one that was killed was a werewolf, and Tanner did not die. The werewolves " \
                                      "have won!"
                else:
                    result_message += "None of the people that died was a werewolf. The werewolves have won!"
            else:
                if tanner_check:
                    result_message += "A werewolf was killed, and Tanner did not die. The Village has succeeded!"
                else:
                    result_message += "A werewolf was killed! The Village has survived!"

