from discord.ext import tasks
from discord.ext import commands
from discord.ext import menus
from discord import app_commands
import discord
import util.util as util
import asyncio
import random
import time


class CustomHelp(menus.Menu):
    def __init__(self, command_name):
        super().__init__()
        self.command_name = command_name

    # async def embed_creator(self, command_name):
    #     self.ctx.bot.get_command(command_name).help
    async def embed_creator(self, ctx, command_name):
        prefix = ctx.bot.command_prefix
        if not self.command_name:
            # Default help construction goes here!
            desc = ""
            for cog in ctx.bot.cogs:
                for command in ctx.bot.get_cog(cog).walk_commands():
                    if not command.hidden:
                        desc += command.name
                        desc += "\n"
            res = discord.Embed(title="General Help",
                    description=None,
                    color=util.generate_random_color())

            for cog in ctx.bot.cogs:
                val = ""
                for command in ctx.bot.get_cog(cog).walk_commands():
                    if not command.hidden:
                        val += command.name
                        val += "\n"
                if val != "":
                    res.add_field(name=cog,
                        value=val,
                        inline=True)
                res.set_footer(text=f'{prefix}help for a list of commands\n{prefix}help <command> for detailed help')
            return res
        elif ctx.bot.get_command(self.command_name):
            cmd = ctx.bot.get_command(self.command_name)
            desc = cmd.short_doc
            aliases = ", ".join(["`" + c + "`" for c in cmd.aliases]) if len(cmd.aliases) != 0 else ""
            details = "\n".join(cmd.help.splitlines()[1:])
            res = discord.Embed(title=f'{cmd.name}', 
                    description=desc, 
                    color=util.generate_random_color())
            if aliases:
                res.add_field(name="Aliases",
                        value=aliases,
                        inline=False)
            if details != "":
                res.add_field(name="Options",
                        value=details,
                        inline=False)
            
            res.set_footer(text=f'{prefix}help for a list of commands\n{prefix}help <command> for detailed help')
            return res
        else: 
            return await ctx.send("Command doesn't exist!")

    async def send_initial_message(self, ctx, channel):
        # print(ctx.bot.get_command(self.command_name).help)
        embed = await self.embed_creator(ctx, self.command_name)
        try:
            return await channel.send(embed=embed)
        except commands.CommandInvokeError:
            pass

    # @menus.button('\N{THUMBS UP SIGN}')
    # async def on_thumbs_up(self, payload):
    #     await self.message.edit(content=f'Thanks {self.ctx.author}!')

    # @menus.button('\N{THUMBS DOWN SIGN}')
    # async def on_thumbs_down(self, payload):
    #     await self.message.edit(content=f"That's not nice {self.ctx.author}...")

    # @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    # async def on_stop(self, payload):
    #     self.stop()

# class Test:
#     def __init__(self, value):
#         self.value = value

#     def __repr__(self):
#         return f'<Test value={self.value}>'

# async def generate(number):
#     for i in range(number):
#         yield Test(i)

# class Source(menus.AsyncIteratorPageSource):
#     def __init__(self):
#         super().__init__(generate(9), per_page=4)

#     async def format_page(self, menu, entries):
#         start = menu.current_page * self.per_page
#         return f'\n'.join(f'{i}. {v!r}' for i, v in enumerate(entries, start=start))

# class MySource(menus.ListPageSource):
#     def __init__(self, data):
#         super().__init__(data, per_page=4)

#     async def format_page(self, menu, entries):
#         offset = menu.current_page * self.per_page
#         return '\n'.join(f'{i}. {v}' for i, v in enumerate(entries, start=offset))

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): 
        print(__name__ + " loaded.")

    @commands.command()
    @commands.guild_only()
    async def help(self, ctx, *args):
        if not args:
            m = CustomHelp(None)
        else:
            m = CustomHelp(*args)
        await m.start(ctx)

    @commands.command()
    async def sync(self, ctx):
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(
            f'Synced {len(fmt)} commands to the current guild.'
        )

    @app_commands.command(name="choosecolor", description="testdescription")
    async def test(self, interaction: discord.Interaction, color:str):
        print(interaction)
        await interaction.response.send_message(f'Color selected:" {color}')

    # @commands.command()
    # @commands.guild_only()
    # async def help2(self, ctx):
    #     pages = menus.MenuPages(source=Source(), clear_reactions_after=True)
    #     await pages.start(ctx)

async def setup(bot): 
    await bot.add_cog(Help(bot), guilds=[discord.Object(id=1047577234577305600)])