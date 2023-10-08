import discord
from discord import app_commands


class Mygroup1(app_commands.Group):
    @app_commands.command()
    async def banana(self, interaction : discord.Interaction):
        await interaction.response.send_message(f'apple')

    @app_commands.command()
    async def apple(self, interaction : discord.Interaction):
        await interaction.response.send_message(f'banana')

async def setup(bot):
    bot.tree.add_command(Mygroup1(name='Test',description='Just a test'))