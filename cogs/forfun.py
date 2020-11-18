import discord
from discord.ext import flags, commands
import random
import util.util as util
import util.wooshutil as wooshutil
import util.jpegtionaryutil as jpegtionaryutil
import util.tenorutil as tenorutil
import io
import uuid
from PIL import Image

class ForFun(commands.Cog):
    @flags.add_flag("-q", type=str, default="pakistan grape meme")
    @flags.add_flag("-l", type=int, default=1)
    @flags.add_flag("-cf", type=str, default="off")
    @flags.add_flag("-mf", type=str, default="minimal")
    @flags.command()
    @commands.guild_only()
    async def tenor(self, ctx, **flags):
        """
        `!tenor [options]`
        **`-q <str>` - Default: "pakistan grape meme"**
        A search string
        **`-l <int>` - Default: 5**
        Fetches up to a specified number of results
        **`-cf <str>` - Default: off**
        values: off | low | medium | high
        specifies content safety filter level
        """
        async with ctx.channel.typing():
            res = await tenorutil.get_random_gif(flags['q'], flags['l'], flags['cf'], flags['mf'])
        await ctx.send(res)
    
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

    @flags.command()
    @commands.is_owner()
    async def bpm(self, ctx):
        if not ctx.message.attachments:
            return await ctx.send("expected .mp3 or .wav file")
        a = ctx.message.attachments[0]
        await ctx.send(str(a.size) + " " + a.filename)
        k = io.BytesIO(await ctx.message.attachments[0].read()) # iobytes of attachment. send to some fn later! 
        k.seek(0)
        open('testa.py', "wb").write(k.read())
        # with ctx.channel.typing():
        #     await a.save(str(uuid.uuid4()))
            # await ctx.send(file=await a.to_file())
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