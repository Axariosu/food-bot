import discord
import asyncio
import util.powutil as powutil
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

class Pow():
    def __init__(self, ctx):
        self.ctx = ctx
        self.game = False
        self.round = 0
        self.maxRound = 10
        self.timer = 10e22
        self.factor = 0.9
        self.minTime = 2
        self.roundTimer = 30
        self.trackedPlayers = {}
        self.trackedPlayersPrevious = {}
        self.currentWord = ""
        self.combinations = ""
        self.minL, self.maxL = 7, 30
        
    async def start(self):
        res = discord.Embed(title="Starting Pow!", color=util.generate_random_color())
        res.add_field(name="Rules", inline=False, value="Players have some time per round to type the word I display!\n")
        await self.ctx.send(embed=res)
        # self.minL = int(args[0]) if len(args) > 0 and 3 <= int(args[0]) <= 7 else 7
        # self.maxL = int(args[1]) if len(args) > 1 and 10 <= int(args[1]) <= 50 else 30
        self.game = True
        self.timer = 1e22
        self.trackedPlayers = {}
        await asyncio.sleep(5)
        res = discord.Embed(title="Let's start!")
        await self.ctx.send(embed=res)
        await self.pow_loop()

    async def stop(self):
        res = discord.Embed(title="Pow! Over!", color=util.generate_random_color())
        await self.ctx.send(embed=res)
        self.trackedPlayers = {}
        self.round = 0
        self.timer = 10e22
        self.game = False
        self.ctx.bot.games.pop(self.ctx.guild.id)

    async def pow_loop(self):
        self.game = True
        loop = asyncio.get_running_loop()
        self.round += 1
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
                res = discord.Embed(title="Winners", description="\n".join([x for x in self.trackedPlayersPrevious.keys()]), color=util.generate_random_color())
                await self.ctx.send(embed=res)
                await self.stop()
                return

            spaceInsertedWord, self.currentWord = powutil.generate_random_word(self.minL, self.maxL)
            
            # start the timer ONLY when all of the above are complete
            if self.round != 1:
                self.roundTimer = round(self.roundTimer * self.factor, 2) if round(self.roundTimer * self.factor, 2) > self.minTime else self.minTime

            res = discord.Embed(title="Pow! Round " + str(self.round), description="You have " + util.bold(self.roundTimer) + " seconds to enter: " + util.bold(spaceInsertedWord) + "\nRemaining players: \n" + ", ".join([x for x in self.trackedPlayers.keys()]), color=util.generate_random_color())
            await self.ctx.send(embed=res)
            self.timer = loop.time() + self.roundTimer

            """
            Logic for timer that recursively calls this function.
            Important for advancing rounds and resetting timer! 
            """
            while self.game:
                if (loop.time()) >= self.timer:
                    res = discord.Embed(title="Round over!", color=util.generate_random_color())
                    self.game = False
                    await self.ctx.send(embed=res)
                    await asyncio.sleep(2)
                    await self.pow_loop()
                    break
                await asyncio.sleep(0.5)

    async def handle_on_message(self, message):
        """
        This method tracks messages sent by users, specific to certain games. 
        """
        if self.game:
            channel = message.channel
            word = message.content
            if self.round == 1:
                if word == self.currentWord: 
                    self.trackedPlayers[message.author.name] = True
            else: 
                if word == self.currentWord and message.author.name in self.trackedPlayers: 
                    self.trackedPlayers[message.author.name] = True
