from string import ascii_lowercase

# TODO think how vote choices are being stored

class GamePoll:
	def __init__(self, bot):
		self.bot = bot

		self.id = -1
		self.locked_in = False
		self.choice_list = []
		self.selected_choices = []
		pass

	async def is_locked_in(self):
		# not good code, but this function may need to expand later
		if self.locked_in:
			return True
		return False

	async def refresh_poll_embed(self):
		embed = discord.Embed('title'='')

		
		if await self.is_locked_in():
						
			pass
		else:
			choices = "** Select From The Following **:"
			for index, choice in enumerate(self.choice_list):
				choices += f":regional_indicator_{ascii_lowercase[index]}: {choice}\n"
			embed.add_field(name="\u200b", value=choices, inline=False)
			embed.set_footer(text="Click ☑️ to lock in your response")
		pass


	async def provide_choice_reactions(self, discord_message):
		discord_message.add_reaction(☑)
		for i in range(len(self.choice_list)):
			letter_emoji_unicode = bytes("\\U0001f1" + hex(230 + i)[2:], "utf-8").decode("unicode-escape")
			discord_message.add_reaction(letter_emoji_unicode)

	async def select(self, user, choice, discord_message):
		if not await self.is_open():
			self.refresh_poll_embed()
			discord_message.clear_reactions()
			return
		if 

	async def deselect(self, user, choice, discord_message):
		pass