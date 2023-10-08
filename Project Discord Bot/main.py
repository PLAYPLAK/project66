import random
from typing import Any

from discord.interactions import Interaction
import settings
import discord
import traceback
import utils
import typing
import enum
from datetime import datetime
from discord.ext import commands
from discord import app_commands


logger = settings.logging.getLogger("bot")


class Food(enum.Enum):
    apple = 1
    banana = 2
    orange = 3



class RegisterModal(discord.ui.Modal, title='Register'):
    std_id = discord.ui.TextInput(label='Student ID', placeholder='ex: 64XXXXXX', style=discord.TextStyle.short, max_length=8)
    fname = discord.ui.TextInput(label='Firstname', placeholder='ex: Somchai', style=discord.TextStyle.short, max_length=30)
    lname = discord.ui.TextInput(label='Lastname', placeholder='ex: Jaidee', style=discord.TextStyle.short, max_length=30)
    age = discord.ui.TextInput(label='Age', placeholder='ex: 22', style=discord.TextStyle.short, max_length=2)
    aboutme = discord.ui.TextInput(label='About Me', placeholder='ex: Tell about yourself...', style=discord.TextStyle.paragraph, max_length=300)
    async def on_submit(self, interaction : discord.Interaction):
        channel = interaction.guild.get_channel(settings.FEEDBACK_CH)
        
        embed = discord.Embed(
            title="Register success!!",
            description="",
            color=discord.Color.green()
        )
        embed.add_field(
            name=f'{self.std_id.label}',
            value=f'{self.std_id.value}',
            inline=False #ขึ้นบรรทัดใหม่
        )
        embed.add_field(
            name=f'{self.fname.label}',
            value=f'{self.fname.value}',
        )
        embed.add_field(
            name=f'{self.lname.label}',
            value=f'{self.lname.value}',
        )
        embed.add_field(
            name=f'{self.age.label}',
            value=f'{self.age.value}',
            inline=False
        )
        embed.set_thumbnail(url=self.user.avatar)
        embed.set_author(name=self.user.name)
        

        # await channel.send(embed=embed)
        await interaction.response.send_message(embed=embed, ephemeral=True) #ส่งข้อมูลที่กรอกออกมาใน embed
        # await interaction.response.send_message(f'thank you {self.user.name}', ephemeral=True)

        async def on_error(self, interaction : discord.Interaction, error):
            ...



        



def run():
    intents = discord.Intents.all()
    # intents.message_content = True  #โต้ตอบกับข้อความ
    # intents.members = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():#เมื่อบอททำงาน
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        logger.info(f'Guild ID : {bot.guilds[0].id}')
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Discord"))#สถานะของบอท
        print('bot started')
       

        for cogs_file in settings.COGS_DIR.glob("*.py"):
            if cogs_file != "__init__.py":
                await bot.load_extension(f"cogs.{cogs_file.name[:-3]}") #เพิ่มคำสั่งจากไฟล์นอก
                print(f'import {cogs_file} success')
                
        # mygroup1 = MyGroup1(name=greetings,description='Welcome User')
        # bot.tree.add_command(mygroup1)
        # for slashcommands_file in settings.SLASHCOMMANDS_DIR.glob("*.py"):
            # if slashcommands_file != "__init__.py":
        # await bot.load_extension(f'slashcommands.test')                    #ต้องแก้
        # print('import slash_cmds success')


        # for cmd_file in settings.CMDS_DIR.glob("*.py"):
        #     if cmd_file.name != "__init__.py":
        #         await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")

        # print(f'Logged in as {bot.user.name} - {bot.user.id}')#แสดงชื่อบอทกับไอดี
        

        bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        await bot.tree.sync(guild=settings.GUILDS_ID)

        print('...................Bot is working Press Ctrl+c for stop Bot...................')


    @bot.tree.command()
    async def register(interaction : discord.Interaction):
        register_modal = RegisterModal()
        register_modal.user = interaction.user
        await interaction.response.send_modal(register_modal)

    @bot.command(name='deletecommands', aliases=['clear'])
    async def delete_commands(ctx):
        bot.tree.clear_commands(guild=None)
        await bot.tree.sync()
        await ctx.send('Unused Commands deleted.')

    


    bot.run(settings.DISCORD_API_SECRET, root_logger=True)#ทำงานด้วยโทเคน

if __name__=="__main__":
    run()