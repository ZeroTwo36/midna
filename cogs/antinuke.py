from discord.ext import commands,tasks
import discord as nextcord
import json
import time
import asyncio
from collections import defaultdict
import threading

global invite_uses_before
invite_uses_before = defaultdict(dict)

global invite_uses_after
invite_uses_after = defaultdict(dict)

global counter
counter = {}

global countdown_task
countdown_task = {}

global spam
spam = {}


class AntiJoin(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.membersjoined = 0


    @commands.Cog.listener()
    async def on_ready(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.update_every_5s())

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def antijoin(self,ctx,activate:bool=False):
        with open("config.json") as f:
            config = json.load(f)

        config[str(ctx.guild.id)]["antijoin"] = activate
        with open("config.json","w+") as f:
            json.dump(config,f)
        await ctx.send(f":white_check_mark: Configured Antijoin - Now set to {activate}")

    @commands.Cog.listener()
    async def on_member_join(self,member):
        gmstart = member.guild.member_count
        print("AAAAAAAAAAAAAAAAAAAAAA")
        with open("config.json") as f:
            config = json.load(f)
        if bool(config[str(member.guild.id)]["antijoin"]) == True:
            embed = nextcord.Embed(color=nextcord.Color.red())
            embed.description = f'You were kicked from {member.guild.name} - AntiJoin is activated'
            await member.send(embed=embed)
            await member.kick(reason="Antijoin enabled")

        time.sleep(5)
        if gmstart < member.guild.member_count:
            # RAID

            with open("config.json") as f:
                config = json.load(f)

            config[str(member.guild.id)]["antijoin"] = True
            with open("config.json","w+") as f:
                json.dump(config,f)
            await member.guild.channels[0].send(f":white_check_mark: Automatically detected Raid, activated antijoin True")



    async def update_invites(self):
        for guild in self.bot.guilds:
            invite_uses_before[guild.id] = []
            invite_uses_before[guild.id] = list()
            invites = await guild.invites()
            invite_uses_before[guild.id].clear()
            for invite in invites:
                invite_uses_before[guild.id].append(invite)

    @commands.Cog.listener()
    async def on_invite_create(self,invite):
        counter[invite.code] = []
        counter[invite.code] = list()

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        invite_uses_before[guild.id] = []
        invite_uses_before[guild.id] = list()
        invites = await guild.invites()
        for invite in invites:
            invite_uses_before[guild.id].append(invite)

    @commands.Cog.listener()
    async def on_member_join(self,member):
        guild = self.bot.get_guild(member.guild.id)
        invite_uses_after[guild.id] = []
        invite_uses_after[guild.id] = list()
        invite_uses_after[guild.id].clear()
        invites = await guild.invites()

        for invite in invites:
            invite_uses_after[guild.id].append(invite)

        for i, invite in enumerate(invite_uses_after[guild.id]):
            countdown_task[invite.code] = asyncio.create_task(self.checkit())
            try:
                if countdown_task[invite.code] in asyncio.all_tasks():
                    pass

                else:
                    countdown_task[invite.code].start()
            except:
                countdown_task[invite.code].start()
            counter[invite.code].append(member.id)
            if int(invite_uses_before[guild.id][i].uses) != int(invite.uses):
                if len(counter[invite.code]) >= 5:

                    with open("config.json") as f:
                        config = json.load(f)

                    config[str(guild.id)]["antijoin"] = True
                    with open("config.json","w+") as f:
                        json.dump(config,f)
                    await guild.channels[0].send(f":white_check_mark: Configured Antijoin - Now set to True")
                    await invite.delete(reason="used for spam")
                    for user in counter[invite.code]:
                        await guild.ban(self.bot.get_user(user), reason = "Flow protector is ON and is protecting you from token spams", delete_message_days = 7)
                        await guild.unban(self.bot.get_user(user))
            else:
                pass

        invite_uses_before[guild.id].clear()
        for invite in invite_uses_after[guild.id]:
            invite_uses_before[guild.id].append(invite)

    async def checkit(self):
        time.sleep(10)
        for guild in self.bot.guilds:
            invites = await guild.invites()
            for invite in invites:
                counter[invite.code] = []
                counter[invite.code] = list()
                counter[invite.code].clear()

    async def update_every_5s(self):
        while True:
            await asyncio.sleep(5)
            await self.update_invites()


def setup(bot):
    bot.add_cog(AntiJoin(bot))
