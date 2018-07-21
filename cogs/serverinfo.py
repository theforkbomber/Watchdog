import asyncio
import discord
from discord.ext import commands
import psycopg2
from datetime import datetime
import config
class ServerInfo:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, brief="displays info about the server")
    async def info(self, ctx):
        online = 0
        for i in ctx.message.server.members:
            if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
                online += 1
        all_users = []
        for user in ctx.message.server.members:
            all_users.append('{}#{}'.format(user.name, user.discriminator))
        all_users.sort()
        all = '\n'.join(all_users)
        textchans = [x for x in ctx.message.server.channels if x.type == discord.ChannelType.text]
        voicechans = [x for x in ctx.message.server.channels if x.type == discord.ChannelType.voice]
        channel_count = len(textchans)
        voices = len(voicechans)
        role_count = len(ctx.message.server.roles)
        emoji_count = len(ctx.message.server.emojis)
        em = discord.Embed(color=0xea7938)
        em.add_field(name='Name', value=ctx.message.server.name)
        em.add_field(name='Owner', value=ctx.message.server.owner, inline=False)
        em.add_field(name='Members', value=ctx.message.server.member_count)
        em.add_field(name='Currently Online', value=online)
        em.add_field(name='Text Channels', value=str(channel_count))
        em.add_field(name='Voice Channels', value=str(voices))
        em.add_field(name='Region', value=ctx.message.server.region)
        em.add_field(name='Verification Level', value=str(ctx.message.server.verification_level))
        em.add_field(name='Highest role', value=ctx.message.server.role_hierarchy[0])
        em.add_field(name='Number of roles', value=str(role_count))
        em.add_field(name='Number of emotes', value=str(emoji_count), inline=True)
        em.add_field(name='Created At', value=ctx.message.server.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
        em.set_thumbnail(url=ctx.message.server.icon_url)
        em.set_author(name='Server Info', icon_url='https://i.imgur.com/RHagTDg.png')
        em.set_footer(text='Server ID: %s' % ctx.message.server.id)
        await self.bot.say(embed=em)

    @commands.command(pass_context=True, brief="Returns caught message.")
    async def snipe(self, ctx):
        db = psycopg2.connect(host=config.host,database=config.database, user=config.user, password=config.password)
        server = ctx.message.server
        cursor = db.cursor()
        cursortwo = db.cursor()
        cursor.execute('''SELECT * FROM deleted''')
        cursortwo.execute('''SELECT * FROM edited''')
        chan = cursor.fetchall()
        chane = cursortwo.fetchall()
        notFound = True
        for x in range(0,len(chan)):
            if chan[x][1] == ctx.message.channel.id:
                notFound = False
                meme = x
                msgde = chan[meme][2]

        for x in range(0,len(chane)):
            if chane[x][1] == ctx.message.channel.id:
                memes = x
                msge = chane[memes][2]
                aftermsg = chane[memes][3]
                notFound = False
        if notFound == True:
            em = discord.Embed(description="There are no sniped messages in this channel")
            em.set_author(name="Whoops!")
            await self.bot.send_message(ctx.message.channel, embed=em)
            return
        elif notFound == False:
            try:
                deletetime = chan[meme][3]
                deleted = True
            except:
                deleted = None
                pass
            try:
                edittime = chane[memes][4]
                edited = True
            except:
                edited = None
                pass
            # deletetime = datetime.strptime(dtime, '%Y-%m-%d %H:%M:%S.%f')
            
            # edittime = datetime.strptime(etime, '%Y-%m-%d %H:%M:%S.%f')
            if edited != None and deleted != None:
                if edittime < deletetime:
                    author = chan[meme][4]
                    membername = server.get_member(author)
                    em = discord.Embed(description=msgde)
                    em.set_author(name=membername.name+" said...")
                    em.set_footer(text=str(deletetime))
                    await self.bot.send_message(ctx.message.channel, embed=em)
                elif edittime > deletetime:
                    author = chane[memes][5]
                    membername = server.get_member(author)
                    if membername.bot == True:
                        return
                    else:
                        em = discord.Embed(description="Before: "+msge+"\nAfter: "+aftermsg)
                        em.set_author(name=membername.name+" said...")
                        em.set_footer(text=str(edittime))
                        await self.bot.send_message(ctx.message.channel, embed=em)
            elif edited == None:
                author = chan[meme][4]
                membername = server.get_member(author)
                em = discord.Embed(description=msgde)
                em.set_author(name=membername.name+" said...")
                em.set_footer(text=str(deletetime))
                await self.bot.send_message(ctx.message.channel, embed=em)
            elif deleted == None:
                author = chane[memes][5]
                membername = server.get_member(author)
                if membername.bot == True:
                    return
                else:
                    em = discord.Embed(description="Before: "+msge+"\nAfter: "+aftermsg)
                    em.set_author(name=membername.name+" said...")
                    em.set_footer(text=str(edittime))
                    await self.bot.send_message(ctx.message.channel, embed=em)
        db.close()

def setup(bot):
    bot.add_cog(ServerInfo(bot))