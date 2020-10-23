import discord
import asyncio
from discord import Embed
from discord.ext import commands
import util.util as util
import util.triviautil as t

class Trivia():
    def __init__(self, ctx, maxRounds=50):
        # self.bot = ctx.bot
        self.game = False
        self.ctx = ctx
        self.answer = None
        self.question = None
        self.maxRounds = maxRounds
        self.timer = 10e22
        self.roundTimer = 20
        self.leaderboard = {}

    async def run(self):
        self.game = True
        res = discord.Embed(title="Starting Trivia!", description="Players answer my question correctly to get one point! There are " + str(self.maxRounds) + " rounds in this Trivia!\nIf the answer is tricky, I'll let some typos slide (1 per 8 characters and 1 for non-alphanumeric characters)!")
        await self.ctx.send(embed=res)
        await asyncio.sleep(2)
        await self.trivia_on()

    async def trivia_on(self):
        loop = asyncio.get_running_loop()

        self.question, self.answer = t.fetch_question()

        self.timer = loop.time() + self.roundTimer
        while self.game:
            if (loop.time()) >= self.timer:
                res = discord.Embed(title="Round over!", color=util.generate_random_color())
                await self.ctx.send(embed=res)
                await self.trivia_on()
                break
            await asyncio.sleep(1)

    async def handle_on_message(self, message):
        
        if message.author.name not in self.leaderboard:
            self.leaderboard[message.author.name] = 1
        await self.ctx.send(message.content + " reached 'handle_on_message' fn")
