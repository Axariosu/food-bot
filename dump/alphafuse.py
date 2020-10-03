import discord
# import time
# import alphafuseutil
from discord.ext import commands
# from player import Player

# tracked_players = []



class AlphaFuse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = False
        # self.server = server
        # self.round = 0
        # self.ingame = []
        # self.eliminated = []

    def game_start(self, ctx):
    
        return 5

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print('Online')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command()
    async def alpha(self, ctx):
        # await ctx.send('!bjStart')
        self.game = True
        # await game_start(ctx)
    
    @commands.Cog.listener()
    async def on_message(self, ctx, message):
        if self.game:
            await ctx.send_message(message.channel, "IN GAME")
        
    # @commands.Cog.listener()
    




def setup(bot): 
    bot.add_cog(AlphaFuse(bot))

    # @bot.event
    # async def on_message(self, ctx):

        # await ctx.send('hello')
        # if message.content.startswith('$greet'):
        #     channel = message.channel
        #     await channel.send('Say hello!')

        #     def check(m):
        #         return m.content == 'hello' and m.channel == channel

        #     msg = await client.wait_for('message', check=check)
        #     await channel.send('Hello {.author}!'.format(msg))

    # async def my_message(message):
    #     pass
    
    # async def add_to_tracked(self, id):
    #     """
    #     Adds the player to trackedplayers. 
    #     """
    #     if not tracked_players.get(id):
    #         tracked_players[id] = Player(id)

    # async def game_start(self, ctx):
        # """
        # Starts the game, players have 60 seconds to type in their first answer. 
        # """

        # message = 'Starting Alpha Fuse!'
        # await ctx.send(message)
        # bot.add_listener
        # pass

    # async def bot_round(self):
    #     """
    #     Picks x characters, maximum of 5 and timer.
    #     """
    #     pass
    #     # for player in self.ingame:
    #     #     player.