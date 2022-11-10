# -*- coding: utf8 -*-
# ------------------------------------
import asyncio
import os
import sys
sys.path.insert(0, f'{os.path.dirname()}')
# ------------------------------------
import discord
from discord.ext import commands
import sqlite3
from datetime import datetime, timedelta
import re
# ------------------------------------
from config import settings
# ------------------------------------

conn = sqlite3.connect("db.db")
cursor = conn.cursor()

# Check if user has permission
def check_status(ctx):
    var_has_permmission = 'None'
    for var_has_permmission in cursor.execute("SELECT player_has_moderator_permission FROM player_info WHERE server_id= (?) AND player_id = (?) ", (str(ctx.guild.id), str(ctx.author.id))):
        if var_has_permmission[0] == '1':
            return 1
        else:
            return 0

# Every 10 seconds check unban list
async def unban(bot):
    while True:
        for info in cursor.execute("SELECT User_ID, Date, Server_ID FROM banned"):
            now = datetime.now()
            if info[1] <= str(now):
                guild = bot.get_guild(int(info[2]))
                banned_users = await guild.bans()
                for ban_entry in banned_users: 
                    user = ban_entry.user
                    if str(user) == info[0]:
                        print(f'User {info[0]} unbanned.')
                        await guild.unban(user)
                        cursor.execute("DELETE FROM banned WHERE server_id = (?) AND User_ID = (?)",[str(guild.id), str(info[0])])
                        conn.commit()
        await asyncio.sleep(10)


# Command for add moderator
@commands.command()
@commands.has_permissions( administrator = True)
async def addmoder(message, arg: discord.User):
    cursor.execute("INSERT OR IGNORE INTO player_info(server_id, player_id,player_has_moderator_permission) VALUES(? , ?, '1')", (str(message.guild.id), str(arg.id)))
    conn.commit()
    await message.channel.purge( limit = 1)
    embed = discord.Embed(title = 'Successfully!', description =f'New moderator is {arg.mention}', colour = discord.Colour.from_rgb(0, 204, 0))
    embed.set_author(name =f"{settings['bot']}", url=embed.Empty , icon_url= settings['avatar'])
    embed.set_footer(text =f'For {message.author.name}.', icon_url=message.author.display_avatar)
    await message.send(embed=embed)


# Command for remove moderator
@commands.command()
@commands.has_permissions( administrator = True)
async def removemoder(message, arg: discord.User):
    cursor.execute("DELETE FROM player_info WHERE server_id = (?) AND player_id = (?)",[str(message.guild.id), str(arg.id)])
    conn.commit()
    await message.channel.purge( limit = 1)
    embed = discord.Embed(title = 'Successfully!', description =f'The moderator {arg.mention} deleted!', colour = discord.Colour.from_rgb(0, 204, 0))
    embed.set_footer(text =f'For {message.author.name}.', icon_url=message.author.display_avatar)
    await message.send(embed=embed)


# Mute user
@commands.command()
async def mute(ctx, member: discord.Member, time = None, *, reason: str = 'Violating rules'):
    if ctx.author.guild_permissions.mute_members == True or check_status(ctx) == 1:
        if time == None:
            mute_time =[0,0,10]
        else:
            mute_time =[]
            
        x = re.search(r"\d{1,}d", time)
        if x != None:
            x = re.sub("d", "", x.group())
            mute_time.append(x)
        else:
            mute_time.append(0)

        x = re.search(r"\d{1,}h", time)
        if x != None:
            x = re.sub("h", "", x.group())
            mute_time.append(x)
        else:
            mute_time.append(0)

        x = re.search(r"\d{1,}m", time)
        if x != None:
            x = re.sub("m", "", x.group())
            mute_time.append(x)
        else:
            mute_time.append(0)

        mute_time_final = datetime.now() + timedelta(days = int(mute_time[0]), hours= int(mute_time[1]), minutes= int(mute_time[1])) - timedelta(hours = 2)
        await member.timeout(mute_time_final)
        for ID in cursor.execute("SELECT COUNT (User_ID) FROM warns WHERE Server_ID = (?) AND Server_ID = (?)", (str(ctx.guild.id),str(ctx.guild.id))):
            cursor.execute("INSERT INTO warns(User_ID, Warn_Text, Server_ID, Moderador_ID,Type,ID,Moderador_Name) VALUES(?,?,?,?,?,?,?)",(str(member.id), reason, str(ctx.guild.id), str(ctx.author.id),'Muted', str(ID[0] + 1),str(ctx.author)))
            conn.commit()
            embed = discord.Embed(title = f'{member} has muted!', description =f'**Reason:** {reason} || **Until:** {mute_time_final}', colour = discord.Colour.from_rgb(0, 204, 0))
            embed.set_footer(text =f'By {ctx.author.name}.', icon_url=ctx.author.display_avatar)
        await ctx.send(embed=embed)
    else:
        pass


# Unmute user
@commands.command()
async def unmute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.mute_members == True or check_status(ctx) == 1:
        await member.remove_timeout()
        embed = discord.Embed(title = f'{member} has unmuted!', description =f'', colour = discord.Colour.from_rgb(0, 204, 0))
        embed.set_footer(text =f'By {ctx.author.name}.', icon_url=ctx.author.display_avatar)
        await ctx.send(embed=embed)
    else:
        pass


# Warn user
@commands.command()
async def warn(ctx, user: discord.User, *, reason: str):
    if ctx.author.guild_permissions.mute_members == True or check_status(ctx) == 1:
        for ID in cursor.execute("SELECT COUNT (User_ID) FROM warns WHERE Server_ID = (?) AND Server_ID = (?)", (str(ctx.guild.id),str(ctx.guild.id))):
            cursor.execute(f"INSERT INTO warns(User_ID, Warn_Text, Server_ID, Moderador_ID,Type,ID, Moderador_Name) VALUES(?,?,?,?,?,?,?)",(str(user.id), str(reason), str(ctx.guild.id), str(ctx.author.id),'Warned',str(ID[0]+1), str(ctx.author)))
            conn.commit()
            embed = discord.Embed(title = f'{user} has warned!', description =f'**Reason:** {reason}', colour = discord.Colour.from_rgb(0, 204, 0))
            embed.set_footer(text =f'By {ctx.author.name}.', icon_url=ctx.author.display_avatar)
        await ctx.send(embed=embed)
    else:
        pass


# Unwarn user
@commands.command()
async def unwarn(ctx, user: discord.User, ID):
    if ctx.author.guild_permissions.mute_members == True or check_status(ctx) == 1:
        cursor.execute("DELETE FROM warns WHERE User_ID = (?) AND ID = (?)",[str(user.id), str(ID)])
        conn.commit()
        embed = discord.Embed(title = f'{user} has unwarned!', description =f'{ID}. warn were taken.', colour = discord.Colour.from_rgb(0, 204, 0))
        embed.set_footer(text =f'By {ctx.author.name}.', icon_url=ctx.author.display_avatar)
        await ctx.send(embed=embed)
    else:
        pass


# Warnlog --------------------------------------------------------Broken--------------------------------------------------------
"""
@commands.command()
async def warnlog(ctx, user: discord.User = None):
    if user == None:
        user = ctx.author
    else:
        pass
    embed = discord.Embed(title = f'{user.name}`s warnlog:', colour = discord.Colour.from_rgb(255, 0, 0))
    embed.set_footer(text =f'For {ctx.author.name}.', icon_url=ctx.author.display_avatar)
    for warns in cursor.execute("SELECT Warn_Text,  Moderador_Name, ID, Type FROM warns WHERE Server_ID= (?) AND User_ID = (?) ", (str(ctx.guild.id), str(user.id))):
        #id = int(warns[1])
        #print (commands.Bot.get_user(307565643593678858,))
        embed.add_field(name = f"{warns[3]} by {warns[1]}", value= f'ID:{warns[2]} || {warns[0]}', inline=True) #Ошибка
    await ctx.send(embed=embed)
"""


# Ban command
@commands.command()
@commands.has_permissions( ban_members = True)
async def ban(ctx, user: discord.Member, time = None, *, reason: str = 'Reeglite rikkumine.'):
    if time == None:
        ban_time =[0,0,10]
    else:
        ban_time =[]
            
    x = re.search(r"\d{1,}d", time)
    if x != None:
        x = re.sub("d", "", x.group())
        ban_time.append(x)
    else:
        ban_time.append(0)

    x = re.search(r"\d{1,}h", time)
    if x != None:
        x = re.sub("h", "", x.group())
        ban_time.append(x)
    else:
        ban_time.append(0)

    x = re.search(r"\d{1,}m", time)
    if x != None:
        x = re.sub("m", "", x.group())
        ban_time.append(x)
    else:
        ban_time.append(0)

    ban_time_final = datetime.now() + timedelta(days = int(ban_time[0]), hours= int(ban_time[1]), minutes= int(ban_time[2])) # Bänni kuupäev.

    embed = discord.Embed(title = f'You was banned from {ctx.guild.name}', description = f'', colour = discord.Colour.from_rgb(255, 0, 0))
    embed.add_field(name = f'Until', value = f'{ban_time_final}')
    embed.add_field(name = f'Reason', value = f'{reason}')
    embed.set_footer(text =f'Moderator: {ctx.author.name}.', icon_url=ctx.author.display_avatar)
    await user.send(embed = embed)

    cursor.execute("INSERT INTO banned(User_ID, Reason, Server_ID, Moderador_ID, Date) VALUES(?,?,?,?,?)",(str(user), reason, str(ctx.guild.id), str(ctx.author.id),str(ban_time_final)))
    conn.commit()
    await user.ban(reason = reason)

    embed = discord.Embed(title = f'{user} has banned!', description = '', colour = discord.Colour.from_rgb(0, 204, 0))
    embed.set_footer(text =f'Moderator: {ctx.author.name}.', icon_url=ctx.author.display_avatar)
    await ctx.send(embed = embed)


# Clear command
@commands.command()
async def clear(ctx, arg):
    if ctx.author.guild_permissions.manage_messages == True or check_status(ctx) == 1:
        await ctx.channel.purge( limit = int(arg) + 1)
    else:
        pass

def setup(bot):
    # Add commands
    bot.add_command(ban)
    # bot.add_command(warnlog)
    bot.add_command(unwarn)
    bot.add_command(warn)
    bot.add_command(unmute)
    bot.add_command(mute)
    bot.add_command(removemoder)
    bot.add_command(addmoder)
    bot.add_command(clear)