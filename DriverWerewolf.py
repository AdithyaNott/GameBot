from Player import Player
from collections import Counter
import Constants
import random
from PlayerRoles import Drunk, Hunter, Insomniac, Mason, Minion, Robber, Seer, Tanner, Troublemaker, Villager, Werewolf

# This is probably the roles they input they want. Below is an example I just have for now
roles_input = ["Werewolf", "Werewolf", "Seer", "Troublemaker", "Robber", "Tanner"]

# Let's assume that the following are the list of discord tags and discord nicknames respectively.
discord_tags = ["PlayerOne#4643", "PlayerTwo#5864", "PlayerThree#8462"]
discord_names = ["PogU", "weirdChamp", "coronaS"]

# Validation check to see that the length of tags == length of names which it should be since this is automatically
# picked up via discord.py
if len(discord_tags) != len(discord_names):
    raise Exception("Error in getting the names/tags of Discord users. There is unequal length between number "
                    "of names and number of discord tags")

player_count = len(discord_tags)

# Validation check that there are 3 more roles than there are players
if len(roles_input) != len(discord_tags) + 3:
    raise Exception("Error in number of roles. There should be 3 more roles than there are players.")

# First need to verify that there are at least 3 players for a functional game.
if player_count < 3:
    raise Exception("Error. Need at least 3 players to play Werewolves.")

# Now we need to check that at most 1 of the other roles is present except for ones which are special cases
# which is described above by special_roles_for_count
role_count = Counter(roles_input)
for role in role_count.keys():
    if role not in Constants.POSSIBLE_ROLES:
        raise Exception("{} role is currently not supported by our bot".format(role))
    if role_count[role] > 1 and role not in Constants.SPECIAL_ROLES_MULTIPLE_COUNT:
        raise Exception("There can only be at most 1 {} role".format(role))
if role_count["Mason"] != 0 and role_count["Mason"] != 2:
    raise Exception("There can only be exactly 0 or 2 Mason roles")
if role_count["Villager"] > 3:
    raise Exception("There can only be at most 3 Villager roles")
if role_count["Werewolf"] > 2:
    raise Exception("There can only be at most 2 Werewolf roles")

# Shuffle the roles for randomization (which will accordingly then be distributed)
random.shuffle(roles_input)

# Boolean to see if there is a Tanner in the game.
tanner_check = "Tanner" in roles_input

# Initializing the players classes for everyone. Will contain discord tag, name, game, and starting role in that order.
# Important Note: For the Player Class, we expect that the start role is a class type (ex: Drunk() instance), but
# current role will be saved as a string as that makes it easier to swap.
player_list = []
starting_roles = []
for i in range(player_count):
    PlayerClass = getattr(roles_input[i], roles_input[i])
    starting_roles.append(roles_input[i])
    start_role = PlayerClass()

    # for updating the Tanner clause if Tanner is in the game
    if tanner_check:
        start_role.update_description_tanner_clause()

    player_list.append(Player(discord_tags[i], discord_names[i], "One Night Ultimate Werewolf", start_role))

# There should be some code here to message all the individual players about their role now, and the
# description and such.

# Storing the middle classes/roles (there will be 3 exactly)
middle_cards = roles_input[-3:].copy()
middle_roles = []
for card in middle_cards:
    PlayerClass = getattr(card, card)
    middle_role = PlayerClass()
    if tanner_check:
        middle_role.update_description_tanner_clause()
    middle_roles.append(middle_role)

# Now to code each person doing their one night action
for role in Constants.PRIORITY:
    if role in starting_roles:
        for player in player_list:
            if player.get_start_role().get_role_name() == role:
                player.get_start_role().do_night_action(player, player_list, middle_roles)
