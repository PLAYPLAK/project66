import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def table(ctx):
    table_content = """
    | Header 1 | Header 2 | Header 3 |
    |----------|----------|----------|
    | Value 1  | Value 2  | Value 3  |
    | Value 4  | Value 5  | Value 6  |
    """
    await ctx.send(f'```\n{table_content}\n```')

bot.run('YOUR_BOT_TOKEN')
