import discord
import asyncio
import powutil
import time
import queue
import json
import threading
import os
import copy
import random
import math
# import player
from player import Player
from discord.ext import commands
from discord.ext import tasks

#
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.wait_for
# https://stackoverflow.com/questions/49947814/python-threading-error-must-be-an-iterable-not-int
# http://www.fileformat.info/info/unicode/char/search.htm

# with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../storage/tracking.json'))) as json_file:
#     data = json.load(json_file)
# f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../storage/output.txt')), "a+")

class Wop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = False
        self.round = 0
        self.maxRound = 10
        self.timer = 10e22
        self.roundTimer = [0, 21, 18, 15, 13, 11, 10, 9, 8, 7, 6, 6, 5, 5, 5, 4, 4, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2]
        self.minTime = 2
        self.context = None        
        self.trackedPlayers = {}
        self.trackedPlayersPrevious = {}
        self.currentWord = ""
        self.combinations = ""
        self.usedWords = set()
        self.minL, self.maxL = 7, 30

    @commands.Cog.listener()
    async def on_ready(self):
        print('cog.wop successfully loaded!')
        
    @commands.command(aliases=['wop'])
    async def start_wop(self, ctx, *args):
        res = discord.Embed(title="Starting woP!", color=self.generate_random_color())
        res.add_field(name="Rules", inline=False, value="Players have some time per round to type the word I display **backwards**!\n")
        await ctx.send(embed=res)
        
        # self.maxRound = int(args[0]) if (len(args) > 0 and (1 <= int(args[0]) <= 20)) else 10
        
        self.minL = int(args[0]) if len(args) > 0 and 3 <= int(args[0]) <= 7 else 7
        self.maxL = int(args[1]) if len(args) > 1 and 10 <= int(args[1]) <= 50 else 30
        self.game = True
        self.timer = 10e22
        self.context = ctx
        self.trackedPlayers = {}
        await self.wop_on(ctx)

    @commands.command()
    async def stop_wop(self, ctx):
        res = discord.Embed(title="woP! Over!", color=self.generate_random_color())
        await ctx.send(embed=res)
        self.trackedPlayers = {}
        self.round = 0
        self.timer = 10e22
        self.game = False

    async def wop_on(self, ctx):
        self.game = True
        loop = asyncio.get_running_loop()
        if self.game:
            # every round, reset this flag, eliminate players that failed to type the word 
            # self.trackedPlayersPrevious = everyone who survives from previous round
            # make a shallow copy
            self.trackedPlayersPrevious = self.trackedPlayers.copy()
            for player, submitted in list(self.trackedPlayers.items()):
                if not submitted:
                    del self.trackedPlayers[player]
                else: 
                    self.trackedPlayers[player] = False
                
            if self.round >= 2 and len(self.trackedPlayers) == 0:
                res = discord.Embed(title="Winners", description="\n".join([x for x in self.trackedPlayersPrevious.keys()]), color=self.generate_random_color())
                await ctx.send(embed=res)
                await self.stop_wop(ctx)
                return
            # if self.round == self.maxRound:
            #     sortedPlayers = sorted(self.trackedPlayers.items(), key=lambda x: x[1], reverse=True)
            #     res = discord.Embed(title="Leaderboards", description="\n".join([(str(i[0]) + ": " + str(i[1])) for i in sortedPlayers]), color=self.generate_random_color())
            #     await ctx.send(embed=res)
            #     await self.stop_chainage(ctx)
            #     return
            self.round += 1

            spaceInsertedWord, self.currentWord[::-1] = powutil.generate_random_word(self.minL, self.maxL)
            res = discord.Embed(title="woP! Round " + str(self.round), description="You have **" + (str(self.roundTimer[self.round]) if self.round < len(self.roundTimer) else str(self.minTime)) + "** seconds to enter: **" + spaceInsertedWord + "**\n**Remaining players: **\n" + ", ".join([x for x in self.trackedPlayers.keys()]), color=self.generate_random_color())
            await ctx.send(embed=res)
            
            # start the timer ONLY when all of the above are complete
            self.timer = loop.time() + self.roundTimer[self.round] if self.round < len(self.roundTimer) else self.minTime
            
            """
            Logic for timer that recursively calls this function.
            Important for advancing rounds and resetting timer! 
            """
            while self.game:
                if (loop.time()) >= self.timer:
                    res = discord.Embed(title="Round over!", color=self.generate_random_color())
                    self.game = False
                    await ctx.send(embed=res)
                    await self.wop_on(ctx)
                    # self.timer = 10e22
                    break
                await asyncio.sleep(0.5)
            await asyncio.sleep(3)
        else:
            self.timer = 10e22


    # @commands.command(aliases=['c25'])
    # async def chainage_25(self, ctx, arg1, brief="Usage: !chainage_25 <string>", description="Usage: !chainage_25 <string>, returns a list of up to 25 neighboring words of the given word."):
    #     """
    #     Returns a list of up to 25 neighboring words of the given word.
    #     """
    #     res = discord.Embed(title=discord.Embed.Empty, description=", ".join(chainageutil.get_levenshtein_neighbors_possibility(arg1)), color=self.generate_random_color())
    #     await ctx.send(embed=res)

    def generate_random_color(self):
        """
        Returns a value between 0 and 16777215, the max value for int(rgb).
        """
        return random.randint(0, 256**3-1)

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        This method tracks messages sent by users, specific to certain games. 
        """
        if not message.author.bot and self.game:
            channel = message.channel
            word = message.content

            if self.round == 1:
                if word == self.currentWord: 
                    self.trackedPlayers[message.author.name] = True
            else: 
                if word == self.currentWord and message.author.name in self.trackedPlayers: 
                    self.trackedPlayers[message.author.name] = True
            #     await message.add_reaction("✅")

def setup(bot): 
    bot.add_cog(Wop(bot))