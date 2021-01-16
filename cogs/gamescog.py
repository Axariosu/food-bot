import games.alphafuse
import games.fourplay
import games.jpegtionary
import games.jstrivia
import games.powracer
import games.pow
import games.reactiontime
import games.schwootsh
import games.scrambivia
import games.trivia
import games.uddercode
import games.unscramble
import discord
from discord.ext import flags, commands
import food

class Games(commands.Cog):
    @commands.command(aliases=['alpha'])
    @commands.guild_only()
    async def alphafuse(self, ctx):
        """
        `!alphafuse [options]`
        """
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.alphafuse.AlphaFuse(ctx)
        await ctx.bot.games[ctx.guild.id].start()

    @commands.command(aliases=['4p', 'fp', 'c4'])
    @commands.guild_only()
    async def fourplay(self, ctx):
        """
        `!fourplay [options]`
        """
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.fourplay.Fourplay(ctx)
        await ctx.bot.games[ctx.guild.id].start()

    @flags.add_flag("-h", type=bool, default=True)
    @flags.add_flag("-r", type=int, default=15)
    @flags.add_flag("-s", type=int, default=80)
    @flags.add_flag("-p", type=int, default=4)
    @flags.add_flag("-rt", type=int, default=90)
    @flags.add_flag("-wl", type=str, default="10000")
    @flags.command(aliases=['jpeg'])
    @commands.guild_only()
    async def jpegtionary(self, ctx, **flags):
        """
        `!jpegtionary [options]`
        **`-h <bool>` - Default: True**
        Enables hangman mode 
        **`-r <int>` - Default: 15**
        Number of rounds
        **`-s <int>` - Default: 70**
        Accepts answers above this similarity percentage
        Use `!scramble` to reshuffle the answer
        """
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.jpegtionary.JPEGtionary(ctx, flags["r"], flags["h"], flags["wl"], flags["s"], flags["p"], flags["rt"])
        await ctx.bot.games[ctx.guild.id].start()

    @flags.add_flag("-r", type=int, default=50)
    @flags.add_flag("-s", type=int, default=70)
    @flags.add_flag("-sc", type=bool, default=False)
    @flags.command()
    @commands.guild_only()
    async def trivia(self, ctx, **flags):
        """
        `!trivia [options]`
        **`-r <int>` - Default: 50**
        Number of rounds
        **`-s <int>` - Default: 70**
        Accepts answers above this similarity percentage
        **`-sc <bool>` - Default: False**
        Enables scramble mode by showing the answer shuffled
        Use `!scramble` to reshuffle the answer
        """
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.jstrivia.jsTrivia(ctx, flags["r"], flags["s"], flags["sc"])
        await ctx.bot.games[ctx.guild.id].start()

    @commands.command(hidden=True)
    @commands.guild_only()
    async def oldtrivia(self, ctx):
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.trivia.Trivia(ctx)
        await ctx.bot.games[ctx.guild.id].start()

    @commands.command()
    @commands.guild_only()
    async def pow(self, ctx):
        """
        `!pow [options]`
        """
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.pow.Pow(ctx)
        await ctx.bot.games[ctx.guild.id].start()

    @flags.add_flag("-r", type=int, default=25)
    @flags.add_flag("-mn", type=int, default=2)
    @flags.add_flag("-mx", type=int, default=7)
    @flags.add_flag("-d", type=int, default=10)
    @flags.command(aliases=['rt', 'rxn', 'rxt'])
    @commands.guild_only()
    async def reactiontime(self, ctx, **flags):
        """
        `!reactiontime aliases [options]`
        **`-r <int>` - Default: 25** 
        Number of rounds
        **`-mn <int>` - Default: 2** 
        Mininum time per round
        **`-mx <int>` - Default: 7** 
        Maximum time per round
        **`-d <int>` - Default: 10** 
        Delay before starting
        """
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.reactiontime.ReactionTime(ctx, flags["r"], flags["mn"], flags["mx"], flags["d"])
        await ctx.bot.games[ctx.guild.id].start()
    
    @flags.add_flag("-s", type=int, default=90)
    @flags.add_flag("-w", type=int, default=30)
    @flags.add_flag("-l", type=int, default=3)
    @flags.add_flag("-h", type=int, default=15)
    @flags.command()
    @commands.guild_only()
    async def powracer(self, ctx, **flags):
        """
        `!powracer [options]`
        **`-s <int>` - Default: 90**
        Accepts answers above this similarity percentage
        **`-w` - Default: 30**
        Number of words
        **`-l` - Default: 3**
        Words will have at least this many characters
        **`-h` - Default: 15**
        Words will have at most this many characters
        """
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.powracer.PowRacer(ctx, flags["s"], flags["w"], flags["l"], flags["h"])
        await ctx.bot.games[ctx.guild.id].start()

    @commands.command()
    @commands.guild_only()
    async def schwootsh(self, ctx):
        """
        `!schwootsh [options]`
        """
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.schwootsh.Schwootsh(ctx)
        await ctx.bot.games[ctx.guild.id].start()

    # @commands.command(enabled=False)
    # @commands.guild_only()
    # async def scrambivia(self, ctx):
    #     if ctx.guild.id in ctx.bot.games:
    #         await ctx.send("A game is already running, wait for it to finish!")
    #         return
    #     ctx.bot.games[ctx.guild.id] = games.scrambivia.Scrambivia(ctx)
    #     await ctx.bot.games[ctx.guild.id].start()

    @flags.add_flag("-l", type=int, default=4)
    @flags.command(aliases=['udder'])
    @commands.guild_only()
    async def uddercode(self, ctx, **flags):
        """
        `!uddercode [options]`
        """
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.uddercode.UdderCode(ctx, flags["l"])
        await ctx.bot.games[ctx.guild.id].start()

    @commands.command()
    @commands.guild_only()
    async def unscramble(self, ctx):
        """
        `!unscramble [options]`
        """
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.unscramble.Unscramble(ctx)
        await ctx.bot.games[ctx.guild.id].start()

    @commands.command(hidden=True)
    @commands.guild_only()
    async def kill(self, ctx):
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("Are you sure you want to end this game? (`y`/`n`)")
        else: 
            await ctx.send("food doesn't see a game!")
            return
        def check(m): 
            return True if m.content.lower() == 'y' else False
        val = await ctx.bot.wait_for('message', check=check)
        if val:
            await ctx.bot.games[ctx.guild.id].stop()

    @commands.command(aliases=["checkgames"], hidden=True)
    @commands.is_owner()
    async def current_games(self, ctx):
        await ctx.send(food.bot.games)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        if not message.author.bot and message.guild.id in food.bot.games:
            await food.bot.games[message.guild.id].handle_on_message(message)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_reaction_add(self, reaction, user):
        if not user.bot and reaction.message.guild.id in food.bot.games:
            await food.bot.games[reaction.message.guild.id].handle_on_reaction_add(reaction, user)
        
    @commands.Cog.listener()
    @commands.guild_only()
    async def on_reaction_remove(self, reaction, user):
        if not user.bot and reaction.message.guild.id in food.bot.games:
            await food.bot.games[reaction.message.guild.id].handle_on_reaction_remove(reaction, user)

def setup(bot): 
    bot.add_cog(Games(bot))