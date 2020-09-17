import os
import random
import discord
import psycopg2

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('PORT')
USER = os.getenv("DB_USER")
PASSWORD = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DB_NAME')

bot = commands.Bot(command_prefix='!')
try:
    db = psycopg2.connect(
        host = HOST,
        port = PORT,
        user = USER,
        password = PASSWORD,
        database = DATABASE
    )
    cur = db.cursor()
    cur.execute("SELECT VERSION()")
    print(cur.fetchone())
    print("database connection initialized")
except Exception as err:
    print(err)

@bot.event
async def on_ready():
    print('bot is live')

@bot.command()
async def ping(ctx):
    await ctx.send(f"`pong! the connection speed is {round (bot.latency * 1000)}ms`")

@bot.command()
async def clear(ctx, amount = 2):
    await ctx.channel.purge(limit = amount)

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    ctx.send("`Loaded`")

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    ctx.send("`Unloaded`'")

@bot.command()
async def reload(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    bot.unload_extension(f'cogs.{extension}')
    ctx.send("`Reloaded`'")

@bot.command()
async def win(ctx, *args):
    if len(args) !=1:
        await ctx.send("Please provide a name `!win <name>`")
        return 
    try:
        cur.execute("UPDATE users SET win = win + 1 WHERE name = %s", [args[0]])
        db.commit()
        cur.execute("SELECT win FROM users WHERE name = %s", [args[0]])    
        await ctx.send(f"Win has been added to `{args[0]}`. Total wins for `{args[0]}` are now: `{cur.fetchone()[0]}`")
    except Exception as err:
        db.rollback()
        print(err)
        await ctx.send(f"{args[0]} does not exist in the leaderboards.")  

@bot.command()
async def lose(ctx, *args):
    if len(args) !=1:
        await ctx.send("Please provide a name `!loss <name>`")
        return
    try:
        cur.execute("UPDATE users SET loss = loss + 1 WHERE name = %s", [args[0]])
        db.commit()
        cur.execute("SELECT loss FROM users WHERE name = %s", [args[0]])    
        await ctx.send(f"Loss has been added to `{args[0]}`. Total wins for `{args[0]}` are now: `{cur.fetchone()[0]}`")
    except:
        db.rollback()
        await ctx.send(f"{args[0]} does not exist in the leaderboards.")  


@bot.command()
async def add(ctx, *args):
    if len(args) !=1:
        await ctx.send("Please provide a name `!add <name>`")
        return
    try:
        cur.execute("INSERT INTO users (name, win, loss) VALUES (%s, 0, 0)", [args[0]])
        db.commit() 
        await ctx.send(f"{args[0]} has been added to the leaderboards.")
    except:
        db.rollback()
        await ctx.send(f"{args[0]} already exists iwn the leaderboards.")


@bot.command()
async def remove(ctx, *args):
    if len(args) !=1:
        await ctx.send("Please provide a name `!remove <name>`")
        return
    try:
        cur.execute("SELECT * FROM users WHERE name = %s", [args[0]]) 
        cur.execute("DELETE FROM users WHERE name = %s", [args[0]])
        db.commit()
        await ctx.send(f"{args[0]} has been removed from the leaderboards.")
    except:
        db.rollback()
        await ctx.send(f"{args[0]} does not exist in the leaderboards.")   



bot.run(TOKEN)