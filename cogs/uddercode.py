
import uddercodeutil
import uuid
import discord
import asyncio
import random
<<<<<<< HEAD
import queue
import threading
=======
>>>>>>> f02717d9793932320b864d40a8d70c4af8486424
from discord.ext import tasks
from discord.ext import commands
from discord import abc


# __CODELENGTH__ = 4
# __READYUP__ = 30
# __ROUNDTIMER__ = 15
# self.tracked_players = {}
# self.created_channels = []
# self.created_roles = []


class UdderCode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
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
        # self.codelength = 4

    @commands.Cog.listener()
    async def on_ready(self):
        print('cog.uddercode successfully loaded!')
    
    @commands.command()
    async def start_udder(self, ctx):
        # global self.created_channels
        # global self.tracked_players
        self.context = ctx
        res = discord.Embed(title="Starting UdderCode!", color=self.generate_random_color())
        res.add_field(name="Rules", inline=False, value="You have **" + str(self.ready_up) + "** seconds to join! React to this message to play!")
        res.add_field(name="\u200b", inline=False, value="I have a code of length **" + str(self.code_length) + "**, you're meant to guess it!")
        res.add_field(name="\u200b", inline=False, value="Each round is **20** seconds, I'll tell you how many Bulls and Cows you have.")
        res.add_field(name="\u200b", inline=False, value="A **Bull** is a **correct number and in correct place.**\nA **Cow** is a **correct number but in an incorrect place.**\nFor example, if my code is **5688** and you guess **1234**, I'll tell you you have **0** Bulls and **0** Cows!\nIf you guess **6518**, I'll tell you you have **1** Bull and **2** Cows!")
        res.add_field(name="\u200b", inline=False, value="To minimize peeking, I'll make a channel just for you! (and sneaky admins)\nI will only respond to messages in that channel, so enter your submissions there!")
        msg = await ctx.send(embed=res)
        self.msgid = msg.id
        self.round = 0
        self.game = True
        self.timer = 0
        
        self.created_channels = []
        self.tracked_players = {}

        await msg.add_reaction("\u2705")
        await asyncio.sleep(self.ready_up)

        # for reactor in msg.reactions:
        #     await ctx.send(reactor.name)
            # reactors = await commands.get_reaction_users(reactor)
            # for member in reactors:
            #     await ctx.send(member.name)

        # cache_msg = discord.utils.get(commands.messages, id = msg.id)
        # for reactor in cache_msg.reactions:
        #     reactors = await commands.get_reaction_users(reactor)
        #     for member in reactors:
        #         await ctx.send(member.name)
        #         print(member)
        # print(msg)
        # users = msg.reactions
        # print(users)

        # await ctx.send("These players are playing!\n" + ", ".join([user.name for user in self.tracked_players]))
        guild = ctx.guild
        
        if len(self.tracked_players) == 0: 
            await ctx.send("No one joined!")
            await self.stop_udder(ctx)
            return
        print(self.tracked_players)
        
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

            # for channel in self.created_channels:
            #     await channel.send(channel.mention())
            
            # print(player, guild, channel)
        self.code = uddercodeutil.generateRandomCode(self.code_length)
        # print(self.code)
        await self.udder_on(ctx)

    @commands.command()
    async def stop_udder(self, ctx):
        # if self.game:
        # global self.created_channels
        # global self.created_roles
        res = discord.Embed(title="UdderCode over!", color=self.generate_random_color())
        await ctx.send(embed=res)

        # TODO: delete made roles + channels
        # guild = ctx.guild
        for channel in self.created_channels:
            await channel.delete()
        for role in self.created_roles:
            await role.delete()
        self.created_channels = []
        self.created_roles = []
        self.tracked_players = {}
        self.round = 0
        self.timer = 10e22
        self.game = False

    def generate_random_color(self):
        """
        Returns a value between 0 and 16777215, the max value for int(rgb).
        """
        return random.randint(0, 256**3-1)

<<<<<<< HEAD
    @commands.command(aliases=['fs'])
    async def findsolution(self, ctx, arg1, arg2, brief="Usage: !findsolution <code1> <code2>, alias='fs'", description="Usage: !findsolution <code1> <code2>, alias='fs'. Returns a solution path between code1 and code2."):
        """
        Returns a solution path between code1 and code2. 
        """
        # print(arg1, arg2)
        if len(arg1) == len(arg2) == 4:
            stack = queue.deque()
            solutionList = [str(x).zfill(len(arg1)) for x in range(len(uddercodeutil.numeric)**len(arg1))]
            uddercodeutil.TPOA(10, 2, 1, uddercodeutil.TPOANode(arg1), arg2, solutionList, stack)
            uddercodeutil.reverseStack(stack)
            res = discord.Embed(title="UdderCode here!", color=self.generate_random_color())
            stringBuild, guess = "", 1
            while stack:
                a = stack.pop()
                stringBuild += "Guess " + str(guess) + ": **"+ str(a[0].code) + "**, " + str(a[1]) + (" Bull, " if a[1] == 1 else " Bulls, ") + str(a[2]) + (" Cow\n" if a[2] == 1 else " Cows\n")
                guess += 1
            res.add_field(name='\u200b', inline=False, value=stringBuild)
            await ctx.send(embed=res)
        else: 
            res = discord.Embed(title="No solution, arguments are not valid (same length, length <= 5)!", color=self.generate_random_color())

=======
>>>>>>> f02717d9793932320b864d40a8d70c4af8486424
    async def udder_on(self, ctx):
        # await ctx.send("Testing: " + str(self.round))
        # loop = asyncio.get_running_loop()
        # end_time = loop.time() + __SECONDS__[self.round] if self.round < len(__SECONDS__) - 1 else 5
        # que = queue.Queue()
        loop = asyncio.get_running_loop()

        if self.game:
            self.round += 1
            # global __ROUNDTIMER__

            res = discord.Embed(title="Round " + str(self.round), color=self.generate_random_color())
            
            # if self.round == 1:
            for player in self.tracked_players:
                self.tracked_players[player] = False
            
            res.add_field(name='\u200b', inline=False, value="You have **" + str(self.round_timer) + " seconds** to submit an entry!")

            # print(self.created_channels)
            for channel in self.created_channels:
                # print("inner loop")
                await channel.send(embed=res)

            """
            Logic for timer that recursively calls this function.
            Important for advancing rounds and resetting timer! 
            """
            self.timer = loop.time() + self.round_timer
            
            # await asyncio.sleep(1)
            
            while self.game:
                # print(self.timer, loop.time())
                if (loop.time()) >= self.timer:
                    res = discord.Embed(title="Round over!", color=self.generate_random_color())
                    for channel in self.created_channels:
                        await channel.send(embed=res)
                    await asyncio.sleep(1)
                    await self.udder_on(ctx)
                    break
                await asyncio.sleep(1)
            # await ctx.send('Test success!')
        else:
            self.timer = 10e22
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.id == self.msgid and not user.bot and user not in self.tracked_players:
            self.tracked_players.setdefault(user, False)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.message.id == self.msgid and not user.bot:
           del self.tracked_players[user]

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and self.game and message.channel in self.created_channels and not self.tracked_players[message.author] and message.content.isnumeric() and len(message.content) == self.code_length:
            b, c = uddercodeutil.calculateDistance(message.content, self.code)
            self.tracked_players[message.author] = True
            if b == self.code_length:
                self.game = False
                # Winner
                for channel in self.created_channels:
                    # Disallow further guesses
                    for player in self.tracked_players:
                        self.tracked_players[player] = True
                    res = discord.Embed(title="Someone guessed my code!", color=self.generate_random_color())
                    res.add_field(name='\u200b', inline=False, value="**" + message.author.name + "** found the code to be **" + str(self.code) + "**!")
                    res.add_field(name='\u200b', inline=False, value="The game will end in **" + str(self.round_timer) + "** seconds.")
                    # await message.channel.send(embed=res)
                    await channel.send(embed=res)
                    await self.context.send(embed=res)
                    await asyncio.sleep(self.round_timer)
                    await self.stop_udder(self.context)
            else: 
                res = discord.Embed(title="You have **" + str(b) + "** bulls and **" + str(c) + " **cows!", color=self.generate_random_color())
                await message.channel.send(embed=res)
            # pass

def setup(bot): 
    bot.add_cog(UdderCode(bot))
