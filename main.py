import discord

from pathlib import Path


TOKEN = Path('secret/token.txt').read_text()


client = discord.ext.commands.Bot(command_prefix="gm!")

client.load_extension("cogs.polling")

@client.event
async def on_ready():
    #simple debug for now
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)