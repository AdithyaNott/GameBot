import discord
import asyncio
from discord.ext import commands
import Constants
import DriverWerewolf

DISCORD_TOKEN = ""

client = commands.Bot(command_prefix='&')

# When you play a game
@client.command()
async def playgame(ctx, *args):

    def startgamecheck(m):
        return m.content.strip().startswith("Start")

    # If the command is just &playgame, then showing which games we support
    if len(args) == 0:
        await ctx.send("Currently I only support One Night Ultimate Werewolf. To play One Night "
                       "Ultimate Werewolf, use &playgame onuw or &playgame werewolf")
    elif len(args) > 0 and str(args[0]).lower() in Constants.ONUWSTRINGS:
        await ctx.send("Now playing One Night Ultimate Werewolf.")

        #TODO: make this neater
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
        reaction_id = (await ctx.send(reaction_string)).id
        player_string = "**Players - One Night Ultimate Werewolf:** React with 👍 if you wish to play."
        player_id = (await ctx.send(player_string)).id
        await ctx.send("""Type "Start" to start the game once you've selected your roles""")
        try:
            await client.wait_for('message', timeout=120.0, check=startgamecheck)
        except asyncio.TimeoutError:
            await ctx.send("Game timed out, try creating game again")
            return
        else:
            try:
                player_msg = await ctx.fetch_message(player_id)
            except Exception:
                await ctx.send("Can't find the message for getting list of players.")
                await ctx.send("Closing game.")
                return
            players = await Constants.HelperMethods.get_players(player_msg, client.user)
            try:
                reaction_msg = await ctx.fetch_message(reaction_id)
            except Exception:
                await ctx.send("Can't find the message for getting list of roles.")
                await ctx.send("Closing game.")
                return
            role_dict = DriverWerewolf.getRoleCounts(reaction_msg.reactions)
            role_list = Constants.HelperMethods.convert_dict_to_list(role_dict)
            #await ctx.send(str(role_list))
            #await ctx.send(str(players))
            try:
                await DriverWerewolf.main(ctx, role_list, players, client)
            except Exception as e:
                await ctx.send(str(e))
                await ctx.send("Closing game")
    elif len(args) > 0 and str(args[0]).lower() == "help":
        await ctx.send("Use &playgame to learn which games are supported")


@client.command()
async def helpgame(ctx):
    await ctx.send("Use &playgame to learn which games are supported")


@client.event
async def on_message(message):
    if message.author == client.user and message.content.startswith("**Roles - One Night Ultimate Werewolf"):
        #TODO: add this under the playgame code.
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