import discord
import asyncio
import alphafuseutil
import time
import queue
import json
import threading
import os
import copy
import random
from player import Player
from discord.ext import commands
from discord.ext import tasks

#
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.wait_for
# https://stackoverflow.com/questions/49947814/python-threading-error-must-be-an-iterable-not-int
# http://www.fileformat.info/info/unicode/char/search.htm


# from player import Player

# GLOBAL VARIABLES
__VALIDCHANNELS__= [755970868219346984, 515125639406419980, 659284289468366858, 617800636297117829]
__TRACKEDPLAYERS__ = {}
__ELIMINATEDPLAYERS__ = []
__USEDWORDS__ = {"DEFAULTWORD": ("bot", 2)}
__COMBINATIONS__ = ""
__DEFAULTLIFECOUNT__ = 3
# self.round = 0
# __SECONDS__ = [30, 30, 26, 22, 19, 17, 15, 13, 11, 10]
# __SECONDS__ = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
# __SECONDS__ = [15, 15, 15, 15, 15, 15, 15, 15, 15, 15]
__SECONDS__ = [25, 25, 25]
__MINTIME__ = 25
# __SECONDS__ = [10, 10]
__LETTERS__ = [0, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7]
# __LETTERS__ = [0, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5]
__MAXLETTERS__ = 8
__CURRENTLETTERS__ = []
__THREADFLAG__ = False
__WINNER__ = []

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../storage/tracking.json'))) as json_file:
    data = json.load(json_file)
f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../storage/output.txt')), "a+")
    


# class AlphaFuseLogic(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self.round = self.round

#     async def advance_round(self, number):
#         self.round += 1
#         print(self.round)

# class Player(commands.Cog):
#     def __init__(self, id=''): 
#         self.id = id
#         self.lives = 3


class AlphaFuse(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.game = False
        self.round = 0
        # self.channel = self.bot.get_channel(755970868219346984)
        # self.round_timer.start()
        self.index = 0
        self.timer = 10e22
        # self.server = server
        # self.server = server
        # self.round = 0
        # self.ingame = []
        # self.eliminated = []

    # def cog_unload(self):
    #     self.printer.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        print('cog.alphafuse successfully loaded!')

    @commands.command()
    async def what_self_game(self, ctx):
        await ctx.send(self.game)

    # @commands.command()
    # async def ping(self, ctx):
    #     await ctx.send('Pong!')
        
    @commands.command()
    async def start_alpha(self, ctx):
        # if arg1 == 'alpha':
        res = discord.Embed(title="Starting Alpha Fuse!", color=self.generate_random_color())
        res.add_field(name="Rules", inline=False, value="Players have some time per round to find a word that contains the displayed letters. ")
        await ctx.send(embed=res)
        self.round = 0
        # await self.advance_round(ctx, time.time())
        self.game = True
        self.timer = 10e22
        __USEDWORDS__ = {}
        __ELIMINATEDPLAYERS__ = []
        __TRACKEDPLAYERS__ = {}
        await self.alpha_on(ctx)

    @commands.command()
    async def stop_alpha(self, ctx):
        # if arg1 == 'alpha':
        res = discord.Embed(title="Stopping Alpha Fuse!", color=self.generate_random_color())
        await ctx.send(embed=res)
        __WINNER__ = []
        self.round = 0
        self.timer = 10e22
        self.game = False

    async def alpha_on(self, ctx):
        # await ctx.send("Testing: " + str(self.round))
        # loop = asyncio.get_running_loop()
        # end_time = loop.time() + __SECONDS__[self.round] if self.round < len(__SECONDS__) - 1 else 5
        # que = queue.Queue()
        loop = asyncio.get_running_loop()

        if self.game:
            self.round += 1
            global __CURRENTLETTERS__
            global __COMBINATIONS__
            global __SECONDS__
            global __TRACKEDPLAYERS__
            global __ELIMINATEDPLAYERS__
            global __USEDWORDS__
            global __WINNER__
            global __MAXLETTERS__
            # calc1 = threading.Thread(target=alphafuseutil.generate_random_string_of_length_biased, args=[__LETTERS__[self.round] if self.round < len(__LETTERS__) - 1 else 8])
            # calc1 = threading.Thread(target=lambda q, arg1: q.put(alphafuseutil.generate_random_string_of_length_biased(arg1)), args=(que, __LETTERS__[self.round] if self.round < len(__LETTERS__) - 1 else 8))
            # preconditionQueue = queue.Queue()
            # currentLettersThread = threading.Thread(target=lambda q, arg1: q.copy(alphafuseutil.generate_random_string_of_length_biased(arg1)), args=(__CURRENTLETTERS__, __LETTERS__[self.round] if self.round < len(__LETTERS__) - 1 else 8))
            # currentLettersThread.start()
            # currentLettersThread.join()
            # combinationsThread = threading.Thread(target=lambda q, arg1: q.copy(str(alphafuseutil.combinations(arg1)), args=(__COMBINATIONS__, __CURRENTLETTERS__)))
            # combinationsThread.start()
            # combinationsThread.join()

            # currentPlayers = ", ".join([x[0] for x in __TRACKEDPLAYERS__])
            
            # calc1.start()
            # calc1.join()
            # while not que.empty():
                # result = que.get()
            # print(__CURRENTLETTERS__)
            # print(calc1)

            # need a submission every round, so we can check that here: 
            
            if self.round >= 2:
                # flag = False
                # trackedPlayersCopy = copy.copy(x=__TRACKEDPLAYERS__)
                #  = __TRACKEDPLAYERS__
                for key, value in __TRACKEDPLAYERS__.items():
                    if value[0] > 0:
                        __WINNER__.append(key)
                    # if they didn't submit a word in the previous round, remove a life
                    # if they have 0 lives, pop the key from the backup. 
                    # We check the backup to see if it's empty-- if it is, then we return 
                    if __TRACKEDPLAYERS__[key][1] == False:
                        __TRACKEDPLAYERS__[key][0] -= 1 if __TRACKEDPLAYERS__[key][0] > 0 else 0
                    
                    if __TRACKEDPLAYERS__[key][0] == 0 and key not in __ELIMINATEDPLAYERS__:
                        __ELIMINATEDPLAYERS__.append(key)
                            # trackedPlayersCopy.pop(key)
                    # Reset the submitted flag to false, reset __WINNER__.
                    if len(__TRACKEDPLAYERS__) == len(__ELIMINATEDPLAYERS__):
                        
                        winner_res = discord.Embed(title="Winner(s)!", color=self.generate_random_color())
                        winner_res.add_field(name="\u200b", inline=False, value=", ".join(["**" + x + "**" for x in __WINNER__]))
                        await ctx.send(embed=winner_res)
                        await ctx.alpha_stop(ctx)

                    __TRACKEDPLAYERS__[key][1] = False
                    __WINNER__ = []
                    # for names in __ELIMINATEDPLAYERS__:
                        # trackedPlayersCopy.pop(key)
                    # flag = False
                    # k, v = __USEDWORDS__.items()
                    # name, rnd = *v
                    # for i in range(len(rnd)):
                    #     if name[i] == key and rnd != self.rnd - 1:
                    #         flag = True
                    # # if key == name and rnd != self.rnd - 1:
                    # #     flag = True
                    # if flag:
                    #     __TRACKEDPLAYERS__[key] -= 1
                    # flag = False
                
                # __TRACKEDPLAYERS__ = sorted(__TRACKEDPLAYERS__.items(), key=lambda x: x[1])

                # for key, value in __TRACKEDPLAYERS__.items():
                #     if __TRACKEDPLAYERS__[key][0] == 0:
                #         __WINNER__ = key

                # for key, value in __TRACKEDPLAYERS__.items():
                #     if value[0] != 0:
                #         flag = True
                #     if not flag:
                #         if __WINNER__ == {}:
                #             __WINNER__ = "No one"
                #         await ctx.send(__WINNER__ + " wins!")
                #         await self.stop_alpha(ctx)
                #         return
                
                #         # __TRACKEDPLAYERS__.pop(key)
                # flag = True
                # __TRACKEDPLAYERS__ 
                # if trackedPlayersCopy == {}:
                #     # res = []
                #     for key, value in __TRACKEDPLAYERS__.items():
                #         if key not in __ELIMINATEDPLAYERS__:
                #             await ctx.send(", ".join([].append(key)) + "win(s)!")
                # else:
                #     __TRACKEDPLAYERS__ = trackedPlayersCopy

            __CURRENTLETTERS__ = alphafuseutil.generate_random_string_of_length_unbiased(__LETTERS__[self.round] if self.round < len(__LETTERS__) - 1 else __MAXLETTERS__)
            __COMBINATIONS__ = str(alphafuseutil.combinations(__CURRENTLETTERS__))
            # currentPlayers = ", ".join([x[0] for x in __TRACKEDPLAYERS__])
            round_timer = str(__SECONDS__[self.round]) if self.round < len(__SECONDS__) - 1 else str(__MINTIME__)
            
            res = discord.Embed(title="Round " + str(self.round), color=self.generate_random_color())
            if self.round == 1:
                res.add_field(name='\u200b', inline=False, value="You have **" + round_timer + "** second(s) to find a word! Good luck!")
                res.add_field(name='\u200b', inline=False, value="\nEnter a word containing the letter(s): **" + ", ".join([x.upper() for x in __CURRENTLETTERS__]) + "**")
                res.add_field(name='\u200b', inline=False, value="\nValid combinations: **" + __COMBINATIONS__ + "**")
                # res = "Round " + str(self.round) + "\nYou have " + round_timer + " second(s) to find a word! Good luck!" + "\nEnter a word containing the letter(s): " + ", ".join([x.upper() for x in __CURRENTLETTERS__]) + "\nValid combinations: " + __COMBINATIONS__
            else: 
                res.add_field(name='\u200b', inline=False, value="You have **" + round_timer + "** second(s) to find a word! Good luck!")
                res.add_field(name='\u200b', inline=False, value="\nEnter a word containing the letter(s): **" + ", ".join([x.upper() for x in __CURRENTLETTERS__]) + "**")
                res.add_field(name='\u200b', inline=False, value="\nValid combinations: **" + __COMBINATIONS__ + "**")
                res.add_field(name='\u200b', inline=False, value="\nRemaining players: " + ", ".join(list(["**" + str(x) + "**" + ": " + str(y[0]) + " lives" if y[0] > 1 else "**" + str(x) + "**" + ": " + str(y[0]) + " life" for (x,y) in __TRACKEDPLAYERS__.items() if str(x) not in __ELIMINATEDPLAYERS__])))
                # res = "Round " + str(self.round) + "\nYou have " + round_timer + " second(s) to find a word! Good luck!" + "\nEnter a word containing the letter(s): " + ", ".join([x for x in __CURRENTLETTERS__]) + "\nValid combinations: " + __COMBINATIONS__ + "\nRemaining players: " + ", ".join(list([str(x) + ": " + str(y[0]) + " lives" for (x,y) in __TRACKEDPLAYERS__.items()]))
            
            # await asyncio.sleep(2)
            await ctx.send(embed=res)
            
            # make timer last for the designated round
            if self.round < len(__SECONDS__) - 1:
                self.timer = loop.time() + __SECONDS__[self.round]
            else:
                self.timer = loop.time() + __MINTIME__
            # self.timer = loop.time() + __SECONDS__[self.round] if self.round < len(__SECONDS__) - 1 else 10
            
            """
            Logic for timer that recursively calls this function.
            Important for advancing rounds and resetting timer! 
            """
            while self.game:
                # await asyncio.sleep(int(round_timer))
                # await alpha_on(ctx)
                # break
                # await ctx.send(loop.time())
                # if (loop.time() + 1) >= self.timer and self.game:
                if (loop.time()) >= self.timer:
                    res = discord.Embed(title="Round over!", color=self.generate_random_color())
                    await ctx.send(embed=res)
                    await self.alpha_on(ctx)
                    break
                await asyncio.sleep(1)
            # await ctx.send('Test success!')
        else:
            self.timer = 10e22
        # await self.alpha_on(ctx)

    # @commands.command()
    # async def alpha_one(self, ctx, arg1):
    #     await ctx.send(alphafuseutil.get_first_possibility(arg1))

    @commands.command()
    async def alpha_random(self, ctx, arg1, brief="Usage: !alpha_random <string>", description="Usage: !alpha_random <string>, returns a single valid possibility if there exists one at random for the given character combination."):
        """
        Returns one valid word at random that satisfies the given letter combination. 
        """
        res = discord.Embed(title=alphafuseutil.get_random_possibility(arg1), color=self.generate_random_color())
        await ctx.send(embed=res)

    @commands.command()
    async def alpha_25(self, ctx, arg1, brief="Usage: !alpha_25 <string>", description="Usage: !alpha_25 <string>, returns a list of at most 25 possible combinations for the given character combination."):
        """
        Returns a list of up to 25 valid words that satisfy the given letter combination. 
        """
        res = discord.Embed(title='\u200b', color=self.generate_random_color())
        res.add_field(name='\u200b', inline=False, value=", ".join(alphafuseutil.get_many_possibilities(arg1)))
        await ctx.send(embed=res)

    @commands.command()
    async def check(self, ctx, arg1):
        """
        Returns "valid" or "invalid" based on the submission. 
        """
        c = "Valid" if alphafuseutil.in_wordlist(arg1) else "Invalid"
        res = discord.Embed(title=c, color=self.generate_random_color())
        await ctx.send(embed=res)

    def generate_random_color(self):
        """
        Returns a value between 0 and 16777215, the max value for int(rgb).
        """
        return random.randint(0, 256**3-1)

    @commands.command()
    async def alpha_poss(self, ctx, arg1, brief="Usage: !alpha_poss <string>", description="Usage: !alpha_poss <strings>, returns the number of valid possibilities for the given character combination."):
        """
        Returns the number of valid combinations for the given letter combination.
        """
        res = discord.Embed(title=alphafuseutil.combinations(arg1), color=self.generate_random_color())
        await ctx.send(embed=res)

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        This method tracks messages sent by users, specific to certain games. 
        We must add valid attempts 
        """
        # if alphaFuse is on, the game is already started. 
        # Precondition: 
        # __CURRENTLETTERS__ is a nonempty list of characters. 
        # We add the message sender to __TRACKEDPLAYERS__
        
        # if not message.author.bot and message.channel.id in __VALIDCHANNELS__:
        #     channel = message.channel
        #     if alphafuseutil.check_valid(__CURRENTLETTERS__, message.content):

        #         await channel.send("Valid submission, " + message.author.name + "!")
        # FOR LOGGING PURPOSES
        # f.write(f"{int(time.time())} {message.author} {message.content}\n")

        if not message.author.bot and self.game:
            
            # if self.game:
                # channel = message.channel
                # if not message.author.bot:
                #     def check(message, letters):
                #         return alphafuseutil.check_valid(letters, message)
                #     # async def sst(): 
                #     #     await channel.send(message.author.name)
                #     # await sst()
                # if message.channel.id in __VALIDCHANNELS__:
                    
                    # logic to send verification message or if the word has already been sent 
            channel = message.channel
            word = message.content
            """
            On first round, 
            Add message.author to __TRACKEDPLAYERS__ if the word is valid, and prevent them from typing. 
            """ 
                    # print(self.round)
                    # if self.round == 1: 
                    # if message.author not in __TRACKEDPLAYERS__: 
                        # sets lives to 3
                        # __TRACKEDPLAYERS__.setdefault(message.author, 3)
                        # __USEDWORDS__.setdefault(message.content, (message.author.name, self.round))
                    # if 0 < self.round < 3: 
            # only accept words if: 
            # 1) they are not eliminated
            # 2) have not submitted a valid word already
            # if message.author.name not in __ELIMINATEDPLAYERS__ and __TRACKEDPLAYERS__[message.author.name][1] == False:
            if message.author.name not in __ELIMINATEDPLAYERS__:
                if alphafuseutil.check_valid(__CURRENTLETTERS__, word):
                    # if __USEDWORDS__ is not {}:
                    keys = __USEDWORDS__.keys()
                    # values = __USEDWORDS__.values()
                    # if the word is already used
                    
                    # register player. 
                    # if the player joins on round 1, they have three lives. 
                    # if the player joins on round 2, they have two lives. 
                    # if the player joins on round 3, they have one life. 
                    # if message.author.name not in __TRACKEDPLAYERS__.keys():
                    #     if 0 < self.round < 4:
                            
                    #         __TRACKEDPLAYERS__.setdefault(message.author.name, __DEFAULTLIFECOUNT__ + 1 - self.round)
                    # else:
                    #     __TRACKEDPLAYERS__[message.author.name] -= 1

                    if word in keys:
                        # u\U0001F187 : http://www.fileformat.info/info/unicode/char/1f187/index.htm
                        # Unicode Character 'NEGATIVE SQUARED LATIN CAPITAL LETTER X' (U+1F187)
                        await message.add_reaction("\u274C")
                        user, rnd = __USEDWORDS__[word]
                        if message.author.name == user:
                            await channel.send("What " + user + "? You already used this word in round " + str(rnd) + "! Use another word! (no penalty)")
                        else:
                            if message.author.name not in __TRACKEDPLAYERS__: 
                                __TRACKEDPLAYERS__.setdefault(message.author.name, [__DEFAULTLIFECOUNT__ - self.round, True])
                            __USEDWORDS__.setdefault(word, (message.author.name, self.round))
                            __TRACKEDPLAYERS__[message.author.name][0] -= 1 if __TRACKEDPLAYERS__[message.author.name][0] > 0 else 0
                            __TRACKEDPLAYERS__[message.author.name][1] = True
                            await channel.send("Unlucky, **" + word + "** was already used by " + user + " on round " + str(rnd) + "! (-1 life)")
                    
                    else: 
                        # if 0 < self.round < 4:
                        if message.author.name not in __TRACKEDPLAYERS__.keys():
                            if self.round <= 3:
                                __TRACKEDPLAYERS__.setdefault(message.author.name, [__DEFAULTLIFECOUNT__ + 1 - self.round, True])
                                __USEDWORDS__.setdefault(word, (message.author.name, self.round))
                        # \u2705 : https://www.fileformat.info/info/unicode/char/2705/index.htm
                        # Unicode Character 'WHITE HEAVY CHECK MARK' (U+2705)
                                await message.add_reaction("\u2705")
                            # await channel.send("Valid submission, " + message.author.name + "!")
                        else: 
                            # __TRACKEDPLAYERS__.setdefault(message.author.name, __DEFAULTLIFECOUNT__ + 1 - self.round)
                            # (names, rnd) = __USEDWORDS__.values()
                            # if (message.author.name, self.round) in __USEDWORDS__.values():
                            #     __TRACKEDPLAYERS__[message.author.name] -= 1
                            #     await message.add_reaction("\u274C")
                            #     await channel.send("Hey! You already submitted a word this round! (-1 life)")
                            # else:
                            __USEDWORDS__.setdefault(word, (message.author.name, self.round))
                            __TRACKEDPLAYERS__[message.author.name][1] = True
                            await message.add_reaction("\u2705")



def setup(bot): 
    bot.add_cog(AlphaFuse(bot))
