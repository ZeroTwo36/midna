import discord as nextcord
import os
from discord.ext import commands,tasks
import json
import time

class Midna(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

client = Midna(command_prefix="m!",intents=nextcord.Intents.all())

@client.event
async def on_guild_join(guild):
    with open("config.json") as f:
        config = json.load(f)

    config[str(guild.id)] = {
        "antijoin":False,
        "ancap":False,
        "emergencyLock":60,
        "panicRate":3,
        "whitelists":[]

    }
    with open("config.json","w+") as f:
            json.dump(config,f)

@client.event
async def on_ready():
    for i in os.listdir("cogs"):
        if i == "__init__.py" or not i.endswith(".py"):
            ...
        else:
            client.load_extension(f'cogs.{i[:-3]}')
            print(i)
    await update.start()

@tasks.loop(seconds=2)
async def update():
        await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching,name=f"over {len(client.guilds)} Servers | m!help"))

client.run("ODk5NzI4NTI2NTExNTkxNDI1.YW2_fA.ApQhQJiGcMsyEPxQz5abgFz1L2k")
