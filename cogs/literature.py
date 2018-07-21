import asyncio
from PyDictionary import PyDictionary
import discord
from discord.ext import commands

class Literature:
    def __init__(self, bot):
        self.bot = bot
    @commands.command(pass_context=True)
    async def define(self, ctx, msgtodefine : str):
        dictionary = PyDictionary()
        defined = dictionary.meaning(msgtodefine)
        defined = str(defined)
        defined = defined.replace("'", "")
        defined = defined.replace("[", "")
        defined = defined.replace("]", "")
        defined = defined.replace("{", "")
        defined = defined.replace("}", "")
        em = discord.Embed(description=defined, colour=0x53bceb)
        em.set_author(name='Define '+msgtodefine)
        await self.bot.say(embed=em)

def setup(bot):
    bot.add_cog(Literature(bot))