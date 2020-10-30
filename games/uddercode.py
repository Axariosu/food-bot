
import util.uddercodeutil as uddercodeutil
import util.util as util
import uuid
import discord
import asyncio
import random
import queue
import time
from discord.ext import tasks
from discord.ext import commands

class UdderCode():
    def __init__(self, ctx):
        self.ctx = ctx
        self.game = False
        self.round = 0
        self.code = ""
        self.timer = 0
        self.msgid = 0
        self.context = None
        self.created_channels = []
        self.created_roles = []
        self.tracked_players = {}
        self.code_length = 4
        self.ready_up = 25
        self.round_timer = 15
    
    async def start(self):
        self.context = self.ctx
        res = discord.Embed(title="Starting UdderCode!", color=util.generate_random_color())
        res.add_field(name="Rules", inline=False, value="You have **" + str(self.ready_up) + "** seconds to join! React to this message to play!")
        res.add_field(name="\u200b", inline=False, value="I have a code of length **" + str(self.code_length) + "**, you're meant to guess it!")
        res.add_field(name="\u200b", inline=False, value="Each round is **20** seconds, I'll tell you how many Bulls and Cows you have.")
        res.add_field(name="\u200b", inline=False, value="A **Bull** is a **correct number and in correct place.**\nA **Cow** is a **correct number but in an incorrect place.**\nFor example, if my code is **5688** and you guess **1234**, I'll tell you you have **0** Bulls and **0** Cows!\nIf you guess **6518**, I'll tell you you have **1** Bull and **2** Cows!")
        res.add_field(name="\u200b", inline=False, value="To minimize peeking, I'll make a channel just for you! (and sneaky admins)\nI will only respond to messages in that channel, so enter your submissions there!")
        msg = await self.ctx.send(embed=res)
        self.msgid = msg.id
        self.round = 0
        self.game = True
        self.timer = 0
        
        self.created_channels = []
        self.tracked_players = {}

        await msg.add_reaction("✅")
        await asyncio.sleep(self.ready_up)

        guild = self.ctx.guild
        
        if len(self.tracked_players) == 0: 
            await self.ctx.send("No one joined!")
            await self.stop()
            return
        
        for player in self.tracked_players:
            uuid_short = str(uuid.uuid4())[:8]    

            role = await guild.create_role(name=uuid_short)
            uuid_role = discord.utils.get(guild.roles, name=uuid_short)

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                uuid_role: discord.PermissionOverwrite(read_messages=True)
            }

            channel = await guild.create_text_channel(uuid_short, overwrites=overwrites, topic="Secret channel just for you! (and sneaky, sneaky admins)")
            
            self.created_channels.append(channel)
            self.created_roles.append(role)

            await player.add_roles(uuid_role)
            await channel.send(player.mention)

        self.code = uddercodeutil.generateRandomCode(self.code_length)
        # print(self.code)
        await self.udder_loop()

    async def stop(self):
        # if self.game:
        # global self.created_channels
        # global self.created_roles
        res = discord.Embed(title="UdderCode over!", color=util.generate_random_color())
        await self.ctx.send(embed=res)
        # TODO: delete made roles + channels
        # guild = self.ctx.guild
        for channel in self.created_channels:
            await channel.delete()
        for role in self.created_roles:
            await role.delete()
        self.created_channels = []
        self.created_roles = []
        self.tracked_players = {}
        self.round = 0
        self.timer = 1e22
        self.game = False
        self.ctx.bot.games.pop(self.ctx.guild.id)

    async def findsolution(self, arg1, arg2):
        if arg2 == "r":
            arg2 = uddercodeutil.generateRandomCode(len(arg1))
        if len(arg1) == len(arg2) <= 6:
            stack = queue.deque()
            solutionList = [str(x).zfill(len(arg1)) for x in range(len(uddercodeutil.numeric)**len(arg1))]
            start = time.time()
            uddercodeutil.TPOA(10, 2, 1, uddercodeutil.TPOANode(arg1), arg2, solutionList, stack)
            stop = time.time()
            uddercodeutil.reverseStack(stack)
            res = discord.Embed(title="UdderCode found!", color=util.generate_random_color())
            stringBuild, guess = "", 0
            while stack:
                a = stack.pop()
                guess += 1
                stringBuild += "Guess " + str(guess) + ": " + util.bold(a[0].code) + ", " + str(a[1]) + (" Bull, " if a[1] == 1 else " Bulls, ") + str(a[2]) + (" Cow\n" if a[2] == 1 else " Cows\n")
                
            res.add_field(name="Solution found at depth " + str(guess), inline=False, value=stringBuild)
            res.add_field(name="Time elapsed", inline=False, value=str(stop-start))
            await self.ctx.send(embed=res)

    async def udder_loop(self):
        loop = asyncio.get_running_loop()
        if self.game:
            self.round += 1
            res = discord.Embed(title="Round " + str(self.round), color=util.generate_random_color())
            for player in self.tracked_players:
                self.tracked_players[player] = False
            res.add_field(name='\u200b', inline=False, value="You have " + util.bold(str(self.round_timer) + " seconds") + " to submit an entry!")
            for channel in self.created_channels:
                await channel.send(embed=res)
            self.timer = loop.time() + self.round_timer
            while self.game:
                if (loop.time()) >= self.timer:
                    res = discord.Embed(title="Round over!", color=util.generate_random_color())
                    for channel in self.created_channels:
                        await channel.send(embed=res)
                    await asyncio.sleep(1)
                    await self.udder_loop()
                    break
                await asyncio.sleep(1)
    
    async def handle_on_reaction_add(self, reaction, user):
        if reaction.message.id == self.msgid and user not in self.tracked_players:
            self.tracked_players[user] = False

    async def handle_on_reaction_remove(self, reaction, user):
        if reaction.message.id == self.msgid:
            self.tracked_players.pop(user)

    async def handle_on_message(self, message):
        if not message.author.bot and self.game and message.channel in self.created_channels and not self.tracked_players[message.author] and message.content.isnumeric() and len(message.content) == self.code_length:
            b, c = uddercodeutil.calculateDistance(message.content, self.code)
            self.tracked_players[message.author] = True
            if b == self.code_length:
                self.game = False
                for channel in self.created_channels:
                    for player in self.tracked_players:
                        self.tracked_players[player] = True
                    res = discord.Embed(title="Someone guessed my code!", color=util.generate_random_color())
                    res.add_field(name='\u200b', inline=False, value=util.bold(message.author.name) + " found the code to be " + util.bold(self.code) + "!")
                    res.add_field(name='\u200b', inline=False, value="The game will end in " + util.bold(self.round_timer) + " seconds.")
                    await channel.send(embed=res)
                    await self.ctx.send(embed=res)
                    await asyncio.sleep(self.round_timer)
                    await self.stop()
            else: 
                res = discord.Embed(title="You have " + util.bold(b) + (" Bull and " if b == 1 else " Bulls and ") + util.bold(c) + (" Cow! " if c == 1 else " Cows!"), color=util.generate_random_color())
                await message.channel.send(embed=res)
