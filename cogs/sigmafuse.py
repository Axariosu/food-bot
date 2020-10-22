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
    

class SigmaFuse(commands.Cog):
    
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
        self.trackedPlayersPrevious = {}
        self.winner = []
        self.eliminatedPlayers = []
        self.combinations = ""
        self.maxLetters = 8
        self.defaultLifeCount = 3
        self.sleep = 3


    @commands.Cog.listener()
    async def on_ready(self):
        print('cog.sigmafuse successfully loaded!')
        
    @commands.command(aliases=['sigma'])
    async def start_sigma(self, ctx, *args):
        res = discord.Embed(title="Starting Sigma Fuse!", color=util.generate_random_color())
        res.add_field(name="Rules", inline=False, value="Players have some time per round to find a word that contains the displayed letters **in order**.\nIf you repeat a word someone else used, you lose a life!\nIf you repeat your own word, there's no penalty.")
        await ctx.send(embed=res)
        self.round = 0
        self.gameMode = int(args[0]) if len(args) > 0 else 0
        self.game = True
        self.timer = 10e22
        self.context = ctx
        self.usedWords = {}
        self.trackedPlayers = {}
        await self.sigma_on(ctx)

    @commands.command()
    async def stop_sigma(self, ctx):
        res = discord.Embed(title="Stopping Sigma Fuse!", color=util.generate_random_color())
        await ctx.send(embed=res)
        self.winner = []
        self.usedWords = {}
        self.trackedPlayers = {}
        self.round = 0
        self.timer = 10e22
        self.game = False

    async def sigma_on(self, ctx):

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
                    await self.stop_alpha(ctx)
                    return

            if self.gameMode == 0:
                self.currentLetters = alphafuseutil.generate_random_string_of_length_unbiased_in_order(self.letters[self.round] if self.round < len(self.letters) - 1 else self.maxLetters)
            else: 
                self.currentLetters = alphafuseutil.generate_random_string_of_length_biased_in_order(self.letters[self.round] if self.round < len(self.letters) - 1 else self.maxLetters)
            self.combinations = str(alphafuseutil.combinations_in_order(self.currentLetters))
            # currentPlayers = ", ".join([x[0] for x in self.trackedPlayers])
            round_timer = str(self.seconds[self.round]) if self.round < len(self.seconds) - 1 else str(self.minTime)
            
            res = discord.Embed(title="Round " + str(self.round), color=util.generate_random_color())
            if self.round == 1:
                res.add_field(name='\u200b', inline=False, value="You have **" + round_timer + "** second(s) to find a word! Good luck!")
                res.add_field(name='\u200b', inline=False, value="\nEnter a word containing the letter(s) in order: **" + ", ".join([x.upper() for x in self.currentLetters]) + "**")
                res.add_field(name='\u200b', inline=False, value="\nValid combinations: **" + self.combinations + "**")
                # res = "Round " + str(self.round) + "\nYou have " + round_timer + " second(s) to find a word! Good luck!" + "\nEnter a word containing the letter(s): " + ", ".join([x.upper() for x in self.currentLetters]) + "\nValid combinations: " + self.combinations
            else: 
                res.add_field(name='\u200b', inline=False, value="You have **" + round_timer + "** second(s) to find a word! Good luck!")
                res.add_field(name='\u200b', inline=False, value="\nEnter a word containing the letter(s) in order: **" + ", ".join([x.upper() for x in self.currentLetters]) + "**")
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
                    await self.sigma_on(ctx)
                    break
                await asyncio.sleep(1)
        else:
            self.timer = 10e22

    @commands.command()
    async def sigma_random(self, ctx, arg1, brief="Usage: !sigma_random <string>", description="Usage: !sigma_random <string>, returns a single valid possibility if there exists one at random for the given character combination."):
        """
        Returns one valid word at random that satisfies the given letter combination. 
        """
        res = discord.Embed(title=alphafuseutil.get_random_possibility_in_order(arg1), color=util.generate_random_color())
        await ctx.send(embed=res)

    @commands.command(aliases=['s25'])
    async def sigma_25(self, ctx, arg1, brief="Usage: !sigma_25 <string>", description="Usage: !sigma_25 <string>, returns a list of at most 25 possible combinations for the given character combination."):
        """
        Returns a list of up to 25 valid words that satisfy the given letter combination. 
        """
        res = discord.Embed(title=discord.Embed.Empty, description=", ".join(alphafuseutil.get_many_possibilities_in_order(arg1)), color=util.generate_random_color())
        # res.add_field(name='\u200b', inline=False, value=", ".join(alphafuseutil.get_many_possibilities_in_order(arg1)))
        await ctx.send(embed=res)

    # @commands.command(aliases=['scheck'])
    # async def sigma_check(self, ctx, arg1):
    #     """
    #     Returns "valid" or "invalid" based on the submission. 
    #     """
    #     c = "Valid" if alphafuseutil.in_wordlist(arg1) else "Invalid"
    #     res = discord.Embed(title=c, color=util.generate_random_color())
    #     await ctx.send(embed=res)

    @commands.command()
    async def sigma_poss(self, ctx, arg1, brief="Usage: !sigma_poss <string>", description="Usage: !sigma_poss <strings>, returns the number of valid possibilities for the given character combination."):
        """
        Returns the number of valid combinations for the given letter combination.
        """
        res = discord.Embed(title=alphafuseutil.combinations_in_order(arg1), color=util.generate_random_color())
        await ctx.send(embed=res)

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        This method tracks messages sent by users, specific to certain games. 
        We must add valid attempts 
        """
        # if sigmaFuse is on, the game is already started. 
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
            if alphafuseutil.check_valid_in_order(self.currentLetters, word):
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
    bot.add_cog(SigmaFuse(bot))
