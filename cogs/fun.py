
import asyncio
import discord
from discord.ext import commands
import random
class Fun:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def fun(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say("Unknown command")

    @fun.command(pass_context=True,aliases=["8ball"])
    async def eightball(self,ctx,string):
        eightballpromptsG = ['It is certain, ','It is decidedly so, ','Without a doubt, ','Yes, definitely','You may rely on it, ','As I see it, yes, ','Most likely, ','Outlook good, ','Yes, ','Signs point to yes ']
        eightballpromptsA = ['Reply hazy, try again, ','Ask again later, ','Better not tell you now, ','Cannot predict now, ','Concentrate and ask again, ']
        eightballpromptsR = ["You shouldn't count on it, ",'My reply is no, ','My sources say no, ','The outlook is not so good, ','Very doubtful, ']
        eightballcategorypicker = random.randint(0,2)

        if eightballcategorypicker == 0:
            eightballpromptpicker = random.randint(0,9)
            eightballfinal = eightballpromptsG[eightballpromptpicker]
            msg = eightballfinal+'{0.author.mention}!'.format(ctx.message)
            em = discord.Embed(description=msg, colour=0x53bceb)
            em.set_author(name='Good news!')
            await self.bot.send_message(ctx.message.channel, embed=em)

        elif eightballcategorypicker == 1:
            eightballpromptpicker = random.randint(0,4)
            eightballfinal = eightballpromptsA[eightballpromptpicker]
            msg = eightballfinal+'{0.author.mention}.'.format(ctx.message)
            em = discord.Embed(description=msg, colour=0x53bceb)
            em.set_author(name="Uhmmmmmmmmm, it didn't go too well")
            await self.bot.send_message(ctx.message.channel, embed=em)

        elif eightballcategorypicker == 2:
            eightballpromptpicker = random.randint(0,4)
            eightballfinal = eightballpromptsR[eightballpromptpicker]
            msg = eightballfinal+'{0.author.mention}.'.format(ctx.message)
            await self.bot.send_typing(ctx.message.channel)
            em = discord.Embed(description=msg, colour=0x53bceb)
            em.set_author(name='I regret to tell you this but:')
            await self.bot.send_message(ctx.message.channel, embed=em)
    
    @fun.command(pass_context=True)
    async def coin(self, ctx):
        cointoss = random.randint(0,1)
        coinfaces = ['heads','tails']
        coinresult = coinfaces[cointoss]
        await self.bot.send_typing(ctx.message.channel)
        em = discord.Embed(description=coinresult, colour=0x53bceb)
        em.set_author(name='You got:')
        await self.bot.send_message(ctx.message.channel, embed=em)

    @fun.command(pass_context=True)
    async def rps(self, ctx, choice):
        result = choice
        await self.bot.send_message(ctx.message.channel,'*Rock, paper, scissors!*')
        rps = ['Rock','Paper','Scissors']
        randrps = random.randint(0,2)
        resultado = rps[randrps]
        resultados = resultado.lower()
        if result == resultados:
            await self.bot.send_message(ctx.message.channel,resultado+'? Damn, we have to have another round.')
        elif (result == 'rock' and resultados == 'paper') or (result == 'scissors' and resultados == 'rock') or (result == 'paper' and resultados == 'scissors'):
            await self.bot.send_message(ctx.message.channel,'I picked '+resultados+'! I win!')
        elif (resultados == 'rock' and result == 'paper') or (resultado == 'scissors' and result == 'rock') or (resultados == 'paper' and result == 'scissors'):
            await self.bot.send_message(ctx.message.channel,'I picked '+resultados+'. You win, fair and square.')
        else:
            await self.bot.send_message(ctx.message.channel,'`INVALID`')

    @fun.command(pass_context=True)
    async def dice(self, ctx):
        resultone = random.randint(1,6)
        resulttwo = random.randint(1,6)
        resultone = str(resultone)
        resulttwo = str(resulttwo)
        await self.bot.send_typing(ctx.message.channel)
        await asyncio.sleep(2)
        await self.bot.send_message(ctx.message.channel,'First roll... '+resultone)
        await asyncio.sleep(2)
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_message(ctx.message.channel,'Second roll... '+resulttwo)
        await self.bot.send_typing(ctx.message.channel)
        resultone = int(resultone)
        resulttwo = int(resulttwo)
        result = resultone + resulttwo
        result = str(result)
        await self.bot.send_message(ctx.message.channel,'In total, you got '+result)

    @fun.command(pass_context=True)
    async def die(self, ctx):
        resultone = random.randint(1,6)
        resultone = str(resultone)
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_message(ctx.message.channel,'You rolled... '+resultone)

    
def setup(bot):
    bot.add_cog(Fun(bot))