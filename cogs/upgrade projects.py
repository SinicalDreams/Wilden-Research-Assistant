import discord
import json
from discord.ext import commands

class UpgradeProjects(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def new_project(self, ctx:commands.Context, title, image, desc, cost, type):
        self.bot.projects[title] = {
            "title": title,
            "image" : image,
            "desc" : desc,
            "cost" : int(cost),
            "progress": 0,
            "type" : type
        }
        

        embed=discord.Embed(title=title, description=desc, color=discord.Color.from_rgb(0,0,0))
        embed.add_field(name=f"Progress: {0}/{cost}{'gp' if type == 'hunter' else 'mp'}", value=f"|▯▯▯▯▯▯▯▯▯▯▯▯|")
        embed.set_image(url=image)
        msg = await ctx.send(embed=embed)
        await ctx.message.delete()

        self.bot.projects[title]["msgId"] = msg.id
        with open("projects.json","w") as file:
            file.write(json.dumps(self.bot.projects))

    @commands.command()
    async def update_project(self, ctx:commands.Context, name, mod):
        if name in self.bot.projects:
            project = self.bot.projects[name]
            project["progress"] = project["progress"] + int(mod) 
        
            msg = await ctx.channel.fetch_message(project["msgId"])
            
            embed=discord.Embed(title=project["title"], description=project["desc"], color=discord.Color.from_rgb(0,0,0))
            prog = int((project["progress"]/project["cost"] * 100)/10)
            rem = 10 - prog

            embed.add_field(name=f"Progress: {project['progress']}/{project['cost']}{'gp' if project['type'] == 'hunter' else 'mp'}", value=f"|{'▮'*prog}{'▯'*rem}|")
            embed.set_image(url=project["image"])
            
            await msg.edit(embed=embed)

        await ctx.message.delete()
        with open("projects.json","w") as file:
            file.write(json.dumps(self.bot.projects))

async def setup(bot):
    await bot.add_cog(UpgradeProjects(bot))