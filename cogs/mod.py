import discord as nextcord
from discord.ext import commands


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self,ctx,member:nextcord.Member,*,reason="Unspecified"):
        await member.kick(reason=reason)
        await ctx.send(f":white_check_mark: Kicked {member}!")

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self,ctx,member:nextcord.Member,*,reason="Unspecified"):
        await member.ban(reason=reason)
        await ctx.send(f":white_check_mark: Banned {member}!")

    


def setup(bot):
    bot.add_cog(Mod(bot))
