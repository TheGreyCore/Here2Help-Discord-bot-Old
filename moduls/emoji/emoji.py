# -*- coding: utf8 -*-
# ------------------------------------
import asyncio
import sys
sys.path.insert(0, '/root/loovtoo')
# ------------------------------------
import discord
from discord.ext import commands
# ------------------------------------
from config import API, settings
import moduls.emoji.lang.lang as lang
# ------------------------------------
import giphy_client
# ------------------------------------
import random


# Juhusliku GIF-i saamise loogika
def random_gif(tag: str):
    api_instance = giphy_client.DefaultApi()
    api_response = api_instance.gifs_search_get(API['key'], tag, rating='g')
    lst = list(api_response.data)
    giff = random.choice(lst)
    embed = discord.Embed(title = '', description =f'', colour = discord.Colour.from_rgb(random.randint(1,225), random.randint(1,225), random.randint(1,225)))
    embed.set_image(url = f'https://media.giphy.com/media/{giff.id}/giphy.gif')      
    return embed



# Laks
@commands.command(aliases=['slap', 'шлёп', 'шлепнуть'])
async def шлёпнуть (message, mention = None):
    await message.channel.purge(limit=1)
    author = message.author.mention
    guild = message.guild.id
    if mention == None:
        await message.channel.send(lang.command_response_text(id = 'error_emoji', author = author ,  mention =  mention, guild_id = guild))
    else: 
        await message.channel.send(lang.command_response_text(id = 'slap', author = author ,  mention =  mention, guild_id = guild))
        await message.channel.send(embed = random_gif(tag = 'slap'))

# Kallistama 
@commands.command(aliases=['hug'])
async def обнять (message, mention = None):
    await message.channel.purge(limit=1)
    author = message.author.mention
    guild = message.guild.id
    if mention == None:
        await message.channel.send(lang.command_response_text(id = 'error_emoji', author = author ,  mention =  mention, guild_id = guild))
    else: 
        await message.channel.send(lang.command_response_text(id = 'hug', author = author ,  mention =  mention, guild_id = guild))
        await message.channel.send(embed = random_gif(tag = 'hug'))

# Musitus
@commands.command(aliases=['поцеловать', 'kiss'])
async def поцелуй(message, mention = None):
    await message.channel.purge(limit=1)
    author = message.author.mention
    guild = message.guild.id
    if mention == None:
        await message.channel.send(lang.command_response_text(id = 'error_emoji', author = author ,  mention =  mention, guild_id = guild))
    else: 
        await message.channel.send(lang.command_response_text(id = 'kiss', author = author ,  mention =  mention, guild_id = guild))
        await message.channel.send(embed = random_gif(tag = 'kiss'))

# Kõditama
@commands.command(aliases=['щекотать', 'tickle'])
async def пощекотать(message, mention = None):
    await message.channel.purge(limit=1)
    author = message.author.mention
    guild = message.guild.id
    if mention == None:
        await message.channel.send(lang.command_response_text(id = 'error_emoji', author = author ,  mention =  mention, guild_id = guild))
    else: 
        await message.channel.send(lang.command_response_text(id = 'tickle', author = author ,  mention =  mention, guild_id = guild))
        await message.channel.send(embed = random_gif(tag = 'tickle'))

# Söötma
@commands.command(aliases=['кормить', 'feed'])
async def покормить(message, mention = None):
    await message.channel.purge(limit=1)
    author = message.author.mention
    guild = message.guild.id
    if mention == None:
        await message.channel.send(lang.command_response_text(id = 'error_emoji', author = author ,  mention =  mention, guild_id = guild))
    else: 
        await message.channel.send(lang.command_response_text(id = 'feed', author = author ,  mention =  mention, guild_id = guild))
        await message.channel.send(embed = random_gif(tag = 'feed'))

# Torkima
@commands.command(aliases=['poke'])
async def тык(message, mention = None):
    await message.channel.purge(limit=1)
    author = message.author.mention
    guild = message.guild.id
    if mention == None:
        await message.channel.send(lang.command_response_text(id = 'error_emoji', author = author ,  mention =  mention, guild_id = guild))
    else: 
        await message.channel.send(lang.command_response_text(id = 'poke', author = author ,  mention =  mention, guild_id = guild))
        await message.channel.send(embed = random_gif(tag = 'poke'))

# Paitama
@commands.command(aliases=['гладить', 'pat'])
async def погладить(message, mention = None):
    await message.channel.purge(limit=1)
    author = message.author.mention
    guild = message.guild.id
    if mention == None:
        await message.channel.send(lang.command_response_text(id = 'error_emoji', author = author ,  mention =  mention, guild_id = guild))
    else: 
        await message.channel.send(lang.command_response_text(id = 'pat', author = author ,  mention =  mention, guild_id = guild))
        await message.channel.send(embed = random_gif(tag = 'pat'))

# Hammustama
@commands.command(aliases=['bite', 'кусь', 'укус'])
async def укусить(message, mention = None):
    await message.channel.purge(limit=1)
    author = message.author.mention
    guild = message.guild.id
    if mention == None:
        await message.channel.send(lang.command_response_text(id = 'error_emoji', author = author ,  mention =  mention, guild_id = guild))
    else: 
        await message.channel.send(lang.command_response_text(id = 'bite', author = author ,  mention =  mention, guild_id = guild))
        await message.channel.send(embed = random_gif(tag = 'bite'))

# Bonk
@commands.command()
async def bonk(message, mention = None):
    await message.channel.purge(limit=1)
    author = message.author.mention
    guild = message.guild.id
    if mention == None:
        await message.channel.send(lang.command_response_text(id = 'error_emoji', author = author ,  mention =  mention, guild_id = guild))
    else: 
        await message.channel.send(lang.command_response_text(id = 'bonk', author = author ,  mention =  mention, guild_id = guild))
        await message.channel.send(embed = random_gif(tag = 'bonk'))

# vabanda!
@commands.command(aliases=['apologize'])
async def извинись(message, mention = None):
    await message.channel.purge(limit=1)
    author = message.author.mention
    guild = message.guild.id
    if mention == None:
        await message.channel.send(lang.command_response_text(id = 'error_emoji', author = author ,  mention =  mention, guild_id = guild))
    else: 
        await message.channel.send(lang.command_response_text(id = 'sorryt', author = author ,  mention =  mention, guild_id = guild))
        embed = discord.Embed(title = '', description =f'', colour = discord.Colour.from_rgb(random.randint(1,225), random.randint(1,225), random.randint(1,225)))
        embed.set_image(url = f'https://media1.tenor.com/images/f77b6e181e15d17c5467baf256ede755/tenor.gif?itemid=12003281')     
        await message.channel.send(embed = embed)

# Vabandama
@commands.command(aliases=['sorry'])
async def извини(message, mention = None):
    await message.channel.purge(limit=1)
    author = message.author.mention
    guild = message.guild.id
    if mention == None:
        await message.channel.send(lang.command_response_text(id = 'error_emoji', author = author ,  mention =  mention, guild_id = guild))
    else: 
        await message.channel.send(lang.command_response_text(id = 'sorry', author = author ,  mention =  mention, guild_id = guild))
        await message.channel.send(embed = random_gif(tag = 'sorry'))

# lakkuma
@commands.command()
async def lick(message, mention = None):
    await message.channel.purge(limit=1)
    author = message.author.mention
    guild = message.guild.id
    if mention == None:
        await message.channel.send(lang.command_response_text(id = 'error_emoji', author = author ,  mention =  mention, guild_id = guild))
    else: 
        await message.channel.send(lang.command_response_text(id = 'lick', author = author ,  mention =  mention, guild_id = guild))
        await message.channel.send(embed = random_gif(tag = 'lick'))

def setup(bot):
    # Lisame käsud käskude listi
    bot.add_command(обнять)
    bot.add_command(шлёпнуть)
    bot.add_command(поцелуй)
    bot.add_command(пощекотать)
    bot.add_command(покормить)
    bot.add_command(тык)
    bot.add_command(погладить)
    bot.add_command(укусить)
    bot.add_command(bonk)
    bot.add_command(извинись)
    bot.add_command(извини)
    bot.add_command(lick)



