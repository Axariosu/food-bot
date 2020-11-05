import discord
from discord.ext import flags, commands
import random
import util.util as util
import util.jpegtionaryutil as jpegtionaryutil
import io
import uuid
from PIL import Image

f = open("wordlist_10000.txt", "r")
wordlist = [x.strip() for x in f]

class ForFun(commands.Cog):
    @flags.add_flag("-q", type=str)
    @flags.add_flag("-p", type=int, default=4)
    @flags.add_flag("-d", type=int, default=1)
    @flags.command(hidden=True)
    @commands.is_owner()
    async def gif(self, ctx, **flags):
        async with ctx.channel.typing():
            res = jpegtionaryutil.generate_unpixellating_gif(flags["q"], flags["p"], flags["d"])
        res.seek(0)
        await ctx.send(file=discord.File(fp=res, filename=f'{flags["q"]}.gif'))

def setup(bot): 
    bot.add_cog(ForFun(bot))