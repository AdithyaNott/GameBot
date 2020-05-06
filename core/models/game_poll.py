from string import ascii_lowercase

# TODO think how vote choices are being stored

class GamePoll:
	__ids = {}
	def __init__(self, question, choice_list, id_prefix=""):
		if id_prefix not in __ids:
			__ids[id_prefix] = 1
		
		self.id = f"{id_prefix}{__ids[id_prefix]}"
		__ids[id_prefix] += 1

		self.locked_in = False
		self.prompt = prompt
		self.choice_list = choice_list
		self.selected_choices = set()

	async def is_locked_in(self):
		# not good code, but this function may need to expand later
		if self.locked_in:
			return True
		return False

	async def is_open(self):
		return not await self.is_locked_in()

	async def refresh_poll_embed(self, discord_message):
		embed = discord.Embed('title'='')

		embed.set_author(name=f"poll_id: {self.id}", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
		

		embed.add_field(name="Game Prompt", value=self.prompt)

		if await self.is_locked_in():
			embed.set_footer(text="Your response is locked in")
		else:
			choices = "** Select From The Following **:"
			for index, choice in enumerate(self.choice_list):
				choices += f":regional_indicator_{ascii_lowercase[index]}: {choice}\n"
			embed.add_field(name="\u200b", value=choices)
			embed.set_footer(text="Click ☑️ to lock in your response")
		discord_message.edit(embed=embed)


	async def provide_choice_reactions(self, discord_message):
		discord_message.add_reaction(☑)
		for i in range(len(self.choice_list)):
			letter_emoji_unicode = bytes("\\U0001f1" + hex(230 + i)[2:], "utf-8").decode("unicode-escape")
			discord_message.add_reaction(letter_emoji_unicode)

	async def select(self, user, choice, discord_message):
		# user should be user id
		# choice should be name of emoji being used
		# discord message is the discord message being affected
		if choice == "ballot_box_with_check":
			self.locked_in = True

		if not await self.is_open() or await self.is_locked_in():
			self.refresh_poll_embed()
			discord_message.clear_reactions()
			return

		vote_to_add = GameVote(self.id, user, choice)
		self.selected_choices.add(vote_to_add)
		await self.refresh_poll_embed(discord_message)

	async def deselect(self, user, choice, discord_message):
		if not await self.is_open() or await self.is_locked_in():
			self.refresh_poll_embed()
			discord_message.clear_reactions()
			return
		vote_to_remove = GameVote(self.id, user, choice)
		self.selected_choices.discard(vote_to_remove)
		await self.refresh_poll_embed(discord_message)