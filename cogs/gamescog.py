import games.alphafuse
import games.fourplay
import games.jservicetrivia
import games.powracer
import games.pow
import games.schwootsh
import games.scrambivia
import games.trivia
import games.uddercode
import games.unscramble
import gamestest
import discord
from discord.ext import flags, commands
import food

class GamesCog(commands.Cog):
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

    @commands.command(aliases=['trivia'])
    @commands.guild_only()
    async def jservicetrivia(self, ctx):
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.jservicetrivia.jServiceTrivia(ctx)
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
    
    @flags.add_flag("-s", type=int, default=90)
    @flags.add_flag("-w", type=int, default=30)
    @flags.command()
    @commands.guild_only()
    async def powracer(self, ctx, **flags):
        """
        Usage: !powracer [options]
        -s [--similarity] *default*: 90
        -w [--words] *default*: 30
        Players have some time per round to type my randomly generated words! 
        I'll accept your message if it's at least [-s]% similar!
        """
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.powracer.PowRacer(ctx, flags["s"], flags["w"])
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
    bot.add_cog(GamesCog(bot))

# @a
# def b:
#   pass

# def b:
#   pass
# b = a(b)