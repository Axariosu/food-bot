import discord
import asyncio
from discord import Embed
from discord.ext import commands
import util.util as util
import util.powutil as powutil
import util.triviautil as triviautil
import util.unscrambleutil as unscrambleutil

class jsTrivia():
    def __init__(self, ctx, maxRound, similarity, scramble):
        # self.bot = ctx.bot
        self.ctx = ctx
        self.maxRound = maxRound
        self.similarity = similarity
        self.scramble = scramble
        self.game = False
        self.answer = None
        self.question = None
        self.round = 0
        self.timer = 1e22
        self.roundTimer = 15
        self.trackedPlayers = {}
        self.accepting_answers = False
        self.questionList = []

    async def start(self):
        self.game = True
        res = discord.Embed(title="Starting jsTrivia!", description="Players answer my question correctly to get one point! There are " + str(self.maxRound) + " rounds in this Trivia!\nI'll give you the point as long as your answer is >=" + util.bold(self.similarity) + "% similar!", color=util.generate_random_color())
        await self.ctx.send(embed=res)
        self.questionList = triviautil.fetch_questions_jservice()
        await asyncio.sleep(5)
        
        if len(self.questionList) == 0:
            await self.ctx.send("Unable to load questions, sorry!")
            await self.stop()
            return
            
        res = discord.Embed(title="Let's begin!")
        await self.ctx.send(embed=res)
        await self.trivia_loop()

    async def trivia_loop(self):
        if self.game:
            loop = asyncio.get_running_loop()

            self.round += 1
            
            if (self.round > self.maxRound):
                await self.stop()
                return

            self.question, self.answer = powutil.insert_zero_width_space(self.questionList[self.round - 1]["question"]), self.questionList[self.round - 1]["answer"].lower().replace("<i>", "").replace("</i>", "")
            if self.answer.startswith("the "):
                self.answer = self.answer[4:]
            if self.answer.startswith("an "):
                self.answer = self.answer[3:]
            if self.answer.startswith("a "):
                self.answer = self.answer[2:]

            self.accepting_answers = True
            
            
            desc = util.insert_zero_width_space(self.question)
            if self.scramble:
                desc += "\nUnscramble: \"" + util.bold(unscrambleutil.scramble(self.answer)) + "\""
            res = discord.Embed(title="jsTrivia Round " + str(self.round) + " of " + str(self.maxRound), description=desc, color=util.generate_random_color())
            await self.ctx.send(embed=res)

            self.timer = loop.time() + self.roundTimer
            while self.game:
                if (loop.time()) >= self.timer:
                    self.accepting_answers = False
                    res = discord.Embed(title="Round over!", description="The answer was: " + util.bold(str(self.answer)), color=util.generate_random_color())
                    
                    await self.ctx.send(embed=res)
                    await asyncio.sleep(2)
                    await self.trivia_loop()
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
        self.questionList = []
        res = discord.Embed(title="jsTrivia Over!")
        await self.ctx.send(embed=res)
        # if stop is called, pop the guild id! 
        self.ctx.bot.games.pop(self.ctx.guild.id)

    async def handle_on_message(self, message):
        if triviautil.valid_guess(message.content.lower(), self.answer, self.similarity) and self.accepting_answers:
            self.accepting_answers = False
            if message.author.name not in self.trackedPlayers:
                self.trackedPlayers[message.author.name] = 1
            else: 
                self.trackedPlayers[message.author.name] += 1
            await message.add_reaction('✅')
            self.timer = 0
        if message.content == "!scramble" and self.scramble and self.accepting_answers:
            res = discord.Embed(title=unscrambleutil.scramble(self.answer))
            await message.channel.send(embed=res)