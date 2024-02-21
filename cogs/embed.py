import discord
from discord.ext import commands

class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def test(self, ctx:commands.Context):
        print("test")

    @commands.command()
    async def embed(self, ctx:commands.Context, title, image, *, desc):
        if ctx.author.get_role(self.bot.adminRoles["head-researcher"]) != None:
            embed=discord.Embed(title=title, description=desc, color=discord.Color.from_rgb(0,0,0))
            if image != "":
                embed.add_image(url=image)
            await ctx.message.delete()
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Embed(bot))