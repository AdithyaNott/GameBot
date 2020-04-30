class GameVote:
	def __init__(self, bot, poll_id, user_id, choice):
		self.bot = bot
		self.poll_id = poll_id
		self.user_id = user_id
		self.choice = choice