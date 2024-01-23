import discord
from discord.ext import commands 

async def is_owner(ctx):
    return ctx.author.id == ctx.guild.owner_id #ใช้คำสั่งได้เฉพาะ Role

class Admin(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.check(is_owner)#เปลี่ยนREQที่ต้องการได้
    async def admin(self, ctx, what = "WHAT"):
        await ctx.send(what)
                       
    @admin.error
    async def admin_error(self, ctx , error):
        if isinstance(error, commands.CommandError):
            await ctx.send("Permission Denied. ")
        
async def setup(bot):
    await bot.add_cog(Admin(bot))