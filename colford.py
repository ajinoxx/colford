import discord
import time
from discord.ext import commands
import os

client = commands.Bot(command_prefix = '.')

logsID = 755893521478582409
mainID = 754438628758913098

adminID = 754449876401520846
starterID = 754449876401520846

trooperID = 262622460321464321

#TODO
#Disconnect joe at random times when he joins a vc
#Make sure joe stays roleless on join



@client.event
async def on_ready():
    print('Bot is ready and running!')

@client.event
async def on_member_join(member):
    print(f'{member} joined the server.')
    mainChannel = client.get_channel(mainID)
    await mainChannel.send(f'{member.mention} ({member}) joined the server.')
    if member.id != trooperID:
        role = discord.utils.get(member.guild.roles, id=starterID) #Make sure IrvinsMom role is ABOVE the target role
        await member.add_roles(role)

@client.event
async def on_member_remove(member):
    print(f'{member} left the server.') 
    mainChannel = client.get_channel(mainID)
    await mainChannel.send(f'{member.mention} ({member}) left the server.')



@client.command(aliases=['p'])
async def ping(ctx):
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
        else:
            await ctx.send('You don\'t have the permissions to do that.')
    except:
        print('Must enter valid amount and user tag.')

@client.command(aliases=['u'])
async def uidCheck(ctx, uid):
    await ctx.send(uid[3:len(uid)-1])


client.run(os.environ['token'])
