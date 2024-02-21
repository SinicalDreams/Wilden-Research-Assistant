import discord
import re
import json
from discord.ext import commands

class Approval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def setup(self, ctx:commands.Context, monsterName):
        if ctx.channel.id in self.bot.channel_list["bot-spam"]:
            id = str(ctx.author.id)
            if id in self.bot.players:
                self.bot.players[id]["chars"]["Monster"] = {
                    "name" : monsterName,
                    "level" : 4,
                    "prog" : 0
                }
                await ctx.send(f"Your monster has been set to {monsterName}!")
            else:
                await ctx.send(f"You don't have an approval yet!")
        else:
            await ctx.send(f"This is the wrong channel to run that command.", delay=15.0)
        
        with open("players.json","w") as file:
           file.write(json.dumps(self.bot.players))
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        
        if message.channel.id in self.bot.channel_list["bot-spam"] and message.author.id == 261302296103747584:
            content = message.embeds[0].to_dict()

            if "Initial Setup" in content["title"]:
                for field in content["fields"]:
                    if field["name"] == "User ID":
                        uid = str(field["value"])
                    if field["name"] == "Current Experience":
                        xp = re.search("\D*\s(.*)xp", field["value"]).group(1)
                if uid in self.bot.players:
                    self.bot.players[uid]["chars"]["Hunter"] = {
                            "name" : content["title"][19:],
                            "xp" : int(xp.replace(',',''))
                        }
                    with open("players.json","w") as file:
                        file.write(json.dumps(self.bot.players))




    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        if reaction.channel_id in self.bot.channel_list["approval-channels"] and reaction.member.get_role(self.bot.adminRoles["sheet-checker"]) != None:
            if str(reaction.emoji) == '🤓' or str(reaction.emoji) == '😈':
                chartype = 'Hunter' if str(reaction.emoji) == '🤓' else 'Monster'
                channel = await self.bot.fetch_channel(reaction.channel_id)
                message = await channel.fetch_message(reaction.message_id)
                log = await self.bot.fetch_channel(self.bot.channel_list["approved-log"])

                embed=discord.Embed(title="", description=message.content, color=discord.Color.from_rgb(0,0,0))
                embed.add_field(name="Submitter", value=f"{message.author.mention}")
                embed.add_field(name="Type", value=f"{chartype}")

                await log.send(f"{reaction.member.mention} approved {message.author.mention}.")
                await log.send(embed=embed)
                messenger = self.bot.get_cog('Messenger')
                try:
                    await messenger.send_char_approval(message.author, chartype)
                except:
                    print("Ignis did it")

                if message.author.id not in self.bot.players:
                    self.bot.players[message.author.id] = {
                        "post_count" : 0,
                        "last_awarded": 0,
                        "last_cd" : "",
                        "chars" : {}
                    }
                    with open("players.json","w") as file:
                        file.write(json.dumps(self.bot.players))
                await message.delete()

async def setup(bot):
    await bot.add_cog(Approval(bot))