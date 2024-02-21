import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv
import asyncio

intents = discord.Intents.default()
intents.reactions = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

with open("channels.json","r") as file:
    bot.channel_list = json.load(file)

with open("roles.json","r") as file:
    bot.adminRoles = json.load(file)

with open("projects.json","r") as file:
    bot.projects = json.load(file)

@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}!")


async def load_extensions():
    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            await bot.load_extension("cogs." + f[:-3])

async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv("TOKEN"))

asyncio.run(main())