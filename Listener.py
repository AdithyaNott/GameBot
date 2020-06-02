import discord
import Constants
import DriverWerewolf

DISCORD_TOKEN = ""

client = discord.Client()

@client.event
async def on_message(message):
    words = message.content.split()
    if words[0] == "!playgame":
        if len(words) > 1 and words[1].lower() in Constants.ONUWSTRINGS:
            await message.channel.send("Now playing One Night Ultimate Werewolf.")
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
            await message.channel.send(reaction_string)
            player_string = "**Players - One Night Ultimate Werewolf:** React with 👍 if you wish to play."
            await message.channel.send(player_string)
            await message.channel.send("Type !startgame to start the game once you've selected your roles")
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
    if message.content.strip() == "!startgame":
        async for msg in message.channel.history(limit=5):
            if msg.author == client.user and msg.content.startswith("**Players - One Night Ultimate Werewolf"):
                players = await Constants.HelperMethods.get_players(msg, client.user)
                #players = [p.display_name for p in players]
                await message.channel.send(players)
            if msg.author == client.user and msg.content.startswith("**Roles - One Night Ultimate Werewolf"):
                role_dict = DriverWerewolf.getRoleCounts(msg.reactions)
                await message.channel.send(str(role_dict))
                role_list = Constants.HelperMethods.convert_dict_to_list(role_dict)
                await message.channel.send(str(role_list))
                #DriverWerewolf.main(roles_list=role_list)
                break

client.run(DISCORD_TOKEN)