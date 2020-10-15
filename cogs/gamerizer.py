import discord
import asyncio
import util.gamequeueutil as gamequeueutil
import util.util as util
import time
import queue
import json
import threading
import os
import copy
import random
import math
from discord.ext import commands
from discord.ext import tasks


class Gamerizer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = queue.deque()
        self.current_game = None
        self.context = None
        self.game = False
        self.sleep = 3
        self.round = 0
        self.games = 0
    
    @commands.command()
    async def gamerizer_on(self, ctx):
        if not self.queue: 
            await self.stop_gamerizer(ctx)
            return
        else: 
            self.current_game = self.queue.popleft() 
            self.round += 1
            res = discord.Embed(title="Game " + str(self.round) + " of " + str(self.games) + ": " + str(self.current_game), color=util.generate_random_color())
            await ctx.send(embed=res)
            await asyncio.sleep(self.sleep)

            current_cog = self.bot.get_cog(self.current_game)
            command_to_invoke = [x.name for x in current_cog.get_commands() if x.name.startswith("start_")][0]

            await ctx.invoke(self.bot.get_command(command_to_invoke))
            await self.gamerizer_on(ctx)

    @commands.command(aliases=['gamerizer', 'gamer'])
    async def start_gamerizer(self, ctx, *args): 
        self.game = True
        self.context = ctx
        cogs = list(self.bot.cogs)
        self.games = 5 if len(args) == 0 else int(args[0])
        cogs.remove("Gamerizer") # don't include self

        for item in cogs: 
            self.queue.append(item)

        res = discord.Embed(title="Gamerizer Started!", description=util.bold("Loaded " + str(self.games) + " games!"), color=util.generate_random_color())
        await ctx.send(embed=res)
        await asyncio.sleep(self.sleep)
        await self.gamerizer_on(ctx)

        # if len(args) == 1:
        #     await ctx.send(", ".join(gamequeueutil.sample_from_list(cogs, int(args[0]))))
        # else: 
        #     await ctx.send("Too many arguments, expected 1")

    @commands.command(aliases=['q'])
    async def queue(self, ctx, arg1):
        if self.game:
            if arg1 in self.bot.cogs:
                self.queue.append(arg1)
            self.games += 1
            await ctx.message.add_reaction('✅')
        else: 
            res = discord.Embed(title="Gamerizer not currently active, I can't queue games!", color=util.generate_random_color())
            await ctx.send(embed=res)

    @commands.command()
    async def stop_gamerizer(self, ctx):
        self.game = False
        self.queue.clear()
        res = discord.Embed(title="Gamerizer over!", description="Thanks for playing!", color=util.generate_random_color())
        await ctx.send(embed=res)
        
    # @commands.command()
    # async def get_is_running(self, ctx):
    #     games_list = [x.name for x in self.bot.commands if x.name.startswith("start")]
    #     await ctx.send(", ".join(games_list))

    #     print(self.bot.get_cog("Wop").is_running())
    #     await ctx.send(self.bot.get_cog("Wop").is_running())

    

def setup(bot): 
    bot.add_cog(Gamerizer(bot))