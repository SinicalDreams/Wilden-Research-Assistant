import discord
import json
from utils import get_level
from discord.ui import Select, View

# class PointShop(discord.ui.modal, title="Point Shop"):

#     async def on_submit(self, interaction: discord.Interaction):
#        await interaction.response.send_message(f'Thanks for your feedback, {self.name.value}!', ephemeral=True)

#     async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
#         await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

class PointShopSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options=[
            discord.SelectOption(label="Gold", emoji="💰", description="A Hunter's Paycheck"),
            discord.SelectOption(label="Experience", emoji="🤓", description="A Hunter's Memory"),
            discord.SelectOption(label="Monster Points", emoji="😈", description="A Monster's Power")
        ]
        super().__init__(placeholder="Select an item", max_values=1, min_values=1, options=options)
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        gold = [100,100,100,100,100,150,150,150,150,150,200,200,200,200,200,250,250,300,300,500,500]
        exp = [150,150,150,150,250,500,600,750,900,1100,1200,1600,2000,2200,2500,2800,3200,3900,4200,4900,5700]
        mpt = [5,5,5,5,5,8,8,8,8,10,10,10,10,12,12,12,12,14,14,14,14,16,16,16,16,18,20,20,20,20,20]
        log = await self.bot.fetch_channel(self.bot.channel_list["loot-log"])
        
        player = self.bot.players[str(interaction.user.id)]
        embed = None

        if player["points"] < 1:
            return await interaction.followup.send(content="You don't have enough points!", ephemeral=True)
            

        if self.values[0] == "Gold":
            if "Hunter" not in player["chars"]:
                await interaction.followup.send(content="You don't have a Hunter!", ephemeral=True)
            else:
                gp = gold[get_level(player["chars"]["Hunter"]["xp"])]
                embed=discord.Embed(title=f"Point Shop Purchase - {self.values[0]}", description=f"{interaction.user.mention} has received a paycheck of {gp}gp!", color=discord.Color.from_rgb(0,0,0))

        if self.values[0] == "Experience":
            if "Hunter" not in player["chars"]:
                await interaction.followup.send(content="You don't have a Hunter!", ephemeral=True)
            else:
                xp = exp[get_level(player["chars"]["Hunter"]["xp"])]
                embed=discord.Embed(title=f"Point Shop Purchase - {self.values[0]}", description=f"{interaction.user.mention} has earned {xp}xp!", color=discord.Color.from_rgb(0,0,0))

        if self.values[0] == "Monster Points":
            if "Monster" not in player["chars"]:
                await interaction.followup.send(content="You don't have a Monster!", ephemeral=True)
            else:
                mp = mpt[player["chars"]["Monster"]["level"]]
                embed=discord.Embed(title=f"Point Shop Purchase - {self.values[0]}", description=f"{interaction.user.mention} has earned {mp}mp!", color=discord.Color.from_rgb(0,0,0))
        if embed != None:
            player["points"] -= 1
            with open("players.json","w") as file:
                file.write(json.dumps(self.bot.players))
            await log.send(content=f"{interaction.user.mention}")
            await log.send(embed=embed)
            await interaction.followup.edit_message(interaction.message.id, content="Purchase made!", view=None)

class PointShopSelectView(discord.ui.View):
    def __init__(self, bot, *, timeout = 180):
        self.bot = bot
        super().__init__(timeout=timeout)
        self.add_item(PointShopSelect(self.bot))

class PointShopButtonView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="", custom_id="pt-shop-open", style=discord.ButtonStyle.primary, emoji="💰")
    async def button_callback(self, interaction, button):
        if str(interaction.user.id) in self.bot.players:
            await interaction.response.send_message(content=f"You have {self.bot.players[str(interaction.user.id)]['points']} points to spend.",view=PointShopSelectView(self.bot), ephemeral=True)
        else:
            await interaction.response.send_message(content=f"You don't have an approved character to spend rewards for!", ephemeral=True)