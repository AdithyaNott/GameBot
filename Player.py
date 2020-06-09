"""This is the true Player class. Will contain role they have, and Discord name/tag."""


class Player:

    # Constructor for Player class. Takes in discord_tag, discord_name, name of game and other args if required
    # like starting/current role for instance

    def __init__(self, user, *args):
        self.user = user
        self.discord_tag = str(user)
        self.discord_name = user.display_name

        if len(args) < 1:
            raise Exception("There need to be at least 2 arguments for type of game and role in game")
        self.game_name = args[0]
        if len(args) > 1:
            self.starting_role = args[1]
            self.current_role = args[1]

    def get_user(self):
        return self.user

    def get_player_tag(self):
        return self.discord_tag

    def get_player_name(self):
        return self.discord_name

    # Need to make sure this was initialized in the constructor

    def get_current_role(self):
        try:
            return self.current_role
        except Exception:
            raise Exception("Error. There was no current role initialized here for player: ", self.discord_tag)

    # Need to make sure this was initialized in the constructor

    def get_start_role(self):
        try:
            return self.starting_role
        except Exception:
            raise Exception("Error. There was no starting role initialized here for player: ", self.discord_tag)

    # Sets the new current role with another role

    def set_current_role(self, role):
        self.current_role = role
