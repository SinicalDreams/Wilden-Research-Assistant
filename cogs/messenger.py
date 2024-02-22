import discord
from discord.ext import commands

class Messenger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def dm(self, ctx:commands.Context, uid, *, content):
        member = ctx.guild.get_member(int(uid))
        dm = await self.get_dm(member)

        await dm.send(content)
        await ctx.message.delete()

    async def get_dm(self, member):
        dm = member.dm_channel
        if member.dm_channel == None:
            dm = await member.create_dm()
        return dm
    
    async def send_char_approval(self, member, chartype):
        dm = await self.get_dm(member)
        
        if chartype == 'Hunter':
            desc = "Please take a moment to run `!setup` in https://discord.com/channels/1208228064543252591/1208554890926882908 to finalize your character and validate them for automated rewards!\n**Failure to do this will result in no rewards being earned!**"
        else:
            desc = "Please take a moment to run `$setup monsterName` in https://discord.com/channels/1208228064543252591/1208554890926882908 to finalize your character and validate them for automated rewards!\n**Failure to do this will result in no rewards being earned!**"
        
        embed=discord.Embed(
            title=f"Intro Gate {type} Approved - Automated Response", 
            description=f"Hi {member.name}! Your {chartype} has been approved! {desc}\n\nThis message is automated. If you have questions, please seek answers by asking them in https://discord.com/channels/1208228064543252591/1208230390033154100.", color=discord.Color.from_rgb(0,0,0))
        
        await dm.send(embed=embed)

    async def send_welcome(self, member):
        dm = await self.get_dm(member)
        
        embed=discord.Embed(
            title="Intro Gate Welcome- Automated Response", 
            description=f"Hi {member.name}! Welcome to our server, and we hope you enjoy our community! Right now, you're in the intro gate which helps us filter out those who just wouldn't fit our community. Please take the time to read the content in https://discord.com/channels/1208228064543252591/1208233911906476062 and https://discord.com/channels/1208228064543252591/1208233929279017032. Then, when you're ready, please read the supplied prompts in https://discord.com/channels/1208228064543252591/1208340372321738832 and post a response to one of them. Players here have the choice of playing a hunter that goes out to hunt and fuck monsters, or to play a monster that defends its territory and tries to breed the hunters. Once you've decided what kind of player you want to be, select and post a response to the prompt for your choice.\n\nThis message is automated. If you have questions, please seek answers by asking them in https://discord.com/channels/1208228064543252591/1208340344320561202.", color=discord.Color.from_rgb(0,0,0))
        
        await dm.send(embed=embed)

    async def send_intro_warning(self, member):
        dm = await self.get_dm(member)
        
        embed=discord.Embed(
            title="Intro Gate - Automated Response", 
            description=f"Hi {member.name}! We've received your submission and have stepped in to let you know that your submission might be too short to accurately assess your compatibility with the server! Please take some time to review your submission and really showcase just what you can do!\n\nThis message is automated. If you have questions, please seek answers by asking them in https://discord.com/channels/1208228064543252591/1208340344320561202.", color=discord.Color.from_rgb(0,0,0))
        
        await dm.send(embed=embed)

    async def send_revision(self, member):
        dm = await self.get_dm(member)
        
        embed=discord.Embed(
            title="Intro Gate Revision - Automated Response", 
            description=f"Hi {member.name}! We've received your submission and respectfully ask that you review and revise your post. It could be length, grammar, or just content that is preventing our reviewers from deciding if you're a good fit. Please spend some time, as your edit will be considered a final revision!\n\nThis message is automated. If you have questions, please seek answers by asking them in https://discord.com/channels/1208228064543252591/1208340344320561202.", color=discord.Color.from_rgb(0,0,0))
        
        await dm.send(embed=embed)
    
    async def send_approval(self, member):
        dm = await self.get_dm(member)

        embed=discord.Embed(
            title="Intro Gate Approval - Automated Response", 
            description=f"Hi {member.name}! Your rp test post has been approved and are welcome to join the server! Please take the time to explore the server and get to know the community! Everything should be laid out in their respective channels for your convenience, but if there is any question, please visit the https://discord.com/channels/1208228064543252591/1208230390033154100 channel and ask questions!", color=discord.Color.from_rgb(0,0,0))
        
        await dm.send(embed=embed)
    
    async def send_rejection(self, member):
        dm = await self.get_dm(member)

        embed=discord.Embed(
            title="Intro Gate Rejection - Automated Response", 
            description=f"Hi {member.name}! Unfortunately, one of our reviewers has rejected your rp test post as they have deemed you are likely not a good fit for our server. We wish you luck in your future RP endeavors.", color=discord.Color.from_rgb(0,0,0))
        
        await dm.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Messenger(bot))