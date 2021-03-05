import discord
from discord.ext import flags, commands
import random
import util.util as util
import util.wooshutil as wooshutil
import util.jpegtionaryutil as jpegtionaryutil
import util.tenorutil as tenorutil
import util.starforceutil as starforceutil
import util.flameutil as flameutil
import io
import uuid
import threading, queue

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
        A search string, in quotations
        **`-l <int>` - Default: 5**
        Fetches up to a specified number of results
        **`-cf <str>` - Default: off**
        Values: `off` | `low` | `medium` | `high`
        Specifies content safety filter level
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
    @flags.add_flag("-p", type=int, default=1)
    @flags.command(hidden=True)
    @commands.guild_only()
    async def img(self, ctx, **flags):
        """
        `!img [options]`
        **`-q <str>`**
        A search string, in quotations
        **`-p <int>` - Default: 1**
        Number of pictures to display
        """
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

    @flags.command(aliases=["sf"])
    @flags.add_flag("-n", type=int, default=10000)
    @flags.add_flag("-l", type=int, default=150)
    @flags.add_flag("-s", type=int, default=12)
    @flags.add_flag("-e", type=int, default=22)
    @flags.add_flag("-sc", type=int, default=0)
    @flags.add_flag("-sg", type=int, default=0)
    @flags.add_flag("-event", type=int, default=0)
    @flags.add_flag("-b", type=int, default=1)
    @flags.add_flag("-si", type=int, default=0)
    @commands.guild_only()
    async def starforce(self, ctx, **flags):
        """
        `!starforce [options]`
        **`-n <int>` - Default: 10000**
        Number of simulations, maximum 10000
        **`-l <int>` - Default: 150**
        Item level
        **`-s <int>` - Default: 12**
        Starting star
        **`-e <int>` - Default: 22**
        Ending star
        **`-sc <int>` - Default: 0**
        Starcatch, values are 0 (False) or 1 (True)
        **`-sg <int>` - Default: 0**
        Safeguard, values are 0 (False) or 1 (True)
        **`-event <int>` - Default: 0**
        0: off event
        1: 30% off
        2: 5/10/15
        **`-b <int>` - Default: 1**
        On destruction, does the item reset to 12?
        values are 0 (False) or 1 (True)
        **`-si <int>` - Default: 0**
        0: n items (fast)
        1: n goals (slow, refrain from using)

        Default call:
        **`!starforce -n 10000 -l 150 -s 12 -e 22 -sc 0 -sg 0 -event 0 -b 1 -si -0`**
        """

        n_simulations = min(abs(flags["n"]), 10000)
        starring_results, histogram, max_meso, min_meso, avg_meso, boom, time_elapsed = await starforceutil.run_simulation(n_simulations, flags["l"], flags["s"], flags["e"], False if flags["sg"] == 0 else True, False if flags["sc"] == 0 else True, flags["event"], False if flags["b"] == 0 else True, False if flags["si"] == 0 else True)
        res_1 = ""
        for i in range(len(starring_results.items())):
            if list(starring_results.values())[i] != 0:
                res_1 += str(list(starring_results.keys())[i]) + " " + str(list(starring_results.values())[i]) + "\n"
        res_1 += "```"
        
        event_dict = {
            0: "off event",
            1: "30% off",
            2: "5/10/15"
        }

        res = discord.Embed(title="Starforcing results for %i simulations" % (n_simulations), color=util.generate_random_color())
        desc = "```%i -> %i\nlevel %i equipment\nstarcatch %s\nsafeguard %s\nevent: %s\n12* on item destruction: %s```" % (flags["s"], flags["e"], flags["l"], "off" if flags["sc"] == 0 else "on", "off" if flags["sg"] == 0 else "on", event_dict[flags["event"]], "false" if flags["b"] == 0 else "true")
        res.add_field(name="Parameters", inline=False, value=desc)
        q50, q75, q85, q95 = await starforceutil.generate_confidence_index_from_histogram(histogram)
        desc = "```minimum meso: %s\nmaximum meso: %s\naverage meso: %s\n\nmedian meso: %s\n75 confidence: %s\n85 confidence: %s\n95 confidence: %s\n\ndestructions: %s\n\n" % ('{:,}'.format(min_meso), '{:,}'.format(max_meso), '{:,}'.format(int(avg_meso)), '{:,}'.format(int(q50)), '{:,}'.format(int(q75)), '{:,}'.format(int(q85)), '{:,}'.format(int(q95)), '{:,}'.format(boom)) + res_1
        res.add_field(name="Results", inline=False, value=desc)
        res.set_footer(text='generated in ' + str(time_elapsed) + 's')
        image_binary = await starforceutil.generate_image_from_histogram(histogram)
        unique = uuid.uuid4()
        f = discord.File(fp=image_binary, filename=f'{unique}.jpeg')
        res.set_image(url=f'attachment://{unique}.jpeg')
        await ctx.send(embed=res, file=f)

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

    @flags.command(aliases=["f"])
    @flags.add_flag("-n", type=int, default=10000)
    @flags.add_flag("-l", type=int, default=150)
    @flags.add_flag("-f", type=int, default=0)
    @flags.add_flag("-t", type=float, default=100)
    @flags.add_flag("-b", type=int, default=1)
    @flags.add_flag("-as", type=float, default=9.5)
    @flags.add_flag("-att", type=float, default=2.5)
    @flags.add_flag("-sec", type=float, default=0.0625)
    @commands.guild_only()
    async def flame(self, ctx, **flags):
        """
        `!starforce [options]`
        **`-n <int>` - Default: 10000**
        Number of simulations, maximum 100000 (slow, refrain from using)
        **`-l <int>` - Default: 150**
        Item level
        **`-f <int>` - Default: 0**
        0: red flame
        1: eternal rebirth flame
        **`-t <int>` - Default: 100**
        Flame threshold 
        **`-b <int>` - Default: 0**
        0: non-boss equip (gollux, sw, etc.) *currently not implemented*
        1: boss equip (arcane, abso, fafnir, etc.)
        **`-as <float>` - Default: 9.5**
        All stat % equivalent
        **`-att <float>` - Default: 2.5**
        Weapon/Magic Attack equivalent
        **`-sec <float>` - Default: 1/16**
        Secondary stat equivalent
        Default call:
        **`!flame -n 10000 -l 150 -t 100 -b 1 -as 9.5 -att 2.5 -sec 0.0625`**
        """
        n_simulations = min(abs(flags["n"]), 100000)
        async with ctx.channel.typing():
            flaming_results, histogram, histogram_threshold, max_flames, min_flames, avg_flames, time_elapsed = await flameutil.run_simulation(n_simulations, flags["l"], flags["t"], flags["f"], flags["b"], flags["as"], flags["att"], flags["sec"])
        res_1 = ""
        for i in range(len(flaming_results.items())):
            if list(flaming_results.values())[i] != 0:
                res_1 += "%-7s %-5s %-.2f" % (str(list(flaming_results.keys())[i]), str(list(flaming_results.values())[i]), (list(flaming_results.values())[i] / n_simulations * 100))+ "%\n"
        res_1 += "```"
        res = discord.Embed(title="Flaming results for %i simulations" % (n_simulations), color=util.generate_random_color())
        desc = "```level %i equipment\n%s\nthreshold: %s\n%s\nall stat equiv. %.3f\natt equiv. %.3f\nsecondary stat equiv. %.4f```" % (flags["l"], "red flames" if flags["f"] == 0 else "rainbow flames", flags["t"], "non-boss equipment" if flags["b"] == 0 else "boss equipment", flags["as"], flags["att"], flags["sec"])
        res.add_field(name="Parameters", inline=False, value=desc)
        q50, q75, q85, q95 = await flameutil.generate_confidence_index_from_histogram(histogram_threshold)
        desc = "```minimum flames: %s\nmaximum flames: %s\naverage flames: %s\n\nmedian flames: %s\n75 confidence: %s\n85 confidence: %s\n95 confidence: %s\n\n" % ('{:,}'.format(min_flames) + ' (' + '{:,}'.format(min_flames * 9120000) + ')', '{:,}'.format(max_flames) + ' (' + '{:,}'.format(max_flames * 9120000) + ')', '{:,}'.format(int(avg_flames)) + ' (' + '{:,}'.format(int(avg_flames) * 9120000) + ')', '{:,}'.format(int(q50)) + ' (' + '{:,}'.format(int(q50) * 9120000) + ')', '{:,}'.format(int(q75)) + ' (' + '{:,}'.format(int(q75) * 9120000) + ')', '{:,}'.format(int(q85)) + ' (' + '{:,}'.format(int(q85) * 9120000) + ')', '{:,}'.format(int(q95)) + ' (' + '{:,}'.format(int(q95) * 9120000) + ')\n\n' + res_1)
        res.add_field(name="Results", inline=False, value=desc)
        res.set_footer(text='generated in ' + str(time_elapsed) + 's')
        image_binary = await flameutil.generate_image_from_histogram(histogram, "flame score", "frequency")
        unique = uuid.uuid4()
        f = discord.File(fp=image_binary, filename=f'{unique}.jpeg')
        res.set_image(url=f'attachment://{unique}.jpeg')
        await ctx.send(embed=res, file=f)


def setup(bot): 
    bot.add_cog(ForFun(bot))