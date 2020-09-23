import discord
import asyncio
import alphafuseutil
import time
import queue
# import thread
import threading

from discord.ext import commands
from discord.ext import tasks
#
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.wait_for
# https://stackoverflow.com/questions/49947814/python-threading-error-must-be-an-iterable-not-int

# from player import Player

# GLOBAL VARIABLES
__VALIDCHANNELS__= [755970868219346984, 515125639406419980]
__TRACKEDPLAYERS__ = {}
__USEDWORDS__ = {}
__COMBINATIONS__ = ""
# self.round = 0
__SECONDS__ = [30, 30, 26, 22, 19, 17, 15, 13, 11, 10]
# __SECONDS__ = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
# __SECONDS__ = [10, 10]
__LETTERS__ = [0, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7]
__CURRENTLETTERS__ = []
__THREADFLAG__ = False


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
        self.channel = self.bot.get_channel(755970868219346984)
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



    async def game_start(self, ctx):
        self.round = 0
        # await self.advance_round(ctx, time.time())
        self.game = True
        await self.alpha_on(ctx)
    
    async def game_stop(self, ctx):
        self.round = 0
        self.timer = 10e22
        self.game = False

    # async def advance_round(self, ctx, t):
    #     # t_end = t + __SECONDS__[self.round] if self.round < len(__SECONDS__) - 1 else 5
    #     # if (time.time() > t_end):
        
    #     self.round += 1
    #     __CURRENTLETTERS__ = alphafuseutil.generate_random_string_of_length_biased(__LETTERS__[self.round] if self.round < len(__LETTERS__) - 1 else 8)
    #     __COMBINATIONS__ = str(alphafuseutil.combinations(__CURRENTLETTERS__))
    #     currentPlayers = ", ".join([x[0] for x in __TRACKEDPLAYERS__])
    #     res = "Round " + str(self.round) + "\nYou have " + str(__SECONDS__[self.round]) if self.round < len(__SECONDS__) - 1 else "10" + " second(s) to find a word! Good luck!" + "\nEnter a word containing the letter(s): " + ", ".join([x for x in __CURRENTLETTERS__]) + "\nValid combinations: " + __COMBINATIONS__ + "\nRemaining players: " + currentPlayers
    #     await ctx.send(res)
        # await ctx.send("Round " + str(self.round))
        # await asyncio.sleep(1)
        # res = "You have " + str(__SECONDS__[self.round]) + " second(s) to find a word! Good luck!"
        # await ctx.send(res)
        # __CURRENTLETTERS__ = alphafuseutil.generate_random_string_of_length_biased(__LETTERS__[self.round] if self.round < len(__LETTERS__) - 1 else 8)
        # res = ", ".join([x for x in __CURRENTLETTERS__])
        # await ctx.send("Enter a word containing the letter(s): " + res)
        # res = str(alphafuseutil.combinations(__CURRENTLETTERS__))
        # await ctx.send("Valid combinations: " + res)
        # currentPlayers = ", ".join([x[0] for x in __TRACKEDPLAYERS__])
        # if currentPlayers is None: 
        #     currentPlayers = 'Currently none!'
        # await ctx.send("Remaining players: " + currentPlayers)
    
    # async def alpha_on(self, ctx):
    #     # await ctx.send("Testing: " + str(self.round))
        
    #     # loop = asyncio.get_running_loop()
    #     # end_time = loop.time() + __SECONDS__[self.round] if self.round < len(__SECONDS__) - 1 else 5

        
    #     # que = queue.Queue()
    #     loop = asyncio.get_running_loop()
    #     async def advance_round_in_timer(ctx):
    #         if self.game:
    #             self.round += 1
    #             global __CURRENTLETTERS__
    #             global __COMBINATIONS__
    #             # global __SECONDS__
    #             # calc1 = threading.Thread(target=alphafuseutil.generate_random_string_of_length_biased, args=[__LETTERS__[self.round] if self.round < len(__LETTERS__) - 1 else 8])
    #             # calc1 = threading.Thread(target=lambda q, arg1: q.put(alphafuseutil.generate_random_string_of_length_biased(arg1)), args=(que, __LETTERS__[self.round] if self.round < len(__LETTERS__) - 1 else 8))
    #             # preconditionQueue = queue.Queue()
    #             # currentLettersThread = threading.Thread(target=lambda q, arg1: q.copy(alphafuseutil.generate_random_string_of_length_biased(arg1)), args=(__CURRENTLETTERS__, __LETTERS__[self.round] if self.round < len(__LETTERS__) - 1 else 8))
    #             # currentLettersThread.start()
    #             # currentLettersThread.join()
    #             # combinationsThread = threading.Thread(target=lambda q, arg1: q.copy(str(alphafuseutil.combinations(arg1)), args=(__COMBINATIONS__, __CURRENTLETTERS__)))
    #             # combinationsThread.start()
    #             # combinationsThread.join()

    #             # currentPlayers = ", ".join([x[0] for x in __TRACKEDPLAYERS__])
                
    #             # calc1.start()
    #             # calc1.join()
    #             # while not que.empty():
    #                 # result = que.get()
    #             # print(__CURRENTLETTERS__)
    #             # print(calc1)
    #             __CURRENTLETTERS__ = alphafuseutil.generate_random_string_of_length_unbiased(__LETTERS__[self.round] if self.round < len(__LETTERS__) - 1 else 8)
    #             __COMBINATIONS__ = str(alphafuseutil.combinations(__CURRENTLETTERS__))
    #             # currentPlayers = ", ".join([x[0] for x in __TRACKEDPLAYERS__])
    #             round_timer = str(__SECONDS__[self.round]) if self.round > len(__SECONDS__) - 1 else "10"
    #             res = "Round " + str(self.round) + "\nYou have " + round_timer + " second(s) to find a word! Good luck!" + "\nEnter a word containing the letter(s): " + ", ".join([x for x in __CURRENTLETTERS__]) + "\nValid combinations: " + __COMBINATIONS__
    #             # await asyncio.sleep(2)
    #             await ctx.send(res)
                
    #             self.timer = loop.time() + __SECONDS__[self.round] if self.round > len(__SECONDS__) - 1 else 10
                
    #             while True:
    #                 # await asyncio.sleep(int(round_timer))
    #                 # await alpha_on(ctx)
    #                 # break
    #                 # await ctx.send(loop.time())
    #                 if loop.time() >= self.timer and self.game:
    #                     await ctx.send("Round over!")
    #                     await advance_round_in_timer(ctx)
    #                     break
    #                 await asyncio.sleep(0.5)
    #             # await ctx.send('Test success!')
    #         else:
    #             return
    #     await advance_round_in_timer(ctx)
        
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
            __CURRENTLETTERS__ = alphafuseutil.generate_random_string_of_length_unbiased(__LETTERS__[self.round] if self.round < len(__LETTERS__) - 1 else 8)
            __COMBINATIONS__ = str(alphafuseutil.combinations(__CURRENTLETTERS__))
            # currentPlayers = ", ".join([x[0] for x in __TRACKEDPLAYERS__])
            round_timer = str(__SECONDS__[self.round]) if self.round < len(__SECONDS__) - 1 else "10"
            res = "Round " + str(self.round) + "\nYou have " + round_timer + " second(s) to find a word! Good luck!" + "\nEnter a word containing the letter(s): " + ", ".join([x for x in __CURRENTLETTERS__]) + "\nValid combinations: " + __COMBINATIONS__
            # await asyncio.sleep(2)
            await ctx.send(res)
            
            if self.round < len(__SECONDS__) - 1:
                self.timer = loop.time() + __SECONDS__[self.round]
            else:
                self.timer = loop.time() + 10
            # self.timer = loop.time() + __SECONDS__[self.round] if self.round < len(__SECONDS__) - 1 else 10
            
            while True:
                # await asyncio.sleep(int(round_timer))
                # await alpha_on(ctx)
                # break
                # await ctx.send(loop.time())
                # if (loop.time() + 1) >= self.timer and self.game:
                if (loop.time()) >= self.timer and self.game:
                    await ctx.send("Round over!")
                    await self.alpha_on(ctx)
                    break
                await asyncio.sleep(1)
            # await ctx.send('Test success!')
        else:
            self.timer = 10e22
        await self.alpha_on(ctx)

    # @tasks.loop(seconds=5, count=5)
    # async def round_timer(self):
    #     print(round_timer.current_loop)

    # @round_timer.after_loop
    # async def after_round(self):
    #     print("post loop")
        # await self.advance_round(ctx)
        # testThread = threading.Thread(None, end_round(), testThread, ctx, {})
        # testThread.start()
        # t = threading.Timer(__SECONDS__[self.round] if self.round < len(__SECONDS__) - 1 else 5, end_round(ctx))
        # t.start()
        # else: 
            # print(time.time(), t_end)
            # await self.advance_round(ctx, t_end)
    
    # async def thread_fn(self, ctx):


    # async def end_round(self, ctx):
    #     await ctx.send("a lololol")
    #     t = threading.Timer(__SECONDS__[self.round] if self.round < len(__SECONDS__) - 1 else 5, end_round(ctx))
    #     t.start()
    #     await ctx.send("Round over!")
    #     self.advance_round(ctx)
    #     pass  

        # time.sleep(__SECONDS__[self.round] if self.round < len(__SECONDS__) - 1 else 5)
        
        # await asyncio.sleep(__SECONDS__[self.round] if self.round < len(__SECONDS__) - 1 else 5)
        
        # start = time.time()
        # while (time.time() - start < __SECONDS__[self.round] if self.round < len(__SECONDS__) - 1 else 5):
        #     pass
        # await self.advance_round(ctx)

    @commands.Cog.listener()
    async def on_ready(self):
        # self.game = True
        print('cog.alphafuse successfully loaded!')

    @commands.command()
    async def what_self_game(self, ctx):
        await ctx.send(self.game)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command()
    async def alpha(self, ctx):
        if not self.game: 
            # self.game = True
            await ctx.send("Starting Alpha Fuse!")
            await self.game_start(ctx)
            # logic = self.bot.get_cog('AlphaFuseLogic')
            # await logic.advance_round(ctx, 0)

        else:
            await self.game_stop(ctx)
            await ctx.send("Stopping Alpha Fuse!")

    # @commands.command()
    # async def force_advance(self, ctx):
    #     await self.advance_round(ctx, time)


    # @commands.command()
    # async def advance_round(self, ctx):
    #     ctx.send("test")
    # async def alpha()

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
        if not message.author.bot:
            if self.game:
                # channel = message.channel
                # if not message.author.bot:
                #     def check(message, letters):
                #         return alphafuseutil.check_valid(letters, message)
                #     # async def sst(): 
                #     #     await channel.send(message.author.name)
                #     # await sst()
                if message.channel.id in __VALIDCHANNELS__:
                    
                    if alphafuseutil.check_valid(__CURRENTLETTERS__, message.content):
                        # logic to send verification message or if the word has already been sent 
                        channel = message.channel
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
                        await message.add_reaction("\u2705")
                        # await channel.send("Valid submission, " + message.author.name + "!")

                        # else:
                        #     await channel.send("Silly " + message.author.name + ", you've already submitted a word in this round!")
                        #     """
                        #     Logic for repeated words: 
                        #     -1 life if you repeat a word someone else has already said
                        #     No penalty if you repeat a word you have already said
                        #     """
                        #     if message.content in __USEDWORDS__:
                        #         word, (user, rnd) = message.content, (__USEDWORDS__[message.content])
                        #         if message.author.name != user:
                        #             __TRACKEDPLAYERS__[message.author.name] -= 1
                                    
                        #             await channel.send("Unlucky, " + message.content + " was already used by " + user + " on round " + rnd + "! (-1 life)")
                        #         else: 
                        #             await channel.send("Silly " + message.author.name + ", you've already used this word! (no penalty)")
                            
                        
                        
                        
                        
                        
                        # channel = message.channel
                        
                # if self.game:
                    # message.content
                    # print(message)
                    # print(message.author.bot)
                    
                        # channel = message.channel
                        # await channel.send(message.content)
    

    # @commands.Cog.listener()
    



def setup(bot): 
    bot.add_cog(AlphaFuse(bot))

    # @bot.event
    # async def on_message(self, ctx):

        # await ctx.send('hello')
        # if message.content.startswith('$greet'):
        #     channel = message.channel
        #     await channel.send('Say hello!')

        #     def check(m):
        #         return m.content == 'hello' and m.channel == channel

        #     msg = await client.wait_for('message', check=check)
        #     await channel.send('Hello {.author}!'.format(msg))

    # async def my_message(message):
    #     pass
    
    # async def add_to_tracked(self, id):
    #     """
    #     Adds the player to trackedplayers. 
    #     """
    #     if not tracked_players.get(id):
    #         tracked_players[id] = Player(id)

    # async def game_start(self, ctx):
        # """
        # Starts the game, players have 60 seconds to type in their first answer. 
        # """

        # message = 'Starting Alpha Fuse!'
        # await ctx.send(message)
        # bot.add_listener
        # pass

    # async def bot_round(self):
    #     """
    #     Picks x characters, maximum of 5 and timer.
    #     """
    #     pass
    #     # for player in self.ingame:
    #     #     player.