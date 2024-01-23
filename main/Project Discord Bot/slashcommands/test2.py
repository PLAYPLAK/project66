import discord
from discord.ext import commands
from discord import app_commands


class Mygroup3(app_commands.Group):
    @app_commands.command()
    async def gg(self, interaction : discord.Interaction):
        await interaction.response.send_message(f'apple')

    @app_commands.command()
    async def ez(self, interaction : discord.Interaction):
        await interaction.response.send_message(f'banana')

async def setup(bot):
    bot.tree.add_command(Mygroup3(name='Test2',description='Just a test'))