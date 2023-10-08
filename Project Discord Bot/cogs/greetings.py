import discord
from discord.ext import commands 


class Greetings(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    # @commands.Cog.listener()
    # async def on_message(self, message: discord.Message):
    #     await message.add_reaction("✅")
    
    @commands.command()
    async def hello(self, ctx, *, member: discord.Member):#อะไรก็ตามตามด้วยชื่อสมาชิก
        await ctx.send(f"Hello {member.name}")

    @commands.command()
    async def add(self, ctx,a:int,b:int):
        await ctx.send(a+b)
        
async def setup(bot):
    await bot.add_cog(Greetings(bot))