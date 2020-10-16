import discord
import asyncio
import util.alphafuseutil as alphafuseutil
import util.util as util
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

# with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../storage/tracking.json'))) as json_file:
#     data = json.load(json_file)
# f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../storage/output.txt')), "a+")
    

class OmegaFuse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = False
        self.round = 0
        self.index = 0
        self.timer = 10e22
        self.context = None        
        self.gameMode = 0
        self.currentLetters = []
        self.seconds = [30, 20, 16, 13, 10]
        self.minTime = 10
        self.letters = [0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 9, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16, 16, 17, 17, 17, 17, 18, 18, 18, 18, 19, 19, 19, 19]
        self.trackedPlayers = {}
        self.trackedPlayersPrevious = {}
        self.winner = []
        self.combinations = ""
        self.maxLetters = 20
        self.defaultLifeCount = 3
        self.sleep = 3

    @commands.Cog.listener()
    async def on_ready(self):
        print('cog.omegafuse successfully loaded!')
        
    @commands.command(aliases=['omega'])
    async def start_omega(self, ctx, *args):
        res = discord.Embed(title="Starting Omega Fuse!", color=util.generate_random_color())
        res.add_field(name="Rules", inline=False, value="Players have some time per round to find a word that **doesn't** contain the displayed letters.\nIf you repeat a word someone else used, you lose a life!\nIf you repeat your own word, there's no penalty.")
        await ctx.send(embed=res)
        self.round = 0
        self.gameMode = int(args[0]) if len(args) > 0 else 0
        self.game = True
        self.timer = 10e22
        self.context = ctx
        self.usedWords = {}
        self.trackedPlayers = {}
        await self.omega_on(ctx)

    @commands.command()
    async def stop_omega(self, ctx):
        res = discord.Embed(title="Stopping Omega Fuse!", color=util.generate_random_color())
        await ctx.send(embed=res)
        self.winner = []
        self.usedWords = {}
        self.trackedPlayers = {}
        self.round = 0
        self.timer = 10e22
        self.game = False

    async def omega_on(self, ctx):

        loop = asyncio.get_running_loop()

        if self.game:
            self.round += 1
            # need a submission every round, so we can check that here: 

            if self.round >= 2:
                if self.round >= 4 and len(self.trackedPlayers) == 0: 
                    await self.context.send("No one joined!")
                    await self.stop_alpha(ctx)

                self.trackedPlayersPrevious = self.trackedPlayers.copy()
                for k, v in list(self.trackedPlayers.items()):
                    # v is a tuple of (lives, submitted_previous)
                    lives, submitted_previous = v
                    if not submitted_previous:
                        self.trackedPlayers[k][0] -= 1
                    self.trackedPlayers[k][1] = False
                    if self.trackedPlayers[k][0] == 0:
                        del self.trackedPlayers[k]
                
                if self.round >= 2 and len(self.trackedPlayers) == 0:
                    res = discord.Embed(title="Winners", description="\n".join([x for x in self.trackedPlayersPrevious.keys()]), color=util.generate_random_color())
                    await ctx.send(embed=res)
                    await asyncio.sleep(self.sleep)
                    await self.stop_omega(ctx)
                    return

            if self.gameMode == 0:
                self.currentLetters = alphafuseutil.generate_random_string_of_length_unbiased_unique(self.letters[self.round] if self.round < len(self.letters) - 1 else self.maxLetters)
            else: 
                self.currentLetters = alphafuseutil.generate_random_string_of_length_biased_unique(self.letters[self.round] if self.round < len(self.letters) - 1 else self.maxLetters)
            self.combinations = str(alphafuseutil.combinations_inverted(self.currentLetters))
            # currentPlayers = ", ".join([x[0] for x in self.trackedPlayers])
            round_timer = str(self.seconds[self.round]) if self.round < len(self.seconds) - 1 else str(self.minTime)
            
            res = discord.Embed(title="Round " + str(self.round), color=util.generate_random_color())
            if self.round == 1:
                res.add_field(name='\u200b', inline=False, value="You have **" + round_timer + "** second(s) to find a word! Good luck!")
                res.add_field(name='\u200b', inline=False, value="\nEnter a word **not** containing the letter(s): **" + ", ".join([x.upper() for x in self.currentLetters]) + "**")
                res.add_field(name='\u200b', inline=False, value="\nValid combinations: **" + self.combinations + "**")
                # res = "Round " + str(self.round) + "\nYou have " + round_timer + " second(s) to find a word! Good luck!" + "\nEnter a word containing the letter(s): " + ", ".join([x.upper() for x in self.currentLetters]) + "\nValid combinations: " + self.combinations
            else: 
                res.add_field(name='\u200b', inline=False, value="You have **" + round_timer + "** second(s) to find a word! Good luck!")
                res.add_field(name='\u200b', inline=False, value="\nEnter a word **not** containing the letter(s): **" + ", ".join([x.upper() for x in self.currentLetters]) + "**")
                res.add_field(name='\u200b', inline=False, value="\nValid combinations: **" + self.combinations + "**")
                res.add_field(name='\u200b', inline=False, value="\nRemaining players: " + ", ".join(list(["**" + str(x) + "**" + ": " + str(y[0]) + " lives" if y[0] > 1 else "**" + str(x) + "**" + ": " + str(y[0]) + " life" for (x,y) in self.trackedPlayers.items()])))
                # res = "Round " + str(self.round) + "\nYou have " + round_timer + " second(s) to find a word! Good luck!" + "\nEnter a word containing the letter(s): " + ", ".join([x for x in self.currentLetters]) + "\nValid combinations: " + self.combinations + "\nRemaining players: " + ", ".join(list([str(x) + ": " + str(y[0]) + " lives" for (x,y) in self.trackedPlayers.items()]))
            
            # await asyncio.sleep(2)
            await ctx.send(embed=res)
            
            # make timer last for the designated round
            if self.round < len(self.seconds) - 1:
                self.timer = loop.time() + self.seconds[self.round]
            else:
                self.timer = loop.time() + self.minTime
            
            """
            Logic for timer that recursively calls this function.
            Important for advancing rounds and resetting timer! 
            """
            while self.game:
                if (loop.time()) >= self.timer:
                    res = discord.Embed(title="Round over!", color=util.generate_random_color())
                    await ctx.send(embed=res)
                    await self.omega_on(ctx)
                    break
                await asyncio.sleep(1)
        else:
            self.timer = 10e22

    @commands.command()
    async def omega_random(self, ctx, arg1, brief="Usage: !omega_random <string>", description="Usage: !omega_random <string>, returns a single valid possibility if there exists one at random for the given character combination."):
        """
        Returns one valid word at random that satisfies the given letter combination. 
        """
        res = discord.Embed(title=alphafuseutil.get_random_possibility(arg1), color=util.generate_random_color())
        await ctx.send(embed=res)

    @commands.command(aliases=['o25'])
    async def omega_25(self, ctx, arg1, brief="Usage: !omega_25 <string>", description="Usage: !omega_25 <string>, returns a list of at most 25 possible combinations for the given character combination."):
        """
        Returns a list of up to 25 valid words that satisfy the given letter combination. 
        """
        res = discord.Embed(title=discord.Embed.Empty, description=", ".join(alphafuseutil.get_many_possibilities(arg1)), color=util.generate_random_color())
        # res.add_field(name='\u200b', inline=False, value=", ".join(alphafuseutil.get_many_possibilities(arg1)))
        await ctx.send(embed=res)

    # @commands.command(aliases=['ocheck'])
    # async def omega_check(self, ctx, arg1):
    #     """
    #     Returns "valid" or "invalid" based on the submission. 
    #     """
    #     c = "Valid" if alphafuseutil.in_wordlist(arg1) else "Invalid"
    #     res = discord.Embed(title=c, color=util.generate_random_color())
    #     await ctx.send(embed=res)

    def generate_random_color(self):
        """
        Returns a value between 0 and 16777215, the max value for int(rgb).
        """
        return random.randint(0, 256**3-1)

    @commands.command()
    async def omega_poss(self, ctx, arg1, brief="Usage: !omega_poss <string>", description="Usage: !omega_poss <strings>, returns the number of valid possibilities for the given character combination."):
        """
        Returns the number of valid combinations for the given letter combination.
        """
        res = discord.Embed(title=alphafuseutil.combinations(arg1), color=util.generate_random_color())
        await ctx.send(embed=res)

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        This method tracks messages sent by users, specific to certain games. 
        We must add valid attempts 
        """
        # if omegaFuse is on, the game is already started. 
        # Precondition: 
        # self.currentLetters is a nonempty list of characters. 
        # We add the message sender to self.trackedPlayers
        if not message.author.bot and self.game:
            
            channel = message.channel
            word = message.content
            """
            On first round, 
            Add message.author to self.trackedPlayers if the word is valid, and prevent them from typing. 
            """ 

            # only accept words if: 
            # 1) they are not eliminated
            # 2) have not submitted a valid word already
            # if message.author.name not in self.eliminatedPlayers and self.trackedPlayers[message.author.name][1] == False:
            if alphafuseutil.check_valid_inverted(self.currentLetters, word):
                keys = self.usedWords.keys()

                if word in keys:
                    await message.add_reaction('❌')
                    user, rnd = self.usedWords[word]
                    if message.author.name == user:
                        await channel.send("What " + user + "? You already used this word in round " + str(rnd) + "! Use another word! (no penalty)")
                    else:
                        if self.round <= 3:
                            if message.author.name not in self.trackedPlayers:
                                self.trackedPlayers[message.author.name] = [self.defaultLifeCount - self.round, True]
                            self.usedWords[word] = [message.author.name, self.round]
                            self.trackedPlayers[message.author.name][0] -= 1 if self.trackedPlayers[message.author.name][0] > 0 else 0
                            self.trackedPlayers[message.author.name][1] = True
                            await channel.send("Unlucky, **" + word + "** was already used by " + user + " on round " + str(rnd) + "! (-1 life)")
                
                else: 
                    if message.author.name not in self.trackedPlayers:
                        if self.round <= 3:
                            self.trackedPlayers[message.author.name] = [self.defaultLifeCount + 1 - self.round, True]
                            self.usedWords[word] = [message.author.name, self.round]
                            await message.add_reaction('✅')
                    else: 

                        self.usedWords[word] = [message.author.name, self.round]
                        self.trackedPlayers[message.author.name][1] = True
                        await message.add_reaction('✅')



def setup(bot): 
    bot.add_cog(OmegaFuse(bot))
