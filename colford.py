#discord.py 
import discord
from discord.ext import commands
#time
import time
from datetime import datetime
#heroku
import os

client = commands.Bot(command_prefix = '.')

scienceClubID = 760895586659467334
biggusBrainusID = 543185885232103434

logsID = 645817145007144981 #755893521478582409 #test
mainBBID = 753429614465908817 #754438628758913098 #test

mainSCID = 760895587184541777
starterSCID = 760896390955401216
boardID = 760895783015809084
logsSCID = 760911595143561276
muteSCID = 760912284154724452

adminID = 627267659364302848 #754449876401520846 #test
starterID = 543187460021288960 #754449876401520846 #test
apID = 543619723842158622
myID = 191334024612937729

bellMsgID = 757598815351078962
bellRoleID = 756238148404510802

muteID = 543921175722721289

trooperID = 262622460321464321

#TODO
#Grab time, ping @bell for changing of periods in seperate chat, as well as the 5-min warnings
#For .cu, make while loop len(deletedMessages) <= amount, purge(limit=None, check=is_user), but check a way to prevent infinite loop/time (wait_for?), maybe while loop len(dM) and timeTaken < 3seconds?

@client.event
async def on_ready():
    print('Bot is ready and running!')

@client.event
async def on_member_join(member):
    print(f'{member} joined the server.')
    #member.guild gives the guild
    #mainChannel = client.get_channel(mainBBID)
    if member.guild.id == biggusBrainusID:
        mainChannel = member.guild.get_channel(mainBBID)
        role = member.guild.get_role(starterID)
    if member.guild.id == scienceClubID:
        mainChannel = member.guild.get_channel(mainSCID)
        role = member.guild.get_role(starterSCID)
    print(f'mainChannel: {mainChannel}')
    await mainChannel.send(f'{member.mention} ({member}) joined the server.')
    #await member.dm_channel.send("Welcome to Biggus Brainus!\nIf you'd like to get notified on class bell updates, make you sure you check out the roles channel.")
    if member.id != trooperID:
        #role = member.guild.get_role(starterID) #discord.utils.get(member.guild.roles, id=starterID) #Make sure IrvinsMom role is ABOVE the target role
        #if role == None:
        #    role = member.guild.get_role(starterSCID)
        await member.add_roles(role)

@client.event
async def on_member_remove(member):
    print(f'{member} left the server.') 
    #mainChannel = member.guild.get_channel(mainBBID)
    #if mainChannel == None:
    #    mainChannel = member.guild.get_channel(mainSCID)
    if member.guild.id == biggusBrainusID:
        mainChannel = member.guild.get_channel(mainBBID)
    if member.guild.id == scienceClubID:
        mainChannel = member.guild.get_channel(mainSCID)
    print(f'mainChannel: {mainChannel}')
    await mainChannel.send(f'{member.mention} ({member}) left the server.')

@client.event
async def on_raw_reaction_add(payload):
    print(f'Someone has reacted ({payload.emoji.name}) to a message.')
    if payload.message_id == bellMsgID and payload.emoji.name == '🔔':
        print('Someone has added a bell to the bell message.')
        guildObj = client.get_guild(payload.guild_id)
        memObj = guildObj.get_member(payload.user_id)
        if memObj != None:
            roleObj = guildObj.get_role(bellRoleID)
            await memObj.add_roles(roleObj)
            print(f'{memObj} got the role of {roleObj.name}')

@client.event
async def on_raw_reaction_remove(payload):
    print(f'Someone has removed a reaction ({payload.emoji.name})to a message.')
    if payload.message_id == bellMsgID and payload.emoji.name == '🔔':
        print('Someone has removed a bell from the bell message.')
        guildObj = client.get_guild(payload.guild_id)
        memObj = guildObj.get_member(payload.user_id)
        if memObj != None:
            if discord.utils.find(lambda r: r.id == bellRoleID,memObj.roles):
                print('Member that removed the reaction has the bell role.')
                roleObj = guildObj.get_role(bellRoleID)
                await memObj.remove_roles(roleObj)
                print(f'{memObj} lost the role of {roleObj.name}')

@client.command(aliases=['p'])
async def ping(ctx):
    if ctx.author.id == myID:
        await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases=['c'])
async def clear(ctx, amount=5):
    try:    
        if amount <= 0:
                await ctx.send('Cannot clear an amount less than 1.')
                return
        elif discord.utils.find(lambda r: r.id == adminID, ctx.message.author.roles):
            print(f'{ctx.message.author} has admin role, clearing {amount} messages in {ctx.channel}.')    
            await ctx.channel.purge(limit=amount)
            numMessage = await ctx.send(f'Cleared {amount} messages.')
            await ctx.guild.get_channel(logsID).send(f'{ctx.author.mention} ({ctx.author}) cleared {amount} messages in {ctx.channel.mention} ({ctx.channel}).')
            await numMessage.delete(delay=3)
        elif discord.utils.find(lambda r: r.id == boardID, ctx.message.author.roles):
            print(f'{ctx.message.author} has admin role, clearing {amount} messages in {ctx.channel}.')    
            await ctx.channel.purge(limit=amount)
            numMessage = await ctx.send(f'Cleared {amount} messages.')
            await ctx.guild.get_channel(logsSCID).send(f'{ctx.author.mention} ({ctx.author}) cleared {amount} messages in {ctx.channel.mention} ({ctx.channel}).')
            await numMessage.delete(delay=3)
        else:
            await ctx.send('You don\'t have the permissions to do that')
    except:
        print('Must enter a valid amount.')

@client.command(aliases=['cu'])
async def clearUser(ctx, tag : discord.abc.User, amount=10):
    try:
        def is_user(m):
            return m.author == tag
        if amount <= 0:
            await ctx.send('Cannot clear an amount less than 1.')
            return
        elif discord.utils.find(lambda r: r.id == adminID, ctx.message.author.roles):                       
            deleted = await ctx.channel.purge(limit=amount, check=is_user)
            print(f'{ctx.message.author} has admin role, searching {amount} messages from {tag.name}. Cleared {len(deleted)} messages in {ctx.channel}.')
            numMessage = await ctx.send(f'Searched {amount} messages, cleared {len(deleted)} messages from {tag.name}.')
            await ctx.guild.get_channel(logsID).send(f'{ctx.author.mention} ({ctx.author}) searched {amount} messages, cleared {len(deleted)} messages from {tag.mention} ({tag}) in {ctx.channel.mention} ({ctx.channel}).')
            await numMessage.delete(delay=5)
            await ctx.message.delete(delay=None)
        elif discord.utils.find(lambda r: r.id == boardID, ctx.message.author.roles):                       
            deleted = await ctx.channel.purge(limit=amount, check=is_user)
            print(f'{ctx.message.author} has admin role, searching {amount} messages from {tag.name}. Cleared {len(deleted)} messages in {ctx.channel}.')
            numMessage = await ctx.send(f'Searched {amount} messages, cleared {len(deleted)} messages from {tag.name}.')
            await ctx.guild.get_channel(logsSCID).send(f'{ctx.author.mention} ({ctx.author}) searched {amount} messages, cleared {len(deleted)} messages from {tag.mention} ({tag}) in {ctx.channel.mention} ({ctx.channel}).')
            await numMessage.delete(delay=5)
            await ctx.message.delete(delay=None)
        else:
            await ctx.send('You don\'t have the permissions to do that.')
    except:
        print('Must enter valid amount and user tag.')

@client.command(aliases=['m'])
async def mute(ctx, tag : discord.Member):
    if discord.utils.find(lambda r: r.id == adminID, ctx.message.author.roles):
        muteRole = discord.utils.get(ctx.guild.roles, id=muteID)
        starterRole = discord.utils.get(ctx.guild.roles, id=starterID)
        await tag.add_roles(muteRole)
        await tag.remove_roles(starterRole)
        await ctx.guild.get_channel(logsID).send(f'{ctx.author.mention} ({ctx.author}) muted {tag.mention} ({tag.name})')
        await ctx.send(f'Muted {tag.mention}')
    elif discord.utils.find(lambda r: r.id == boardID, ctx.message.author.roles):
        muteRole = discord.utils.get(ctx.guild.roles, id=muteSCID)
        starterRole = discord.utils.get(ctx.guild.roles, id=starterSCID)
        await tag.add_roles(muteRole)
        await tag.remove_roles(starterRole)
        await ctx.guild.get_channel(logsSCID).send(f'{ctx.author.mention} ({ctx.author}) muted {tag.mention} ({tag.name})')
        await ctx.send(f'Muted {tag.mention}')
    else:
        await ctx.send("You don't have permission to use this command.")

@client.command(aliases=['um'])
async def unmute(ctx, tag : discord.Member):
    if discord.utils.find(lambda r: r.id == adminID, ctx.message.author.roles):
        muteRole = discord.utils.get(ctx.guild.roles, id=muteID)
        starterRole = discord.utils.get(ctx.guild.roles, id=starterID)
        await tag.remove_roles(muteRole)
        await tag.add_roles(starterRole)
        await ctx.guild.get_channel(logsID).send(f'{ctx.author.mention} ({ctx.author}) unmuted {tag.mention} ({tag.name})')
        await ctx.send(f'Unmuted {tag.mention}')
    elif discord.utils.find(lambda r: r.id == boardID, ctx.message.author.roles):
        muteRole = discord.utils.get(ctx.guild.roles, id=muteSCID)
        starterRole = discord.utils.get(ctx.guild.roles, id=starterSCID)
        await tag.remove_roles(muteRole)
        await tag.add_roles(starterRole)
        await ctx.guild.get_channel(logsSCID).send(f'{ctx.author.mention} ({ctx.author}) unmuted {tag.mention} ({tag.name})')
        await ctx.send(f'Unmuted {tag.mention}')
    else:
        await ctx.send("You don't have permission to use this command.")

@client.command(aliases=['v'])
async def version(ctx):
    if ctx.author.id == myID:
        await ctx.send('Bot version 1.6.0')

@client.command()
async def dow(ctx):
    #await ctx.send(time.struct_time().tm_wday)#datetime.date.today().weekday())
    await ctx.send(datetime.now().strftime("%H:%M:%S"))

@client.command()
async def load(ctx, extension):
    if ctx.author.id == myID:
        client.load_extension(f'cogs.{extension}')
        ctx.send('Loaded extension!')
    else:
        ctx.send("You don't have permission to use this command.")

@client.command()
async def unload(ctx, extension):
    if ctx.author.id == myID:
        client.unload_extension(f'cogs.{extension}')
        ctx.send('Unloaded extension!')
    else:
        ctx.send("You don't have permission to use this command.")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#@client.command()
#async def cum(ctx):
#    if discord.utils.find(lambda r: r.id == adminID, ctx.message.author.roles) and discord.utils.find(lambda r: r.id == apID, ctx.message.author.roles):
#        await ctx.send("You're good to go for cum.")
#    else:
#        await ctx.send("No cumming allowed.")

#@client.command(aliases=['u'])
#async def uidCheck(ctx, uid):
    #await ctx.send(uid[3:len(uid)-1])

client.run(os.environ['token'])