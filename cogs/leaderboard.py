import discord
from discord.ext import commands

class Leaderboard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('cog is live')

    @commands.command()
    async def add(self, ctx, pt: int, name: str):
        await ctx.send('temp')

def setup(bot):
    bot.add_cog(Leaderboard(bot))
