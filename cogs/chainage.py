import discord
import asyncio
import chainageutil
import time
import queue
import json
import threading
import os
import copy
import random
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
    

class Chainage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = False
        self.round = 0
        self.maxRound = 10
        # self.index = 0
        self.timer = 10e22
        self.roundTimer = 10
        self.context = None        
        # self.gameMode = 0
        # self.currentLetters = []
        # self.seconds = [30, 20, 16, 13, 10]
        # self.minTime = 10
        # self.letters = [0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 9, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16, 16, 17, 17, 17, 17, 18, 18, 18, 18, 19, 19, 19, 19]
        self.trackedPlayers = {}
        # self.winner = []
        # self.eliminatedPlayers = []
        self.currentWord = ""
        self.combinations = ""
        self.usedWords = set()
        
        # self.maxLetters = 20
        # self.defaultLifeCount = 3


    @commands.Cog.listener()
    async def on_ready(self):
        print('cog.chainage successfully loaded!')
        
    @commands.command(aliases=['chainage', 'chain'])
    async def start_chainage(self, ctx, *args):
        res = discord.Embed(title="Starting Chainage!", color=self.generate_random_color())
        res.add_field(name="Rules", inline=False, value="Players have some time per round to find a word that **neighbors** the current word.\nA neighboring word differs by at most 1 character, or has one more or less character than the previous word.\nIf no one can find a word which chains off the previous, I'll end the round and start a new one!")
        await ctx.send(embed=res)
        
        self.maxRound = int(args[0]) if (len(args) > 0 and (1 <= int(args[0]) <= 20)) else 10
        self.game = True
        self.timer = 10e22
        self.context = ctx
        self.trackedPlayers = {}
        await self.chainage_on(ctx)

    @commands.command()
    async def stop_chainage(self, ctx):
        res = discord.Embed(title="Chainage Over!", color=self.generate_random_color())
        await ctx.send(embed=res)
        self.trackedPlayers = {}
        self.round = 0
        self.timer = 10e22
        self.game = False

    async def chainage_on(self, ctx):

        loop = asyncio.get_running_loop()
        if self.game:
            if self.round == self.maxRound:
                sortedPlayers = sorted(self.trackedPlayers.items(), key=lambda x: x[1], reverse=True)
                res = discord.Embed(title="Leaderboards", description="\n".join([(str(i[0]) + ": " + str(i[1])) for i in sortedPlayers]), color=self.generate_random_color())
                await ctx.send(embed=res)
                await self.stop_chainage(ctx)
                return
            self.round += 1

            self.currentWord = chainageutil.generate_random_start()
            res = discord.Embed(title="Chainage Round " + str(self.round) + "/" + str(self.maxRound), description="Type in neighboring words to my word: **" + self.currentWord.upper() + "**", color=self.generate_random_color())
            await ctx.send(embed=res)
            self.usedWords = set()
            self.usedWords.add(self.currentWord)
            self.timer = loop.time() + self.roundTimer
            
            """
            Logic for timer that recursively calls this function.
            Important for advancing rounds and resetting timer! 
            """
            while self.game:
                if (loop.time()) >= self.timer:
                    res = discord.Embed(title="Round over!", color=self.generate_random_color())
                    await ctx.send(embed=res)
                    await self.chainage_on(ctx)
                    break
                await asyncio.sleep(1)
        else:
            self.timer = 10e22


    @commands.command(aliases=['c25'])
    async def chainage_25(self, ctx, arg1, brief="Usage: !chainage_25 <string>", description="Usage: !chainage_25 <string>, returns a list of up to 25 neighboring words of the given word."):
        """
        Returns a list of up to 25 neighboring words of the given word.
        """
        res = discord.Embed(title=discord.Embed.Empty, description=", ".join(chainageutil.get_levenshtein_neighbors_possibility(arg1)), color=self.generate_random_color())
        # res.add_field(name='\u200b', inline=False, value=", ".join(alphafuseutil.get_many_possibilities(arg1)))
        await ctx.send(embed=res)

    def generate_random_color(self):
        """
        Returns a value between 0 and 16777215, the max value for int(rgb).
        """
        return random.randint(0, 256**3-1)

    # @commands.command()
    # async def omega_poss(self, ctx, arg1, brief="Usage: !omega_poss <string>", description="Usage: !omega_poss <strings>, returns the number of valid possibilities for the given character combination."):
    #     """
    #     Returns the number of valid combinations for the given letter combination.
    #     """
    #     res = discord.Embed(title=alphafuseutil.combinations(arg1), color=self.generate_random_color())
    #     await ctx.send(embed=res)

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        This method tracks messages sent by users, specific to certain games. 
        """
        if not message.author.bot and self.game:
            channel = message.channel
            word = message.content
            if chainageutil.levenshtein_1(self.currentWord, word) and word not in self.usedWords:
                loop = asyncio.get_running_loop()
                self.timer = loop.time() + self.roundTimer
                # keeps track of score
                self.usedWords.add(word)
                self.currentWord = word

                if message.author.name not in self.trackedPlayers:
                    self.trackedPlayers[message.author.name] = 1
                else:
                    self.trackedPlayers[message.author.name] += 1

                await message.add_reaction("✅")

def setup(bot): 
    bot.add_cog(Chainage(bot))
