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
# __VALIDCHANNELS__= [755970868219346984, 515125639406419980, 659284289468366858, 617800636297117829]
# self.trackedPlayers = {}
# self.eliminatedPlayers = []
# self.usedWords = {}
# self.combinations = ""
# self.defaultLifeCount = 3
# self.round = 0
# self.seconds = [30, 30, 26, 22, 19, 17, 15, 13, 11, 10]
# self.seconds = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
# self.seconds = [15, 15, 15, 15, 15, 15, 15, 15, 15, 15]
# self.seconds = [25, 25, 25]
# self.seconds = [20, 20]
# self.minTime = 20
# self.seconds = [10, 10]
# self.letters = [0, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7]
# self.letters = [0, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5]
# self.maxLetters = 8
# self.winner = []

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
        self.index = 0
        self.timer = 10e22
        self.context = None        
        self.gameMode = 0
        self.currentLetters = []
        self.seconds = [20]
        self.minTime = 20
        self.letters = [0, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7]
        self.trackedPlayers = {}
        self.winner = []
        self.eliminatedPlayers = []
        self.combinations = ""
        self.maxLetters = 8
        self.defaultLifeCount = 3
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
        
    @commands.command(aliases=['alpha'])
    async def start_alpha(self, ctx, *args):
        #
        res = discord.Embed(title="Starting Alpha Fuse!", color=self.generate_random_color())
        res.add_field(name="Rules", inline=False, value="Players have some time per round to find a word that contains the displayed letters.\nIf you repeat a word someone else used, you lose a life!\nIf you repeat your own word, there's no penalty.")
        await ctx.send(embed=res)
        self.round = 0
        # await self.advance_round(ctx, time.time())
        self.game = True
        self.timer = 10e22
        self.context = ctx
        self.usedWords = {}
        self.eliminatedPlayers = []
        self.trackedPlayers = {}
        self.gameMode = args[0] if len(args) > 0 else 0
        await self.alpha_on(ctx)

    @commands.command()
    async def stop_alpha(self, ctx):
        res = discord.Embed(title="Stopping Alpha Fuse!", color=self.generate_random_color())
        await ctx.send(embed=res)
        self.winner = []
        self.usedWords = {}
        self.eliminatedPlayers = []
        self.trackedPlayers = {}
        self.round = 0
        self.timer = 10e22
        self.game = False

    async def alpha_on(self, ctx):
        # await ctx.send("Testing: " + str(self.round))
        # loop = asyncio.get_running_loop()
        # end_time = loop.time() + self.seconds[self.round] if self.round < len(self.seconds) - 1 else 5
        # que = queue.Queue()
        loop = asyncio.get_running_loop()

        if self.game:
            self.round += 1
            # need a submission every round, so we can check that here: 
            
            if self.round >= 2:
                if self.round >= 4 and len(self.trackedPlayers) == 0: 
                    await self.context.send("No one joined!")
                    await self.stop_alpha(ctx)
                # flag = False
                # trackedPlayersCopy = copy.copy(x=self.trackedPlayers)
                #  = self.trackedPlayers
                for key, value in self.trackedPlayers.items():
                    if value[0] > 0:
                        self.winner.append(key)
                    # if they didn't submit a word in the previous round, remove a life
                    # if they have 0 lives, pop the key from the backup. 
                    # We check the backup to see if it's empty-- if it is, then we return 
                    if self.trackedPlayers[key][1] == False:
                        self.trackedPlayers[key][0] -= 1 if self.trackedPlayers[key][0] > 0 else 0
                    
                    if self.trackedPlayers[key][0] == 0 and key not in self.eliminatedPlayers:
                        self.eliminatedPlayers.append(key)
                            # trackedPlayersCopy.pop(key)
                    # Reset the submitted flag to false, reset self.winner.
                    if len(self.trackedPlayers) == len(self.eliminatedPlayers):
                        
                        winner_res = discord.Embed(title="Winner(s)!", color=self.generate_random_color())
                        winner_res.add_field(name="\u200b", inline=False, value=", ".join(["**" + x + "**" for x in self.winner]))
                        await ctx.send(embed=winner_res)
                        await self.stop_alpha(ctx)

                    self.trackedPlayers[key][1] = False
                    self.winner = []

            if self.gameMode == 0:
                self.currentLetters = alphafuseutil.generate_random_string_of_length_unbiased(self.letters[self.round] if self.round < len(self.letters) - 1 else self.maxLetters)
            else: 
                self.currentLetters = alphafuseutil.generate_random_string_of_length_biased(self.letters[self.round] if self.round < len(self.letters) - 1 else self.maxLetters)
            self.combinations = str(alphafuseutil.combinations(self.currentLetters))
            # currentPlayers = ", ".join([x[0] for x in self.trackedPlayers])
            round_timer = str(self.seconds[self.round]) if self.round < len(self.seconds) - 1 else str(self.minTime)
            
            res = discord.Embed(title="Round " + str(self.round), color=self.generate_random_color())
            if self.round == 1:
                res.add_field(name='\u200b', inline=False, value="You have **" + round_timer + "** second(s) to find a word! Good luck!")
                res.add_field(name='\u200b', inline=False, value="\nEnter a word containing the letter(s): **" + ", ".join([x.upper() for x in self.currentLetters]) + "**")
                res.add_field(name='\u200b', inline=False, value="\nValid combinations: **" + self.combinations + "**")
                # res = "Round " + str(self.round) + "\nYou have " + round_timer + " second(s) to find a word! Good luck!" + "\nEnter a word containing the letter(s): " + ", ".join([x.upper() for x in self.currentLetters]) + "\nValid combinations: " + self.combinations
            else: 
                res.add_field(name='\u200b', inline=False, value="You have **" + round_timer + "** second(s) to find a word! Good luck!")
                res.add_field(name='\u200b', inline=False, value="\nEnter a word containing the letter(s): **" + ", ".join([x.upper() for x in self.currentLetters]) + "**")
                res.add_field(name='\u200b', inline=False, value="\nValid combinations: **" + self.combinations + "**")
                res.add_field(name='\u200b', inline=False, value="\nRemaining players: " + ", ".join(list(["**" + str(x) + "**" + ": " + str(y[0]) + " lives" if y[0] > 1 else "**" + str(x) + "**" + ": " + str(y[0]) + " life" for (x,y) in self.trackedPlayers.items() if str(x) not in self.eliminatedPlayers])))
                # res = "Round " + str(self.round) + "\nYou have " + round_timer + " second(s) to find a word! Good luck!" + "\nEnter a word containing the letter(s): " + ", ".join([x for x in self.currentLetters]) + "\nValid combinations: " + self.combinations + "\nRemaining players: " + ", ".join(list([str(x) + ": " + str(y[0]) + " lives" for (x,y) in self.trackedPlayers.items()]))
            
            # await asyncio.sleep(2)
            await ctx.send(embed=res)
            
            # make timer last for the designated round
            if self.round < len(self.seconds) - 1:
                self.timer = loop.time() + self.seconds[self.round]
            else:
                self.timer = loop.time() + self.minTime
            # self.timer = loop.time() + self.seconds[self.round] if self.round < len(self.seconds) - 1 else 10
            
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

    @commands.command(aliases=['a25'])
    async def alpha_25(self, ctx, arg1, brief="Usage: !alpha_25 <string>", description="Usage: !alpha_25 <string>, returns a list of at most 25 possible combinations for the given character combination."):
        """
        Returns a list of up to 25 valid words that satisfy the given letter combination. 
        """
        res = discord.Embed(title=discord.Embed.Empty, description=", ".join(alphafuseutil.get_many_possibilities(arg1)), color=self.generate_random_color())
        # res.add_field(name=discord.Embed.Empty, inline=False, value=", ".join(alphafuseutil.get_many_possibilities(arg1)))
        await ctx.send(embed=res)

    @commands.command(aliases=['check'])
    async def alpha_check(self, ctx, arg1):
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
        # self.currentLetters is a nonempty list of characters. 
        # We add the message sender to self.trackedPlayers
        
        # if not message.author.bot and message.channel.id in __VALIDCHANNELS__:
        #     channel = message.channel
        #     if alphafuseutil.check_valid(self.currentLetters, message.content):

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
            Add message.author to self.trackedPlayers if the word is valid, and prevent them from typing. 
            """ 
                    # print(self.round)
                    # if self.round == 1: 
                    # if message.author not in self.trackedPlayers: 
                        # sets lives to 3
                        # self.trackedPlayers.setdefault(message.author, 3)
                        # self.usedWords.setdefault(message.content, (message.author.name, self.round))
                    # if 0 < self.round < 3: 
            # only accept words if: 
            # 1) they are not eliminated
            # 2) have not submitted a valid word already
            # if message.author.name not in self.eliminatedPlayers and self.trackedPlayers[message.author.name][1] == False:
            if message.author.name not in self.eliminatedPlayers:
                if alphafuseutil.check_valid(self.currentLetters, word):
                    # if self.usedWords is not {}:
                    keys = self.usedWords.keys()
                    # values = self.usedWords.values()
                    # if the word is already used
                    
                    # register player. 
                    # if the player joins on round 1, they have three lives. 
                    # if the player joins on round 2, they have two lives. 
                    # if the player joins on round 3, they have one life. 
                    # if message.author.name not in self.trackedPlayers.keys():
                    #     if 0 < self.round < 4:
                            
                    #         self.trackedPlayers.setdefault(message.author.name, self.defaultLifeCount + 1 - self.round)
                    # else:
                    #     self.trackedPlayers[message.author.name] -= 1

                    if word in keys:
                        # u\U0001F187 : http://www.fileformat.info/info/unicode/char/1f187/index.htm
                        # Unicode Character 'NEGATIVE SQUARED LATIN CAPITAL LETTER X' (U+1F187)
                        await message.add_reaction("\u274C")
                        user, rnd = self.usedWords[word]
                        if message.author.name == user:
                            await channel.send("What " + user + "? You already used this word in round " + str(rnd) + "! Use another word! (no penalty)")
                        else:
                            if self.round <= 3:
                                if message.author.name not in self.trackedPlayers:
                                    self.trackedPlayers.setdefault(message.author.name, [self.defaultLifeCount - self.round, True])
                                self.usedWords.setdefault(word, (message.author.name, self.round))
                                self.trackedPlayers[message.author.name][0] -= 1 if self.trackedPlayers[message.author.name][0] > 0 else 0
                                self.trackedPlayers[message.author.name][1] = True
                                await channel.send("Unlucky, **" + word + "** was already used by " + user + " on round " + str(rnd) + "! (-1 life)")
                    
                    else: 
                        # if 0 < self.round < 4:
                        if message.author.name not in self.trackedPlayers:
                            if self.round <= 3:
                                self.trackedPlayers.setdefault(message.author.name, [self.defaultLifeCount + 1 - self.round, True])
                                self.usedWords.setdefault(word, (message.author.name, self.round))
                        # \u2705 : https://www.fileformat.info/info/unicode/char/2705/index.htm
                        # Unicode Character 'WHITE HEAVY CHECK MARK' (U+2705)
                                await message.add_reaction("\u2705")
                            # await channel.send("Valid submission, " + message.author.name + "!")
                        else: 
                            # self.trackedPlayers.setdefault(message.author.name, self.defaultLifeCount + 1 - self.round)
                            # (names, rnd) = self.usedWords.values()
                            # if (message.author.name, self.round) in self.usedWords.values():
                            #     self.trackedPlayers[message.author.name] -= 1
                            #     await message.add_reaction("\u274C")
                            #     await channel.send("Hey! You already submitted a word this round! (-1 life)")
                            # else:
                            self.usedWords.setdefault(word, (message.author.name, self.round))
                            self.trackedPlayers[message.author.name][1] = True
                            await message.add_reaction("\u2705")



def setup(bot): 
    bot.add_cog(AlphaFuse(bot))
