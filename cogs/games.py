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
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.alphafuse.AlphaFuse(ctx)
        await ctx.bot.games[ctx.guild.id].start()

    @commands.command(aliases=['4p'])
    @commands.guild_only()
    async def fourplay(self, ctx):
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.fourplay.Fourplay(ctx)
        await ctx.bot.games[ctx.guild.id].start()

    @flags.add_flag("-h", type=bool, default=False)
    @flags.add_flag("-r", type=int, default=15)
    @flags.add_flag("-wl", type=str, default="10000")
    @flags.command(aliases=['jpeg'])
    @commands.guild_only()
    async def jpegtionary(self, ctx, **flags):
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.jpegtionary.JPEGtionary(ctx, flags["r"], flags["h"], flags["wl"])
        await ctx.bot.games[ctx.guild.id].start()

    @flags.add_flag("-r", type=int, default=50)
    @flags.add_flag("-s", type=int, default=70)
    @flags.add_flag("-sc", type=bool, default=False)
    @flags.command()
    @commands.guild_only()
    async def trivia(self, ctx, **flags):
        """
        Usage: !trivia [options]
        -s  [similarity]    default: 70
        -r  [rounds]        default: 50
        -sc [scramble]      default: False
        I'll accept your answer if it's at least [-s]% similar!
        """
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.jstrivia.jsTrivia(ctx, flags["r"], flags["s"], flags["sc"])
        await ctx.bot.games[ctx.guild.id].start()

    @commands.command()
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
        Usage: !powracer [options]
        -s [--similarity] *default*: 90
        -w [--words] *default*: 30
        -l [--lowercharlimit] *default*: 3
        -h [--highercharlimit] *default*: 15
        Players have some time per round to type my randomly generated words! 
        I'll accept your message if it's at least [-s]% similar!
        """
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.powracer.PowRacer(ctx, flags["s"], flags["w"], flags["l"], flags["h"])
        await ctx.bot.games[ctx.guild.id].start()

    @commands.command()
    @commands.guild_only()
    async def schwootsh(self, ctx):
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.schwootsh.Schwootsh(ctx)
        await ctx.bot.games[ctx.guild.id].start()

    @commands.command()
    @commands.guild_only()
    async def scrambivia(self, ctx):
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.scrambivia.Scrambivia(ctx)
        await ctx.bot.games[ctx.guild.id].start()

    @commands.command(aliases=['udder'])
    @commands.guild_only()
    async def uddercode(self, ctx):
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.uddercode.UdderCode(ctx)
        await ctx.bot.games[ctx.guild.id].start()

    @commands.command()
    @commands.guild_only()
    async def unscramble(self, ctx):
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.unscramble.Unscramble(ctx)
        await ctx.bot.games[ctx.guild.id].start()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def kill(self, ctx):
        await ctx.bot.games[ctx.guild.id].stop()

    # commands shouldn't get more complicated than this.
    # all the game functionallity should be handled by the game class,
    # and not the command.
    @commands.command(aliases=["changestate", "sawp_state", "sawpstate"])
    @commands.guild_only()
    async def change_state(self, ctx, new_state: int):
        game = ctx.bot.games[ctx.guild.id]
        if not game:
            await ctx.send("No game found, Start a game with `!start_game` first!")
            return

        old_state = game.some_state
        game.change_state(new_state)

        await ctx.send(f"Changed state from {old_state} to {game.some_state}")

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