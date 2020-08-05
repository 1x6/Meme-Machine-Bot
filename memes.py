import asyncio
import random
import os

import discord
from discord.ext import commands, tasks

client = commands.Bot(command_prefix='?')
client.remove_command('help')



def check_if_owner(ctx):
    return ctx.message.author.id == 445656896876183552 or 470261090798796800


@client.event
async def on_ready():
    print('Bot is ready.')
    print('MemeMachine')
    await client.change_presence(activity=discord.Game(name="still in BETA!"))


@client.command(aliases=["postmeme", "Pm", "PM", "Postmeme", "PostMeme"])
async def pm(ctx):
    try:
        memelink = ctx.message.attachments[0].url
        with open(f"{ctx.message.id}.txt", "a") as f:
            f.write(f"{memelink}")
        #await ctx.channel.purge(limit=1)
        await ctx.send("Your meme has been submitted!")
        gyro = client.get_user(445656896876183552)
        tic = client.get_user(470261090798796800)
        await gyro.send(f"{ctx.author} has requested to publish a meme with the id of {ctx.message.id} {memelink}")
        await tic.send(f"{ctx.author} has requested to publish a meme with the id of {ctx.message.id} {memelink}")
    except Exception as e:
        print(e)
        await ctx.send("That is not a valid meme.")


@client.command()
@commands.check(check_if_owner)
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


@client.command(aliases=["Meme"])
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

@client.command()
async def ping(ctx) :
    await ctx.send(f'Pong! `{round(client.latency * 1000)}ms`')

# ------------------------------------- moderation

@client.command()
async def report(ctx, member : discord.Member, *, reason="Unspecified Reason"):
    await member.send(f"You have been reported by {ctx.author} for {reason}")
    gyro = client.get_user(445656896876183552)
    tic = client.get_user(470261090798796800)
    await gyro.send(f"{ctx.author} has reported {member} for {reason}.")
    await tic.send(f"{ctx.author} has reported {member} for {reason}.")
    warning = "Report filed. Admins will decide whether or not to take action."
    await ctx.send(warning)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None) :
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention} https://media1.tenor.com/images/67b785d584e64306adb6b5fdb8f7378f/tenor.gif?itemid=17493177')
    print('damn, ban hammer hit hard.')

@ban.error
async def on_command_error(ctx, error) :
    if isinstance(error, commands.MissingRequiredArgument) :
        await ctx.send('Who do you want me to ban?')

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None) :
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}.')
    print('lol kicked bro')


@kick.error
async def on_command_error(ctx, error) :
    if isinstance(error, commands.MissingRequiredArgument) :
        await ctx.send('Please input a user to kick.')


# --------------------------------------------------------------------------- help cmd
@client.command(aliases=['cmds'])
async def help(ctx) :
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title="Help",
        description='All commands.',
        timestamp = ctx.message.created_at,
    )

    embed.set_author(name="Meme Machine", icon_url="https://tic.questionable.link/HzSDLl.png")
    embed.add_field(name="?meme", value="Sends a meme.", inline=False)
    embed.add_field(name="?pm [attach image/gif] ", value="Sends a meme to be reviewed.", inline=False)
    embed.add_field(name="?am [message id]", value="Accepts a meme. Admins only.", inline=False)
    embed.add_field(name="?ping", value="Test Command.", inline=False)
    embed.add_field(name="?report", value="Reports a user to bot admins.", inline=False)
    embed.add_field(name="?kick", value="Kicks specified user.", inline=False)
    embed.add_field(name="?ban", value="Bans specified user.", inline=False)
    embed.add_field(name="?help", value="Shows this help message.", inline=False)
    embed.set_footer(text=f"Made by GyroXI#7548 & Tic#0001 | {client.user.name}")

    await ctx.send(embed=embed)


client.run('token')
