import random
from typing import Any

from discord.interactions import Interaction
import settings
import discord
import traceback
# import utils
import typing
import enum
from datetime import datetime
from discord.ext import commands
from discord import app_commands


logger = settings.logging.getLogger("bot")

class colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'

class Food(enum.Enum):
    apple = 1
    banana = 2
    orange = 3



class RegisterModal(discord.ui.Modal, title='Register'):
    std_id = discord.ui.TextInput(label='Student ID', placeholder='ex: 64XXXXXX', style=discord.TextStyle.short, max_length=13)
    name_th = discord.ui.TextInput(label='ชื่อ - สกุล', placeholder='ex: สมชาย ใจดี', style=discord.TextStyle.short, max_length=100)
    name_en = discord.ui.TextInput(label='Full Name', placeholder='ex: Somchai Jaidee', style=discord.TextStyle.short, max_length=100)
    tel_num = discord.ui.TextInput(label='เบอร์โทรศัพท์', placeholder='ex: 08XXXXXXXX', style=discord.TextStyle.short, max_length=10)
    e_mail = discord.ui.TextInput(label='E-mail', placeholder='ex: example@gmail.com', style=discord.TextStyle.short, max_length=100)
    # age = discord.ui.TextInput(label='Age', placeholder='ex: 22', style=discord.TextStyle.short, max_length=2)
    # aboutme = discord.ui.TextInput(label='About Me', placeholder='ex: Tell about yourself...', style=discord.TextStyle.paragraph, max_length=300)
    async def on_submit(self, interaction : discord.Interaction):
        channel = interaction.guild.get_channel(settings.FEEDBACK_CH)
        
        embed = discord.Embed(
            title="Register success!!",
            description="โปรดตรวจสอบความถูกต้องของข้อมูล",
            color=discord.Color.green()
        )
        embed.add_field(
            name=f'{self.std_id.label}',
            value=f'{self.std_id.value}',
            inline=False #ขึ้นบรรทัดใหม่
        )
        embed.add_field(
            name=f'{self.name_th.label}',
            value=f'{self.name_th.value}',
        )
        embed.add_field(
            name=f'{self.name_en.label}',
            value=f'{self.name_en.value}',
            inline=False
        )
        embed.add_field(
            name=f'{self.tel_num.label}',
            value=f'{self.tel_num.value}',
            inline=False
        )
        embed.add_field(
            name=f'{self.e_mail.label}',
            value=f'{self.e_mail.value}',
            inline=False
        )       
        embed.set_thumbnail(url=self.user.avatar) #รูปโปรไฟล์
        embed.set_author(name=self.user.display_name) #ชื่อผู้ใช้
        

        # await channel.send(embed=embed)
        await interaction.response.send_message(embed=embed, ephemeral=True) #ส่งข้อมูลที่กรอกออกมาใน embed
        print(self.std_id.value)
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
        print(colors.GREEN + 'bot started' + colors.RESET)
       

        for cogs_file in settings.COGS_DIR.glob("*.py"):
            if cogs_file != "__init__.py":
                await bot.load_extension(f"cogs.{cogs_file.name[:-3]}") #เพิ่มคำสั่งจากไฟล์นอก
                print(f'import {cogs_file} success')
                
        
        
        # mygroup1 = MyGroup1(name=greetings,description='Welcome User')
        # bot.tree.add_command(mygroup1)
        # for slashcommands_file in settings.SLASHCOMMANDS_DIR.glob("*.py"):
        #     if slashcommands_file != "__init__.py":
        #         await bot.load_extension(f"slashcommands.{slashcommands_file.name[:-3]}")                    #ต้องแก้
        #         print('import slash_cmds success')
                
    


        # for cmd_file in settings.CMDS_DIR.glob("*.py"):
        #     if cmd_file.name != "__init__.py":
        #         await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")
        #         print(f'import {cmd_file} success')

        # print(f'Logged in as {bot.user.name} - {bot.user.id}')#แสดงชื่อบอทกับไอดี
        

        bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        await bot.tree.sync(guild=settings.GUILDS_ID)

        print(colors.YELLOW + '...................Bot is working Press Ctrl+c for stop Bot...................' + colors.RESET)


    @bot.tree.command(description='register for new member')
    async def register(interaction : discord.Interaction):
        register_modal = RegisterModal()
        register_modal.user = interaction.user
        await interaction.response.send_modal(register_modal)



    @bot.tree.command(description='find groupwork')
    async def group(interaction : discord.Interaction, topic : str, member_amount : int):
        embed = discord.Embed(
            title=f'{topic}',
            description=f"จำนวน : {member_amount} คน",
            color=discord.Color.green()
        )
        view = discord.ui.View()
        button1 = discord.ui.Button(label='Join', style=discord.ButtonStyle.green)
        button2 = discord.ui.Button(label='leave', style=discord.ButtonStyle.red)
        view.add_item(button1)
        view.add_item(button2)
        
        await interaction.response.send_message(embed=embed, view=view)

        

    @bot.command(name='deletecommands', aliases=['clear'])
    async def delete_commands(ctx):
        bot.tree.clear_commands(guild=None)
        await bot.tree.sync()
        await ctx.send('Unused Commands deleted.')

    


    bot.run(settings.DISCORD_API_SECRET, root_logger=True)#ทำงานด้วยโทเคน

if __name__=="__main__":
    run()