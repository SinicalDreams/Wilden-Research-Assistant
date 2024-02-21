import discord
from discord.ext import commands

class Onboarding(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messenger = messenger = self.bot.get_cog('Messenger')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name="Pending")
        await member.add_roles(role)
        await self.messenger.send_welcome(member)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.bot.channel_list["rp-test"] and message.author.id != 658201358247264257 and message.author.id != 1208257805459521546:
            if len(message.content) < 400:
                await self.messenger.send_intro_warning(message.author)
            
            await message.add_reaction("🤓")
            await message.add_reaction("😈")
            await message.add_reaction("🔄")
            await message.add_reaction("❌")
    

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        if reaction.channel_id == self.bot.channel_list["rp-test"] and (reaction.member.get_role(self.bot.adminRoles["assistant-researcher"]) != None or reaction.member.get_role(self.bot.adminRoles["head-researcher"]) != None):
            channel = await self.bot.fetch_channel(reaction.channel_id)
            message = await channel.fetch_message(reaction.message_id)
            log = await self.bot.fetch_channel(self.bot.channel_list["rp-submission-log"])
            
            if str(reaction.emoji) == "🤓" or str(reaction.emoji) == "😈":
                

                embed=discord.Embed(title="", description=message.content, color=discord.Color.from_rgb(0,0,0))
                embed.add_field(name="Submitter", value=f"{message.author.mention}")

                await log.send(f"{reaction.member.mention} approved {message.author.mention}.")
                await log.send(embed=embed)
            
                pendingRole = discord.utils.get(message.guild.roles, name="Pending")
                hunterRole = discord.utils.get(message.guild.roles, name="Hunter")
                monsterRole = discord.utils.get(message.guild.roles, name="Monster")
                
                await message.author.remove_roles(pendingRole)
                
                if str(reaction.emoji) == "🤓":
                    await message.author.add_roles(hunterRole)
                if str(reaction.emoji) == "😈":
                    await message.author.add_roles(monsterRole)
                
                await self.messenger.send_approval(message.author)

                await message.delete()

            if str(reaction.emoji) == "🔄":
                # send dm to user asking to improve their post
                await self.messenger.send_revision(message.author)

                embed=discord.Embed(title="", description=message.content, color=discord.Color.from_rgb(0,0,0))
                embed.add_field(name="Submitter", value=f"{message.author.mention}")

                await log.send(f"{reaction.member.mention} asked {message.author.mention} to expand on their post.")
                await log.send(embed=embed)

            if str(reaction.emoji) == "❌":
                await self.messenger.send_rejection(message.author)

                embed=discord.Embed(title="", description=message.content, color=discord.Color.from_rgb(0,0,0))
                embed.add_field(name="Submitter", value=f"{message.author.mention}")

                await log.send(f"{reaction.member.mention} rejected {message.author.mention}'s post.")
                await log.send(embed=embed)

                await message.delete()

async def setup(bot):
    await bot.add_cog(Onboarding(bot))