import games.trivia
import games.scrambivia
import games.jservicetrivia
import gamestest
import discord
from discord.ext import commands
import food

class GamesCog(commands.Cog):
    @commands.command()
    @commands.guild_only()
    async def trivia(self, ctx):
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.trivia.Trivia(ctx)
        await ctx.bot.games[ctx.guild.id].start()

    @commands.command()
    @commands.guild_only()
    async def scrambivia(self, ctx):
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.scrambivia.Scrambivia(ctx)
        await ctx.bot.games[ctx.guild.id].start()

    @commands.command(aliases=['jstrivia'])
    @commands.guild_only()
    async def jservicetrivia(self, ctx):
        if ctx.guild.id in ctx.bot.games:
            await ctx.send("A game is already running, wait for it to finish!")
            return
        ctx.bot.games[ctx.guild.id] = games.jservicetrivia.jServiceTrivia(ctx)
        await ctx.bot.games[ctx.guild.id].start()

    @commands.command()
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

    @commands.command(aliases=["checkgames"])
    @commands.guild_only()
    async def current_games(self, ctx):
        await ctx.send(food.bot.games)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        if not message.author.bot and message.guild.id in food.bot.games:
            await food.bot.games[message.guild.id].handle_on_message(message)

def setup(bot): 
    bot.add_cog(GamesCog(bot))