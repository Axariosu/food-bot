import discord
import asyncio
from discord import Embed
from discord.ext import commands
import util.util as util
import util.triviautil as triviautil
import util.unscrambleutil as unscrambleutil

class Scrambivia():
    def __init__(self, ctx, maxRound=50):
        # self.bot = ctx.bot
        self.game = False
        self.ctx = ctx
        self.answer = None
        self.question = None
        self.maxRound = maxRound
        self.round = 0
        self.timer = 1e22
        self.roundTimer = 10
        self.trackedPlayers = {}
        self.accepting_answers = False

    async def start(self):
        self.game = True
        res = discord.Embed(title="Starting Scrambivia!", description="Players answer my question correctly to get one point! There are " + str(self.maxRound) + " rounds in this Scrambivia!\nI'll display the answer randomly scrambled, use !scramble to shuffle the answer!\nIf the answer is tricky, I'll let some typos slide (1 per 8 characters and 1 for non-alphanumeric characters)!", color=util.generate_random_color())
        await self.ctx.send(embed=res)
        await asyncio.sleep(10)
        await self.scrambivia_loop()

    async def scrambivia_loop(self):
        if self.game:
            loop = asyncio.get_running_loop()
            self.round += 1
            if (self.round > self.maxRound):
                await self.stop()
                return

            self.question, self.answer = triviautil.fetch_question()
            self.accepting_answers = True

            res = discord.Embed(title="Scrambivia Round " + str(self.round) + " of " + str(self.maxRound), description=util.insert_zero_width_space(self.question) + "\nAnswer: \"" + util.bold(unscrambleutil.scramble(self.answer)) + "\"", color=util.generate_random_color())
            
            await self.ctx.send(embed=res)

            self.timer = loop.time() + self.roundTimer
            while self.game:
                if (loop.time()) >= self.timer:
                    self.accepting_answers = False
                    res = discord.Embed(title="Round over!", description="The answer was: " + util.bold(str(self.answer)), color=util.generate_random_color())
                    
                    await self.ctx.send(embed=res)
                    await asyncio.sleep(2)
                    await self.scrambivia_loop()
                    break
                await asyncio.sleep(1)

    async def stop(self):
        sorted_leaderboard = sorted(self.trackedPlayers.items(), key=lambda x: x[1], reverse=True)
        res = discord.Embed(title="Leaderboard", description="\n".join([str(k) + ": " + str(v) for (k, v) in sorted_leaderboard]), color=util.generate_random_color())
        await self.ctx.send(embed=res)
        self.round = 0
        self.game = False
        self.accepting_answers = False
        self.trackedPlayers = {}
        res = discord.Embed(title="Scrambivia Over!")
        await self.ctx.send(embed=res)
        # if stop is called, pop the guild id! 
        self.ctx.bot.games.pop(self.ctx.guild.id)

    async def handle_on_message(self, message):
        if self.accepting_answers:
            if triviautil.valid_guess(message.content, self.answer):
                self.accepting_answers = False
                if message.author.name not in self.trackedPlayers:
                    self.trackedPlayers[message.author.name] = 1
                else: 
                    self.trackedPlayers[message.author.name] += 1
                await message.add_reaction('✅')
                self.timer = 0
            if message.content == '!scramble':
                res = discord.Embed(title=unscrambleutil.scramble(self.answer), color=util.generate_random_color())
                await self.ctx.send(embed=res)

