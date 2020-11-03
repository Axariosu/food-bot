import util.util as util
import discord
import asyncio

class TemplateGame():
    def __init__(self, ctx, maxRound):
        self.ctx = ctx
        self.timer = 0
        self.roundTime = 5
        self.round = 0
        self.maxRound = maxRound
        self.delay = 10
        self.trackedPlayers = {}

    def __del__(self):
        pass

    async def start(self):
        await asyncio.sleep(self.delay)
        await self.template_loop()

    async def template_loop(self):
        loop = asyncio.get_running_loop()

        self.round += 1
        if (self.round > self.maxRound):
            await self.stop()
            return
        
        # round over logic
        # current round logic

        self.timer = loop.time() + self.roundTime
        while True:
            if loop.time() >= self.timer:
                res = discord.Embed(title="Round Over!")
                await self.ctx.send(embed=res)
                await asyncio.sleep(2)
                await self.template_loop() # TODO: CHANGE THIS FN NAME
                break
            await asyncio.sleep(0.5) 

    async def stop(self):
        sortedPlayers = sorted(self.trackedPlayers.items(), key=lambda x: x[1], reverse=True)
        res = discord.Embed(title="Leaderboards", description="\n".join([(str(i[0]) + ": " + str(i[1])) for i in sortedPlayers]), color=util.generate_random_color())
        await self.ctx.send(embed=res)        
        res = discord.Embed(title="Template Over!", color=util.generate_random_color())
        await self.ctx.send(embed=res)
        self.ctx.bot.games.pop(self.ctx.guild.id)

    async def handle_on_message(self, message):
        pass

    async def handle_on_reaction_add(self, reaction, user):
        pass

    async def handle_on_reaction_remove(self, reaction, user):
        pass