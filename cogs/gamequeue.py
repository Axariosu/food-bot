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


class GameQueue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = queue.deque()
        self.current_game_is_running = False
        self.current_game = None
        self.context = None
        self.game = False
        self.timer = 1e22
        self.check_every = 5
        self.sleep = 3
    
    @commands.command()
    async def gamerizer_on(self, ctx):
        # loop = asyncio.get_running_loop()
        # print(queue.deque())
        
        if not self.queue: # if queue is empty
            await self.stop_gamerizer(ctx)
            return
        else: 
            self.current_game = self.queue.popleft() 
            
            res = discord.Embed(title="Next Game: ", description=self.current_game, color=util.generate_random_color())
            await ctx.send(embed=res)

            current_cog = self.bot.get_cog(self.current_game)
            
            command_to_invoke = [x.name for x in current_cog.get_commands() if x.name.startswith("start_")][0]
            await ctx.invoke(self.bot.get_command(command_to_invoke))
            await self.gamerizer_on(ctx)
        # self.timer = loop.time() + self.check_every # checks whether previous game is still running, every check_every seconds
        # print("here3")
        # while self.game:
        #     if loop.time() >= self.timer:
        #         print("here4")
        #         # res = discord.Embed(title="Round over!", color=util.generate_random_color())
        #         self.game = False
        #         # await ctx.send(embed=res)
        #         # self.timer = 10e22
        #         break
        #     await asyncio.sleep(1)
        # await asyncio.sleep(3)

    @commands.command(aliases=['gamerizer', 'gamer'])
    async def start_gamerizer(self, ctx, *args): 
        self.game = True
        self.context = ctx
        # cogs = list(self.bot.cogs)
        cogs = ["Pow", "Wop"]
        # cogs.remove("GameQueue") # don't include self

        for item in cogs: 
            self.queue.append(item)

        res = discord.Embed(title="Gamerizer Started!", description="Loaded " + str(args[0]) + " games!", color=util.generate_random_color())
        await ctx.send(embed=res)
        await asyncio.sleep(self.sleep)
        await self.gamerizer_on(ctx)

        # if len(args) == 1:
        #     await ctx.send(", ".join(gamequeueutil.sample_from_list(cogs, int(args[0]))))
        # else: 
        #     await ctx.send("Too many arguments, expected 1")

    @commands.command()
    async def add_game(self, ctx, arg1):
        if self.game:
            if arg1 in self.bot.cogs:
                self.queue.append(arg1)
        else: 
            res = discord.Embed(title="Gamerizer not currently active, sorry!", color=util.generate_random_color())

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
    bot.add_cog(GameQueue(bot))