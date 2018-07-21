import asyncio
import discord
from discord.ext import commands

class Moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, brief="'remove @someone --tmp' kicks, 'remove @someone --pm' bans")
    @commands.has_permissions(manage_roles=True)
    async def remove(self, ctx, member, typer=None, *, reason=None):
        if typer == "--pm":
            if reason == None:
                for user in ctx.message.mentions:
                    em = discord.Embed(description='No reason given.', colour=0xf44242)
                    em.set_author(name="You have been removed from directory `"+ctx.message.server.name+"` by "+ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
                    await self.bot.send_message(user, embed=em)
                    await self.bot.ban(user, delete_message_days=7)
                    await self.bot.say("*"+user.name+".chr deleted successfully.*")
            else:
                for user in ctx.message.mentions:
                    em = discord.Embed(description='Reason: '+str(reason), colour=0xf44242)
                    em.set_author(name="You have been removed from directory `"+ctx.message.server.name+"` by "+ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
                    await self.bot.send_message(user, embed=em)
                    await self.bot.ban(user, delete_message_days=7)
                    await self.bot.say("*"+user.name+".chr deleted successfully.*")
        elif typer == "--tmp":
            if reason == None:
                for user in ctx.message.mentions:
                    em = discord.Embed(description='No reason given.', colour=0xf44242)
                    em.set_author(name="You have been removed from directory `"+ctx.message.server.name+"` by "+ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
                    await self.bot.send_message(user, embed=em)
                    await self.bot.kick(user)
                    await self.bot.say("*"+user.name+".chr deleted successfully.*")
            else:
                for user in ctx.message.mentions:
                    em = discord.Embed(description='Reason: '+str(reason), colour=0xf44242)
                    em.set_author(name="You have been removed from directory `"+ctx.message.server.name+"` by "+ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
                    await self.bot.send_message(user, embed=em)
                    await self.bot.kick(user)
                    await self.bot.say("*"+user.name+".chr deleted successfully.*")

    @commands.command(pass_context=True, brief="Remove channels", aliases=["rmchan", "removechannel"])
    @commands.has_permissions(manage_roles=True)
    async def rmchannel(self, ctx, channel):
        for x in ctx.message.raw_channel_mentions:
            channel = ctx.message.server.get_channel(x)
            await self.bot.delete_channel(channel)

    @commands.command(pass_context=True, brief="Edits channels.")
    @commands.has_permissions(manage_roles=True)
    async def editchannels(self, ctx, channel, *, name):
        for channels in ctx.message.raw_channel_mentions:
            channels = self.bot.get_channel(channels)
            await self.bot.edit_channel(name=name, channel=channels)

    @commands.command(pass_context="True")
    @commands.has_permissions(manage_roles=True)
    async def addchannel(self, ctx, typer=None, *, name=None):
        server = ctx.message.server  
        if typer == "V":
            await self.bot.create_channel(server, name, type=discord.ChannelType.voice)
        else:
            await self.bot.create_channel(server, typer)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def clean(self, ctx, num=None):
        channel = ctx.message.channel
        if num == None:
            try:
                await self.bot.purge_from(channel, limit=20)
                mess = await self.bot.send_message(ctx.message.channel,"Done!")
                
            except Exception as e:
                getid = ctx.message.server.get_member("447737745365008385")
                if getid.server_permissions.manage_server == False:
                    em = discord.Embed(description="Requirements not met:\n-Manage server\nDETAILS:\n"+e, colour=0xf44242)
                    em.set_author(name="Failed to purge bot messages.", icon_url=ctx.message.author.avatar_url)
                    my_message = await self.bot.send_message(ctx.message.channel, embed=em)  
                else:
                    em = discord.Embed(description="Caught an error!\nDETAILS:\n"+e, colour=0xf44242)
                    em.set_author(name="Failed to purge bot messages.", icon_url=ctx.message.author.avatar_url)
                    my_message = await self.bot.send_message(ctx.message.channel, embed=em) 
        else:
            try:
                todelet = int(num)
                await self.bot.purge_from(channel, limit=todelet)
                mess = await self.bot.send_message(ctx.message.channel,"Done!")
                
            except Exception as e:
                e = str(e)
                getid = ctx.message.server.get_member("447737745365008385")
                if getid.server_permissions.manage_server == False:
                    em = discord.Embed(description="Requirements not met:\n-Manage server\nDETAILS:\n"+e, colour=0xf44242)
                    em.set_author(name="Failed to purge bot messages.", icon_url=ctx.message.author.avatar_url)
                    my_message = await self.bot.send_message(ctx.message.channel, embed=em)  
                else:
                    em = discord.Embed(description="Caught an error!\nDETAILS:\n"+e, colour=0xf44242)
                    em.set_author(name="Failed to purge bot messages.", icon_url=ctx.message.author.avatar_url)
                    my_message = await self.bot.send_message(ctx.message.channel, embed=em) 

def setup(bot):
    bot.add_cog(Moderation(bot))