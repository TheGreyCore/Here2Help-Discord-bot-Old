# -*- coding: utf8 -*-
# ------------------------------------
import asyncio
import sys
sys.path.insert(0, '/root/loovtoo')
# ------------------------------------
import discord
from discord.ext import commands
# ------------------------------------
import random


# Dice
@commands.command(aliases=['r'])
async def roll (ctx, arg1: int=None, arg2: int = None):
    if arg1 == None:
        embed = discord.Embed(title = f'{ctx.author.name} throws {random.randint(1,100)} out of 100!', description =f'', colour = discord.Colour.from_rgb(random.randint(1,225), random.randint(1,225), random.randint(1,225)))
        await ctx.channel.send(embed = embed)
    else:
        if arg2 == None:
            embed = discord.Embed(title = f'{ctx.author.name} throws {random.randint(1,arg1)} out of {arg1}!', description =f'', colour = discord.Colour.from_rgb(random.randint(1,225), random.randint(1,225), random.randint(1,225)))
            await ctx.channel.send(embed = embed)
        else:
            try:
                embed = discord.Embed(title = f'{ctx.author.name} throws {random.randint(arg1,arg2)} out of {arg2}!', description =f'', colour = discord.Colour.from_rgb(random.randint(1,225), random.randint(1,225), random.randint(1,225)))
                await ctx.channel.send(embed = embed)
            except:
                embed = discord.Embed(title = f'Error!', description =f'The minimum value cannot be greater than the maximum!', colour = discord.Colour.from_rgb(255, 0, 0))
                await ctx.channel.send(embed = embed)

def setup(bot):
    # Lisame käsk
    bot.add_command(roll)
