# -*- coding: utf8 -*-
# ------------------------------------
import asyncio
import sys
sys.path.insert(0, '/root/loovtoo')
# ------------------------------------
import discord
from discord.ext import commands
from discord import utils
# ------------------------------------
import json
# ------------------------------------
from config import settings
from moduls.emoji.lang.Text.Text import command_response
import sqlite3

# ------------------------------------
conn = sqlite3.connect(settings['DB'])
cursor = conn.cursor()

def command_response_text(id, author, mention: None, guild_id):
    for language in cursor.execute("SELECT language FROM bot_settings WHERE server_id= ? ", [str(guild_id)]):
        return command_response(id = id, author = author, mention = mention, language = language[0])

