import discord
import asyncio
from discord import Embed
from discord.ext import commands
import util.util as util
import util.triviautil as triviautil

class Trivia():
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
        res = discord.Embed(title="Starting Trivia!", description="Players answer my question correctly to get one point! There are " + str(self.maxRound) + " rounds in this Trivia!\nIf the answer is tricky, I'll let some typos slide (1 per 8 characters and 1 for non-alphanumeric characters)!")
        await self.ctx.send(embed=res)
        await asyncio.sleep(2)
        await self.trivia_loop()

    async def trivia_loop(self):
        loop = asyncio.get_running_loop()

        self.round += 1
        
        if (self.round > self.maxRound):
            await self.trivia_off()
            return

        self.question, self.answer = triviautil.fetch_question()
        # print(self.question, self.answer)
        self.accepting_answers = True

        res = discord.Embed(title="Trivia Round " + str(self.round) + " of " + str(self.maxRound), description=util.bold(util.insert_zero_width_space(self.question)), color=util.generate_random_color())
        await self.ctx.send(embed=res)

        self.timer = loop.time() + self.roundTimer
        while self.game:
            if (loop.time()) >= self.timer:
                res = discord.Embed(title="Round over! The answer was " + str(self.answer), color=util.generate_random_color())
                
                await self.ctx.send(embed=res)
                await asyncio.sleep(2)
                await self.trivia_loop()
                break
            await asyncio.sleep(1)

    async def stop(self):
        sorted_leaderboard = sorted(self.trackedPlayers.items(), key=lambda x: x[1], reverse=True)
        res = discord.Embed(title="Leaderboard", description="\n".join([util.bold(str(k) + ": " + str(v)) for (k, v) in self.trackedPlayers.items()]), color=util.generate_random_color())
        await self.ctx.send(embed=res)
        self.round = 0
        self.game = False
        self.accepting_answers = False
        self.trackedPlayers = {}
        res = discord.Embed(title="Trivia Over!")
        await self.ctx.send(embed=res)
        
    async def handle_on_message(self, message):
        if triviautil.valid_guess(message.content, self.answer) and self.accepting_answers:
            self.accepting_answers = False
            if message.author.name not in self.trackedPlayers:
                self.trackedPlayers[message.author.name] = 1
            else: 
                self.trackedPlayers[message.author.name] += 1
            await message.add_reaction('✅')
            self.timer = 0
