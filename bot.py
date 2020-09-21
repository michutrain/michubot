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
        if name in scores:
            scores[name]["win"] += 1
            save()
            await ctx.send(f"Win has been added to `{name}`. Total wins for `{name}` are now: `{scores[name]['win']}`")
        else:
            await ctx.send(f"{name} does not exist in the leaderboards.")


@bot.command(brief='!unwin <name>', description='Removes a win from a designated player')
async def unwin(ctx, *args):
    print('unwin', flush=True)
    if len(args) < 1:
        await ctx.send("Please provide a name `!win <name>`")
        return
    for name in args:
        name = name.capitalize()
        if name in scores:
            if scores[name]["win"] == 0:
                await ctx.send(f"{name} is already at 0 wins.")
            else:
                scores[name]["win"] -= 1
                save()
                await ctx.send(f"Win has been removed from `{name}`. Total wins for `{name}` are now: `{scores[name]['win']}`")
        else:
            await ctx.send(f"{name} does not exist in the leaderboards.")


@bot.command(brief='!lost <name>', description='Adds a loss to a designated player')
async def lose(ctx, *args):
    print('lose', flush=True)
    if len(args) < 1:
        await ctx.send("Please provide a name `!loss <name>`")
    for name in args:
        name = name.capitalize()
        if name in scores:
            scores[name]["loss"] += 1
            save()
            await ctx.send(f"Loss has been added to `{name}`. Total losses for `{name}` are now: `{scores[name]['loss']}`")
        else:
            await ctx.send(f"{name} does not exist in the leaderboards.")


@bot.command(brief='!unlose <name>', description='Removes a loss from a designated player')
async def unlose(ctx, *args):
    print('unlose', flush=True)
    if len(args) < 1:
        await ctx.send("Please provide a name `!loss <name>`")
        return
    for name in args:
        name = name.capitalize()
        if name in scores:
            if scores[name]["loss"] == 0:
                await ctx.send(f"{name} is already at 0 losses.")
            else:
                scores[name]["loss"] -= 1
                save()
                await ctx.send(f"Loss has been removed from `{name}`. Total losses for `{name}` are now: `{scores[name]['loss']}`")
        else:
            await ctx.send(f"{name} does not exist in the leaderboards.")


@bot.command(brief='!add <name>', description='Adds a player to the leaderboards')
async def add(ctx, *args):
    print('added', flush=True)
    if len(args) != 1:
        await ctx.send("Please provide a name `!add <name>`")
        return
    for name in args:
        name = name.capitalize()
        if name not in scores:
            scores[name] = {"win": 0, "loss": 0}
            save()
            await ctx.send(f"{name} has been added to the leaderboards.")
        else:
            await ctx.send(f"{name} already exists in the leaderboards.")


@bot.command(brief='!remove <name>', description='Removes a player from the leaderboards')
async def remove(ctx, *args):
    print('removed', flush=True)
    if len(args) != 1:
        await ctx.send("Please provide a name `!remove <name>`")
        return
    for name in args:
        name = name.capitalize()
        if name in scores:
            del scores[name]
            save()
            await ctx.send(f"{name} has been removed from the leaderboards.")
        else:
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
        return str(reaction) == emoji and reaction.message.id == message.id and reaction.count == 11

    try:
        (reaction, user) = await bot.wait_for('reaction_add', check = signup_check)
        if 'michu bot' in users:
            users.remove('michu bot')
        else:
            print("foo")
        # TODO: add option for draft or randomize
        print(users)
        i = 0
        while i < 5:                                                             # test val
                selected = random.choice(users)
                team1.append(selected)                                           # for win/lose calculation
                team1_str += selected + "\n"                                     # for the embed
                users.remove(selected)
                i += 1
        team2 = users                                                             # for win/lose calculation
        for user in users:              
            team2_str += user + "\n"                                              # for the embed                                      
        await ctx.send("`The lobby has been filled.`")
        map = random.choice(maps)
        print(team1_str, flush=True)
        print(team2_str, flush=True)
        print(map, flush=True)
        embed = discord.Embed(title="Valorant 5v5 Teams", color=0x930101)
        embed.add_field(name="Team 1", value=team1_str, inline=True)
        embed.add_field(name="Team 2", value=team2_str, inline=True)
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


bot.run(TOKEN)