
import uddercodeutil
import uuid
import discord
import asyncio
import random
from discord.ext import tasks
from discord.ext import commands
from discord import abc


__CODELENGTH__ = 4
__READYUP__ = 30
__ROUNDTIMER__ = 20
__TRACKEDPLAYERS__ = {}
__CREATEDCHANNELS__ = []
__CREATEDROLES__ = []


class UdderCode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = False
        self.round = 0
        self.code = ""
        self.timer = 10e22
        self.msgid = 0
        self.context = None
        # self.codelength = 4

    @commands.Cog.listener()
    async def on_ready(self):
        print('cog.uddercode successfully loaded!')
    
    @commands.command()
    async def start_udder(self, ctx):
        global __CREATEDCHANNELS__
        global __TRACKEDPLAYERS__
        self.context = ctx
        res = discord.Embed(title="Starting UdderCode!", color=self.generate_random_color())
        res.add_field(name="Rules", inline=False, value="You have **" + str(__READYUP__) + "** seconds to join! React to this message to play!")
        res.add_field(name="\u200b", inline=False, value="I have a code of length **" + str(__CODELENGTH__) + "**, you're meant to guess it!")
        res.add_field(name="\u200b", inline=False, value="Each round is **20** seconds, I'll tell you how many Bulls and Cows you have.")
        res.add_field(name="\u200b", inline=False, value="A **Bull** is a **correct number and in correct place.**\nA **Cow** is a **correct number but in an incorrect place.**\nFor example, if my code is **5688** and you guess **1234**, I'll tell you you have **0** Bulls and **0** Cows!\nIf you guess **6518**, I'll tell you you have **1** Bull and **2** Cows!")
        res.add_field(name="\u200b", inline=False, value="To minimize peeking, I'll make a channel just for you! (and sneaky admins)\nI will only respond to messages in that channel, so enter your submissions there!")
        msg = await ctx.send(embed=res)
        self.msgid = msg.id
        self.round = 0
        self.game = True
        self.timer = 10e22
        
        __CREATEDCHANNELS__ = []
        __TRACKEDPLAYERS__ = {}

        await msg.add_reaction("\u2705")
        await asyncio.sleep(__READYUP__)

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

        # await ctx.send("These players are playing!\n" + ", ".join([user.name for user in __TRACKEDPLAYERS__]))
        guild = ctx.guild
        
        if len(__TRACKEDPLAYERS__) == 0: 
            await ctx.send("No one joined!")
            await self.stop_udder(ctx)
            return
        for player in __TRACKEDPLAYERS__:
            uuid_short = str(uuid.uuid4())[:8]    

            role = await guild.create_role(name=uuid_short)
            uuid_role = discord.utils.get(guild.roles, name=uuid_short)

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                uuid_role: discord.PermissionOverwrite(read_messages=True)
            }

            channel = await guild.create_text_channel(uuid_short, overwrites=overwrites, topic="Secret channel just for you! (and sneaky, sneaky admins)")
            
            __CREATEDCHANNELS__.append(channel)
            __CREATEDROLES__.append(role)

            await player.add_roles(uuid_role)
            
            # print(player, guild, channel)
        self.code = uddercodeutil.generateRandomCode(__CODELENGTH__)
        # print(self.code)
        await self.udder_on(ctx)

    @commands.command()
    async def stop_udder(self, ctx):
        # if self.game:
        global __CREATEDCHANNELS__
        global __CREATEDROLES__
        res = discord.Embed(title="UdderCode over!", color=self.generate_random_color())
        await ctx.send(embed=res)

        # TODO: delete made roles + channels
        # guild = ctx.guild
        for channel in __CREATEDCHANNELS__:
            await channel.delete()
        for role in __CREATEDROLES__:
            await role.delete()
        __TRACKEDPLAYERS__ = {}
        __CREATEDCHANNELS__ = []
        __CREATEDROLES__ = []
        self.round = 0
        self.timer = 10e22
        self.game = False

    def generate_random_color(self):
        """
        Returns a value between 0 and 16777215, the max value for int(rgb).
        """
        return random.randint(0, 256**3-1)

    async def udder_on(self, ctx):
        # await ctx.send("Testing: " + str(self.round))
        # loop = asyncio.get_running_loop()
        # end_time = loop.time() + __SECONDS__[self.round] if self.round < len(__SECONDS__) - 1 else 5
        # que = queue.Queue()
        loop = asyncio.get_running_loop()

        if self.game:
            self.round += 1
            global __ROUNDTIMER__

            res = discord.Embed(title="Round " + str(self.round), color=self.generate_random_color())
            
            # if self.round == 1:
            for player in __TRACKEDPLAYERS__:
                __TRACKEDPLAYERS__[player] = False
            res.add_field(name='\u200b', inline=False, value="You have **" + str(__ROUNDTIMER__) + " seconds** to submit an entry!")
            
                # res.add_field(name='\u200b', inline=False, value="You have **" + round_timer + "** second(s) to find a word! Good luck!")
                # res.add_field(name='\u200b', inline=False, value="\nEnter a word containing the letter(s): **" + ", ".join([x.upper() for x in __CURRENTLETTERS__]) + "**")
                # res.add_field(name='\u200b', inline=False, value="\nValid combinations: **" + __COMBINATIONS__ + "**")
                # res = "Round " + str(self.round) + "\nYou have " + round_timer + " second(s) to find a word! Good luck!" + "\nEnter a word containing the letter(s): " + ", ".join([x.upper() for x in __CURRENTLETTERS__]) + "\nValid combinations: " + __COMBINATIONS__
            # else: 
            #     res.add_field(name='\u200b', inline=False, value="Round Over!")
                # res.add_field(name='\u200b', inline=False, value="You have **" + round_timer + "** second(s) to find a word! Good luck!")
                # res.add_field(name='\u200b', inline=False, value="\nEnter a word containing the letter(s): **" + ", ".join([x.upper() for x in __CURRENTLETTERS__]) + "**")
                # res.add_field(name='\u200b', inline=False, value="\nValid combinations: **" + __COMBINATIONS__ + "**")
                # res.add_field(name='\u200b', inline=False, value="\nRemaining players: " + ", ".join(list(["**" + str(x) + "**" + ": " + str(y[0]) + " lives" if y[0] > 1 else "**" + str(x) + "**" + ": " + str(y[0]) + " life" for (x,y) in __TRACKEDPLAYERS__.items() if str(x) not in __ELIMINATEDPLAYERS__])))
                # res = "Round " + str(self.round) + "\nYou have " + round_timer + " second(s) to find a word! Good luck!" + "\nEnter a word containing the letter(s): " + ", ".join([x for x in __CURRENTLETTERS__]) + "\nValid combinations: " + __COMBINATIONS__ + "\nRemaining players: " + ", ".join(list([str(x) + ": " + str(y[0]) + " lives" for (x,y) in __TRACKEDPLAYERS__.items()]))
            
            # await asyncio.sleep(2)
            for channel in __CREATEDCHANNELS__:
                await channel.send(embed=res)

            """
            Logic for timer that recursively calls this function.
            Important for advancing rounds and resetting timer! 
            """
            self.timer = loop.time() + __ROUNDTIMER__
            while True:
                if (loop.time()) >= self.timer and self.game:
                    res = discord.Embed(title="Round over!", color=self.generate_random_color())
                    for channel in __CREATEDCHANNELS__:
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
        if reaction.message.id == self.msgid and not user.bot:
            __TRACKEDPLAYERS__.setdefault(user, False)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.message.id == self.msgid and not user.bot:
           del __TRACKEDPLAYERS__[user]

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and self.game and message.channel in __CREATEDCHANNELS__ and not __TRACKEDPLAYERS__[message.author] and message.content.isnumeric() and len(message.content) == __CODELENGTH__:
            b, c = uddercodeutil.calculateDistance(message.content, self.code)
            __TRACKEDPLAYERS__[message.author] = True
            if b == __CODELENGTH__:
                self.game = False
                # Winner
                for channel in __CREATEDCHANNELS__:
                    # Disallow further guesses
                    for player in __TRACKEDPLAYERS__:
                        __TRACKEDPLAYERS__[player] = True
                    res = discord.Embed(title="Someone guessed my code!", color=self.generate_random_color())
                    res.add_field(name='\u200b', inline=False, value="**" + message.author.name + "** found the code to be **" + str(self.code) + "**!")
                    res.add_field(name='\u200b', inline=False, value="The game will end in **" + str(__ROUNDTIMER__) + "** seconds.")
                    # await message.channel.send(embed=res)
                    await channel.send(embed=res)
                    await self.context.send(embed=res)
                    await asyncio.sleep(__ROUNDTIMER__)
                    await self.stop_udder(self.context)
            else: 
                res = discord.Embed(title="You have **" + str(b) + "** bulls and **" + str(c) + " **cows!", color=self.generate_random_color())
                await message.channel.send(embed=res)
            # pass

def setup(bot): 
    bot.add_cog(UdderCode(bot))
