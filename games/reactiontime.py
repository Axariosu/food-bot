import util.util as util
import util.reactiontimeutil as rtu
import discord
import asyncio

class ReactionTime():
    def __init__(self, ctx, maxRounds, minTime, maxTime, delay):
        self.ctx = ctx
        self.maxRounds = maxRounds
        self.minTime = minTime
        self.maxTime = maxTime
        self.round = 0
        self.delay = delay
        self.trackedPlayers = {}
        self.cannotAnswer = []
        self.currentRoundMessage = None
        self.acceptingAnswer = False
    
    def __del__(self):
        print("bye!")

    async def start(self):
        res = discord.Embed(title="Reaction Time", description="A reaction game (or, maybe ping diff) for you!", color=util.generate_random_color())
        res.add_field(name="Rules", value="Type anything in chat to get a point, but only after my message changes!\nIf you type too early, you won't be able to get the points for the round!")
        res.add_field(name="Time Control", value="There are " + util.bold(self.maxRounds) + " in this game!\nMy messages will change between " + util.bold(self.minTime) + " and " + util.bold(self.maxTime) + "!")
        res.add_field(name="\u200b", value="The game begins in " + util.bold(self.delay) + " seconds!")
        await self.ctx.send(embed=res)
        await asyncio.sleep(self.delay)
        res = discord.Embed(title="Let's begin!")
        await self.ctx.send(embed=res)
        await self.reaction_loop()

    async def reaction_loop(self):
        loop = asyncio.get_running_loop()
        self.acceptingAnswer = True

    async def stop(self):
        self.ctx.bot.games.pop(self.ctx.guild.id)

    async def handle_on_message(self, message):
        pass
    async def handle_on_reaction_add(self, reaction, user):
        pass
    async def handle_on_reaction_remove(self, reaction, user):
        pass