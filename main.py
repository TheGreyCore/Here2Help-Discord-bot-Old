# -*- coding: utf8 -*-
import os
import discord
from discord import File
from discord.ext import commands
from config import settings, link
import sqlite3
import asyncio
import random
from PIL import Image, ImageDraw, ImageFont
import io
from moduls.admin.admin import unban
from moduls.admin.admin import check_status

# Connect SQLite3 database
conn = sqlite3.connect("db.db")
cursor = conn.cursor()

# Toggle on intents
intents = discord.Intents.default()
intents.members = True


# Change bot status ev
async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game('Type !help for help'))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game('Have a nice day!'))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name=f"Running on {len(bot.guilds)} servers!"))
        await asyncio.sleep(10)


# Set bot prefix
async def get_prefix(ctx, message):
    for prefix in cursor.execute("SELECT bot_prefix FROM bot_settings WHERE server_id= ? ", [str(message.guild.id)]):
        return prefix


bot = commands.Bot(command_prefix=get_prefix, intents=intents)  # Prefix

# Toggle extensions
bot.load_extension("moduls.roll.roll")
bot.load_extension("moduls.admin.admin")

# Remove help command
bot.remove_command("help")


# On bot start
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    bot.loop.create_task(status_task())
    bot.loop.create_task(unban(bot))


# Add new information about server to DataBase
@bot.event
async def on_guild_join(guild):
    cursor.execute("INSERT INTO bot_settings(server_id, bot_prefix) VALUES(? , '!')", [guild.id])
    conn.commit()


# Delete information about server when bot leaves
@bot.event
async def on_guild_remove(guild):
    cursor.execute("DELETE FROM bot_settings WHERE server_id = (?)", [str(guild.id)])
    conn.commit()


# Check if someone react RoleMenu
@bot.event
async def on_raw_reaction_add(payload):
    msg_id = payload.message_id
    emoji = str(payload.emoji)
    author = payload.user_id
    user = payload.member
    if author != 889958184041726013:
        for RoleMenu in cursor.execute("SELECT * FROM rolemenu WHERE messageid = (?)", (str(msg_id),)):
            i = 2
            while i <= 10:
                if emoji == RoleMenu[i]:
                    guild = bot.get_guild(payload.guild_id)
                    role = guild.get_role(int(RoleMenu[i - 1]))
                    await user.add_roles(role)
                    i = i + 2
                else:
                    i = i + 2


# Check if someone remove reaction in RoleMenu
@bot.event
async def on_raw_reaction_remove(payload):
    msg_id = payload.message_id
    emoji = str(payload.emoji)
    author = payload.user_id
    member = await bot.fetch_user(author)
    if author != 889958184041726013:
        for RoleMenu in cursor.execute("SELECT * FROM rolemenu WHERE messageid = (?)", (str(msg_id),)):
            i = 2
            while i <= 10:
                if emoji == RoleMenu[i]:
                    guild = bot.get_guild(payload.guild_id)
                    role = guild.get_role(int(RoleMenu[i - 1]))
                    member = guild.get_member(author)
                    await member.remove_roles(role)
                    i = i + 2
                else:
                    i = i + 2


# Add role(s) to newcomer, send welcome message.
@bot.event
async def on_member_join(member):
    # Attempt to give role
    try:
        for role in cursor.execute("SELECT welcome_role FROM bot_settings WHERE server_id= (?)",
                                   (str(member.guild.id),)):
            server = member.guild
            role = server.get_role(int(role[0]))
            await member.add_roles(role)
    finally:
        pass

    # Attempt to send welcome message
    try:
        for var_greeting_channel in cursor.execute(
                "SELECT greeting_channel_id, greeting_channel_png FROM bot_settings WHERE server_id= ? ",
                [str(member.guild.id)]):
            welcome = bot.get_channel(int(var_greeting_channel[0]))
            # Background
            x = 255
            y = 144
            y2 = 100
            if var_greeting_channel[1] == "random":
                image = Image.open(f'{os.path.dirname()}/welcome/{random.randint(1, 5)}.png')
            else:
                image = Image.open(f'{os.path.dirname()}{var_greeting_channel[1]}.png')
            draw = ImageDraw.Draw(image)
            text = member.name
            text2 = "WELCOME!"
            font = ImageFont.truetype("DejaVuSans.ttf", 35)
            draw.text((x, y + 3), text, font=font, fill=(0, 0, 0))  # vari
            draw.text((x, y), text, font=font, fill=(255, 255, 255))  # tekst
            draw.text((x, y2 + 3), text2, font=font, fill=(0, 0, 0))  # vari
            draw.text((x, y2), text2, font=font, fill=(255, 255, 255))  # tekst
            buffer = io.BytesIO()

            # Avatar
            AVATAR_SIZE = 150
            avatar_asset = member.display_avatar
            buffer_avatar = io.BytesIO(await avatar_asset.read())
            avatar_image = Image.open(buffer_avatar)
            avatar_image = avatar_image.resize((AVATAR_SIZE, AVATAR_SIZE))  #
            circle_image = Image.new('L', (AVATAR_SIZE, AVATAR_SIZE))
            circle_draw = ImageDraw.Draw(circle_image)
            circle_draw.ellipse((0, 0, AVATAR_SIZE, AVATAR_SIZE), fill=255)
            image.paste(avatar_image, (55, 70), circle_image)
            image.save(buffer, format='PNG')
            buffer.seek(0)

            for text in cursor.execute("SELECT greeting_message FROM bot_settings WHERE server_id= (?)",
                                       (str(member.guild.id),)):
                x = text[0]
                x = x.replace('(user.mention)', f'{member.mention}')
                x = x.replace('(user)', f'{member}')
                x = x.replace('(server)', f'{member.guild}')
            await welcome.send(x, file=File(buffer, 'greeting.png'))
    finally:
        for var_greeting_channel in cursor.execute(
                "SELECT greeting_channel_id, greeting_channel_png FROM bot_settings WHERE server_id= ? ",
                [str(member.guild.id)]):
            welcome = bot.get_channel(int(var_greeting_channel[0]))
        for text in cursor.execute("SELECT greeting_message FROM bot_settings WHERE server_id= (?)",
                                   (str(member.guild.id),)):
            text = text[0].replace('(user.mention)', f'{member.mention}')
            text = text[0].replace('(user)', f'{member}')
            text = text[0].replace('(server)', f'{member.guild}')
        await welcome.send(text)


# Command for add RoleMenu
@bot.command()
async def rolemenu(ctx, messageid, role1: discord.Role, emoji1, role2: discord.Role = None, emoji2=None,
                   role3: discord.Role = None, emoji3=None, role4: discord.Role = None, emoji4=None,
                   role5: discord.Role = None, emoji5=None):
    if ctx.author.guild_permissions.kick_members == True or check_status(ctx) == 1:
        try:
            role1 = role1.id
        except:
            pass
        try:
            role2 = role2.id
        except:
            pass
        try:
            role3 = role3.id
        except:
            pass
        try:
            role4 = role4.id
        except:
            pass
        try:
            role5 = role5.id
        except:
            pass

        cursor.execute(f"""INSERT INTO rolemenu(messageid, role1, emoji1,role2, emoji2,role3, emoji3,role4, emoji4,role5, emoji5) 
        VALUES(?,?,?,?,?,?,?,?,?,?,?)""", (
        str(messageid), str(role1), str(emoji1), str(role2), str(emoji2), str(role3), str(emoji3), str(role4),
        str(emoji4), str(role5), str(emoji5),))
        conn.commit()
        message = await ctx.fetch_message(messageid)
        await message.add_reaction(str(emoji1))
        await message.add_reaction(str(emoji2))
        await message.add_reaction(str(emoji3))
        await message.add_reaction(str(emoji4))
        await message.add_reaction(str(emoji5))


# Command for set greeting channel
@bot.command(aliases=['setwelcomechannel', 'welcome'])
async def setgreetingchannel(ctx, arg: discord.TextChannel):
    await ctx.channel.purge(limit=1)
    if ctx.author.guild_permissions.administrator == True or check_status(ctx) == 1:
        cursor.execute("UPDATE bot_settings SET greeting_channel_id = (?) WHERE server_id = (?)",
                       (arg.id, ctx.guild.id))
        conn.commit()
        embed = discord.Embed(title='Successfully!', description=f'New weclome channel is {arg.mention}',
                              colour=discord.Colour.from_rgb(0, 204, 0))
        embed.set_footer(text=f'For {ctx.author.name}.', icon_url=ctx.author.display_avatar)
        embed.set_author(name=f"{settings['bot']}", url=embed.Empty, icon_url=settings['avatar'])
        await ctx.send(embed=embed)


# Command for set autorole
@bot.command(aliases=['autorole', 'role'])
@commands.has_permissions(administrator=True)
async def setwelcomerole(ctx, role: discord.Role):
    await ctx.channel.purge(limit=1)
    if ctx.author.guild_permissions.administrator == True or check_status(ctx) == 1:
        cursor.execute("UPDATE bot_settings SET welcome_role = (?) WHERE server_id = (?)", (role.id, str(ctx.guild.id)))
        conn.commit()
        embed = discord.Embed(title='Successfully!', description=f'New welcome role: {role}',
                              colour=discord.Colour.from_rgb(0, 204, 0))
        embed.set_author(name=f"{settings['bot']}", url=embed.Empty, icon_url=settings['avatar'])
        embed.set_footer(text=f'For {ctx.author.name}.', icon_url=ctx.author.display_avatar)
        await ctx.send(embed=embed)


# Command for set welcome message
@bot.command(aliases=['welcomemessage'])
@commands.has_permissions(administrator=True)
async def setwelcomemessage(ctx, *, arg: str):
    await ctx.channel.purge(limit=1)
    if ctx.author.guild_permissions.administrator == True or check_status(ctx) == 1:
        cursor.execute("UPDATE bot_settings SET greeting_message = (?) WHERE server_id = (?)", (arg, str(ctx.guild.id)))
        conn.commit()
        embed = discord.Embed(title='Successfully!', description=f'New greeting message is ***{arg}***',
                              colour=discord.Colour.from_rgb(0, 204, 0))
        embed.set_author(name=f"{settings['bot']}", url=embed.Empty, icon_url=settings['avatar'])
        embed.set_footer(text=f'For {ctx.author.name}.', icon_url=ctx.author.display_avatar)
        await ctx.send(embed=embed)


# Server info command
@bot.command()
async def info(ctx):
    for role in cursor.execute("SELECT welcome_role FROM bot_settings WHERE server_id= (?)", (str(ctx.guild.id),)):
        pass
    for var_greeting_channel in cursor.execute(
            "SELECT greeting_channel_id, greeting_channel_png FROM bot_settings WHERE server_id= ? ",
            [str(ctx.guild.id)]):
        var_greeting_channel = bot.get_channel(int(var_greeting_channel[0]))
    for prefix in cursor.execute("SELECT bot_prefix FROM bot_settings WHERE server_id= ? ", [str(ctx.guild.id)]):
        pass
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title=f'"{ctx.guild.name}" server info:', description=f"""
    Prefix: `{prefix[0]}`
    Autorole: <@&{role[0]}>
    Welcome channel id: `{var_greeting_channel}`
    """, colour=discord.Colour.from_rgb(255, 255, 0))
    embed.set_author(name=f"{settings['bot']}", url=embed.Empty, icon_url=settings['avatar'])
    embed.set_footer(text=f'For {ctx.author.name}.', icon_url=ctx.author.display_avatar)
    await ctx.send(embed=embed)


# Command for change the prefix
@bot.command()
async def changeprefix(message, arg):
    await message.channel.purge(limit=1)
    if message.author.guild_permissions.administrator == True or check_status(message) == 1:
        cursor.execute("UPDATE bot_settings SET bot_prefix = (?) WHERE server_id = (?)", (arg, str(message.guild.id)))
        conn.commit()
        embed = discord.Embed(title='Successfully!', description=f'New prefix is `{arg}`',
                              colour=discord.Colour.from_rgb(0, 204, 0))
        embed.add_field(name=f"Thanks for using {settings['bot']}!", value=f'[Invite link]({link})', inline=False)
        embed.set_author(name=f"{settings['bot']}", url=embed.Empty, icon_url=settings['avatar'])
        embed.set_footer(text=f'For {message.author.name}.', icon_url=message.author.display_avatar)
        await message.send(embed=embed)


# Command for get invite link
@bot.command()
async def invite(message):
    await message.channel.purge(limit=1)
    embed = discord.Embed(color=discord.Colour.from_rgb(255, 0, 102))
    embed.add_field(name=f"Thanks for using {settings['bot']}!", value=f'[Invite link]({link})', inline=False)
    embed.set_author(name=f"{settings['bot']}", url=embed.Empty, icon_url=settings['avatar'])
    embed.set_footer(text=f'For {message.author.name}.', icon_url=message.author.display_avatar)
    await message.send(embed=embed)


# Help command
@bot.command()
async def help(message):
    await message.channel.purge(limit=1)
    embed = discord.Embed(title='General Commands', description='''`roll[r]`
    `info`
    `invite`
    `warnlog`
    ''', colour=discord.Colour.from_rgb(random.randint(1, 225), random.randint(1, 225), random.randint(1, 225)))
    embed.set_author(name=f"{settings['bot']} help", url=embed.Empty, icon_url=settings['avatar'])
    embed.add_field(name='Emojis:',
                    value='`hug` `slap` `kiss` `tickle` `feed` `poke` `pat` `bite` `bonk` `apologize` `sorry` `lick`',
                    inline=False)
    embed.add_field(name='Available for moderators:', value='''`mute <mention> <time: 1d1h1m> <reason>`
    `unmute <mention>`
    `ban <mention> <time: 1d1h1m> <reason>`
    `warn <reason>`
    `unwarn <mention> <id>`
    `changeprefix`
    `setgreetingchannel`
    `setwelcomerole` `role` `autorole`
    `clear`
    `welcomemessage` `setwelcomemessage`
    `rolemenu <message id> <role mention> <emoji> up to 5 times`
    ''', inline=False)
    embed.add_field(name='Inventory system:', value='''`inventory <mention>`
    `items`
    `create <Name in ""> <Description>`
    `give <mention> <item id>`
    `take <mention> <item unique id>`
    ''', inline=False)
    embed.add_field(name='Available for owner:', value='''`addmoder`
    `removemoder`''', inline=False)
    embed.add_field(name='Bot version:', value=f'''`{settings['Version']}`''', inline=False)
    embed.set_footer(text=f'For {message.author.name}.', icon_url=message.author.display_avatar)
    await message.send(embed=embed)
# -----------------------------------------------------------------------------------------------------------------------


# Run bot! Don`t touch! 
bot.run(settings['token'])
