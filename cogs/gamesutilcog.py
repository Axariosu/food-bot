    

import util.alphafuseutil as alphafuseutil
import util.util as util
import uuid
import discord
import asyncio
import random
import time
from discord.ext import tasks
from discord.ext import commands


class GamesUtil(commands.Cog):
    @commands.command(aliases=['a25'], hidden=True)
    @commands.guild_only()
    async def alpha_25(self, ctx, arg1, brief="Usage: !alpha_25 <string>", description="Usage: !alpha_25 <string>, returns a list of at most 25 possible combinations for the given character combination."):
        """
        Returns a list of up to 25 valid words that satisfy the given letter combination. 
        """
        res = discord.Embed(title=discord.Embed.Empty, description=", ".join(alphafuseutil.get_many_possibilities(arg1)), color=util.generate_random_color())
        await ctx.send(embed=res)

    @commands.command(aliases=['o25'], hidden=True)
    @commands.guild_only()
    async def omega_25(self, ctx, arg1, brief="Usage: !omega_25 <string>", description="Usage: !omega_25 <string>, returns a list of at most 25 possible combinations for the given character combination."):
        """
        Returns a list of up to 25 valid words that satisfy the given letter combination. 
        """
        res = discord.Embed(title=discord.Embed.Empty, description=", ".join(alphafuseutil.get_random_possibility_inverted(arg1)), color=util.generate_random_color())
        await ctx.send(embed=res)

    @commands.command(aliases=['s25'], hidden=True)
    @commands.guild_only()
    async def sigma_25(self, ctx, arg1, brief="Usage: !sigma_25 <string>", description="Usage: !sigma_25 <string>, returns a list of at most 25 possible combinations for the given character combination."):
        """
        Returns a list of up to 25 valid words that satisfy the given letter combination. 
        """
        res = discord.Embed(title=discord.Embed.Empty, description=", ".join(alphafuseutil.get_many_possibilities_in_order(arg1)), color=util.generate_random_color())
        await ctx.send(embed=res)

    @commands.command(hidden=True)
    @commands.guild_only()
    async def check(self, ctx, arg1):
        """
        Returns "valid" or "invalid" based on the submission. 
        """
        c = "Valid" if alphafuseutil.in_wordlist(arg1) else "Invalid"
        res = discord.Embed(title=c, color=util.generate_random_color())
        await ctx.send(embed=res)
    
    @commands.command(hidden=True)
    @commands.guild_only()
    async def ping(self, ctx):
        """
        `!ping`
        Displays ping to the server.
        """
        await ctx.send(str(round(ctx.bot.latency * 1000)) + "ms")

def setup(bot): 
    bot.add_cog(GamesUtil(bot))