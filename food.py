import os
import uuid
import discord
from dotenv import load_dotenv
from discord.ext import commands

# from alphafuse import AlphaFuse
from player import Player

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

__COGS__ = ['alphafuse.py']
# GUILD = os.getenv('DISCORD_GUILD')

# client = discord.Client()

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# @bot.command(name='alpha')
# async def alpha(ctx):
#     message = 'Starting Alpha Fuse!'
#     # AlphaFuse.__init__(bot)
#     await ctx.send(message)

@bot.command()
async def quit(ctx):
    message = 'Quitting!'
    await ctx.send(message)
    await bot.logout()

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename in __COGS__ :
        # bot.load_extension(f'cogs.alphafuse.py'[:-3])
        bot.load_extension(f'cogs.{filename[:-3]}')

# @bot.event
# async def on_message(message):
#     if message.content.startswith('$greet'):
#         channel = message.channel
#         await channel.send('Say hello!')

#         def check(m):
#             return m.content == 'hello' and m.channel == channel

#         msg = await client.wait_for('message', check=check)
#         await channel.send('Hello {.author}!'.format(msg))

# bot.add_cog(AlphaFuse(bot))

# @client.event
# async def on_ready():
#     for guild in client.guilds:
#         # if guild.name == GUILD:
#             # break

#         print(
#             f'{client.user} is connected to the following guild:\n'
#             f'{guild.name}(id: {guild.id})'
#         )

#client.run(TOKEN)
bot.run(TOKEN)