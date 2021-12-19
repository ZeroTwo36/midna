import discord as nextcord
from discord.ext import commands

admins = [878726683195240468,685180177419993102,899722893603274793]

class Root(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def view_guilds(self,ctx):
        if ctx.author.id in admins:
            embed = nextcord.Embed(title="Midna Guilds")
            for guild in self.bot.guilds:
                embed.add_field(name=guild.name,value=f'Guild ID: {guild.id}\nGuild Members: {guild.member_count}\nOwner:{guild.owner}\nRegion:{guild.region}')
            await ctx.send(embed=embed)

    @commands.command()
    async def unload(self,ctx,cog:str):
        if ctx.author.id in admins:
            self.bot.unload_extension(cog)
            await ctx.send("Unloaded {}".format(cog))

    @commands.command()
    async def load(self,ctx,cog:str):
        if ctx.author.id in admins:
            self.bot.load_extension(cog)
            await ctx.send("Loaded {}".format(cog))


def setup(bot):
    bot.add_cog(Root(bot))
