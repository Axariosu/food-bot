
import util.fourplayutil as fourplayutil
import util.util as util
import uuid
import discord
import asyncio
import random
import time
from discord.ext import tasks
from discord.ext import commands

# https://emojipedia.org/

class Fourplay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = False
        self.context = None
        self.msgid = 0
        self.finished_games = 0
        self.created_channels = {}
        self.created_roles = []
        self.tracked_players = []
        self.round_timer = 25
        self.ready_up = 30
        self.timer = 10e22
        self.emojiMap = {'1️⃣': 0, '2️⃣': 1, '3️⃣': 2, '4️⃣': 3, '5️⃣': 4, '6️⃣': 5, '7️⃣': 6}

    # TODO: 
    # minimax for odd player games so the bot can play against someone as well (?)
    # timer .. might be weird.
    # if player doesn't respond within x seconds, place piece at random for the player
    # wait till all games are finished / have finished result, end game automatically 
    #     if game finished, count += 1, if count == len(self.created_channels), call ctx.stop
    # within util file, check for valid placement (if column is too high, reprompt for another column)
    # msg / getBoard function to be replaced by emojis 
    
    # xey = x*10**y
    # in keyword searches type (?) 
    # 

    @commands.Cog.listener()
    async def on_ready(self):
        print('cog.fourplay successfully loaded!')

    # @commands.command(hidden=True)
    # async def check_games(self, ctx):
    #     loop = asyncio.get_running_loop()
    #     self.timer = loop.time() + 5
    #     while self.game:
    #         # print(self.timer, loop.time())
    #         if (loop.time()) >= self.timer:
    #             # res = discord.Embed(title="Round over!", color=util.generate_random_color())
    #             # for channel in self.created_channels:
    #                 # await channel.send(embed=res)
    #             if self.finished_games >= len(self.created_channels):
    #                 for channel in self.created_channels:
    #                     await channel.send("All games are finished! Fourplay will end in 15 seconds.")
    #                 await asyncio.sleep(15)
    #                 await self.stop_fourplay(ctx)
    #             await self.check_games(ctx)
    #             break

    @commands.command()
    async def fourplay_on(self, ctx):
        # create channel -> post board 
        # assign players 1, 2
        # wait for player 1's move 

        # message has board, board has player ids
        
        for channel in self.created_channels:
            board = self.created_channels[channel]
            # boardString = board.getBoard()
            res = discord.Embed(title=board.player1.name + " vs. " + board.player2.name, color=util.generate_random_color())
            res.add_field(name='\u200b', inline=False, value=board.getBoard())
            msg = await channel.send(embed=res)
            # add reactions 1-7, a one-time operation per board (might be heavy but executes one at a time)
            # may need to convert to on_message instead
            await msg.add_reaction('1️⃣')
            await msg.add_reaction('2️⃣')
            await msg.add_reaction('3️⃣')
            await msg.add_reaction('4️⃣')
            await msg.add_reaction('5️⃣')
            await msg.add_reaction('6️⃣')
            await msg.add_reaction('7️⃣')
            # await channel.send("Player 1:" + board.player1.name + "\nPlayer 2:" + board.player2.name)
        # await self.check_games(ctx)


    @commands.command(aliases=['4p', 'c4', 'connect', 'fourplay'])
    async def start_fourplay(self, ctx):
        self.context = ctx
        res = discord.Embed(title="Starting Fourplay!", color=util.generate_random_color())
        res.add_field(name="Rules", inline=False, value="You have **" + str(self.ready_up) + "** seconds to join! React to this message to play!\nIf there are an odd number of players, one of you won't have an opponent. That one person will play me instead!")
        res.add_field(name="How to Win", inline=False, value="Line up **4** chips against your opponent, and you win!")
        res.add_field(name="Time Control", inline=False, value="If your opponent doesn't respond within **15** seconds, I will make a move for them!")
        # res.add_field(name="\u200b", inline=False, value="I have a code of length **" + str(self.code_length) + "**, you're meant to guess it!")
        # res.add_field(name="\u200b", inline=False, value="Each round is **20** seconds, I'll tell you how many Bulls and Cows you have.")
        # res.add_field(name="\u200b", inline=False, value="A **Bull** is a **correct number and in correct place.**\nA **Cow** is a **correct number but in an incorrect place.**\nFor example, if my code is **5688** and you guess **1234**, I'll tell you you have **0** Bulls and **0** Cows!\nIf you guess **6518**, I'll tell you you have **1** Bull and **2** Cows!")
        # res.add_field(name="\u200b", inline=False, value="To minimize peeking, I'll make a channel just for you! (and sneaky admins)\nI will only respond to messages in that channel, so enter your submissions there!")
        msg = await ctx.send(embed=res)
        self.msgid = msg.id
        self.game = True
        self.context = ctx
        self.created_channels = {}
        self.tracked_players = []

        await msg.add_reaction("\u2705")
        await asyncio.sleep(self.ready_up)

        guild = ctx.guild

        if len(self.tracked_players) == 0: 
            await ctx.send("No one joined!")
            await self.stop_fourplay(ctx)

        # print(type(self.tracked_players))
        # random.shuffle(self.tracked_players)
        # need to check for odd players
        for i in range(0, (len(self.tracked_players) if len(self.tracked_players) % 2 == 0 else (len(self.tracked_players) - 1)), 2):
            uuid_short = str(uuid.uuid4())[:8]
            role = await guild.create_role(name=uuid_short)
            uuid_role = discord.utils.get(guild.roles, name=uuid_short)

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                uuid_role: discord.PermissionOverwrite(read_messages=True)
            }

            channel = await guild.create_text_channel(uuid_short, overwrites=overwrites, topic="Secret channel just for and your opponent! (and admins)")
            
            b = fourplayutil.Board()
            b.player1 = self.tracked_players[i]
            b.player2 = self.tracked_players[i+1]

            self.created_channels.setdefault(channel, b)
            self.created_roles.append(role)
            
            await self.tracked_players[i].add_roles(uuid_role)
            await self.tracked_players[i+1].add_roles(uuid_role)
        await self.fourplay_on(ctx)

    @commands.command()
    async def stop_fourplay(self, ctx):
        res = discord.Embed(title="Fourplay over!", color=util.generate_random_color())
        await ctx.send(embed=res)

        for channel in self.created_channels:
            await channel.delete()
        for role in self.created_roles:
            await role.delete()
        self.created_channels = {}
        self.created_roles = []
        self.tracked_players = []
        self.timer = 1e22
        self.game = False

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.id == self.msgid and not user.bot and user not in self.tracked_players:
            self.tracked_players.append(user)
        # print(reaction)
        # print(reaction.emoji)
        # not the bot game
        if reaction.message.channel in self.created_channels and not user.bot:
            board = self.created_channels[reaction.message.channel]
            if not board.placePiece(self.emojiMap[reaction.emoji], user):
                pass
            else: 
                res = discord.Embed(title=board.player1.name + " vs. " + board.player2.name, description=board.getBoard())
                await reaction.message.edit(embed=res)
                (p1, p2) = board.checkWin()
                if p1:
                    self.finished_games += 1
                    res = discord.Embed(title=board.player1.name + " Wins!", color=util.generate_random_color())
                    await reaction.message.channel.send(embed=res)
                if p2: 
                    self.finished_games += 1
                    res = discord.Embed(title=board.player2.name + " Wins!", color=util.generate_random_color())
                    await reaction.message.channel.send(embed=res)
            
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.message.id == self.msgid and not user.bot:
            self.tracked_players.remove(user)

    # @commands.Cog.listener() 
    # async def on_message(self, message):
    #     if not message.author.bot and self.game and message.channel in self.created_channels:
            
    #         board = self.created_channels[message.channel]
    #         # for channel, board in message.channel:
    #         if message.author == board.player1 and board.turn == 1:
    #             board.placePiece(int(message.content), message.author)
    #             await message.channel.send(board.getBoard())
    #         if message.author == board.player2 and board.turn == 2:
    #             board.placePiece(int(message.content), message.author)
    #             await message.channel.send(board.getBoard())



def setup(bot): 
    bot.add_cog(Fourplay(bot))