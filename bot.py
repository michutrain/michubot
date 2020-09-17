import os
import discord
import json

from discord.ext import commands
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
    print('bot is live')

@bot.command(brief = '!ping', description = 'Pings the bot')
async def ping(ctx):
    await ctx.send(f"`pong! the connection speed is {round (bot.latency * 1000)}ms`")

@bot.command(brief = '!clear <number>', description = 'Deletes the previous n messages')
async def clear(ctx, amount = 1):
    await ctx.channel.purge(limit = amount + 1)

@bot.command(brief = '!load <cog>', description = 'Loads cogs <deprecated>')
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    ctx.send("`Loaded`")

@bot.command(brief = '!unload <cog>', description = 'Unloads cogs <deprecated>')
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    ctx.send("`Unloaded`'")

@bot.command(brief = '!reload <cog>', description = 'Reloads cogs <deprecated>')
async def reload(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    bot.unload_extension(f'cogs.{extension}')
    ctx.send("`Reloaded`'")

@bot.command(brief = '!win <name>', description = 'Adds a win to designated player')
async def win(ctx, *args):
    if len(args) !=1:
        await ctx.send("Please provide a name `!win <name>`")
        return 
    if args[0] in scores:
        scores[args[0]]["win"] += 1
        save()
        await ctx.send(f"Win has been added to `{args[0]}`. Total wins for `{args[0]}` are now: `{scores[args[0]]['win']}`")
    else:
        await ctx.send(f"{args[0]} does not exist in the leaderboards.")  

@bot.command(brief = '!unwin <name>', description = 'Removes a win from a designated player')
async def unwin(ctx, *args):
    if len(args) !=1:
        await ctx.send("Please provide a name `!win <name>`")
        return 
    if args[0] in scores:
        if scores[args[0]]["win"] == 0:
            await ctx.send(f"{args[0]} is already at 0 wins.")
        else:
            scores[args[0]]["win"] -= 1
            save()
            await ctx.send(f"Win has been removed from `{args[0]}`. Total wins for `{args[0]}` are now: `{scores[args[0]]['win']}`")
    else:
        await ctx.send(f"{args[0]} does not exist in the leaderboards.")  

@bot.command(brief = '!lost <name>', description = 'Adds a loss to a designated player')
async def lose(ctx, *args):
    if len(args) !=1:
        await ctx.send("Please provide a name `!loss <name>`")
        return
    if args[0] in scores:
        scores[args[0]]["loss"] += 1
        save()
        await ctx.send(f"Loss has been added to `{args[0]}`. Total losses for `{args[0]}` are now: `{scores[args[0]]['loss']}`")
    else:
        await ctx.send(f"{args[0]} does not exist in the leaderboards.")  

@bot.command(brief = '!unlose <name>', description = 'Removes a loss from a designated player')
async def unlose(ctx, *args):
    if len(args) !=1:
        await ctx.send("Please provide a name `!loss <name>`")
        return
    if args[0] in scores:
        if scores[args[0]]["loss"] == 0:
            await ctx.send(f"{args[0]} is already at 0 losses.")
        else:
            scores[args[0]]["loss"] -= 1
            save()
            await ctx.send(f"Loss has been removed from `{args[0]}`. Total losses for `{args[0]}` are now: `{scores[args[0]]['loss']}`")
    else:
        await ctx.send(f"{args[0]} does not exist in the leaderboards.")  

@bot.command(brief = '!add <name>', description = 'Adds a player to the leaderboards')
async def add(ctx, *args):
    if len(args) !=1:
        await ctx.send("Please provide a name `!add <name>`")
        return
    if args[0] not in scores:
        scores[args[0]] = {"win": 0, "loss": 0}
        save()
        await ctx.send(f"{args[0]} has been added to the leaderboards.")
    else:
        await ctx.send(f"{args[0]} already exists in the leaderboards.")


@bot.command(brief = '!remove <name>', description = 'Removes a player from the leaderboards')
async def remove(ctx, *args):
    if len(args) !=1:
        await ctx.send("Please provide a name `!remove <name>`")
        return
    if args[0] in scores:
        del scores[args[0]]
        save()
        await ctx.send(f"{args[0]} has been removed from the leaderboards.")
    else:
        await ctx.send(f"{args[0]} does not exist in the leaderboards.")   

@bot.command(pass_context = True , aliases = ['leaderboard', 'show', 'score', 'lits', 'lsit'], brief = '!list', description='Displays the leaderboard')
async def list(ctx):
    rows = [[key, scores[key]["win"], scores[key]["loss"]] for key in scores]
    cols = ["Player", "Wins", "Losses"]
    rows = [cols] + rows

    for col in range(len(cols)):
        col_size = max([len(str(row[col])) for row in rows])

        for row in rows:
             row[col] = str(row[col]).ljust(col_size)

    row_strings = ["║ " + " │ ".join(row) + " ║" for row in rows]

    line1 = "╔" + "═" * (max([len(s[0]) for s in rows]) + 2) + "╤" + "═" * (max([len(s[1]) for s in rows]) + 2) + "╤" + "═" * (max([len(s[2]) for s in rows]) + 2) + "╗"
    line2 = "╟" + "─" * (max([len(s[0]) for s in rows]) + 2) + "┼" + "─" * (max([len(s[1]) for s in rows]) + 2) + "┼" + "─" * (max([len(s[2]) for s in rows]) + 2) + "╢"
    line3 = "╚" + "═" * (max([len(s[0]) for s in rows]) + 2) + "╧" + "═" * (max([len(s[1]) for s in rows]) + 2) + "╧" + "═" * (max([len(s[2]) for s in rows]) + 2) + "╝"

    row_strings = [line1] + row_strings[:1] + [line2] + row_strings[1:] + [line3]
    bigBlockOfText = "\n".join(row_strings)
    ret = discord.Embed(title = "Valorant Leaderboard", description = f"```{bigBlockOfText}```", color=0x930101)
    ret.set_thumbnail(url = "https://cdn.discordapp.com/attachments/755958167908909108/756073229671596103/88253746_110183627255722_3150517730348630016_n.png")
    ret.set_footer(text = "Type !help for a list of commands")
    await ctx.send(embed=ret)

bot.run(TOKEN)