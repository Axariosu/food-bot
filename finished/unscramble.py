import discord
import asyncio
import util.unscrambleutil as unscrambleutil
import util.util as util
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

class Unscramble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = False
        self.round = 0
        self.maxRound = 50
        self.timer = 10e22
        self.mode = 0
        self.roundTimer = 30
        self.context = None        
        self.trackedPlayers = {}
        self.currentWord = ""
        self.combinations = ""
        self.usedWords = set()
        self.guessed = False
        self.minL, self.maxL = 4, 30

    @commands.Cog.listener()
    async def on_ready(self):
        print('cog.unscramble successfully loaded!')
        
    @commands.command(aliases=['unscramble'])
    async def start_unscramble(self, ctx, *args):
        res = discord.Embed(title="Starting Unscramble!", color=util.generate_random_color())
        res.add_field(name="Rules", inline=False, value="Players have some time per round to unscramble the word I display!\nEach correct guess is 1 point.\nUse !scramble (rate limited) to shuffle the current word!\nEach round lasts 30 seconds, if you can't get the word by then, no one gets a point!\nLet's start!")
        await ctx.send(embed=res)
        
        # self.maxRound = int(args[0]) if (len(args) > 0 and (1 <= int(args[0]) <= 20)) else 10
        
        # self.minL = int(args[0]) if len(args) > 0 and 3 <= int(args[0]) <= 7 else 3
        # self.maxL = int(args[1]) if len(args) > 1 and 10 <= int(args[1]) <= 50 else 20
        self.maxRound = int(args[0]) if len(args) > 0 else 50
        self.mode = int(args[1]) if len(args) > 0 else 0
        self.game = True
        self.timer = 10e22
        self.context = ctx
        self.trackedPlayers = {}
        await self.unscramble_on(ctx)

    @commands.command()
    async def stop_unscramble(self, ctx):
        res = discord.Embed(title="Unscramble Over!", color=util.generate_random_color())
        await ctx.send(embed=res)
        self.trackedPlayers = {}
        self.round = 0
        self.timer = 10e22
        self.game = False
        self.currentWord = ""

    async def unscramble_on(self, ctx):
        self.game = True
        self.guessed = False
        loop = asyncio.get_running_loop()
        if self.game:                
            if self.round == self.maxRound:
                sorted_leaderboard = sorted(self.trackedPlayers.items(), key=lambda x: x[1], reverse=True)
                res = discord.Embed(title="Leaderboard", description="\n".join([util.bold(str(k) + ": " + str(v)) for (k, v) in sorted_leaderboard]), color=util.generate_random_color())
                await ctx.send(embed=res)
                await self.stop_unscramble(ctx)
                return
            # if self.round == self.maxRound:
            #     sortedPlayers = sorted(self.trackedPlayers.items(), key=lambda x: x[1], reverse=True)
            #     res = discord.Embed(title="Leaderboards", description="\n".join([(str(i[0]) + ": " + str(i[1])) for i in sortedPlayers]), color=util.generate_random_color())
            #     await ctx.send(embed=res)
            #     await self.stop_chainage(ctx)
            #     return
            self.round += 1

            spaceInsertedWord, self.currentWord = unscrambleutil.generate_random_word_scrambled(self.mode, self.minL, self.maxL)
            res = discord.Embed(title="Unscramble Round " + str(self.round) + " of " + str(self.maxRound), description="You have " + util.bold(str(self.roundTimer)) + " seconds to unscramble: " + util.bold(spaceInsertedWord), color=util.generate_random_color())
            await ctx.send(embed=res)
            
            # start the timer ONLY when all of the above are complete
            self.timer = loop.time() + self.roundTimer
            """
            Logic for timer that recursively calls this function.
            Important for advancing rounds and resetting timer! 
            """
            while self.game:
                if (loop.time()) >= self.timer:
                    res = discord.Embed(title="Round over! The word was: " + self.currentWord, color=util.generate_random_color())
                    self.game = False
                    await ctx.send(embed=res)
                    await asyncio.sleep(1)
                    await self.unscramble_on(ctx)
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
    #     res = discord.Embed(title=None, description=", ".join(chainageutil.get_levenshtein_neighbors_possibility(arg1)), color=util.generate_random_color())
    #     await ctx.send(embed=res)
    @commands.command()
    @commands.cooldown(1, 2, type=commands.BucketType.user)
    async def scramble(self, ctx):
        if self.currentWord != "" and self.game:
            res = discord.Embed(title=unscrambleutil.scramble(self.currentWord), color=util.generate_random_color())
            await ctx.send(embed=res)

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        This method tracks messages sent by users, specific to certain games. 
        """
        if not message.author.bot and self.game and not self.guessed:
            channel = message.channel
            word = message.content
            # if self.round == 1:
            if word == self.currentWord: 
                if message.author.name not in self.trackedPlayers: 
                    self.trackedPlayers[message.author.name] = 1
                else: 
                    self.trackedPlayers[message.author.name] += 1
                await message.add_reaction("✅")
                self.guessed = True
                self.timer = 0


def setup(bot): 
    bot.add_cog(Unscramble(bot))