import discord
import asyncio
import util.alphafuseutil as alphafuseutil
import util.util as util
import time
import queue
import json
import threading
import os
import copy
import random
from discord.ext import commands
from discord.ext import tasks

#
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.wait_for
# https://stackoverflow.com/questions/49947814/python-threading-error-must-be-an-iterable-not-int
# http://www.fileformat.info/info/unicode/char/search.htm

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../storage/tracking.json'))) as json_file:
    data = json.load(json_file)
f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../storage/output.txt')), "a+")

class AlphaFuse():
    def __init__(self, ctx):
        self.ctx = ctx
        self.game = False
        self.round = 0
        self.timer = 1e22
        self.gameMode = 0
        self.currentLetters = []
        self.minTime = 10
        self.factor = 0.9
        self.roundTimer = 30
        self.letters = [0, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7]
        self.trackedPlayers = {}
        self.trackedPlayersPrevious = {}
        self.usedWords = {}
        self.combinations = 0
        self.maxLetters = 8
        self.defaultLifeCount = 3
        self.sleep = 1
        self.acceptingAnswers = False

    async def start(self):
        res = discord.Embed(title="Starting Alpha Fuse!", color=util.generate_random_color())
        res.add_field(name="Rules", inline=False, value="Players have some time per round to find a word that contains the displayed letters.\nIf you repeat a word someone else used, you lose a life!\nIf you repeat your own word, there's no penalty.")
        await self.ctx.send(embed=res)
        self.game = True
        await asyncio.sleep(5)
        res = discord.Embed(title="Let's begin!")
        await self.ctx.send(embed=res)
        await self.alpha_loop()

    async def stop(self):
        res = discord.Embed(title="Stopping Alpha Fuse!", color=util.generate_random_color())
        await self.ctx.send(embed=res)
        self.usedWords = {}
        self.trackedPlayers = {}
        self.round = 0
        self.timer = 10e22
        self.game = False
        self.ctx.bot.games.pop(self.ctx.guild.id)

    async def alpha_loop(self):
        if self.game:
            # need a submission every round, so we can check that here: 
            loop = asyncio.get_running_loop()
            self.round += 1
            if self.round >= 2:
                if self.round >= 4 and len(self.trackedPlayers) == 0: 
                    await self.ctx.send("No one joined!")
                    await self.stop()
                    return
                self.trackedPlayersPrevious = self.trackedPlayers.copy()
                for k, v in list(self.trackedPlayers.items()):
                    # v is a list of [lives, submitted_previous]
                    lives, submitted_previous = v
                    if not submitted_previous:
                        self.trackedPlayers[k][0] -= 1
                    self.trackedPlayers[k][1] = False
                    if self.trackedPlayers[k][0] == 0:
                        del self.trackedPlayers[k]
                
                if len(self.trackedPlayers) == 0:
                    res = discord.Embed(title="Winners", description="\n".join([x for x in self.trackedPlayersPrevious.keys()]), color=util.generate_random_color())
                    await self.ctx.send(embed=res)
                    await self.stop()
                    loop.close()
                    return

            if self.gameMode == 0:
                self.currentLetters = alphafuseutil.generate_random_string_of_length_unbiased(self.letters[self.round] if self.round < len(self.letters) - 1 else self.maxLetters)
            else: 
                self.currentLetters = alphafuseutil.generate_random_string_of_length_biased(self.letters[self.round] if self.round < len(self.letters) - 1 else self.maxLetters)
            self.combinations = alphafuseutil.combinations(self.currentLetters)
            
            
            
            res = discord.Embed(title="Alpha Fuse Round " + str(self.round), color=util.generate_random_color())
            if self.round == 1:
                res.add_field(name='\u200b', inline=False, value="You have " + util.bold(self.roundTimer) + " second(s) to find a word! Good luck!")
                res.add_field(name='\u200b', inline=False, value="\nEnter a word containing the letter(s): " + util.bold(", ".join([x.upper() for x in self.currentLetters])))
                res.add_field(name='\u200b', inline=False, value="\nValid combinations: " + util.bold(self.combinations))
            else: 
                res.add_field(name='\u200b', inline=False, value="You have " + util.bold(self.roundTimer) + " second(s) to find a word! Good luck!")
                res.add_field(name='\u200b', inline=False, value="\nEnter a word containing the letter(s): " + util.bold(", ".join([x.upper() for x in self.currentLetters])))
                res.add_field(name='\u200b', inline=False, value="\nValid combinations: " + util.bold(self.combinations))
                res.add_field(name='\u200b', inline=False, value="\nRemaining players: " + ", ".join(list([util.bold(str(x)) + ": " + str(y[0]) + " lives" if y[0] > 1 else util.bold(str(x)) + ": " + str(y[0]) + " life" for (x,y) in self.trackedPlayers.items()])))
            
            await self.ctx.send(embed=res)
            self.acceptingAnswers = True
            
            # make timer last for the designated round
            
            if self.round != 1:
                self.roundTimer = round(self.roundTimer * self.factor, 2) if round(self.roundTimer * self.factor, 2) > self.minTime else self.minTime
            self.timer = loop.time() + self.roundTimer
            """
            Logic for timer that recursively calls this function.
            Important for advancing rounds and resetting timer! 
            """
            while self.game:
                if (loop.time()) >= self.timer:
                    res = discord.Embed(title="Round over!", color=util.generate_random_color())
                    await self.ctx.send(embed=res)
                    self.acceptingAnswers = False
                    await asyncio.sleep(2)
                    await self.alpha_loop()
                    break
                await asyncio.sleep(1)

    async def handle_on_message(self, message):
        channel = message.channel
        word = message.content.lower()
        if alphafuseutil.check_valid(self.currentLetters, word) and self.acceptingAnswers:
            if message.author.name in self.trackedPlayers:
                if word in self.usedWords.keys():
                    await message.add_reaction('❌')
                    user, rnd = self.usedWords[word]
                    if message.author.name == user:
                        await channel.send("What " + user + "? You already used this word in round " + util.bold(rnd) + "! Use another word! (no penalty)")
                    else: 
                        self.trackedPlayers[message.author.name][0] -= 1
                        self.trackedPlayers[message.author.name][1] = True
                        await channel.send("Unlucky, " + util.bold(word) + " was already used by " + util.bold(user) + " on round " + util.bold(rnd) + "! (-1 life)")
                else: 
                    await message.add_reaction('✅')
                    self.usedWords[word] = [message.author.name, self.round]
                    self.trackedPlayers[message.author.name][1] = True
            else: 
                if 1 <= self.round <= 3:
                    if word in self.usedWords.keys():
                        await message.add_reaction('❌')
                        user, rnd = self.usedWords[word]
                        self.trackedPlayers[message.author.name] = [self.defaultLifeCount - self.round + 1, True]
                        self.trackedPlayers[message.author.name][0] -= 1
                        await channel.send("Unlucky, " + util.bold(word) + " was already used by " + util.bold(user) + " on round " + util.bold(rnd) + "! (-1 life)")
                    else: 
                        await message.add_reaction('✅')
                        self.usedWords[word] = [message.author.name, self.round]
                        self.trackedPlayers[message.author.name] = [self.defaultLifeCount - self.round + 1, True]

        