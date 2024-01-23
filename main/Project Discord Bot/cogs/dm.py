import discord
from discord.ext import commands 


class Directmessege(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def dm(self, ctx, member: discord.Member, *, message: str):
        await member.send(f"Hello {member.name} + {message}")

    

    
        
async def setup(bot):
    await bot.add_cog(Directmessege(bot))