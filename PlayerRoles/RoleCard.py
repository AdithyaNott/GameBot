from Constants import Faction
"""This is the interface which the various unique roles will inherit from"""


class RoleCard:

    # Default Constructor. Is different for each role.
    def __init__(self):
        self.faction = Faction.NEUTRAL
        self.name = ""
        self.description = ""
        self.loses_to_tanner = True

    def get_role_name(self):
        return self.name

    def get_faction(self):
        return self.faction

    def get_description(self):
        return self.description

    # This method updates the "Description/WinCon" of each role based on whether a Tanner is present in the game.
    def update_description_tanner_clause(self):
        if self.loses_to_tanner:
            extra_clause = ""
            if self.faction == Faction.WEREWOLF:
                extra_clause = "\nIn addition, since there is a Tanner in the game, {} needs to ensure " \
                          "that Tanner does not die during the voting phase, else {} loses. ".format(self.name,
                                                                                                     self.name)
            elif self.faction == Faction.VILLAGE:
                extra_clause = "\nIn addition, there is a Tanner in the game. As long as a werewolf dies should one" \
                               "be present, {} will win. However, if Tanner dies and a werewolf doesn't die, {} " \
                               "loses.".format(self.name, self.name)
            self.description += extra_clause

    # Default night action is to do nothing, which some roles will copy. This is updated for required roles accordingly.
    # I am still figuring out how to design this, but I feel like this method would take in array of the players in
    # the order they're sitting. Maybe another Player class which has discord tag, Discord nickname, starting role,
    # and current role

    async def do_night_action(self, player, player_list, middle_cards, bot, client, summary_msg):
        return summary_msg
