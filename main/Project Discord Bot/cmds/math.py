from discord.ext import commands

# @commands.command()
# async def add(ctx,a:int,b:int):
#         await ctx.send(a+b)

@commands.command()
async def sub(ctx,a:int,b:int):
        await ctx.send(a-b)

async def setup(bot):
        bot.add_command()