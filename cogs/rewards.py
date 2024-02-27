import discord
import pointshop_modal
import json
import time as time_
import datetime
from discord.ext import commands, tasks

utc = datetime.timezone.utc
time = datetime.time(hour=0, minute=0, tzinfo=utc)

class Rewards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.task_reward.start()

    def cog_unload(self):
        self.task_reward.cancel()

    @tasks.loop(time=time)
    async def task_reward(self):
        log = await self.bot.fetch_channel(self.bot.channel_list["loot-log"])

        for player in self.bot.players:
            user = self.bot.get_user(int(player))
            print(user)
            print(user.mention)
            p = self.bot.players[player]
            if p["post_count"] - p["last_awarded"] > 5000:
                rewards = divmod(p["post_count"] - p["last_awarded"], 5000)
                p["last_awarded"] += rewards[0]*5000
                p["points"] += rewards[0]
                embed = discord.Embed(title="RP Award", description=f"{user.mention} has earned {rewards[0]} {'points' if rewards[0] > 1 else 'point'} for roleplaying!")
                await log.send(content=f"{user.mention}")
                await log.send(embed=embed)
        
        with open("players.json","w") as file:
           file.write(json.dumps(self.bot.players))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != self.bot.uid:
            if message.channel.category_id in self.bot.channel_list["rp-categories"]:
                if str(message.author.id) in self.bot.players:
                    curTime = time_.time_ns()
                    if self.bot.players[str(message.author.id)]["last_cd"] == "":
                        self.bot.players[str(message.author.id)]["last_cd"] = curTime
                    
                    if self.bot.players[str(message.author.id)]["last_cd"] + 60000000000 < curTime:
                        pass
                    self.bot.players[str(message.author.id)]["last_cd"] = curTime
                    self.bot.players[str(message.author.id)]["post_count"] += len(message.content)

                    with open("players.json","w") as file:
                        file.write(json.dumps(self.bot.players))

    @commands.command()
    async def calculate(self, ctx:commands.Context):
        tupperNames = {}
        for player in self.bot.players:
            if "Hunter" in self.bot.players[player]["chars"]:
                tupperNames[self.bot.players[player]["chars"]["Hunter"]["name"]] = player
            if "Monster" in self.bot.players[player]["chars"]:
                tupperNames[self.bot.players[player]["chars"]["Monster"]["name"]] = player
        
        async for message in ctx.channel.history(limit=200):
            
            if str(message.author.id) in self.bot.players:

                self.bot.players[str(message.author.id)]["post_count"] += len(message.content)
            elif message.author.name in tupperNames.keys():
                self.bot.players[tupperNames[message.author.name]]["post_count"] += len(message.content)
        
        with open("players.json","w") as file:
            file.write(json.dumps(self.bot.players))
        
        await ctx.message.delete()

    @commands.command()
    async def populate_point_shop(self, ctx:commands.Context):
        if ctx.author.get_role(self.bot.adminRoles["head-researcher"]) != None:
            await ctx.message.delete()
            embed = discord.Embed(title="Point Shop", description=f"Spend your RP Points here! Rewards are scaled depending on the level or CR of your hunter/monster, reward dependant.\n Click the 💰 button to get a shop menu!")
                 
            await ctx.send(embed=embed, view=pointshop_modal.PointShopButtonView(self.bot))

    @commands.command()
    async def reward(self, ctx:commands.Context):
        log = await self.bot.fetch_channel(self.bot.channel_list["loot-log"])

        for player in self.bot.players:
            user = self.bot.get_user(int(player))
            print(user)
            p = self.bot.players[player]
            if p["post_count"] - p["last_awarded"] > 5000:
                rewards = divmod(p["post_count"] - p["last_awarded"], 5000)
                p["last_awarded"] += rewards[0]*5000
                p["points"] += rewards[0]
                embed = discord.Embed(title="RP Award", description=f"{user.mention} has earned {rewards[0]} {'points' if rewards[0] > 1 else 'point'} for roleplaying!")
                await log.send(content=f"{user.mention}")
                await log.send(embed=embed)
        
        with open("players.json","w") as file:
           file.write(json.dumps(self.bot.players))

        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(Rewards(bot))