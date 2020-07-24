import asyncio
import random
import os

import discord
from discord.ext import commands, tasks

client = commands.Bot(command_prefix='?')


@client.event
async def on_ready():
    print('Bot is ready.')
    await client.change_presence(activity=discord.Game(name="still in BETA!"))


@client.command(aliases=["-postmeme", "-Pm", "-PM", "-Postmeme", "-PostMeme"])
async def pm(ctx):
    try:
        memelink = ctx.message.attachments[0].url
        with open(f"{ctx.message.id}.txt", "a") as f:
            f.write(f"{memelink}")
        # await ctx.channel.purge(limit=1)
        await ctx.send("Your meme has been submitted!")
        for channel in ctx.author.guild.channels:
            if str(channel) == "pending-memes":
                await channel.send(f"{ctx.author} has requested to publish a meme with the id of {ctx.message.id}")
    except Exception as e:
        print(e)
        await ctx.send("That is not a valid meme.")


@client.command()
@commands.has_permissions(manage_messages=True)
async def am(ctx, id):
    try:
        with open(f"{id}.txt", "r") as f:
            url = f.read()
        with open("memes.txt", "a") as f:
            f.write(f"{url}\n")
            await ctx.send("That meme has been accepted.")
        os.remove(f"{id}.txt")
    except Exception as e:
        print(e)
        await ctx.send("That meme couldn't be accepted.")


@client.command(aliases=["-Meme"])
async def meme(ctx):
    try:
        lines = open('memes.txt', "r").read().splitlines()
        myline = random.choice(lines)
        rmeme = discord.Embed(title="Here is a meme for you!")
        rmeme.set_image(url=f"{myline}")
        await ctx.send(embed=rmeme)
    except Exception as e:
        print(e)
        await ctx.send("There has been an error while trying to cheer you up!")


@client.command()
async def test(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send('Test.')






























client.run('NzM2MTU4Mjc1NDY0MjAwMjA1.Xxqu0g.owKc5W59Y4-B8OPxMiau06EhjUM')