import games
import discord
from discord.ext import commands

class GamesCog(commands.Cog):
    @commands.command(aliases=["startg"])
    @commands.guild_only()
    async def start_game(self, ctx):
        ctx.bot.games[ctx.guild.id] = games.Game(20)

    @commands.command(aliases=["checkstate"])
    @commands.guild_only()
    async def check_state(self, ctx):
        game = ctx.bot.games[ctx.guild.id]
        if not game:
            await ctx.send("No game found, Start a game with `!start_game` first!")
            return

        await ctx.send(f"Current state: {game.some_state}")

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

def setup(bot): 
    bot.add_cog(GamesCog(bot))