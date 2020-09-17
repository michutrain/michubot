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
    print('Logged in as: '+bot.user.name)

@bot.command()
async def ping(ctx):
    await ctx.send(f'`pong! the connection speed is {round (bot.latency * 1000)}ms`')

bot.run(TOKEN)