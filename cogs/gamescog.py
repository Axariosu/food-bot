from games.trivia import Trivia
import gamestest
import discord
from discord.ext import commands
import food

class GamesCog(commands.Cog):
    @commands.command(aliases=["trivia"])
    @commands.guild_only()
    async def start_trivia(self, ctx):
        # food.games[ctx.guild.id] = Trivia(ctx)
        awaitctx.bot.games[ctx.guild.id] = Trivia(ctx)
        # ctx.bot.games[ctx.guild.id] = gamestest.Game(20)
        await ctx.bot.games[ctx.guild.id].run()
        # await food.games[ctx.guild.id].run()

    # @commands.command(aliases=["checkstate"])
    # @commands.guild_only()
    # async def check_state(self, ctx):
    #     game = ctx.bot.games[ctx.guild.id]
    #     if not game:
    #         await ctx.send("No game found, Start a game with `!start_game` first!")
    #         return

    #     await ctx.send(f"Current state: {game.some_state}")

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
        if not message.author.bot:
            await food.bot.games[message.guild.id].handle_on_message(message)
            pass
            # ctx = await commands.Bot.get_context(message=message)
            # await ctx.send("test")
            # ctx = message.channel
            # await ctx.bot.games[ctx.guild.id].handle_on_message(message)
            # ctx = await commands.Bot.get_context(self, message)
            # await ctx.send("test: " + message.content)
            # await ctx.bot.games[ctx.guild.id].handle_on_message(message)
        # if not message.author.bot:
            # await message.channel.send("hi")

def setup(bot): 
    bot.add_cog(GamesCog(bot))