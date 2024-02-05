import random
from typing import Any

from discord.interactions import Interaction
import settings
import discord
import aiosqlite
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

class Days(enum.Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class RegisterModal(discord.ui.Modal, title='Register'):
    std_id = discord.ui.TextInput(label='Student ID', placeholder='ex: 64XXXXXX', style=discord.TextStyle.short, max_length=8)
    name_th = discord.ui.TextInput(label='ชื่อ - สกุล', placeholder='ex: สมชาย ใจดี', style=discord.TextStyle.short, max_length=100)
    name_en = discord.ui.TextInput(label='Full Name', placeholder='ex: Somchai Jaidee', style=discord.TextStyle.short, max_length=100)
    tel_num = discord.ui.TextInput(label='เบอร์โทรศัพท์', placeholder='ex: 08XXXXXXXX', style=discord.TextStyle.short, max_length=10)
    e_mail = discord.ui.TextInput(label='E-mail', placeholder='ex: example@gmail.com', style=discord.TextStyle.short, max_length=100)
    async def on_submit(self, interaction : discord.Interaction):

        channel = interaction.guild.get_channel(settings.FEEDBACK_CH) #ดึงช่องที่ต้องการส่งข้อความ

        
        embed1 = discord.Embed(
            title="Register success!!",
            description="**โปรดตรวจสอบความถูกต้องของข้อมูล\nหากข้อมูลไม่ถูกต้อง กรุณาใช้คำสั่ง /register ใหม่อีกครั้ง**",
            color=discord.Color.green()
        )
        embed1.add_field(
            name=f'{self.std_id.label}',
            value=f'{self.std_id.value}',
            inline=False #ขึ้นบรรทัดใหม่
        )
        embed1.add_field(
            name=f'{self.name_th.label}',
            value=f'{self.name_th.value}',
        )
        embed1.add_field(
            name=f'{self.name_en.label}',
            value=f'{self.name_en.value}',
            inline=False
        )
        embed1.add_field(
            name=f'{self.tel_num.label}',
            value=f'{self.tel_num.value}',
            inline=False
        )
        embed1.add_field(
            name=f'{self.e_mail.label}',
            value=f'{self.e_mail.value}',
            inline=False
        )       
        embed1.set_thumbnail(url=self.user.avatar) #รูปโปรไฟล์
        embed1.set_author(name=self.user.display_name) #ชื่อผู้ใช้

        #ดึงไอดีของผู้ใช้ในเซิฟเวอร์
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)

        role_id_1 = 1203950522952851526  # กำหนด id ของ role

        # ดึง role ที่ต้องการจะกำหนด
        role_1 = discord.utils.get(guild.roles, id=role_id_1)
        
        await member.add_roles(role_1) #กำหนด role ให้กับผู้ใช้
        
        std_email = (f'{self.std_id.value}@kmitl.ac.th') #เมลนักศึกษา

        #await channel.send(embed=embed)
        await interaction.response.send_message(embed=embed1, ephemeral=True) #ส่งข้อมูลที่กรอกออกมาใน embed
        print(std_email)
        #await interaction.response.send_message('หากข้อมูลไม่ถูกต้องใช้คำสั่ง /register อีกครั้งเพื่อแก้ไข', ephemeral=True)

        async def on_error(self, interaction : discord.Interaction, error):
            ...


class GroupworkView(discord.ui.View):
    def __init__(self, topic: str, member_amount: int, member: str):
        super().__init__()

        self.topic = topic
        self.member_amount = member_amount

        self.member = member
        
        # self.sub = sub
        self.sub = len(self.member)
        self.remaining =  member_amount - self.sub 

        self.embed = discord.Embed(
            title=f'📢   {topic}   📌',
            description=f"กลุ่มจำนวน : **{member_amount}** คน"+
                        f"\nเหลืออีก : **{self.remaining}** คน",
            color=discord.Color.random()
        )
        
        self.embed.set_thumbnail(url='') #ใส่รูป

        self.update_embed()


    def update_embed(self):
        self.embed.remove_field(0)
        member_list_with_numbers = [f"{index + 1}. {self.member[index]}" for index in range(len(self.member))]
        self.embed.add_field(
            name='👤 รายชื่อสมาชิก',
            # value='\n'.join(f"{self.member[item]}" for item in range(len(self.member))),
            value='\n'.join(member_list_with_numbers),
            inline=False
        )    
        

    @discord.ui.button(label='Join', style=discord.ButtonStyle.green)
    async def join(self, interaction : discord.Interaction, button : discord.ui.Button):
        new_member_name = str(interaction.user.display_name)
        self.member.append(new_member_name)

        if self.remaining > 0 :

            testg = GroupworkView(self.topic, self.member_amount, self.member)
            testg.update_embed()
            await interaction.response.edit_message(embed=testg.embed, view=testg)

        else:
            button.disabled = True
            await interaction.response.edit_message(embed=self.embed, view=self)

        # ตรวจสอบว่าคนครบแล้ว
        if self.remaining == 1:
            # รวม mention ทุกคนในกลุ่ม
            mention_string = ' '.join([f'<@{interaction.guild.get_member_named(member_name).id}>' for member_name in self.member])
            await interaction.followup.send(f'🎉 กลุ่ม **"{self.topic}"** ครบจำนวนแล้ว, สามารถเริ่มงานได้เลยครับ 🎉 {mention_string}')

        else:
            button.disabled = True


    @discord.ui.button(label='Leave', style=discord.ButtonStyle.red)
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.sub > 0:
            button.disabled = False
            # ตรวจสอบว่า interaction.user.display_name อยู่ใน self.member หรือไม่
            if str(interaction.user.display_name) in self.member:
                self.member.remove(str(interaction.user.display_name))  # ลบชื่อคนที่กดปุ่ม Leave ออกจาก self.member
            testg = GroupworkView(self.topic, self.member_amount, self.member)
            await interaction.response.edit_message(embed=testg.embed, view=testg)
        else:
            button.disabled = True
            await interaction.response.edit_message(embed=self.embed, view=self)
            
            
        
    async def on_timeout(self):
        # Cleanup logic if needed
        pass


class StudyPlanEmbed(discord.ui.View):
    def __init__(self, day_name: str, start_time: str, end_time: str, subject: str):
        super().__init__()

        self.embed = discord.Embed(
            title='Study Plan',
            description="รายละเอียด",
            color=discord.Color.green(),
        )
        self.embed.add_field(
            name=day_name,
            value=f'   {start_time} น. - {end_time} น. | {subject}',
            inline=False
        )       


class Profile(discord.ui.View):
    def __init__(self, of: discord.Member):
        super().__init__()
        
        self.embed = discord.Embed(
            title=f'Profile',
            description=f"Name : {of.display_name}"+
                        f"\nUsername : {of.name}",
            color=discord.Color.green(),
        )
        self.embed.add_field(
            name='ID',
            value=f'{of.id}',
            inline=False
        )
        self.embed.add_field(
            name='E-mail',
            value=f'{of.display_name}@gmail.com',
            inline=False
        )
        self.embed.set_thumbnail(url=of.avatar)

    async def on_timeout(self):
        # Cleanup logic if needed
        pass
   



def run():
    intents = discord.Intents.all()
    # intents.message_content = True  #โต้ตอบกับข้อความ
    # intents.members = True

    bot = commands.Bot(command_prefix="!", intents=intents)


    @bot.event
    async def on_ready():#เมื่อบอททำงาน
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

        #แสดงไอดีและชื่อของ guilds ทั้งหมดที่บอทอยู่
        for guild in bot.guilds:
            logger.info(f'Guild Name: {guild.name} (ID: {guild.id})')

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Discord"))#สถานะของบอท
        print(colors.GREEN + '.'*32 +'Bot is started' + '.'*32 + colors.RESET)
       
        #load cogs
        for cogs_file in settings.COGS_DIR.glob("*.py"):
            if cogs_file != "__init__.py":
                await bot.load_extension(f"cogs.{cogs_file.name[:-3]}") #เพิ่มคำสั่งจากไฟล์นอก
                print(colors.BLUE + 'import : ' + colors.RESET + f' {cogs_file}' + colors.GREEN + '  success' + colors.RESET)
                
        
                
        # for slashcommands_file in settings.SLASHCOMMANDS_DIR.glob("*.py"):
        #     if slashcommands_file != "__init__.py":
        #         await bot.load_extension(f"slashcommands.{slashcommands_file.name[:-3]}")                    #ต้องแก้
        #         print('import slash_cmds success')
                

        # for cmd_file in settings.CMDS_DIR.glob("*.py"):
        #     if cmd_file.name != "__init__.py":
        #         await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")
        #         print(f'import {cmd_file} success')

        
        #sync slash commands global
        try:
            synced = await bot.tree.sync()
            print(f'synced {len(synced)} commands')
        except Exception as e:
            print(e)
            
        #sync slash commands guild
        # bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        # await bot.tree.sync(guild=settings.GUILDS_ID)
            

        #connect database
        # bot.db = await aiosqlite.connect('Main.db')
        # c = await bot.db.cursor()
        # await c.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER)")
        # await bot.db.commit()

        print(colors.YELLOW + '...................Bot is working Press Ctrl+c for stop Bot...................' + colors.RESET)

#context menu zone

    @bot.tree.context_menu(name="View Profile")
    async def get_profile(interaction: discord.Interaction, of : discord.Member):
        view = Profile(of)
        await interaction.response.send_message(embed=view.embed, view=view, ephemeral=True)
    

#slash commands zone

    #register
    @bot.tree.command(description='Register for New member | ลงทะเบียนสำหรับสมาชิกใหม่') #คำอธิบายของคำสั่ง
    async def register(interaction : discord.Interaction):
        register_modal = RegisterModal()
        register_modal.user = interaction.user
        channel = interaction.guild.get_channel(settings.FEEDBACK_CH) #ดึงช่องที่ต้องการส่งข้อความ
        if settings.FEEDBACK_CH and interaction.channel_id != settings.FEEDBACK_CH:
            await interaction.response.send_message("คำสั่งนี้สามารถใช้ได้เฉพาะในช่องที่กำหนดเท่านั้น", ephemeral=True)
        else:
            await interaction.response.send_modal(register_modal) #รองรับการกำหนด channel ที่ใช้งานได้
        


    #profile
    @bot.tree.command(description='View profile | ดูโปรไฟล์ของผู้ใช้')
    @app_commands.describe(of='ดูโปรไฟล์ของผู้ใช้ที่กำหนด')
    async def profile(interaction: discord.Interaction, of: discord.Member):
        view = Profile(of)
        await interaction.response.send_message(embed=view.embed, view=view, ephemeral=True)
            
        

    #study_plan
    @bot.tree.command(description='Manage study plan | จัดการตารางเรียน')
    @app_commands.choices(
        day=[
            app_commands.Choice(name="🔴 Sunday - วันอาทิตย์", value="1"),
            app_commands.Choice(name="🟡 Monday - วันจันทร์", value="2"), 
            app_commands.Choice(name="🩷 Tuesday - วันอังคาร", value="3"),
            app_commands.Choice(name="🟢 Wednesday - วันพุธ", value="4"),
            app_commands.Choice(name="🟠 Thursday - วันพฤหัสบดี", value="5"),
            app_commands.Choice(name="🔵 Friday - วันศุกร์", value="6"),
            app_commands.Choice(name="🟣 Saturday - วันเสาร์", value="7"),
        ])
    @app_commands.describe(day='วัน', start='เวลาเริ่มเรียน **EX. 09.00**', until='เวลาเลิกเรียน **EX. 18.00**', subject='ชื่อวิชา')
    async def study_plan_edit(interaction: discord.Interaction, day: app_commands.Choice[str], start: str, until: str, subject: str):
        study_plan_embed = StudyPlanEmbed(day.name, start, until, subject)
        await interaction.response.send_message(embed=study_plan_embed.embed, view=study_plan_embed)


    #groupwork
    @bot.tree.command(description='Create groupwork | สร้างกลุ่มงาน')
    @app_commands.describe(topic='หัวข้อ', member_amount='จำนวนสมาชิก')
    async def groupwork(interaction: discord.Interaction, topic: str, member_amount: int):
        # print(interaction.user.display_name)
        initial_member = [interaction.user.display_name]
        view = GroupworkView(topic, member_amount, initial_member)
        await interaction.response.send_message(embed=view.embed, view=view)
    

    #random
    @bot.tree.command(description='Random | การสุ่ม')
    @app_commands.describe(entries='สิ่งที่ต้องการสุ่ม โดยใช้ช่องว่างเป็นตัวคั่น')
    async def randoms(interaction: discord.Interaction, entries: str):
        entries_list = entries.split(' ')
        random_result = random.choice(entries_list)
        await interaction.response.send_message(f'ผลลัพธ์ที่ได้คือ {random_result}', ephemeral=True)
    

    #delete commands unused
    @bot.command(name='deletecommands', aliases=['clear'])
    async def delete_commands(ctx):
        bot.tree.clear_commands(guild=None)
        await bot.tree.sync()
        await ctx.send('Unused Commands deleted.')

    
    

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)#ทำงานด้วยโทเคน

if __name__=="__main__":
    run()