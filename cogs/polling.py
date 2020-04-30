import discord
from discord.ext import commands


class Polling(commands.Cog):
	def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, data):
    	if data.user_id == self.bot.user.id or not data.emoji:
    		# Ignore bot's own reacts and invalid reacts
    		return

    	channel = self.bot.getchannel(data.channel_id)
    	# check where the message came from
    	if isinstance(channel, discord.TextChannel):
    		# get label from message
    		pass

    	# should have label at this point

    	# call vote control function for poll model
    	pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, data):
    	pass


def setup(bot):
	bot.add_cog(Polling(bot))