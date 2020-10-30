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

    async def start(self):
        await asyncio.sleep(self.delay)
        await self.template_loop()

    async def template_loop(self):
        self.round += 1
        loop = asyncio.get_running_loop()
        
        # round over logic

        # current round logic

        self.timer = loop.time() + self.roundTime
        while True:
            if loop.time() >= self.timer:
                res = discord.Embed(title="Round Over!")
                await self.ctx.send(embed=res)
                break
            await asyncio.sleep(0.5) 

    async def stop(self):
        self.ctx.bot.games.pop(self.ctx.guild.id)

    async def handle_on_message(self, message):
        pass

    async def handle_on_reaction_add(self, reaction, user):
        pass

    async def handle_on_reaction_remove(self, reaction, user):
        pass