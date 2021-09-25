import discord
from discord.ext import commands
from discord.ext.commands import Bot

client: Bot = commands.Bot(command_prefix=['-'], case_insensitive=True, description="Train an AI to send "
                                                                                                "messages.")
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

file = open("discord.key", "r")
token = file.read()
client.run(token)