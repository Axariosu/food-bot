import discord
import asyncio
import util.triviautil as triviautil
import util.powutil as powutil
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

class PowRacer():
    def __init__(self, ctx, similarity, wordCount, l, h):
        self.ctx = ctx
        self.game = False
        self.timer = 1e22
        self.similarity = similarity
        self.wordCount = wordCount
        self.minL = l
        self.maxL = h
        self.timePerWord = 2
        self.trackedPlayers = {}
        self.brokenText = ""
        self.text = ""
        self.startTime = 0
        self.delayTime = 10

    async def start(self):
        res = discord.Embed(title="Starting PowRacer!", color=util.generate_random_color())
        res.add_field(name="Rules", inline=False, value="Players have some time per round to type my randomly generated words!\nThere are " + util.bold(self.delayTime) + " seconds before it starts!\nI'll accept your message if it's at least " + util.bold(self.similarity) + "% similar!")
        await self.ctx.send(embed=res)
        await asyncio.sleep(self.delayTime)
        res = discord.Embed(title="Let's begin!")
        self.brokenText, self.text = await powutil.generate_k_random_words(self.minL, self.maxL, self.wordCount)
        await self.ctx.send(embed=res)
        await self.powracer_loop()

    async def stop(self):
        self.game = False
        sorted_leaderboard = sorted(self.trackedPlayers.items(), key=lambda x: x[1], reverse=True)
        res = discord.Embed(title="Leaderboard", description="\n".join((util.bold(k) + " WPM: " + util.bold(v[0]) + ", Similarity: " + util.bold(v[1]) + "%, Typos: " + util.bold(v[2])) for (k, v) in sorted_leaderboard), color=util.generate_random_color())
        await self.ctx.send(embed=res)
        res = discord.Embed(title="Stopping PowRacer!", color=util.generate_random_color())
        await self.ctx.send(embed=res)
        self.usedWords = {}
        self.trackedPlayers = {}
        self.timer = 1e22
        self.ctx.bot.games.pop(self.ctx.guild.id)

    async def powracer_loop(self):
        self.game = True
        loop = asyncio.get_running_loop()

        if self.game:
            res = discord.Embed(title="Type the words below as quickly as possible!", description=self.brokenText + "\n\nYou have " + util.bold(self.wordCount * self.timePerWord) + " seconds!")
            await self.ctx.send(embed=res)
            self.startTime = loop.time()
            self.timer = loop.time() + self.wordCount * self.timePerWord
            """
            Logic for timer that recursively calls this function.
            Important for advancing rounds and resetting timer! 
            """
            while self.game:
                if (loop.time()) >= self.timer:
                    res = discord.Embed(title="PowRacer over!", color=util.generate_random_color())
                    await self.ctx.send(embed=res)
                    await asyncio.sleep(2)
                    await self.stop()
                    break
                await asyncio.sleep(1)

    async def handle_on_message(self, message):
        if self.game:
            channel = message.channel
            submission = message.content.lower()
            lehvensteinDistance = triviautil.lehvenstein_distance(submission, self.text)
            submissionSimilarity = (len(self.text) - lehvensteinDistance) / len(self.text) * 100
            print(lehvensteinDistance, submissionSimilarity)
            if submissionSimilarity > self.similarity:
                await message.add_reaction('✅')
                wpm = round((len(self.text) / 5) / (asyncio.get_running_loop().time() - self.startTime) * 60, 3)
                sim = round(submissionSimilarity, 3)
                typos = round(lehvensteinDistance)
                self.trackedPlayers[message.author.name] = [wpm, sim, typos]

    async def handle_on_reaction_add(self, reaction, user):
        pass

    async def handle_on_reaction_remove(self, reaction, user):
        pass