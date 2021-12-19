import discord
from discord.ext import commands

members_subscribed = []

class Updates(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    async def newsletter_subscribe(self,ctx):
        global members_subscribed
        members_subscribed.append(ctx.author)
        embed = discord.Embed(title=":white_check_mark: Subscribed!")
        embed.description = "You are now successfully subscribed to our newsletter!\nYou will receive DMs from me, whenever we announce something."
        await ctx.author.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def announce(self,ctx,*,message=None):
        embed = discord.Embed(title=":bell: Announcement!",description=message)
        await self.bot.get_guild(902589030858891265).get_channel(902589031626465280).send(embed=embed)
        for member in members_subscribed:
            await member.send(embed=embed)

def setup(bot):
    bot.add_cog(Updates(bot))
