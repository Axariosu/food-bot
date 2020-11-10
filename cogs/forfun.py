import discord
from discord.ext import flags, commands
import random
import util.util as util
import util.wooshutil as wooshutil
import util.jpegtionaryutil as jpegtionaryutil
import io
import uuid
from PIL import Image

class ForFun(commands.Cog):
    @flags.add_flag("-q", type=str)
    @flags.add_flag("-p", type=int, default=4)
    @flags.add_flag("-d", type=int, default=1)
    @flags.command(hidden=True)
    @commands.is_owner()
    async def gif(self, ctx, **flags):
        async with ctx.channel.typing():
            res = jpegtionaryutil.generate_unpixellating_gif(flags["q"], flags["p"], flags["d"])
        await ctx.send(file=discord.File(fp=res, filename=f'{flags["q"]}.gif'))


    @flags.add_flag("-q", type=str)
    @flags.add_flag("-p", type=int, default=4)
    @flags.command(hidden=True)
    @commands.is_owner()
    async def img(self, ctx, **flags):
        async with ctx.channel.typing():
            res = jpegtionaryutil.generate_google_images_scrape_mosaic_BytesIO(flags["q"], flags["p"])
        await ctx.send(file=discord.File(fp=res, filename=f'{flags["q"]}.jpg'))

    @flags.command(aliases=["rw"], hidden=True)
    @commands.guild_only()
    async def random_word(self, ctx, **flags):
        await ctx.send(wooshutil.generate_random_start())
    # @flags.add_flag("-q", type=str)
    # @flags.add_flag("-p", type=int, default=4)
    # @flags.command(hidden=True)
    # @commands.is_owner()
    # async def img(self, ctx, **flags):
    #     async with ctx.channel.typing():
    #         res = jpegtionaryutil.scrap(flags["q"], flags["p"])
    #     res.seek(0)
    #     await ctx.send(file=discord.File(fp=res, filename=f'{flags["q"]}.jpg'))

def setup(bot): 
    bot.add_cog(ForFun(bot))