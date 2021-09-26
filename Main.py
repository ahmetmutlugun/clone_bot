import discord
from discord.ext import commands
from discord.ext.commands import Bot

client: Bot = commands.Bot(command_prefix=['-'], case_insensitive=True, description="Train an AI to send messages.")
guilds = []
guild_ids = []


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("-" + "help"))
    print("Bot Ready")
    for guild in client.guilds:
        guilds.append(guild)
        guild_ids.append(guild.id)


@client.command(brief='Displays bot ping')
async def ping(ctx):
    await ctx.send(f"My ping is: {round(client.latency * 1000)}ms")


@client.event
async def on_message(ctx):
    if check_user(str(ctx.author.id)) and "-train off" not in ctx.content:
        with open("messages.txt", "a") as f:
            f.write(str(ctx.author.id) + ": " + ctx.content + "\n")
    await client.process_commands(ctx)


@client.command(brief='Turn on or off the AI training.')
async def train(ctx, preference):
    if preference is None:
        await ctx.send("Please pick \"on\" or \"off\" to train the bot.")
        return
    if preference.lower() == "off":
        remove_user(str(ctx.author.id))
        await ctx.send("Your messages will no longer be recorded.")
        return
    elif preference.lower() == "on":
        add_user(str(ctx.author.id))
        await ctx.send("Your messages will now be used to train this bot.")
        return


def add_user(author_id):
    if not check_user(author_id):
        with open("whitelist.txt", "a") as f:
            f.write(str(author_id) + "\n")


def remove_user(author_id):
    with open("whitelist.txt", "r") as f:
        lines = f.readlines()
    with open("whitelist.txt", "w") as f:
        for line in lines:
            if line.strip("\n") != author_id:
                f.write(line)


def check_user(author_id):
    f = open("whitelist.txt", "r")
    data = f.read()
    f.close()
    if author_id not in data:
        return False
    return True


fl = open("discord.key", "r")
token = fl.read()
client.run(token)
