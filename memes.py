import asyncio
import random
import json

import discord
from discord.ext import commands, tasks

client = commands.Bot(command_prefix='?')


@client.event
async def on_ready() :
    print('Bot is ready.')
    print('MemeMachine')
    await client.change_presence(activity=discord.Game(name="still in BETA!"))


@client.command()
async def test(ctx) :
    await ctx.send('Test.')


client.run('NzM2MTU4Mjc1NDY0MjAwMjA1.Xxqu0g.owKc5W59Y4-B8OPxMiau06EhjUM')
