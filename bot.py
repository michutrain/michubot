import os
import random
import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('bot is live')

@bot.command()
async def ping(ctx):
    await ctx.send(f'`pong! the connection speed is {round (bot.latency * 1000)}ms`')

@bot.command()
async def clear(ctx, amount = 2):
    await ctx.channel.purge(limit = amount)

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    ctx.send('`Loaded`')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    ctx.send('`Unloaded`')

@bot.command()
async def reload(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    bot.unload_extension(f'cogs.{extension}')
    ctx.send('`Reloaded`')

    
for filename in os.listdir('./cogs'):
    if filename.endswith('py'):
        bot.load_extension(f'cogs.{filename[:-3]}')






bot.run(TOKEN)