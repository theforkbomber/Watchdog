
import os
import sys
from datetime import datetime
from os import listdir
from os.path import isfile, join

import discord
import psycopg2
from discord.ext import commands
from googletrans import Translator
from PyDictionary import PyDictionary

import config

from opus_loader import load_opus_lib

load_opus_lib()

bot = commands.Bot(command_prefix=">os.")
cogs_dir = "cogs"

uk = discord.Reaction(emoji="\U0001f1ec\U0001f1e7")
us = discord.Reaction(emoji="\U0001f1fa\U0001f1f8")
jp = discord.Reaction(emoji="\U0001f1ef\U0001f1f5")
ind = discord.Reaction(emoji="\U0001f1ee\U0001f1f3")
es = discord.Reaction(emoji="\U0001f1ea\U0001f1f8")
de = discord.Reaction(emoji="\U0001f1ea\U0001f1f8")
fr = discord.Reaction(emoji="\U0001f1eb\U0001f1f7")
pt = discord.Reaction(emoji="\U0001f1f5\U0001f1f9")
cn = discord.Reaction(emoji="\U0001f1e8\U0001f1f3")
pole = discord.Reaction(emoji="\U0001f1f5\U0001f1f1")

initial_extensions = (
    'cogs.literature',
    'cogs.moderation',
    'cogs.voting',
    'cogs.serverinfo',
    'cogs.epdesigner',
    'cogs.admin',
    'cogs.fun',
    'cogs.music',
)


def translate(payload, lang):
    translating = Translator()
    translated = translating.translate(payload, dest=lang)
    translatedtext = translated.text
    return translatedtext



@bot.event
async def on_ready():
    print('Successfully logged in.')
    print('Username -> ' + bot.user.name)
    print('ID -> ' + str(bot.user.id))

@bot.event
async def on_message_edit(before, after):
    db = psycopg2.connect(host=config.host,database=config.database, user=config.user, password=config.password)  
    cursor = db.cursor()
    # cursor.execute('''DROP TABLE edited''')
    # db.commit()
    # cursor.execute('''CREATE TABLE edited(id SERIAL PRIMARY KEY, channel TEXT, messagebefore TEXT, messageafter TEXT, timestamp TIME, author TEXT)''')
    # db.commit()
    aftermsg = after.content
    beforemsg = before.content
    ts = str(after.timestamp)
    ch = str(after.channel.id)
    author = after.author.id
    server = after.server
    mem = server.get_member(author)
    if mem.bot == True:
        db.close()
        return
    else:
        cursor.execute('''DELETE FROM edited WHERE channel ='%s';'''% str(ch),)
        cursor.execute('''INSERT INTO edited(channel, messagebefore, messageafter, timestamp, author)VALUES(%s,%s,%s,%s,%s) RETURNING id;''', (ch, beforemsg, aftermsg, ts, author))
        db.commit()
        db.close()

@bot.event
async def on_message_delete(message):
    db = psycopg2.connect(host=config.host,database=config.database, user=config.user, password=config.password)  
    cursor = db.cursor()
    if message.edited_timestamp != None:
        pass
    # cursor.execute('''DROP TABLE deleted''')
    # db.commit()
    # cursor.execute('''CREATE TABLE deleted(id SERIAL PRIMARY KEY, channel TEXT, message TEXT, timestamp TIME, author TEXT)''')
    # db.commit()
    else:
        msg = message.content
        ts = str(message.timestamp)
        ch = str(message.channel.id)
        author = message.author.id
        cursor.execute('''DELETE FROM deleted WHERE channel ='%s';'''% str(ch),)
        cursor.execute('''INSERT INTO deleted(channel, message, timestamp, author)VALUES(%s,%s,%s,%s) RETURNING id;''', (ch, msg, ts, author))
        db.commit()
        db.close()

@bot.event
async def on_member_join(member):
    server = member.server
    for role in server.roles:
        if role.name == "roleless":
            roleuno = role
        if role.name == "MP5 A":
            roledos = role
    await bot.add_roles(member, roleuno)
    await bot.add_roles(member, roledos)


@bot.event
async def on_message(message):
    if message.author.bot == True:
        return

    elif message.content == ">os.help epdesign":
        arg = """Here lies the abandoned remains of a project that had potential, no extra work has been done on this since the 6th of the 6th 2018, and there will be no more work done for it. You may mess around with the commands at your pleasure.\n```>os.epdesign

Commands:
  make   
  start  
  list   
  remove 

Type >os.help command for more info on a command.
You can also type >os.help category for more info on a category.```"""
        await bot.send_message(message.channel, arg)

    elif message.content == ">os.help EpDesign":
        arg = """Here lies the abandoned remains of a project that had potential, no extra work has been done on this since the 6th of the 6th 2018, and there will be no more work done for it. You may mess around with the commands at your pleasure.\n```Commands:
  epdesign     

Type >os.help command for more info on a command.
You can also type >os.help category for more info on a category.```"""
        await bot.send_message(message.channel, arg)

    elif message.content.startswith(">os."):
        await bot.process_commands(message)

    else:
        waitforreact = await bot.wait_for_reaction(message=message, timeout=500)
        if waitforreact != None:
            if waitforreact.reaction == uk or waitforreact.reaction == us:
                lang = "en"
                payload = message.content
                await bot.send_typing(message.channel)
                em = discord.Embed(description=translate(payload, lang), colour=0x53bceb)
                await bot.send_message(message.channel, embed=em)

            elif waitforreact.reaction == cn:
                lang = "zh-tw"
                payload = message.content
                await bot.send_typing(message.channel)
                em = discord.Embed(description=translate(payload, lang), colour=0x53bceb)
                await bot.send_message(message.channel, embed=em)

            elif waitforreact.reaction == fr:
                lang = "fr"
                payload = message.content
                await bot.send_typing(message.channel)
                em = discord.Embed(description=translate(payload, lang), colour=0x53bceb)
                await bot.send_message(message.channel, embed=em)

            elif waitforreact.reaction == es:
                lang = "es"
                payload = message.content
                await bot.send_typing(message.channel)
                em = discord.Embed(description=translate(payload, lang), colour=0x53bceb)
                await bot.send_message(message.channel, embed=em)

            elif waitforreact.reaction == pt:
                lang = "pt"
                payload = message.content
                await bot.send_typing(message.channel)
                em = discord.Embed(description=translate(payload, lang), colour=0x53bceb)
                await bot.send_message(message.channel, embed=em)

            elif waitforreact.reaction == jp:
                lang = "ja"
                payload = message.content
                await bot.send_typing(message.channel)
                em = discord.Embed(description=translate(payload, lang), colour=0x53bceb)
                await bot.send_message(message.channel, embed=em)

            elif waitforreact.reaction == de:
                lang = "de"
                payload = message.content
                await bot.send_typing(message.channel)
                em = discord.Embed(description=translate(payload, lang), colour=0x53bceb)
                await bot.send_message(message.channel, embed=em)

            elif waitforreact.reaction == ind:
                lang = "in"
                payload = message.content
                await bot.send_typing(message.channel)
                em = discord.Embed(description=translate(payload, lang), colour=0x53bceb)
                await bot.send_message(message.channel, embed=em)

            elif waitforreact.reaction == pole:
                lang = "pl"
                payload = message.content
                await bot.send_typing(message.channel)
                em = discord.Embed(description=translate(payload, lang), colour=0x53bceb)
                await bot.send_message(message.channel, embed=em)


for extension in initial_extensions:
    bot.load_extension(extension)

bot.run(config.token)
