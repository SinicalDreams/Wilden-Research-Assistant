import discord
from discord.ext import commands

class Rewards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != self.bot.uid:
            if message.channel.id in self.bot.rpChannels:
                pass

    @commands.command()
    async def embed(self, ctx:commands.Context, title, image, *, desc):
        if ctx.author.get_role(self.bot.adminRoles["head-researcher"]) != None:
            embed=discord.Embed(title=title, description=desc, color=discord.Color.from_rgb(0,0,0))
            if image != "":
                embed.add_image(url=image)
            await ctx.message.delete()
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Rewards(bot))