import discord
from discord.ext import commands

class Game:
    
    def __init__(self, some_state: int):
        self.some_state = some_state
        self.context = None

    def change_state(self, some_state: int):
        self.some_state = some_state

    async def sendMessage(self, ctx):
        await ctx.send("hi")

