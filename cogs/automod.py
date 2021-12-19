import discord as nextcord
import asyncio
from discord.ext import commands
import json
import time
import typing

def log(*,text):
    ...

class AutoMod(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self._cd = commands.CooldownMapping.from_cooldown(5, 5, commands.BucketType.member) # Change accordingly

    def get_ratelimit(self, message: nextcord.Message) -> typing.Optional[int]:
        """Returns the ratelimit left"""
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot:return
        with open("config.json") as f:
            config = json.load(f)

        if message.content == message.content.upper():
            print("ALL CAPS")
            if config[str(message.guild.id)]["ancap"] == True and not str(message.channel.id) in config[str(message.guild.id)]["whitelists"]:
                await message.delete()
                await message.author.send("Please don't spam Capital letters")

        
        ratelimit = self.get_ratelimit(message)
        if ratelimit is None:
            ...
        else:
            role = nextcord.utils.get(message.guild.roles,name="MUTED (By Midna)")
            if not role:
                role = await message.guild.create_role(name="MUTED (By Midna)",permissions=nextcord.Permissions(send_messages=False,read_messages=True))
                await role.edit(position=2)
            for c in message.guild.categories:
                await c.set_permissions(role,send_messages=False)
            await message.author.add_roles(role)
            embed = nextcord.Embed(title="🔇 Member silenced | 2m")
            embed.add_field(name="Reason",value="Message Spam")
            embed.set_footer(text=f'{message.author} | {message.author.id}')
            await message.channel.send(embed=embed)
            await asyncio.sleep(120)
            await message.author.remove_roles(role)

    

    @commands.command()
    async def anticaps(self,ctx,enabled:bool=False):
        with open("config.json") as f:
            config = json.load(f)

        config[str(ctx.guild.id)]["ancap"] = enabled

        with open("config.json","w+") as f:
            json.dump(config,f)

        embed = nextcord.Embed(color=nextcord.Color.green())
        embed.description = f':white_check_mark: Anti Caps is now set to {enabled}!'
        await ctx.send(embed=embed)



    @commands.command(help="Open the Lockdown")
    @commands.has_permissions(manage_channels=True)
    async def openlockdown(self,ctx):
        with open("config.json") as f:
            config = json.load(f)

        await ctx.channel.edit(slowmode_delay=0)
        await ctx.send("This channel is no longer under lockdown")

    @commands.command(help="Starts a Lockdown in the current channel")
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self,ctx):
        with open("config.json") as f:
            config = json.load(f)

        await ctx.channel.edit(slowmode_delay=config[str(ctx.guild.id)]["emergencyLock"])
        await ctx.send("This channel is now under lockdown")

    @commands.command(help="Set the Rate Limit, a channel will be put into upon being spammed")
    @commands.has_permissions(manage_channels=True)
    async def emratelimit(self,ctx,rate=60):
        with open("config.json") as f:
            config = json.load(f)

        config[str(ctx.guild.id)]["emergencyLock"] = rate

        with open("config.json","w+") as f:
            json.dump(config,f)

        embed = nextcord.Embed(color=nextcord.Color.green())
        embed.description = f':white_check_mark: Emergency Member Rate limit is now set to {rate}!'
        await ctx.send(embed=embed)

    @commands.command(help="The Threshold of how many messages a user can send before its detected as spam")
    @commands.has_permissions(manage_channels=True)
    async def empanicrate(self,ctx,rate=5):
        with open("config.json") as f:
            config = json.load(f)

        config[str(ctx.guild.id)]["panicRate"] = rate

        with open("config.json","w+") as f:
            json.dump(config,f)

        embed = nextcord.Embed(color=nextcord.Color.green())
        embed.description = f':white_check_mark: Emergency Member Rate limit is now set to {rate}!'
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(AutoMod(bot))
