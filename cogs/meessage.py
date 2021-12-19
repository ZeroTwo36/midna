import discord as nextcord
from discord.ext import commands


class MeessageEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messageDeleted = None
        self.messageEdited = None

    @commands.command()
    async def snipe(this,ctx):
        if this.messageDeleted:
            embed = nextcord.Embed(description=this.messageDeleted.content)
            embed.set_author(name=this.messageDeleted.author,icon_url=this.messageDeleted.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Nothing to snipe!")


    @commands.command()
    async def editsnipe(this,ctx):
        if this.messageEdited:
            embed = nextcord.Embed(description=this.messageEdited[1].content)
            embed.add_field(name="Previous",value=this.messageEdited[0].content)
            embed.set_author(name=this.messageEdited[1].author,icon_url=this.messageEdited[1].author.avatar.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Nothing to snipe!")

    @commands.Cog.listener()
    async def on_message_delete(this,message):
        this.messageDeleted = message

    @commands.Cog.listener()
    async def on_message_edit(this,before,after):
        this.messageEdited = (before,after)


def setup(bot):
    bot.add_cog(MeessageEvent(bot))
