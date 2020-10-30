import discord
import asyncio
import util.wooshutil as wooshutil
import util.util as util
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

class Schwootsh():
    def __init__(self, ctx):
        self.ctx = ctx
        self.game = False
        self.round = 0
        self.maxRound = 10
        self.timer = 10e22
        self.roundTimer = 10
        self.context = None        
        self.trackedPlayers = {}
        self.currentWord = ""
        self.combinations = ""
        self.usedWords = set()

    async def start(self):
        res = discord.Embed(title="Starting Schwootsh!", color=util.generate_random_color())
        res.add_field(name="Rules", inline=False, value="Players have some time per round to find a word that **neighbors** the current word.\nA neighboring word differs by at most 1 character, or has one more or less character than the previous word.\nIf no one can find a word which chains off the previous, I'll end the round and start a new one!")
        await self.ctx.send(embed=res)
        self.game = True
        self.timer = 1e22
        self.trackedPlayers = {}
        await asyncio.sleep(5)
        res = discord.Embed(title="Let's begin!")
        await self.ctx.send(embed=res)
        await self.schwootsh_loop()

    async def stop(self):
        sortedPlayers = sorted(self.trackedPlayers.items(), key=lambda x: x[1], reverse=True)
        res = discord.Embed(title="Leaderboards", description="\n".join([(str(i[0]) + ": " + str(i[1])) for i in sortedPlayers]), color=util.generate_random_color())
        await self.ctx.send(embed=res)        
        res = discord.Embed(title="Schwootsh Over!", color=util.generate_random_color())
        await self.ctx.send(embed=res)
        self.trackedPlayers = {}
        self.round = 0
        self.timer = 10e22
        self.game = False
        self.ctx.bot.games.pop(self.ctx.guild.id)

    async def schwootsh_loop(self):
        loop = asyncio.get_running_loop()
        self.round += 1
        if self.game:
            if self.round > self.maxRound:
                await self.stop()
                return

            self.currentWord = wooshutil.generate_random_start()
            res = discord.Embed(title="Schwootsh Round " + str(self.round) + "/" + str(self.maxRound), description="Type in neighboring words to my word: " + util.bold(self.currentWord.upper()), color=util.generate_random_color())
            await self.ctx.send(embed=res)
            self.usedWords = set()
            self.usedWords.add(self.currentWord)
            self.timer = loop.time() + self.roundTimer
            
            """
            Logic for timer that recursively calls this function.
            Important for advancing rounds and resetting timer! 
            """
            while self.game:
                if (loop.time()) >= self.timer:
                    res = discord.Embed(title="Round over!", color=util.generate_random_color())
                    await self.ctx.send(embed=res)
                    await self.schwootsh_loop()
                    break
                await asyncio.sleep(1)

    async def schwootsh_25(self, arg1):
        """
        Returns a list of up to 25 neighboring words of the given word.
        """
        res = discord.Embed(title=discord.Embed.Empty, description=", ".join(wooshutil.get_levenshtein_neighbors_possibility(arg1)), color=util.generate_random_color())
        await self.ctx.send(embed=res)

    async def handle_on_message(self, message):
        """
        This method tracks messages sent by users, specific to certain games. 
        """
        if not message.author.bot and self.game:
            channel = message.channel
            word = message.content
            if wooshutil.levenshtein_1(self.currentWord, word) and word not in self.usedWords:
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
