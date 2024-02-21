import discord
import json
import time
from discord.ext import commands

class Rewards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != self.bot.uid:
            if message.channel.category_id in self.bot.channel_list["rp-categories"]:
                if str(message.author.id) in self.bot.players:
                    curTime = time.time()
                    if self.bot.players[str(message.author.id)]["last_cd"] == "":
                        self.bot.players[str(message.author.id)]["last_cd"] = curTime
                    
                    if self.bot.players[str(message.author.id)]["last_cd"] + 60 > curTime:
                        self.bot.players[str(message.author.id)]["last_cd"] = curTime
                        self.bot.players[str(message.author.id)]["post_count"] += len(message.content)

                        with open("players.json","w") as file:
                            file.write(json.dumps(self.bot.players))

async def setup(bot):
    await bot.add_cog(Rewards(bot))