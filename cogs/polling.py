import discord
from discord.ext import commands


class Polling(commands.Cog):
	def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def parse_poll_id(discord_message):
    	try:
    		prefix = "Poll Id: "
    		i = len(prefix)
    		return discord_message.embeds[0].author.name[i:]
    	except:
    		return None

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, data):
    	if data.user_id == self.bot.user.id or not data.emoji:
    		# Ignore bot's own reacts and invalid reacts
    		return

    	channel = self.bot.getchannel(data.channel_id)


    	poll_id = None
    	# check where the message came from
    	if isinstance(channel, discord.TextChannel):
    		# get label from message
    		discord_message = await channel.fetch_message(id=data.message_id)
    		poll_id = parse_poll_id(discord_message)

    	# should have label at this point

    	# call vote control function for poll model
    	poll = PollManager.get_poll(poll_id)
    	await poll.select(data.user_id, data.emoji.name, discord_message)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, data):
    	pass


def setup(bot):
	bot.add_cog(Polling(bot))