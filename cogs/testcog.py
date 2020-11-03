import util.util as util
import discord
import asyncio
import random
import time
from discord.ext import tasks
from discord.ext import commands
import util.jpegtionaryutil as jpegtionaryutil

class TestCog(commands.Cog):
    # @commands.command()
    # async def loadpic(self, ctx):
    pass

def setup(bot): 
    bot.add_cog(TestCog(bot))