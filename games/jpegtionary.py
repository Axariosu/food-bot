import util.util as util
import discord
import asyncio
import util.jpegtionaryutil as jpegtionaryutil
import util.triviautil as triviautil
import threading, queue
from PIL import Image
import io
import uuid
import math

# With thanks to: 
# https://stackoverflow.com/questions/63209888/send-pillow-image-on-discord-without-saving-the-image
# https://stackoverflow.com/questions/63422822/attach-a-file-in-an-embed-discord-py

wordlistDictionary = {"10000": "wordlist_10000.txt", 
    "lol": "wordlist_league_of_legends.txt", 
}

class JPEGtionary():
    def __init__(self, ctx, max_round, hangman, wordlist, similarity, picture_amount):
        self.ctx = ctx
        self.game = False
        self.timer = 0
        self.round_timer = 100
        self.current_round_timer = 0
        self.round = 0
        self.similarity = 90
        self.max_round = max_round
        self.hangman = hangman
        self.wordlist = wordlist
        self.delay = 10
        self.trackedPlayers = {}
        self.answer = ""
        self.image_list = None
        self.queue = queue.Queue()
        self.mosaic_size = picture_amount
        self.msgid = None
        self.internal_round = 0

    def __del__(self):
        print("killed jpegtionary")
        pass

    def initialize_queue(self, word, queue):
        """
        Given a word and a queue: 
        Enqueues [word, image]. 
        """
        print(word)
        if self.wordlist == "lol":
            query = "league of legends " + word
        queue.put([word, jpegtionaryutil.generate_unpixellating_pictures(query, self.mosaic_size)])
        print("done")

    async def start(self):
        self.game = True
        res = discord.Embed(title="JPEGtionary", description="", color=util.generate_random_color())
        res.add_field(name="Rules", inline=False, value="Every round, **food** has a **secret word**!\nYour task is to find out what **food's word** is!\nEvery round, pictures of the word will be shown!\nGuess food's word correctly, and rack up points!\nThe earlier you do so, the more points you will get!\nThe game starts in 10 seconds!")
        await self.ctx.send(embed=res)
        f = open(wordlistDictionary[self.wordlist], "r")
        wl = [x.strip() for x in f]
        wordlist = util.generate_random_words_from_wordlist(self.max_round, wl)
        threads = [threading.Thread(target=self.initialize_queue, args=(word, self.queue)) for word in wordlist]
        for thread in threads:
            thread.daemon = True
            thread.start() # time scales based on self.mosaic_size
        
        await asyncio.sleep(self.delay)
        res = discord.Embed(title="Let's begin!", color=util.generate_random_color())
        await self.ctx.send(embed=res)
        await self.template_loop()

    async def template_loop(self):
        
        loop = asyncio.get_running_loop()

        self.round += 1
        if (self.round > self.max_round):
            await self.stop()
            return
        
        self.answer, self.image_list = self.queue.get()
        self.accepting_answers = True

        self.timer = loop.time() + self.round_timer
        self.current_round_timer = loop.time()
        self.internal_round = 0
        while self.game: 
            if loop.time() >= self.current_round_timer:
                image_binary = io.BytesIO()
                image = self.image_list[self.internal_round]
                image.save(image_binary, 'jpeg')
                image_binary.seek(0)
                unique = uuid.uuid4()
                f = discord.File(fp=image_binary, filename=f'{unique}.jpeg')
                res = discord.Embed(title="JPEGtionary Round " + str(self.round) + " of " + str(self.max_round), footer="Image " + str(self.internal_round) + " of " + str(len(self.image_list)), description=discord.Embed.Empty if not self.hangman else jpegtionaryutil.generate_hangman(self.answer), color=util.generate_random_color())
                res.set_image(url=f'attachment://{unique}.jpeg')
                await self.ctx.send(embed=res, file=f)
                self.current_round_timer = loop.time() + self.round_timer / len(self.image_list)
                self.internal_round += 1 if self.internal_round < len(self.image_list) else 0

            if loop.time() >= self.timer:
                image_binary = io.BytesIO()
                image = self.image_list[len(self.image_list) - 1]
                image.save(image_binary, 'jpeg')
                image_binary.seek(0)
                f = discord.File(fp=image_binary, filename=f'{self.answer}.jpeg')
                res = discord.Embed(title="Round Over!", description="The answer was: " + util.bold(self.answer))
                res.set_image(url=f'attachment://{self.answer}.jpeg')
                await self.ctx.send(embed=res, file=f)
                await asyncio.sleep(2)
                await self.template_loop()
                break
            await asyncio.sleep(0.5)

    async def stop(self):
        sortedPlayers = sorted(self.trackedPlayers.items(), key=lambda x: x[1], reverse=True)
        res = discord.Embed(title="Leaderboards", description="\n".join([(str(i[0]) + ": " + str(i[1])) for i in sortedPlayers]), color=util.generate_random_color())
        await self.ctx.send(embed=res)        
        res = discord.Embed(title="JPEGtionary Over!", color=util.generate_random_color())
        await self.ctx.send(embed=res)
        self.ctx.bot.games.pop(self.ctx.guild.id)

    async def handle_on_message(self, message):
        if triviautil.valid_guess(message.content.lower(), self.answer, self.similarity) and self.accepting_answers:
            # points = round(math.log2(self.image_list[self.internal_round].width) - self.internal_round)
            loop = asyncio.get_running_loop()
            points = round(self.timer - loop.time(), 3)
            self.accepting_answers = False
            self.timer = 0
            await message.add_reaction('✅')
            if message.author.name not in self.trackedPlayers:
                self.trackedPlayers[message.author.name] = points
            else: 
                self.trackedPlayers[message.author.name] += points
            await self.ctx.send(message.author.name + " got it for **`" + str(points) + "`** points!")
        pass

    async def handle_on_reaction_add(self, reaction, user):
        pass

    async def handle_on_reaction_remove(self, reaction, user):
        pass