import asyncio
import discord
from discord.ext import commands

class JMAF:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, brief="simple vote system, on to-do list")
    async def vote(self, ctx):
        msg = await self.bot.say("Should I?\n1. Wear my uniform.\n2. Get breakfast.\n3. Call Natsuki.")
        await self.bot.add_reaction(emoji="🛑", message=msg)
        await self.bot.add_reaction(emoji="1\u20e3", message=msg)
        await self.bot.add_reaction(emoji="2\u20e3", message=msg)
        await self.bot.add_reaction(emoji="3\u20e3", message=msg)
        await self.bot.wait_for_reaction(message=msg, emoji="🛑")
        em = discord.Embed(color=0xea7938)
        waa = discord.Reaction(emoji="1\u20e3", message=msg)
        wa = await self.bot.get_reaction_users(waa)
        em.add_field(name='1', value=str(len(wa)-1))
        wbb = discord.Reaction(emoji="2\u20e3", message=msg)
        wb = await self.bot.get_reaction_users(wbb)
        em.add_field(name='2', value=str(len(wb)-1))
        wcc = discord.Reaction(emoji="3\u20e3", message=msg)
        wc = await self.bot.get_reaction_users(wcc)
        em.add_field(name='3', value=str(len(wc)-1))
        em.set_footer(text='Do not choose more than one option, just as you would with a normal vote.')
        await self.bot.say(embed=em)

def setup(bot):
    bot.add_cog(JMAF(bot))