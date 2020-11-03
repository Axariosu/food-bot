import util.util as util
import discord
import asyncio
import util.jpegtionaryutil as jpegtionaryutil
import threading, queue
from PIL import Image
import io
import uuid
import math

# With thanks to: 
# https://stackoverflow.com/questions/63209888/send-pillow-image-on-discord-without-saving-the-image
# https://stackoverflow.com/questions/63422822/attach-a-file-in-an-embed-discord-py



class JPEGtionary():
    def __init__(self, ctx, max_round, hangman):
        self.ctx = ctx
        self.game = False
        self.timer = 0
        self.round_timer = 100
        self.current_round_timer = 0
        self.round = 0
        self.max_round = max_round
        self.hangman = hangman
        self.delay = 10
        self.trackedPlayers = {}
        self.answer = ""
        self.image_list = None
        self.queue = queue.Queue()
        self.mosaic_size = 4
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
        queue.put([word, jpegtionaryutil.generate_unpixellating_pictures(word, self.mosaic_size)])
        print("done")

    async def start(self):
        self.game = True
        res = discord.Embed(title="JPEGtionary", description="", color=util.generate_random_color())
        res.add_field(name="Rules", inline=False, value="Every round, **food** has a **secret word**!\nYour task is to find out what **food's word** is!\nEvery round, pictures of the word will be shown!\nGuess food's word correctly, and rack up points!\nThe earlier you do so, the more points you will get!\nThe game starts in 10 seconds!")
        await self.ctx.send(embed=res)
        wordlist = jpegtionaryutil.generate_list_of_words(self.max_round)
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
        # TESTING
        # self.current_image.show()
        # threading.Thread(target=self.image_queue_next, args=(self.current_image, self.image_queue, self.current_blur)).start()
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
                res = discord.Embed(title="JPEGtionary Round " + str(self.round) + " of " + str(self.max_round), footer="Image " + str(self.internal_round) + " of " + str(round(math.log2(self.image_list[self.internal_round].width))), description=discord.Embed.Empty if not self.hangman else jpegtionaryutil.generate_hangman(self.answer), color=util.generate_random_color())
                res.set_image(url=f'attachment://{unique}.jpeg')
                await self.ctx.send(embed=res, file=f)
                self.current_round_timer = loop.time() + self.round_timer / len(self.image_list)
                self.internal_round += 1

            if loop.time() >= self.timer:
                res = discord.Embed(title="Round Over!", description="The answer was: " + self.answer)
                await self.ctx.send(embed=res)
                await asyncio.sleep(2)
                await self.template_loop()
                break
            await asyncio.sleep(0.5)

        # while self.current_blur < 11: 
            # if self.timer == 0:
                # break
            # if loop.time() >= self.timer:
        # some magic
        # image_binary = io.BytesIO()
        # image = self.current_image
        # image.save(image_binary, 'jpeg')
        # image_binary.seek(0)
        # unique = uuid.uuid4()
        # f = discord.File(fp=image_binary, filename=f'{unique}.jpeg')
        # res = discord.Embed(title="JPEGtionary Round " + str(self.round) + " of " + str(self.max_round), author="food", footer=discord.Embed.Empty if not self.hangman else jpegtionaryutil.generate_hangman(self.answer), color=util.generate_random_color())
        # res.set_image(url=f'attachment://{unique}.jpeg')
        # # await self.ctx.send(file=f)
        # await self.ctx.send(embed=res, file=f)
        #     # threading.Thread(target=self.image_queue_next, args=(self.current_image, self.image_queue, self.current_blur)).start()
        #     # self.timer = loop.time() + self.roundTime // 10
        # # await asyncio.sleep(0.5)
        # await self.stop()
        # self.current_blur = 0
        # res = discord.Embed(title="Round Over!", description="The answer was: " + self.answer)
        # await self.ctx.send(embed=res)
        # await asyncio.sleep(2)
        # await self.template_loop() # TODO: CHANGE THIS FN NAME

    async def stop(self):
        sortedPlayers = sorted(self.trackedPlayers.items(), key=lambda x: x[1], reverse=True)
        res = discord.Embed(title="Leaderboards", description="\n".join([(str(i[0]) + ": " + str(i[1])) for i in sortedPlayers]), color=util.generate_random_color())
        await self.ctx.send(embed=res)        
        res = discord.Embed(title="JPEGtionary Over!", color=util.generate_random_color())
        await self.ctx.send(embed=res)
        self.ctx.bot.games.pop(self.ctx.guild.id)

    async def handle_on_message(self, message):
        if message.content.lower() == self.answer and self.accepting_answers:
            points = math.log2(self.image_list[self.internal_round].width) - self.internal_round
            self.accepting_answers = False
            self.timer = 0
            await message.add_reaction('✅')
            if message.author.name not in self.trackedPlayers:
                self.trackedPlayers[message.author.name] = points
            else: 
                self.trackedPlayers[message.author.name] += points
            await self.ctx.send(message.author.name + " got it for `" + str(points) + "` points!")
        pass

    async def handle_on_reaction_add(self, reaction, user):
        pass

    async def handle_on_reaction_remove(self, reaction, user):
        pass