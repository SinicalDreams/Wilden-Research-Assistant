import discord
from discord.ext import commands

class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles = {  
            "🛑" : "DMs Closed",
            "🟢" : "DMs Open",
            "⚠️" : "Ask to DM",
            "⬆️" : "Dominant",
            "↕️" : "Switch",
            "⬇️" : "Submissive",
            "🍑" : "Breedable",
            "🍆" : "Breeder",
            "🎨" : "Artist",
            "📣" : "Server Announcements",
            "📯" : "Hunt Ping",
            "🎭" : "Looking for RP",
            "🩸" : "Looking for Spar",
            "🔀" : "Looking for Trade",
            "😈" : "Monster",
            "🤓" : "Hunter"
        }
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        if reaction.member.id != 1208257805459521546:
            if reaction.channel_id == self.bot.channel_list["role-selection"] and str(reaction.emoji) in self.roles:
                role = discord.utils.get(reaction.member.guild.roles, name=self.roles[str(reaction.emoji)])
                await reaction.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction):
        guild = self.bot.get_guild(reaction.guild_id)
        member = guild.get_member(reaction.user_id)
        reaction.member = member
        if reaction.member.id != 1208257805459521546:
            if reaction.channel_id == self.bot.channel_list["role-selection"] and str(reaction.emoji) in self.roles:
                role = discord.utils.get(reaction.member.guild.roles, name=self.roles[str(reaction.emoji)])
                await reaction.member.remove_roles(role)

    @commands.command()
    async def pop_swap(self, ctx:commands.Context):
        await ctx.message.delete()
        embed = discord.Embed(title="Role Swap", description=f"For people who want to change their side or play both sides, use these to assign the respective roles.\n\n🤓 <@&1208337904091402240> - Hunter\n😈 <@&1208337327643172924> - Monster")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("😈")
        await msg.add_reaction("🤓")

    @commands.command()
    async def populate_role(self, ctx:commands.Context):
        await ctx.message.delete()
        
        embed = discord.Embed(title="DM Preferences", description=f"🛑 <@&1208336147630133268> - please do not DM\n🟢 <@&1208331701332217886> - Feel free to DM\n⚠️ <@&1208336105414463529> - Please ask before sending a DM")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🛑")
        await msg.add_reaction("🟢")
        await msg.add_reaction("⚠️")

        embed = discord.Embed(title="Sexual Dispositions", description="⬆️ <@&1208588971375075359>\n↕️ <@&1208589117051375637>\n⬇️ <@&1208589091135033374>\n\n🍑 <@&1208589139339911238>\n🍆 <@&1208589169245298708>")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("⬆️")
        await msg.add_reaction("↕️")
        await msg.add_reaction("⬇️")
        await msg.add_reaction("🍑")
        await msg.add_reaction("🍆")

        embed = discord.Embed(title="Artist", description="We love our artists! If you wish to be pinged from players seeking commissions, or just want to show off your creative disposition, react to get the <@&1208589255824379914> role.")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🎨")

        embed = discord.Embed(title="Notification Roles", description="📣 <@&1208589286492864604> - Receive notifications from #announcements\n📯 <@&1208589524737720420> - Receive a notification when an adventure is being run\n🎭 <@&1208589570254577664> - Receive a notification when someone wants to RP\n🩸 <@&1208589646494433340> - Receive a notification when someone wants to Spar\n🔀 <@&1208589703557685278> - Receive a notification for when someone wnats to trade items.")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("📣")
        await msg.add_reaction("📯")
        await msg.add_reaction("🎭")
        await msg.add_reaction("🩸")
        await msg.add_reaction("🔀")

async def setup(bot):
    await bot.add_cog(Role(bot))