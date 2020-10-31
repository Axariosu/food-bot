import util.util as util
import util.reactiontimeutil as rtu
import discord
import asyncio

class ReactionTime():
    def __init__(self, ctx, maxRound, minTime, maxTime, delay):
        self.game = True
        self.ctx = ctx
        self.maxRound = maxRound
        self.minTime = minTime
        self.maxTime = maxTime
        self.round = 0
        self.delay = delay
        self.trackedPlayers = {}
        self.cannotAnswer = []
        self.currentRoundMessage = None
        self.acceptingAnswer = False
        self.timer = 0
        self.minReactionSpeed = [1e100, None]
        self.tooearly = []
    
    async def start(self):
        res = discord.Embed(title="Reaction Time", description="A reaction game (or, maybe ping diff) for you!", color=util.generate_random_color())
        res.add_field(inline=False, name="Rules", value="Type anything in chat to get a point, but only after my message changes!\nIf you type too early, you won't be able to get the points for the round!")
        res.add_field(inline=False, name="Time Control", value="There are " + util.bold(self.maxRound) + " rounds in this game!\nMy messages will change between " + util.bold(self.minTime) + " and " + util.bold(self.maxTime) + " seconds!\nIf no one types within " + util.bold(self.minTime) + " seconds, no one gets the point!\nNote: I don't take into account my or your pings to discord servers, so that's added onto your reaction times! Blame internet, **not** food!")
        res.add_field(inline=False, name="\u200b", value="The game begins in " + util.bold(self.delay) + " seconds!")
        await self.ctx.send(embed=res)
        await asyncio.sleep(self.delay)
        if self.game:
            res = discord.Embed(title="Let's begin!")
            await self.ctx.send(embed=res)
            await self.reaction_loop()

    async def reaction_loop(self):
        loop = asyncio.get_running_loop()
        self.round += 1
        if self.game:
            if (self.round > self.maxRound):
                await self.stop()
                return
            res = discord.Embed(title="Reaction Time Round " + str(self.round) + " of " + str(self.maxRound), description="Wait to type something after this message changes!", color=util.generate_random_color())
            self.msgid = await self.ctx.send(embed=res)
            self.tooearly = []
            self.acceptingAnswer = False
            await asyncio.sleep(await rtu.generate_random_time(self.minTime, self.maxTime))
            self.acceptingAnswer = True
            res = discord.Embed(title="Reaction Time Round " + str(self.round) + " of " + str(self.maxRound), description="Type something now!", color=util.generate_random_color())
            await self.msgid.edit(embed=res)

            self.timer = loop.time() + self.minTime
            while True:
                if (loop.time()) >= self.timer:
                    res = discord.Embed(title="Round Over!")
                    await self.ctx.send(embed=res)
                    await asyncio.sleep(2)
                    await self.reaction_loop()
                    break
                await asyncio.sleep(0.5)

    async def stop(self):
        self.game = False
        sorted_leaderboard = sorted(self.trackedPlayers.items(), key=lambda x: x[1], reverse=True)
        res = discord.Embed(title="Leaderboard", description="\n".join([str(k) + ": " + str(v) for (k, v) in sorted_leaderboard]), color=util.generate_random_color())
        await self.ctx.send(embed=res)
        await asyncio.sleep(1)
        res = discord.Embed(title="Fastest Reaction", description=util.bold(str(self.minReactionSpeed[1]) + ": `" + str(round(self.minReactionSpeed[0] * 1000, 3)) + "ms`"), color=util.generate_random_color())
        await self.ctx.send(embed=res)
        res = discord.Embed(title="Reaction Time Over!")
        await self.ctx.send(embed=res)
        del self
        self.ctx.bot.games.pop(self.ctx.guild.id)

    async def handle_on_message(self, message):
        if self.acceptingAnswer and message.author.name not in self.tooearly:
            self.acceptingAnswer = False
            self.timer = 0
            if message.author.name not in self.trackedPlayers:
                self.trackedPlayers[message.author.name] = 1
            else: 
                self.trackedPlayers[message.author.name] += 1
            reactionTime = message.created_at - self.msgid.edited_at
            if (reactionTime.total_seconds()) < self.minReactionSpeed[0]:
                self.minReactionSpeed = [reactionTime.total_seconds(), message.author.name]
            await self.ctx.send(message.author.name + " got it in **`" + str(round((reactionTime.total_seconds()) * 1000, 3)) + "ms`** !")
        else:
            self.tooearly.append(message.author.name)

    async def handle_on_reaction_add(self, reaction, user):
        pass
    async def handle_on_reaction_remove(self, reaction, user):
        pass