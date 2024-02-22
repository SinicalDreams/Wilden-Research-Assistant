import discord
from discord.ui import Select, View

class PointShop(discord.ui.modal, title="Point Shop"):

    async def on_submit(self, interaction: discord.Interaction):
       await interaction.response.send_message(f'Thanks for your feedback, {self.name.value}!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

class PointShopSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options=[
            discord.SelectOption(label="Gold", emoji="", description="A Hunter's Paycheck"),
            discord.SelectOption(label="Experience", emoji="", description="A Hunter's Memory"),
            discord.SelectOption(label="Monster Points", emoji="", description="A Monster's Power")
        ]
        super().__init__(placeholder="Select an item", max_values=1, min_values=1, options=options)
    async def callback(self, interaction: discord.Interaction):
        log = await self.bot.fetch_channel(self.bot.channel_list["loot-log"])
        
        player = self.bot.players[str(interaction.user.id)]
        embed = None

        if self.values[0] == "Gold":
            if "Hunter" not in player["chars"]:
                await interaction.response.send_message(content="You don't have a Hunter!", ephemeral=True)
            else:
                gold = 100
                embed=discord.Embed(title=f"Point Shop Purchase - {self.values[0]}", description=f"{interaction.user.mention} has received a paycheck of {gold}gp!", color=discord.Color.from_rgb(0,0,0))

        if self.values[0] == "Experience":
            if "Hunter" not in player["chars"]:
                await interaction.response.send_message(content="You don't have a Hunter!", ephemeral=True)
            else:
                xp = 250
                embed=discord.Embed(title=f"Point Shop Purchase - {self.values[0]}", description=f"{interaction.user.mention} has earned {xp}xp!", color=discord.Color.from_rgb(0,0,0))

        if self.value[0] == "Monster Points":
            if "Monster" not in player["chars"]:
                await interaction.response.send_message(content="You don't have a Monster!", ephemeral=True)
            else:
                mp = 5
                embed=discord.Embed(title=f"Point Shop Purchase - {self.values[0]}", description=f"{interaction.user.mention} has earned {mp}mp!", color=discord.Color.from_rgb(0,0,0))
        if embed != None:
            await log.send_message(embed=embed)

class PointShopSelectView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(PointShopSelect())

class PointShopButtonView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="", custom_id="pt-shop-open", style=discord.ButtonStyle.primary, emoji="💰")
    async def button_callback(self, button, interaction):
        await interaction.response.send_message(view=PointShopSelectView(self.bot), ephemeral=True)