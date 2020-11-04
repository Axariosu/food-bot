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
    @flags.add_flag("-q", type=str, default=util.generate_random_words_from_wordlist(1, wordlist))
    @flags.command()
    @commands.guild_only()
    async def gif(self, ctx, **flags):
        res = jpegtionaryutil.generate_unpixellating_gif(flags["q"], 4, 30)
        res.seek(0)
        await ctx.send(file=discord.File(fp=res, filename=f'{uuid.uuid4}.gif'))
        # res = jpegtionaryutil.generate_unpixellating_gif(flags["q"], 4, 30)
        # gif = Image.new(mode="RGB", size=res.size)
        # gif.save(res, format="GIF")
        # gif.seek(0)
        # f = discord.File(gif)


def setup(bot): 
    bot.add_cog(ForFun(bot))