import discord
import time
import alphafuseutil
from discord.ext import commands
from player import Player

tracked_players = []



class AlphaFuse(object):
    def __init__(self, bot=None, server=None):
        self.bot = bot
        self.server = server
        # self.round = 0
        # self.ingame = []
        # self.eliminated = []


    # def game_start():



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