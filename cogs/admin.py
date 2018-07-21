import asyncio
import os
import psycopg2
import sys
from io import StringIO
import config
import discord
from discord.ext import commands

def admincheck(ctx):
    return ctx.message.author.id == "275312272975462411"


class Admin():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.check(admincheck)
    async def run(self, ctx, *, torun):
        try:
            old_stdout = sys.stdout
            redirected_output = sys.stdout = StringIO()
            exec(torun)
            sys.stdout = old_stdout
            todisplay = redirected_output.getvalue()
            em = discord.Embed(description=todisplay, colour=0x53bceb)
            em.set_author(name='System output:', icon_url=ctx.message.author.avatar_url)
            await self.bot.send_message(ctx.message.channel, embed=em)
        except Exception as e:
            e = str(e)
            em = discord.Embed(description=e, colour=0xf44242)
            em.set_author(name='Error encountered!', icon_url=ctx.message.author.avatar_url)
            await self.bot.send_message(ctx.message.channel, embed=em)

    @commands.command(pass_context=True)
    @commands.check(admincheck)
    async def initialise(self, ctx):
        db = psycopg2.connect(host=config.host,database=config.database, user=config.user, password=config.password)  
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE edited(id SERIAL PRIMARY KEY, channel TEXT, messagebefore TEXT, messageafter TEXT, timestamp TIME, author TEXT)''')
        cursor.execute('''CREATE TABLE deleted(id SERIAL PRIMARY KEY, channel TEXT, message TEXT, timestamp TIME, author TEXT)''')
        db.commit()
        db.close()

    # @commands.command(pass_context=True)
    # @commands.check(admincheck)
    # async def opusstart(self, ctx):
    #     if not discord.opus.is_loaded():
    #         for opus_lib in opus_libs:
    #             opus.load_opus(opus_lib)
    #             return

    
def setup(bot):
    bot.add_cog(Admin(bot))
