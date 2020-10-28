import os, re, asyncio
import uuid
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import CommandNotFound

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

__COGS__ = ['alphafuse.py']
GUILD = os.getenv('DISCORD_GUILD')

# client = discord.Client()

bot = commands.Bot(command_prefix="!")

"""
Two dictionaries to start and stop games -- definitely a better way to manage this
startdict (sd)
stopdict (pd)
extension (ext)
"""
td = {
    'alpha': 'alpha', 
    'omega': 'omega',
    'sigma': 'sigma',
    'udder': 'udder', 
    'c4': 'fourplay',
    '4p': 'fourplay', 
    'schwootsh': 'schwootsh',
    'pow': 'pow',
    'wop': 'wop',
    'unscramble': 'unscramble',
}
pd = {
    'alpha': 'stop_alpha', 
    'udder': 'stop_udder',
    'sigma': 'stop_sigma',
    'omega': 'stop_omega',
    'c4': 'stop_fourplay',
    '4p': 'stop_fourplay', 
    'schwootsh': 'stop_schwootsh',
    'pow': 'stop_pow',
    'wop': 'stop_wop',
    'unscramble': 'stop_unscramble',
}
ext = {
    'alpha': 'alphafuse',
    'omega': 'omegafuse',
    'sigma': 'sigmafuse',
    'udder': 'uddercode',
    'c4': 'fourplay',
    '4p': 'fourplay',
    'schwootsh': 'schwootsh',
    'pow': 'pow', 
    'wop': 'wop',
    'unscramble': 'unscramble',
}

bot.games = {}

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def quit(ctx):
    message = 'Quitting!'
    await ctx.send(message)
    await bot.logout()

@bot.command()
async def load(ctx, extension):
    if extension in ext:
        bot.load_extension(f'cogs.{ext[extension]}')
    else:
        bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    if extension in ext:
        bot.unload_extension(f'cogs.{ext[extension]}')
    else:
        bot.unload_extension(f'cogs.{extension}')

@bot.command()
async def reload(ctx, extension):
    if extension in ext:
        bot.unload_extension(f'cogs.{ext[extension]}')
        bot.load_extension(f'cogs.{ext[extension]}')
    else:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')

@bot.command()
async def avatar(ctx, *, avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)

@bot.command()
async def start(ctx, arg1):
    # print(bot.get_command(td[arg1])
    await ctx.invoke(bot.get_command(td[arg1]))

@bot.command()
async def stop(ctx, arg1):
    await ctx.invoke(bot.get_command(pd[arg1]))

@bot.command()
async def commandlist(ctx):
    helptext = "```"
    for command in bot.commands:
        helptext+=f"{command}\n"
    helptext+="```"
    await ctx.send(helptext)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

for filename in os.listdir('./cogs'):
    # if filename in __COGS__:
    #     bot.load_extension(f'cogs.alphafuse.py'[:-3])
    if filename != "__pycache__":
        bot.load_extension(f'cogs.{filename[:-3]}')


# create game module? or something 
# ctx of where the command is called 
# -> run that game in that context (?) 


# game in different class 
# -> where to store the timers asyncio.sleep or loop.time() cog (?) 
# !start game -> (create instance of class, and somehow run that instance on a server)
# dictionary (guildid : class instance)
# class Game: .... and when you run it first make an instance like game = Game(some arguments) and then call game.start
# bot.games = {}; bot.games[ctx.guild.id] = Game(); and on every command, you do: game = bot.games.get(ctx.guild.id); 
# how to include on_message in this? 
# you make it so it only listens to messages within its specified server
# check if game is None, if it's not, then game will be the Game instance of that guild, where you can then call it's methods to do stuff on the game
# -> APScheduler



# on_message 
# main file: global ? dictionary -> 
# global game dict (has all games) 
# 
# inside start command: i get guildid, guildid as argument into the game? 
# save the guildid within the cog class, do some functionality with that? << 
# dictionary {guildid : self.game (?)}
# -> run the game within the guildid

# invoke does pass additional arg 
# ctx.invoke(bot.get_command('command'), "arg", "arg")

# have the Game class with all the attributes related to the game; then on that class, make methods that will be the game functionality; then you use commands to call those methods
# when initializing the game, you create a new instance of Game, and store it as the value of a dict, where the key is the guild id, and the other commands the the existing game from that dict, and call the required functions

# -> make game from scratch using this idea ^ 

# @bot.command()
# async def gamequeue(ctx, *args):
    
#     for cog in bot.cogs:
#         for command in bot.get_cog(f'{cog}').get_commands():
#             print(command.name)
    
#     print(bot.get_cog('Wop').is_running())
#         # for c in cog:
#             # print(c.commands)



# _mentions_transforms = {
#     '@everyone': '@\u200beveryone',
#     '@here': '@\u200bhere'
# }

# _mention_pattern = re.compile('|'.join(_mentions_transforms.keys()))

# @asyncio.coroutine
# def _default_help_command(ctx, *commands : str):
#     """Shows this message."""
#     bot = ctx.bot
#     destination = ctx.message.author if bot.pm_help else ctx.message.channel

#     def repl(obj):
#         return _mentions_transforms.get(obj.group(0), '')

#     # help by itself just lists our own commands.
#     if len(commands) == 0:
#         pages = bot.formatter.format_help_for(ctx, bot)
#     elif len(commands) == 1:
#         # try to see if it is a cog name
#         name = _mention_pattern.sub(repl, commands[0])
#         command = None
#         if name in bot.cogs:
#             command = bot.cogs[name]
#         else:
#             command = bot.commands.get(name)
#             if command is None:
#                 yield from bot.send_message(destination, bot.command_not_found.format(name))
#                 return

#         pages = bot.formatter.format_help_for(ctx, command)
#     else:
#         name = _mention_pattern.sub(repl, commands[0])
#         command = bot.commands.get(name)
#         if command is None:
#             yield from bot.send_message(destination, bot.command_not_found.format(name))
#             return

#         for key in commands[1:]:
#             try:
#                 key = _mention_pattern.sub(repl, key)
#                 command = command.commands.get(key)
#                 if command is None:
#                     yield from bot.send_message(destination, bot.command_not_found.format(key))
#                     return
#             except AttributeError:
#                 yield from bot.send_message(destination, bot.command_has_no_subcommands.format(command, key))
#                 return

#         pages = bot.formatter.format_help_for(ctx, command)

#     if bot.pm_help is None:
#         characters = sum(map(lambda l: len(l), pages))
#         # modify destination based on length of pages.
#         if characters > 1000:
#             destination = ctx.message.author

#     for page in pages:
#         yield from bot.send_message(destination, page)

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