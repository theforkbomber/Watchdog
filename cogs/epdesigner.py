import asyncio

import discord
from discord.ext import commands
from PyDictionary import PyDictionary
import psycopg2
import config

class EpDesign:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    @commands.has_role("DOKI DOKI Literature Club!") 
    async def epdesign(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say("Unknown command")

    @epdesign.command(pass_context=True)
    @commands.has_role("DOKI DOKI Literature Club!")
    async def make(self, ctx):
        db = psycopg2.connect(host=config.host,database=config.database, user=config.user, password=config.password)
        cursor = db.cursor()
        msg = await self.bot.send_message(ctx.message.channel, "What is the episode name?")
        await asyncio.sleep(1)
        epname = await self.bot.wait_for_message(channel=ctx.message.channel)
        epname = epname.content
        epname = epname.replace(" ","_")
        cursor.execute('''CREATE TABLE '''+epname+'''(id SERIAL PRIMARY KEY, channel TEXT, trigger TEXT, type TEXT, prompt TEXT, answer TEXT DEFAULT NULL, response TEXT DEFAULT NULL)''')
        db.commit()
        msg = await self.bot.send_message(ctx.message.channel, "How many prompts")
        await asyncio.sleep(1)
        waiting = await self.bot.wait_for_message(channel=ctx.message.channel)
        waiting = waiting.content
        
        print(waiting)
        if waiting.lower() == "cancel":
            db.close()
            return
        else:
            if waiting.isnumeric() == True:
                iterate = int(waiting)
                await self.bot.send_message(ctx.message.channel, "Where will we be performing?")
                await asyncio.sleep(1)
                channeld = await self.bot.wait_for_message(channel=ctx.message.channel)
                if channeld.raw_channel_mentions.__len__()>0:
                    for channel in channeld.raw_channel_mentions:
                        channeld = self.bot.get_channel(channel)
                        channeld = channeld.id
                else:
                    channeld = str(channeld.content)
                for x in range(0, iterate):
                    msg = await self.bot.send_message(ctx.message.channel, "What will the trigger be? ["+str(x+1)+"]")
                    await asyncio.sleep(1)
                    trigger = await self.bot.wait_for_message(channel=ctx.message.channel)
                    trigger = str(trigger.content)
                    await self.bot.edit_message(msg, "What type of prompt? ["+str(x+1)+"]")
                    typeprompt = await self.bot.wait_for_message(channel=ctx.message.channel)
                    typeprompt = typeprompt.content
                    types = ["n","sq","ynv","nv","rsq"]
                    invalid = True
                    while invalid == True:
                        if typeprompt in types:
                            invalid = False
                            break
                        else:
                            await self.bot.edit_message(msg, "That's not right, use `n` `sq` `ynv` `rsq` or `nv` ["+str(x+1)+"]")
                            typeprompt = await self.bot.wait_for_message(channel=ctx.message.channel)
                            typeprompt = typeprompt.content
                    if typeprompt == "n":
                        await self.bot.edit_message(msg, "What do you want me to say? ["+str(x+1)+"]")
                        prompt = await self.bot.wait_for_message(channel=ctx.message.channel)
                        await self.bot.edit_message(msg, "👌")
                        prompt = str(prompt.content)
                        cursor.execute('''INSERT INTO '''+epname+'''(channel, trigger, type, prompt)VALUES(%s,%s,%s,%s)RETURNING id;''', (channeld, trigger, typeprompt, prompt))
                    
                    elif typeprompt == "sq":
                        await self.bot.edit_message(msg, "What's the security question? ["+str(x+1)+"]")
                        prompt = await self.bot.wait_for_message(channel=ctx.message.channel)
                        await self.bot.edit_message(msg, "What's the answer? ["+str(x+1)+"]")
                        answer = await self.bot.wait_for_message(channel=ctx.message.channel)
                        await self.bot.edit_message(msg, "👌")
                        prompt = str(prompt.content)
                        answer = str(answer.content)
                        cursor.execute('''INSERT INTO '''+epname+'''(channel, trigger, type, prompt, answer)VALUES(%s,%s,%s,%s,%s)RETURNING id;''', (channeld, trigger, typeprompt, prompt, answer))
                    
                    elif typeprompt == "rsq":
                        await self.bot.edit_message(msg, "What's the security question? ["+str(x+1)+"]")
                        prompt = await self.bot.wait_for_message(channel=ctx.message.channel)
                        await self.bot.edit_message(msg, "What's the answer(in numerical emojis, split with spaces)? ["+str(x+1)+"]")
                        answer = await self.bot.wait_for_message(channel=ctx.message.channel)
                        await self.bot.edit_message(msg, "What's the response? ["+str(x+1)+"]")
                        response = await self.bot.wait_for_message(channel=ctx.message.channel)
                        await self.bot.edit_message(msg, "👌")
                        prompt = str(prompt.content)
                        answer = str(answer.content)
                        response = str(response.content)
                        cursor.execute('''INSERT INTO '''+epname+'''(channel, trigger, type, prompt, answer, response)VALUES(%s,%s,%s,%s,%s,%s)RETURNING id;''', (channeld, trigger, typeprompt, prompt, answer, response))
                        

                    elif typeprompt == "ynv":
                        await self.bot.edit_message(msg, "What's the prompt? ["+str(x+1)+"]")
                        prompt = await self.bot.wait_for_message(channel=ctx.message.channel)
                        prompt = str(prompt.content)
                        await self.bot.edit_message(msg, "👌")
                        cursor.execute('''INSERT INTO '''+epname+'''(channel, trigger, type, prompt)VALUES(%s,%s,%s,%s)RETURNING id;''', (channeld, trigger, typeprompt, prompt))

                    elif typeprompt == "nv":
                        await self.bot.edit_message(msg, "What's the prompt? ["+str(x+1)+"] `this only takes a prompt, will soon allow a choice of options between 2-10, not just a 1-10 vote.`")
                        prompt = await self.bot.wait_for_message(channel=ctx.message.channel)
                        # await self.bot.edit_message(msg, "How many options? ["+str(x+1)+"]")
                        # answer = await self.bot.wait_for_message(channel=ctx.message.channel)
                        prompt = str(prompt.content)
                        await self.bot.edit_message(msg, "👌")
                        # answer = str(answer.content)
                        cursor.execute('''INSERT INTO '''+epname+'''(channel, trigger, type, prompt)VALUES(%s,%s,%s,%s)RETURNING id;''', (channeld, trigger, typeprompt, prompt))
                db.commit()
                db.close()

    @epdesign.command(pass_context=True)
    @commands.has_role("DOKI DOKI Literature Club!")
    async def start(self, ctx):
        msg = await self.bot.send_message(ctx.message.channel, "What is the episode name?")
        await asyncio.sleep(1)
        epname = await self.bot.wait_for_message(channel=ctx.message.channel)
        epname = epname.content
        try:
            db = psycopg2.connect(host=config.host,database=config.database, user=config.user, password=config.password)
            c = db.cursor()
            c.execute('SELECT * FROM '+epname) 
            table = c.fetchall()
            server = ctx.message.server
            channel = server.get_channel(str(table[0][1]))
            for x in range(0,len(table)):
                await self.bot.wait_for_message(channel=channel, content=table[x][2])
                typer = table[x][3]
                if typer == "n":
                    await self.bot.send_message(channel, table[x][4])
                    print(table[x][4])
                elif typer == "sq":
                    await self.bot.send_message(channel, table[x][4])
                    print(table[x][4])
                    await self.bot.wait_for_message(channel=channel, content=table[x][5])
                    await self.bot.send_message(channel, "Correct!")
                elif typer == "ynv":
                    msg = await self.bot.send_message(channel, table[x][4])
                    await self.bot.add_reaction(emoji="\U00002705", message=msg)
                    await self.bot.add_reaction(emoji="\U0000274e", message=msg)
                    await self.bot.wait_for_reaction(message=msg, emoji="🛑")
                    em = discord.Embed(color=0xea7938)
                    waa = discord.Reaction(emoji="\U00002705", message=msg)
                    wa = await self.bot.get_reaction_users(waa)
                    em.add_field(name='Yes', value=str(len(wa)-1))
                    wbb = discord.Reaction(emoji="\U0000274e", message=msg)
                    wb = await self.bot.get_reaction_users(wbb)
                    em.add_field(name='No', value=str(len(wb)-1))
                    await self.bot.say(embed=em)
                    if len(wa)-1 > len(wb)-1:
                        await self.bot.say("Yes output(still in the works)")
                    elif len(wa)-1 < len(wb)-1:
                        await self.bot.say("No output(still in the works)")
                    if len(wa)-1 == len(wb)-1:
                        await self.bot.say("Tie!(still in the works)")
                elif typer == "nv":
                    msg = await self.bot.send_message(channel, table[x][4])
                    await self.bot.add_reaction(emoji="1\u20e3", message=msg)
                    await self.bot.add_reaction(emoji="2\u20e3", message=msg)
                    await self.bot.add_reaction(emoji="3\u20e3", message=msg)
                    await self.bot.add_reaction(emoji="4\u20e3", message=msg)
                    await self.bot.add_reaction(emoji="5\u20e3", message=msg)
                    await self.bot.add_reaction(emoji="6\u20e3", message=msg)
                    await self.bot.add_reaction(emoji="7\u20e3", message=msg)
                    await self.bot.add_reaction(emoji="8\u20e3", message=msg)
                    await self.bot.add_reaction(emoji="9\u20e3", message=msg)
                    await self.bot.add_reaction(emoji="\U0001f51f", message=msg)
                    await self.bot.wait_for_reaction(message=msg, emoji="🛑")
                    em = discord.Embed(color=0xea7938)
                    waa = discord.Reaction(emoji="1\u20e3", message=msg)
                    one = await self.bot.get_reaction_users(waa)
                    wbb = discord.Reaction(emoji="2\u20e3", message=msg)
                    two = await self.bot.get_reaction_users(wbb)
                    wbb = discord.Reaction(emoji="3\u20e3", message=msg)
                    three = await self.bot.get_reaction_users(wbb)
                    wbb = discord.Reaction(emoji="4\u20e3", message=msg)
                    four = await self.bot.get_reaction_users(wbb)
                    wbb = discord.Reaction(emoji="5\u20e3", message=msg)
                    five = await self.bot.get_reaction_users(wbb)
                    wbb = discord.Reaction(emoji="6\u20e3", message=msg)
                    six = await self.bot.get_reaction_users(wbb)
                    wbb = discord.Reaction(emoji="7\u20e3", message=msg)
                    seven = await self.bot.get_reaction_users(wbb)
                    wbb = discord.Reaction(emoji="8\u20e3", message=msg)
                    eight = await self.bot.get_reaction_users(wbb)
                    wbb = discord.Reaction(emoji="9\u20e3", message=msg)
                    nine = await self.bot.get_reaction_users(wbb)
                    wbb = discord.Reaction(emoji="\U0001f51f", message=msg)
                    ten = await self.bot.get_reaction_users(wbb)
                    nums = []
                    nums.append(int(len(one)))
                    nums.append(int(len(two)))
                    nums.append(int(len(three)))
                    nums.append(int(len(four)))
                    nums.append(int(len(five)))
                    nums.append(int(len(six)))
                    nums.append(int(len(seven)))
                    nums.append(int(len(eight)))
                    nums.append(int(len(nine)))
                    nums.append(int(len(ten)))
                    maxi = nums.index(max(nums)) + 1
                    if maxi == 1:
                        await self.bot.send_message(channel, "1")
                    if maxi == 2:
                        await self.bot.send_message(channel, "2")
                    if maxi == 3:
                        await self.bot.send_message(channel, "3")
                    if maxi == 4:
                        await self.bot.send_message(channel, "4")
                    if maxi == 5:
                        await self.bot.send_message(channel, "5")
                    if maxi == 6:
                        await self.bot.send_message(channel, "6")
                    if maxi == 7:
                        await self.bot.send_message(channel, "7")
                    if maxi == 8:
                        await self.bot.send_message(channel, "8")
                    if maxi == 9:
                        await self.bot.send_message(channel, "9")
                    if maxi == 10:
                        await self.bot.send_message(channel, "10")
                elif typer == "rsq":
                    t = table[x][5]
                    ta = t.split(" ")
                    ppl = await self.bot.send_message(channel, table[x][4])
                    print(ta)
                    for y in range(0,len(ta)):
                        emoji = ta[y]
                        print(emoji)
                        if emoji == "1⃣":
                            emoji = "1\u20e3"
                        if emoji == "2⃣":
                            emoji = "2\u20e3"
                        if emoji == "3⃣":
                            emoji = "3\u20e3"
                        if emoji == "4⃣":
                            emoji = "4\u20e3"
                        if emoji == "5⃣":
                            emoji = "5\u20e3"
                        if emoji == "6⃣":
                            emoji = "6\u20e3"
                        if emoji == "7⃣":
                            emoji = "7\u20e3"
                        if emoji == "8⃣":
                            emoji = "8\u20e3"
                        if emoji == "9⃣":
                            emoji = "9\u20e3"
                        if emoji == "🔟":
                            emoji = "\U0001f51f"
                        await self.bot.wait_for_reaction(message=ppl, emoji=str(emoji))
                    await self.bot.send_message(channel, table[x][6])

                db.close()
        except:
            self.bot.say("It seems that was not a valid episode name. Use >os.epdesign list to find out the list of episodes designed.")

    @epdesign.command(pass_context=True)
    @commands.has_role("DOKI DOKI Literature Club!")
    async def list(self, ctx):
        db = psycopg2.connect(host=config.host,database=config.database, user=config.user, password=config.password)      
        c = db.cursor()
        a = ""
        d = c.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
        d = c.fetchall()
        for x in range(0,len(d)):
            e = str(d[x])
            if e == "deleted" or e == "edited":
                pass
            else:
                a = a + str(e[2:len(e)-3])+"\n"
        if len(a) == 0:
            await self.bot.say("NOTHING PRESENT")
        else:
            await self.bot.send_message(ctx.message.channel, str(a))
            db.close()

    @epdesign.command(pass_context=True)
    @commands.has_role("DOKI DOKI Literature Club!")
    async def remove(self, ctx, tablename):
        try:
            db = psycopg2.connect(host=config.host,database=config.database, user=config.user, password=config.password)      
            c = db.cursor()
            c.execute('DROP TABLE '+tablename)
            db.commit()
            db.close()
            await self.bot.say("👌")
        except:
            await self.bot.say("That just doesn't exist :P, look in the list with >os.epdesign list")
            
                        



    
def setup(bot):
    bot.add_cog(EpDesign(bot))
