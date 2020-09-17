import discord
import json
import ast

from discord.ext import commands

class Leaderboard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('cog is live')

    @commands.command()
    async def add(self, ctx):
        embed=discord.Embed(title="Leaderboard", description="description text")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/755958167908909108/756009280234324078/Untitled-1.png")
        embed.add_field(name="aaaaaaaaaaaaaaaaaaaaaaaaaaaa", value="aaaaaaaaaaaaaaaaaaaaaaaaaaaa", inline=True)
        embed.set_footer(text="footer text")

        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Leaderboard(bot))
