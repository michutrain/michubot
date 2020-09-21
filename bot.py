import asyncio
import os
import discord
import json
import random

from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

if os.path.exists("leaderboard"):
    scores = json.load(open("leaderboard", "r"))
else:
    scores = {}


def save():
    json.dump(scores, open("leaderboard", "w+"))


@bot.event
async def on_ready():
    print('bot is live', flush=True)

@bot.command(brief='!ping', description='Pings the bot')
async def ping(ctx):
    print("a\nb\nc\nd   ", flush=True)
    await ctx.send(f"`pong! the connection speed is {round (bot.latency * 1000)}ms`")


@bot.command(pass_context=True, aliases=['delete'], brief='!clear <number>', description='Deletes the previous n messages')
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount + 1)


@bot.command(brief='!load <cog>', description='Loads cogs <deprecated>')
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    ctx.send("`Loaded`")


@bot.command(brief='!unload <cog>', description='Unloads cogs <deprecated>')
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    ctx.send("`Unloaded`'")


@bot.command(brief='!reload <cog>', description='Reloads cogs <deprecated>')
async def reload(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    bot.unload_extension(f'cogs.{extension}')
    ctx.send("`Reloaded`'")


@bot.command(brief='!win <name>', description='Adds a win to designated player')
async def win(ctx, *args):
    print('win', flush=True)
    if len(args) < 1:
        await ctx.send("Please provide a name `!win <name>`")
        return
    for name in args:
        name = name.capitalize()
        for user in scores:
            curr_name = str(scores[user].get('name'))
            if curr_name == name:
                scores[user]["win"] += 1
                save()
                await ctx.send(f"Win has been added to `{name}`. Total wins for `{name}` are now: `{scores[user]['win']}`")
                return
            elif curr_name is None:
                print(f"user {curr_name} does not have name field yet", flush=True)

        await ctx.send(f"{name} does not exist in the leaderboards.")


@bot.command(brief='!unwin <name>', description='Removes a win from a designated player')
async def unwin(ctx, *args):
    print('unwin', flush=True)
    if len(args) < 1:
        await ctx.send("Please provide a name `!win <name>`")
        return
    for name in args:
        name = name.capitalize()
        for user in scores:
            curr_name = str(scores[user].get('name'))
            if curr_name == name:
                if scores[user]["win"] == 0:
                    await ctx.send(f"{name} is already at 0 wins.")
                else:
                    scores[user]["win"] -= 1
                    save()
                    await ctx.send(
                        f"Win has been removed from `{name}`. Total wins for `{name}` are now: `{scores[user]['win']}`")
                return
            elif curr_name is None:
                print(f"user {curr_name} does not have name field yet", flush=True)

    await ctx.send(f"{name} does not exist in the leaderboards.")


@bot.command(brief='!lost <name>', description='Adds a loss to a designated player')
async def lose(ctx, *args):
    print('lose', flush=True)
    if len(args) < 1:
        await ctx.send("Please provide a name `!loss <name>`")
    for name in args:
        name = name.capitalize()
        for user in scores:
            curr_name = str(scores[user].get('name'))
            if curr_name == name:
                scores[user]["loss"] += 1
                save()
                await ctx.send(
                    f"Loss has been added to `{name}`. Total losses for `{name}` are now: `{scores[user]['loss']}`")
                return
            elif curr_name is None:
                print(f"user {curr_name} does not have name field yet", flush=True)

        await ctx.send(f"{name} does not exist in the leaderboards.")


@bot.command(brief='!unlose <name>', description='Removes a loss from a designated player')
async def unlose(ctx, *args):
    print('unlose', flush=True)
    if len(args) < 1:
        await ctx.send("Please provide a name `!loss <name>`")
        return
    for name in args:
        name = name.capitalize()
        for user in scores:
            curr_name = str(scores[user].get('name'))
            if curr_name == name:
                if scores[user]["loss"] == 0:
                    await ctx.send(f"{name} is already at 0 losses.")
                else:
                    scores[user]["loss"] -= 1
                    save()
                    await ctx.send(
                        f"Loss has been removed from `{name}`. Total losses for `{name}` are now: `{scores[user]['loss']}`")
                return
            elif curr_name is None:
                print(f"user {curr_name} does not have name field yet", flush=True)

        await ctx.send(f"{name} does not exist in the leaderboards.")


@bot.command(brief='!add <name>', description='Adds a player to the leaderboards, using the user ID as a dictionary key')
async def add(ctx, *args):
    print('added', flush=True)
    emoji = '🎁'
    if len(args) != 1:
        await ctx.send("Please provide a name `!add <name>`")
        return
    name = args[0].capitalize()
    message = await ctx.send(f"{emoji} `React to this message to add yourself to the leaderboard!` {emoji}")
    await message.add_reaction(emoji)

    # handler function for when user reacts to the bot's message
    # function will add reacting user to the leaderboard, under the name given on function call
    async def handle_user_import(this_user):
        if str(this_user.id) in scores.keys() or this_user.id in scores.keys():
            await user.send("You have already been added to the leaderboard")
            return False
        else:
            scores[this_user.id] = {"win": 0, "loss": 0, "name": name}
            save()
            await user.send(f"You have been added successfully to the leaderboard under {name}!")
            await ctx.send(f"{this_user.name} has been added to the leaderboard under {name}!")
            return True

    # retry logic to handle when the wrong user reacts to the add message
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=120, check= lambda reaction, user: user != bot.user)
            if await (handle_user_import(user)):
                break
            else:
                continue
        except Exception as error:
            if error is TimeoutError:
                print("Reaction script has timed out", flush=True)
                await ctx.send("The add script has timed out, please run again to update more users")
            else:
                print(error, flush=True)
            break

@bot.command(brief='!remove <name>', description='Removes a player with the given name from the leaderboards')
async def remove(ctx, *args):
    print('removed', flush=True)
    if len(args) != 1:
        await ctx.send("Please provide a name `!remove <name>`")
        return
    name = args[0].capitalize()
    for user in scores:
        curr_name = str(scores[user].get('name'))
        if curr_name == name:
            print(scores[user], flush=True)
            del scores[user]
            save()
            await ctx.send(f"{name} has been removed from the leaderboards.")
            return
    await ctx.send(f"{name} does not exist in the leaderboards.")


@bot.command(pass_context=True, aliases=['leaderboard', 'show', 'score', 'lits', 'lsit'], brief='!list', description='Displays the leaderboard')
async def list(ctx, *args):
    print('list', flush=True)
    if len(args) == 0:
        sorter = "Elo"
    else:
        sorter = args[0].capitalize()
    if len(args) > 1:
        await ctx.send("`!list` to display leaderboard sorted by elo. Otherwise you can sort by: `win, loss, ratio`.")
        return
        
    def ratio(key):
        res = "{:.2f}".format((1.0*scores[key]["win"]/(scores[key]["win"]+scores[key]["loss"]) if scores[key]["win"]+scores[key]["loss"] > 0 else 0))
        return float(res)

    def elo(key):
        wlr = ratio(key)
        base = 1000
        pos_win =  (scores[key]["win"]  * 5) + round((wlr * 7))
        pos_loss = (scores[key]["loss"] * 5) + round((wlr * 10))
        neg_win =  (scores[key]["win"]  * 5) + round((wlr * 10))
        neg_loss = (scores[key]["loss"] * 5) + round((wlr * 7))
        if wlr >= 0.5:
            return base + pos_win - pos_loss
        else:
            return base + neg_win - neg_loss

    cols = ["Player", "W", "L", "W/L", "Elo"]
    rows = [[key, scores[key]["win"], scores[key]["loss"], str(round(ratio(key)*100))+"%", elo(key)] for key in scores]
    if sorter == "Win":
        rows.sort(key=lambda x: x[1], reverse=True)
        if sorter == "Loss":
            rows.sort(key=lambda x: x[2], reverse=True)
            if sorter == "Kdr" or sorter == "Ratio" or sorter == "W/l":
                rows.sort(key=lambda x: x[3], reverse=True)
                if sorter == "Elo":
                    rows.sort(key=lambda x: x[4], reverse=True)
    else:
        rows.sort(key=lambda x: x[4], reverse=True)
                
    rows = [cols] + rows

    for col in range(len(cols)):
        col_size = max([len(str(row[col])) for row in rows])

        for row in rows:
            row[col] = str(row[col]).ljust(col_size)

    row_strings = ["║ " + " │ ".join(row) + " ║" for row in rows]

    line1 = "╔" + "═" * (max([len(s[0]) for s in rows]) + 2) + "╤" + "═" * (max([len(s[1]) for s in rows]) + 2) + "╤" + "═" * \
        (max([len(s[2]) for s in rows]) + 2) + "╤" + "═" * (max([len(s[3]) for s in rows]) + 2) + "╤" + "═" * (max([len(s[4]) for s in rows]) + 2) + "╗"
    line2 = "╟" + "─" * (max([len(s[0]) for s in rows]) + 2) + "┼" + "─" * (max([len(s[1]) for s in rows]) + 2) + "┼" + "─" * \
        (max([len(s[2]) for s in rows]) + 2) + "┼" + "─" * (max([len(s[3]) for s in rows]) + 2) + "┼" + "─" * (max([len(s[4]) for s in rows]) + 2) + "╢"
    line3 = "╚" + "═" * (max([len(s[0]) for s in rows]) + 2) + "╧" + "═" * (max([len(s[1]) for s in rows]) + 2) + "╧" + "═" * \
        (max([len(s[2]) for s in rows]) + 2) + "╧" + "═" * (max([len(s[3]) for s in rows]) + 2) + "╧" + "═" * (max([len(s[4]) for s in rows]) + 2) + "╝"

    row_strings = [line1] + row_strings[:1] + [line2] + row_strings[1:] + [line3]
    leaderboard = "\n".join(row_strings)

    embed = discord.Embed(title="Valorant Leaderboard",
                        description=f"Base Elo at 1000 \n ```{leaderboard}```", color=0x930101)
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/755958167908909108/756073229671596103/88253746_110183627255722_3150517730348630016_n.png")
    embed.set_footer(text="Type !help for a list of commands")
    await ctx.send(embed=embed)


@bot.command(brief='!game', description='Sends queue message')
async def game(ctx):
    team1 = []
    team2 = []
    team1_str = ""
    team2_str = ""
    users = []
    print('game', flush=True)
    emoji = '<:valorant:756270078156210177>'
    maps = ['Bind', 'Haven', 'Split', 'Ascent']
    message = await ctx.send(f"{emoji} `React to this message to signup for inhouse valorant!` {emoji}")
    await message.add_reaction(emoji)

    def signup_check(reaction, user):
        users.append(user.name)
        print(users, flush=True)
        return str(reaction) == emoji and reaction.message.id == message.id and reaction.count == 3

    try:
        (reaction, user) = await bot.wait_for('reaction_add', check = signup_check)
        if 'michu bot' in users:
            users.remove('michu bot')
        else:
            print("foo")
        # TODO: add option for draft or randomize
        print(users)
        i = 0
        while i < 1:                                                    # test val
                selected = random.choice(users)
                team1.append(selected)                                  # for win/lose calculation
                team1_str += selected                                   # for the embed
                users.remove(selected)
                i += 1
        team2 = users                                                   # for win/lose calculation
        for user in users:              
            team2_str += user                                           # for the embed                                      
        await ctx.send("`The lobby has been filled.`")
        map = random.choice(maps)
        print(team1_str, flush=True)
        print(team2_str, flush=True)
        print(map, flush=True)
        embed = discord.Embed(title="Valorant 5v5 Teams", color=0x930101)               # ERROR sometimes happens here???
        embed.add_field(name="Team 1", value=team1_str, inline=True)                    # 400 Bad Request (error code: 50035): Invalid Form Body
        embed.add_field(name="Team 2", value=team2_str, inline=True)                    # In embed.fields.1.value: This field is required
        embed.add_field(name="The map that has been selected for this match:", value=f"{emoji}  {map}  {emoji}", inline=False)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/755958167908909108/756073229671596103/88253746_110183627255722_3150517730348630016_n.png")
        embed.set_footer(text="Match Over: Click the number of the winning team.")
        teams = await ctx.send(embed=embed)
        await teams.add_reaction('1️⃣')
        await teams.add_reaction('2️⃣')

        def finish_check(reaction, user):
            print(user)
            return str(reaction) == '1️⃣' or str(reaction) == '2️⃣' and reaction.message.id == teams.id and reaction.count == 2

        try:
            (reaction2, user2) = await bot.wait_for('reaction_add', check = finish_check)
            if str(reaction2) == '1️⃣':
                winner = 1
            else:
                winner = 2
            await ctx.send(f"🎉  `The winner is Team {winner}`  🎉")
            #------------------------------------------
            # TODO: HANDLE WIN/LOSS DISTRIBUTION
            #------------------------------------------
        except Exception as error:
            print(error, flush=True)
            print("inner")
    except Exception as error:
        print(error, flush=True)


@bot.command(brief='!map', description='Rolls the map pool')
async def map(ctx):
    print('map', flush=True)
    maps = ['Bind', 'Haven', 'Split', 'Ascent']
    emoji = '<:valorant:756270078156210177>'
    response = random.choice(maps)
    await ctx.send(f"{emoji} The map `{response}` has been selected for this match. {emoji}")


@bot.command(brief='!update', description='Migrates the user to use the new ID system')
async def update(ctx):
    print('migrate_user', flush=True)
    emoji = '👍'
    message = await ctx.send(f"{emoji} `React to this message to update your user profile!` {emoji}")
    await message.add_reaction(emoji)

    # Handles a reaction from a user, and ensures that
    #   1) the reaction is not from the bot, and
    #   2) the correct message is being reacted to

    def handleReaction(reaction, user):
        return user != bot.user and reaction.message.id == message.id

    # We only break out of this loop when the method times out.
    # This loop will create a new call to handle_migration each time a user reacts to the message.
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=120,
                                                check=handleReaction)
            asyncio.create_task(handle_migration(user))
        except Exception as error:
            if error is TimeoutError:
                print("Reaction script has timed out", flush=True)
                await ctx.send("The update script has timed out, please run again to update more users")
            else:
                print(error, flush=True)
            break


@bot.event
async def handle_migration(curr_user):
    print('handle_migration', flush=True)

    # Handler that responds to a user's reply to the bot, and performs the leaderboard migration
    # from user's plain-text name to the user's ID
    async def perform_migration(message):
        reply_content = message.content
        if str(curr_user.id) in scores.keys() or curr_user.id in scores.keys():
            await curr_user.send(f"Your user has already been migrated, under {scores.get(str(curr_user.id))['name']}.")
            return True
        elif reply_content in scores:
            scores[curr_user.id] = dict(scores[reply_content], name=reply_content)
            del scores[reply_content]
            save()
            await curr_user.send("Your user profile has been successfully updated")
            return True
        elif reply_content == "Cancel":
            await curr_user.send("Leaderboard update has been cancelled.")
            return True
        else:
            await curr_user.send("This is not a valid username, please try again. "
                                 "If you would like to cancel the user update, please type 'Cancel'")
            return False

    await curr_user.send("What is your name on the leaderboard?")

    # Retry loop to handle a user replying with the wrong name
    while True:
        reply = await bot.wait_for("message",
                                   check=lambda reply: reply.author == curr_user and reply.author != bot.user)
        if await perform_migration(reply) is True:
            return
        else:
            continue

bot.run(TOKEN)