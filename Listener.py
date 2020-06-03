import discord
import asyncio
from discord.ext import commands
import Constants
import DriverWerewolf

DISCORD_TOKEN = ""

client = commands.Bot(command_prefix='&')

@client.command()
async def playgame(ctx, *args):
    if len(args) == 0:
        await ctx.send("Currently I only support One Night Ultimate Werewolf. To play One Night "
                       "Ultimate Werewolf, use !playgame onuw or !playgame werewolf")
    elif len(args) > 0 and args[0] in Constants.ONUWSTRINGS:
        await ctx.send("Now playing One Night Ultimate Werewolf.")
        reaction_string = "**Roles - One Night Ultimate Werewolf:** The following roles are currently supported " \
                          "supported by our bot. "
        reaction_string += "React wth the roles you would wish to use: \n"
        reaction_string += "🧍: ""Villager""\n"
        reaction_string += "👨: ""Villager""\n"
        reaction_string += "👩: ""Villager""\n"
        reaction_string += "🐺: ""Werewolf""\n"
        reaction_string += "☠️: ""Werewolf""\n"
        reaction_string += "🍺: ""Drunk""\n"
        reaction_string += "🔫: ""Hunter""\n"
        reaction_string += "😴: ""Insomniac""\n"
        reaction_string += "⬅️: ""Mason""\n"
        reaction_string += "➡️: ""Mason""\n"
        reaction_string += "💁: ""Minion""\n"
        reaction_string += "💰: ""Robber""\n"
        reaction_string += "🧠: ""Seer""\n"
        reaction_string += "😐: ""Tanner""\n"
        reaction_string += "😲: ""Troublemaker""\n"
        await ctx.send(reaction_string)
        player_string = "**Players - One Night Ultimate Werewolf:** React with 👍 if you wish to play."
        await ctx.send(player_string)
        await ctx.send("Type &startgame to start the game once you've selected your roles")
    elif len(args) > 0 and str(args[0]).lower() == "help":
        await ctx.send("Use &playgame to learn which games are supported")


@client.command()
async def startgame(ctx):
    async for msg in ctx.message.channel.history(limit=5):
        if msg.author == client.user and msg.content.startswith("**Players - One Night Ultimate Werewolf"):
            players = await Constants.HelperMethods.get_players(msg, client.user)
            # players = [p.display_name for p in players]
            await ctx.send(players)
        if msg.author == client.user and msg.content.startswith("**Roles - One Night Ultimate Werewolf"):
            role_dict = DriverWerewolf.getRoleCounts(msg.reactions)
            await ctx.send(str(role_dict))
            role_list = Constants.HelperMethods.convert_dict_to_list(role_dict)
            await ctx.send(str(role_list))
            # DriverWerewolf.main(roles_list=role_list)
            break

@client.command()
async def helpgame(ctx):
    await ctx.send("Use &playgame to learn which games are supported")


@client.event
async def on_message(message):
    if message.author == client.user and message.content.startswith("**Roles - One Night Ultimate Werewolf"):
        await message.add_reaction("🧍")
        await message.add_reaction("👨")
        await message.add_reaction("👩")
        await message.add_reaction("🐺")
        await message.add_reaction("☠")
        await message.add_reaction("🍺")
        await message.add_reaction("🔫")
        await message.add_reaction("😴")
        await message.add_reaction("⬅")
        await message.add_reaction("➡")
        await message.add_reaction("💁")
        await message.add_reaction("💰")
        await message.add_reaction("🧠")
        await message.add_reaction("😐")
        await message.add_reaction("😲")
    elif message.author == client.user and message.content.startswith("**Players - One Night Ultimate Werewolf"):
        await message.add_reaction("👍")
    await client.process_commands(message)

client.run(DISCORD_TOKEN)