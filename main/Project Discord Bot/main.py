import random
from typing import Any

from discord.interactions import Interaction
import settings
import discord
# import aiosqlite
import traceback
# import utils
import typing
import enum
from datetime import datetime
from discord.ext import commands
from discord import app_commands
import ast

# from database import Database
# db = Database()



logger = settings.logging.getLogger("bot")



def have_permission():
    async def predicate(interaction: discord.Interaction):
        role_id = 0  # กำหนด id ของ role, None = 0
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        
        if role_id == 0:
            role = guild.default_role  # ใช้ role ที่กำหนดเป็น default (everyone)
        else:
            role = guild.get_role(role_id)

        return role in member.roles

    return app_commands.check(predicate)


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
    tel_num = discord.ui.TextInput(label='เบอร์โทรศัพท์ (ไม่จำเป็น)', placeholder='ex: 08XXXXXXXX', style=discord.TextStyle.short, max_length=10, default='-', required=False)
    e_mail = discord.ui.TextInput(label='E-mail  (ไม่จำเป็น)', placeholder='ex: example@gmail.com', style=discord.TextStyle.short, max_length=100, default='-', required=False)
    async def on_submit(self, interaction : discord.Interaction):

        channel = interaction.guild.get_channel(settings.FEEDBACK_CH) #ดึงช่องที่ต้องการส่งข้อความ


        db.register_user( self.std_id.value, self.name_th.value, self.name_en.value, interaction.user.id, interaction.user.display_name, interaction.guild_id, self.tel_num.value, self.e_mail.value)
        
        embed1 = discord.Embed(
            title="✅ Register success!!",
            description="\n⚠️ โปรดตรวจสอบความถูกต้องของข้อมูล ⚠️\nหากข้อมูลไม่ถูกต้อง กรุณาใช้คำสั่ง **/register** ใหม่อีกครั้ง\n",
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
            # inline=False
        )
        embed1.add_field(
            name=f'เบอร์โทรศัพท์',
            value=f'{self.tel_num.value}',
            inline=False
        )
        embed1.add_field(
            name=f'E-mail',
            value=f'{self.e_mail.value}',
            inline=False
        )       
        embed1.set_thumbnail(url=self.user.avatar) #รูปโปรไฟล์
        # embed1.set_author(name=self.user.display_name) #ชื่อผู้ใช้

        #ดึงไอดีของผู้ใช้ในเซิฟเวอร์
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)

        role_id_1 = 0  # กำหนด id ของ role

        if role_id_1 == 0:
            await interaction.response.send_message('ผู้ดูแลยังไม่ได้กำหนด role ที่จะมอบให้ผู้ใช้งาน', ephemeral=True)
            return

        # ดึง role ที่ต้องการจะกำหนด
        role_1 = discord.utils.get(guild.roles, id=role_id_1)

        if role_1 not in member.roles: #ตรวจสอบว่าผู้ใช้มี role นี้หรือยัง
        
            await member.add_roles(role_1) #กำหนด role ให้กับผู้ใช้
        
        std_email = (f'{self.std_id.value}@kmitl.ac.th') #เมลนักศึกษา

        #await channel.send(embed=embed)
        await interaction.response.send_message(embed=embed1, ephemeral=True) #ส่งข้อมูลที่กรอกออกมาใน embed
        print(std_email)
        #await interaction.response.send_message('หากข้อมูลไม่ถูกต้องใช้คำสั่ง /register อีกครั้งเพื่อแก้ไข', ephemeral=True)

        async def on_error(self, interaction : discord.Interaction, error):
            ...


class GroupworkView(discord.ui.View):
    def __init__(self, topic: str, descriptions: str, member_amount: int, member: str):
        super().__init__()

        self.topic = topic
        self.member_amount = member_amount
        self.descriptions = descriptions
        

        self.member = member
        
        # self.sub = sub
        self.sub = len(self.member)
        self.remaining =  member_amount - self.sub 

        self.embed = discord.Embed(
            title=f'📢   {topic}   📌',
            description=f"กลุ่มจำนวน : **{member_amount}** คน"+
                        f"\nเหลืออีก : **{self.remaining}** คน"+
                        f"\n\n**📃รายละเอียด**"+
                        f"\n{self.descriptions}",
            color=discord.Color.random()
        )
        
        self.embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1206514380645208104/1209079987152494642/Icons-Land-Vista-People-Groups-Meeting-Dark.256.png?ex=65e59e7c&is=65d3297c&hm=8906a84729e8df490124a4c04236270f4390a1d9eb2d11a9d410fd44c958ae57&') #ใส่รูป

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
    @have_permission()
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_member_name = str(interaction.user.display_name)

        # ตรวจสอบว่า new_member_name อยู่ใน self.member หรือไม่
        if new_member_name not in self.member :
            self.member.append(new_member_name)

            if self.remaining > 0:
                testg = GroupworkView(self.topic, self.descriptions, self.member_amount, self.member)
                testg.update_embed()
                await interaction.response.edit_message(embed=testg.embed, view=testg)
            else:
                del self.member[-1]
                button.disabled = True
                await interaction.response.edit_message(embed=self.embed, view=self)

            # ตรวจว่ากลุ่มครบจำนวนแล้วหรือยัง
            if self.remaining == 1:
                mention_string = ' '.join([f'<@{interaction.guild.get_member_named(member_name).id}>' for member_name in self.member])
                await interaction.followup.send(f'🎉 กลุ่ม **"{self.topic}"** จำนวนสมาชิกครบแล้ว เริ่มทำงานกันได้เลย!! 🎉 {mention_string}')

        else:
            await interaction.response.edit_message(embed=self.embed, view=self)
            await interaction.followup.send(f'คุณ **{new_member_name}** ได้เข้าร่วมกลุ่ม **"{self.topic}"** ไปแล้ว', ephemeral=True)



    @discord.ui.button(label='Leave', style=discord.ButtonStyle.red)
    @have_permission()
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.sub > 0:
            button.disabled = False
            # ตรวจสอบว่า interaction.user.display_name อยู่ใน self.member หรือไม่
            if str(interaction.user.display_name) in self.member:
                self.member.remove(str(interaction.user.display_name))  # ลบชื่อคนที่กดปุ่ม Leave ออกจาก self.member
            testg = GroupworkView(self.topic, self.descriptions, self.member_amount, self.member)
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

class StudyPlanView(discord.ui.View):
    def __init__(self, user_id : int,  day_values: int):
        super().__init__()

        num = 8
        print(type(day_values))
        print(type(num))
        

        if int(day_values) == num:
            print("pass")
            day1, times1, subject1, day_num1 = db.study_plan_view(12345679, 1)
            day2, times2, subject2, day_num2 = db.study_plan_view(12345679, 2)
            day3, times3, subject3, day_num3 = db.study_plan_view(12345679, 3)
            day4, times4, subject4, day_num4 = db.study_plan_view(12345679, 4)
            day5, times5, subject5, day_num5 = db.study_plan_view(12345679, 5)
            day6, times6, subject6, day_num6 = db.study_plan_view(12345679, 6)
            day7, times7, subject7, day_num7 = db.study_plan_view(12345679, 7)

            value_string1=' '
            value_string2=' '
            value_string3=' '
            value_string4=' '
            value_string5=' '
            value_string6=' '
            value_string7=' '

            if day1 == None :
                value_string1 = ' - '

            else :
                time1 = [ast.literal_eval(time_range) for time_range in times1]
                for i in range(len(day1)):
                    value_string1 += f'   {time1[i][0]} น. - {time1[i][1]} น. | {subject1[i]}\n'
                
            if day2 == None :
                value_string2 = ' - '

            else :
                time2 = [ast.literal_eval(time_range) for time_range in times2]
                for i in range(len(day2)):
                    value_string2 += f'   {time2[i][0]} น. - {time2[i][1]} น. | {subject2[i]}\n'
                    
            if day3 == None :
                value_string3 = ' - '

            else :
                time3 = [ast.literal_eval(time_range) for time_range in times3]
                for i in range(len(day3)):
                    value_string3 += f'   {time3[i][0]} น. - {time3[i][1]} น. | {subject3[i]}\n'
                
            if day4 == None :
                value_string4 = ' - '

            else :
                time4 = [ast.literal_eval(time_range) for time_range in times4]
                for i in range(len(day4)):
                    value_string4 += f'   {time4[i][0]} น. - {time4[i][1]} น. | {subject4[i]}\n'

            if day5 == None :
                value_string5 = ' - '

            else :
                time5 = [ast.literal_eval(time_range) for time_range in times5]
                for i in range(len(day5)):
                    value_string5 += f'   {time5[i][0]} น. - {time5[i][1]} น. | {subject5[i]}\n'
                
            if day6 == None :
                value_string6 = ' - '

            else :
                time6 = [ast.literal_eval(time_range) for time_range in times6]
                for i in range(len(day6)):
                    value_string6 += f'   {time6[i][0]} น. - {time6[i][1]} น. | {subject6[i]}\n'
                    
            if day7 == None :
                value_string7 = ' - '

            else :
                time7 = [ast.literal_eval(time_range) for time_range in times7]
                for i in range(len(day7)):
                    value_string7 += f'   {time7[i][0]} น. - {time7[i][1]} น. | {subject7[i]}\n'


            # สร้าง Embed จาก value_string ที่ได้
            self.embed = discord.Embed(
                title='Study Plan',
                description="รายละเอียด",
                color=discord.Color.green(),
            )
            self.embed.add_field(
                name= '🔴 Sunday - วันอาทิตย์',
                value= value_string1,
                inline= False
            )
            self.embed.add_field(
                name= '🟡 Monday - วันจันทร์',
                value= value_string2,
                inline= False
            )
            self.embed.add_field(
                name= '🩷 Tuesday - วันอังคาร',
                value= value_string3,
                inline= False
            )
            self.embed.add_field(
                name= '🟢 Wednesday - วันพุธ',
                value= value_string4,
                inline= False
            )
            self.embed.add_field(
                name= '🟠 Thursday - วันพฤหัสบดี',
                value= value_string5,
                inline= False
            )
            self.embed.add_field(
                name= '🔵 Friday - วันศุกร์',
                value= value_string6,
                inline= False
            )
            self.embed.add_field(
                name= '🟣 Saturday - วันเสาร์',
                value= value_string7,
                inline= False
            )

        else :
            day, times, subject, day_num = db.study_plan_view(12345679, day_values)
            time = [ast.literal_eval(time_range) for time_range in times]

            value_string = ''
            for i in range(len(day)):
                value_string += f'   {time[i][0]} น. - {time[i][1]} น. | {subject[i]}\n'

            self.embed = discord.Embed(
                title='Study Plan',
                description="รายละเอียด",
                color=discord.Color.green(),
            )
            self.embed.add_field(
                name= day[0],
                value= value_string,
                inline= False
            )

class ProfileView(discord.ui.View):
    def __init__(self, interaction : discord.Interaction, of: discord.Member):
        super().__init__()
        
        self.embed = discord.Embed(
            title='Profile',
            description=f"ชื่อ-สกุล : {db.profile(of.id,'TH', interaction.guild_id)}"+
                        f"\nFull Name : {db.profile(of.id,'EN', interaction.guild_id)}"+
                        f"\nUsername : {of.name}",
            color=discord.Color.green(),
        )
        self.embed.add_field(
            name='ID',
            value=f"{db.profile(of.id,'ID', interaction.guild_id)}",
            inline=False
        )
        self.embed.add_field(
            name='E-mail',
            value=f"{db.profile(of.id,'Email', interaction.guild_id)}",
            inline=False
        )
        self.embed.add_field(
            name='Tel.',
            value=f"{db.profile(of.id,'Phone', interaction.guild_id)}",
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

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Discord server"))#สถานะของบอท
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
        # try:
        #     synced = await bot.tree.sync()
        #     print(f'synced {len(synced)} commands')
        # except Exception as e:
        #     print(e)
            
        #sync slash commands guild
        bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        await bot.tree.sync(guild=settings.GUILDS_ID)
            


        print(colors.YELLOW + '...................Bot is working Press Ctrl+c for stop Bot...................' + colors.RESET)

#on_messages conditions
    @bot.event
    async def on_message(message):
        if message.author == bot.user:  # ไม่ต้องตอบกลับถ้าข้อความเป็นของบอทเอง
            return
        
        channel_respond = db.check_feedback_ch("register", discord.Interaction.guild_id)

        if channel_respond and message.channel.id not in channel_respond:
            return

        # question = db.get_question()  # ดึงคำถามจากฐานข้อมูล
        # answer = db.get_answer()  # ดึงคำตอบจากฐานข้อมูล
        # type_answer = db.get_type_answer()  # ดึงประเภทของคำตอบจากฐานข้อมูล

        # if type_answer == "in_word":  # ตรวจสอบประเภทของคำตอบ
        #     for word in question:  # วนลูปคำค้นหา
        #         if word in message.content:  # ตรวจสอบว่ามีคำถามในข้อความหรือไม่
        #             await message.channel.send(answer)  # ส่งคำตอบกลับไปในช่องเดิมที่ข้อความถูกส่งมา

        # if type_answer == "match":  # ตรวจสอบประเภทของคำตอบ
        #     for word in question:
        #         if word == message.content: # ตรวจสอบว่าคำถามเป็นคำตอบที่ตรงกันหรือไม่
        #             await message.channel.send(answer)

        if "สวัสดี" in message.content:  # ตรวจสอบว่ามีคำว่า "สวัสดี" ในข้อความหรือไม่
            await message.channel.send("สวัสดีครับ")

        if "GG" == message.content:  # ตรวจสอบว่าข้อความเป็น "GG" หรือไม่
            await message.channel.send("GGWP")

        await bot.process_commands(message)  # ตรวจสอบว่าข้อความเป็นคำสั่งหรือไม่ และประมวลผลต่อไป

#on_member_join
    @bot.event
    async def on_member_join(member : discord.Member):
        # สร้างข้อความต้อนรับ
        welcome_message = f"👋 ยินดีต้อนรับคุณ **{member.mention}** เข้าสู่เซิฟเวอร์\n\nกรุณาใช้คำสั่ง /register สำหรับลงทะเบียนเพื่อแสดงแชลแนลต่าง ๆ ในเซิฟเวอร์\n"
        
        welcome_embed = discord.Embed(
            description= welcome_message,
            color=discord.Color.random(),
        )
        # welcome_embed.set_image(url="https://cdn.discordapp.com/attachments/1206514380645208104/1213394754436472862/anime.gif?ex=65f550ed&is=65e2dbed&hm=0d81a259401b312e9ac6a54e7a84863c56448ba7aa6a50461bd0db53cf5c007d&")
        welcome_embed.set_author(name=member.guild.name, icon_url=member.guild.icon)
        welcome_embed.set_thumbnail(url=member.display_avatar)

        # หาช่องที่ต้องการส่งข้อความต้อนรับ
        channel = member.guild.system_channel  # หากต้องการให้ส่งในช่อง system_channel
        # channel = member.guild.get_channel(1136582643765493772)
        # หากต้องการส่งในช่องที่มีชื่อ "welcome" สามารถใช้ชื่อได้เลย เช่น member.guild.get_channel("welcome")
        # หรือหากต้องการใช้ ID ของช่องให้ใช้ member.guild.get_channel(ID) โดย ID เป็น ID ของช่อง
        # ตัวอย่างเช่น: channel = member.guild.get_channel(CHANNEL_ID)
        
        if channel is not None:
            # ส่งข้อความต้อนรับ
            await channel.send(embed=welcome_embed)
            

#function update bot data
    async def update_bot():
        list(bot)

#Feedback_channel
    async def feedback(interaction : discord.Interaction, channel : list=None):
        FEEDBACK_CH = channel
        valid_channel = interaction.channel_id in FEEDBACK_CH

        if not valid_channel and FEEDBACK_CH:
            await interaction.response.send_message('คำสั่งนี้สามารถใช้ได้เฉพาะในช่องที่กำหนดเท่านั้น', ephemeral=True)
            return


#context menu zone

    @bot.tree.context_menu(name="View Profile")
    @have_permission()
    async def get_profile(interaction: discord.Interaction, of : discord.Member):
        view = ProfileView(interaction, of)
        # await update_bot #อัพเดทข้อมูลบอท
        await interaction.response.send_message(embed=view.embed, view=view, ephemeral=True)
    
    @get_profile.error
    async def get_profile_error(interaction: discord.Interaction, error):
        await interaction.response.send_message("คุณไม่มีสิทธิ์ในการใช้คำสั่งนี้", ephemeral=True)
        
    

#slash commands zone

    #register
    @bot.tree.command(description='Register for New member | ลงทะเบียนสำหรับสมาชิกใหม่')
    async def register(interaction: discord.Interaction):
        FEEDBACK_CH = db.check_feedback_ch("register", interaction.guild_id) #ไอดีแชลแนลที่ต้องการให้ตอบสนอง
        await feedback(interaction, FEEDBACK_CH)
        

        register_modal = RegisterModal()
        register_modal.user = interaction.user
        await interaction.response.send_modal(register_modal)
    

    #profile
    @bot.tree.command(description='View profile | ดูโปรไฟล์ของผู้ใช้')
    @have_permission()
    @app_commands.describe(of='ดูโปรไฟล์ของผู้ใช้ที่กำหนด')
    async def profile(interaction: discord.Interaction, of: discord.Member):
        FEEDBACK_CH = db.check_feedback_ch("profile", interaction.guild_id)
        await feedback(interaction, FEEDBACK_CH)
        
        view = ProfileView(interaction, of) #ส่งข้อมูลตัวแปรเข้าตัวทำงานหลัก
        await interaction.response.send_message(embed=view.embed, view=view, ephemeral=True) #แสดง embed ที่อยู่ใน ProfileView พร้อมส่ง of ไปด้วย

    @profile.error
    async def profile_error(interaction: discord.Interaction, error):
        await interaction.response.send_message("คุณไม่มีสิทธิ์ในการใช้คำสั่งนี้", ephemeral=True)       
        

    #study_plan
    @bot.tree.command(description='Manage study plan | จัดการตารางเรียน')
    @have_permission()
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
    @app_commands.describe(day='วัน', start='เวลาเริ่มเรียน **EX. 09:00**', until='เวลาเลิกเรียน **EX. 18:00**', subject='ชื่อวิชา')
    async def study_plan_edit(interaction: discord.Interaction, day: app_commands.Choice[str], start: str, until: str, subject: str):

        FEEDBACK_CH = db.check_feedback_ch("plan_edit", interaction.guild_id) #ไอดีแชลแนลที่ต้องการให้ตอบสนอง
        await feedback(interaction, FEEDBACK_CH)

        # db.study_plan(day.name, start, until, subject, interaction.user.id, day.value)

        study_plan_embed = StudyPlanEmbed(day.name, start, until, subject)
        await interaction.response.send_message(embed=study_plan_embed.embed, view=study_plan_embed)
    
    @study_plan_edit.error
    async def study_plan_edit_error(interaction: discord.Interaction, error):
        await interaction.response.send_message("คุณไม่มีสิทธิ์ในการใช้คำสั่งนี้", ephemeral=True)

    @bot.tree.command(description='View study plan | ดูตารางเรียน')
    @have_permission()
    @app_commands.choices(
        day=[
            app_commands.Choice(name="📅 ALL days - ทุกวัน", value="8"),
            app_commands.Choice(name="🔴 Sunday - วันอาทิตย์", value="1"),
            app_commands.Choice(name="🟡 Monday - วันจันทร์", value="2"), 
            app_commands.Choice(name="🩷 Tuesday - วันอังคาร", value="3"),
            app_commands.Choice(name="🟢 Wednesday - วันพุธ", value="4"),
            app_commands.Choice(name="🟠 Thursday - วันพฤหัสบดี", value="5"),
            app_commands.Choice(name="🔵 Friday - วันศุกร์", value="6"),
            app_commands.Choice(name="🟣 Saturday - วันเสาร์", value="7"),
        ]
    )
    @app_commands.describe(day='วันที่ต้องการดูตารางเรียน',share_to='ระบุผู้ใช้ที่ต้องการแชร์ {@user}')
    async def study_plan_view(interaction: discord.Interaction, day: app_commands.Choice[str], share_to: discord.Member=None):
        study_plan_embed = StudyPlanView(interaction.user.id, day.value)

        FEEDBACK_CH = db.check_feedback_ch("plan_view", interaction.guild_id) #ไอดีแชลแนลที่ต้องการให้ตอบสนอง
        await feedback(interaction, FEEDBACK_CH)

        if share_to is not None:
            await share_to.send(embed=study_plan_embed.embed, view=study_plan_embed)
            await interaction.response.send_message(f'ได้แชร์ตารางเรียนไปให้ {share_to} แล้ว ✅', ephemeral=True)
        await interaction.response.send_message(embed=study_plan_embed.embed, view=study_plan_embed, ephemeral=True)

    @study_plan_view.error
    async def study_plan_view_error(interaction: discord.Interaction, error):
        await interaction.response.send_message("คุณไม่มีสิทธิ์ในการใช้คำสั่งนี้", ephemeral=True)

    #groupwork
    @bot.tree.command(description='Create groupwork | สร้างกลุ่มงาน')
    @have_permission()
    @app_commands.describe(topic='หัวข้อ', descriptions='รายละเอียดเพิ่มเติม', member_amount='จำนวนสมาชิก')
    async def groupwork(interaction: discord.Interaction, topic: str, descriptions: str, member_amount: int):
        # print(interaction.user.display_name)

        FEEDBACK_CH = db.check_feedback_ch("group", interaction.guild_id) #ไอดีแชลแนลที่ต้องการให้ตอบสนอง
        await feedback(interaction, FEEDBACK_CH)

        initial_member = [interaction.user.display_name]
        view = GroupworkView(topic, descriptions, member_amount, initial_member)
        await interaction.response.send_message(embed=view.embed, view=view)

    @groupwork.error
    async def groupwork_error(interaction: discord.Interaction, error):
        await interaction.response.send_message("คุณไม่มีสิทธิ์ในการใช้คำสั่งนี้", ephemeral=True)
    

    #random
    @bot.tree.command(description='Random | การสุ่ม')
    @have_permission()
    @app_commands.describe(entries='Options to randomize using spaces as separators. | สิ่งที่ต้องการสุ่ม โดยใช้ช่องว่างเป็นตัวคั่น')
    async def randoms(interaction: discord.Interaction, entries: str):

        FEEDBACK_CH = db.check_feedback_ch("random", interaction.guild_id) #ไอดีแชลแนลที่ต้องการให้ตอบสนอง
        await feedback(interaction, FEEDBACK_CH)

        entries_list = entries.split(' ')
        random_result = random.choice(entries_list)
        await interaction.response.send_message(f'🎉 ผลลัพธ์ที่ได้คือ **{random_result}** 🎉')
    
    @randoms.error
    async def randoms_error(interaction: discord.Interaction, error):
        await interaction.response.send_message("คุณไม่มีสิทธิ์ในการใช้คำสั่งนี้", ephemeral=True)

    #poll
    @bot.tree.command(name="poll", description="Create a poll (max 5 options) | สร้างโพลล์ (มากสุด 5 ตัวเลือก)")
    @have_permission()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(question="คุณต้องการจะถามอะไร", option1="ตัวเลือกที่ 1", option2="ตัวเลือกที่ 2", option3="ตัวเลือกที่ 3", option4="ตัวเลือกที่ 4",option5="ตัวเลือกที่ 5", role="mention (role) | คุณจะกล่าวสิ่งนี้กับใคร (บทบาท)")
    async def poll(interaction: discord.Interaction, question: str, option1: str, option2: str, option3:str=None, option4:str=None, option5:str=None, role:discord.Role=None):

        FEEDBACK_CH = db.check_feedback_ch("poll", interaction.guild_id) #ไอดีแชลแนลที่ต้องการให้ตอบสนอง
        await feedback(interaction, FEEDBACK_CH)

        await interaction.response.send_message("⌛ กำลังสร้างโพลล์...", ephemeral=True)
        try:
            listen = [option1, option2, option3, option4, option5]
            yonice = []
            for i in listen:
                if i != None:
                    yonice.append(i)
            if role == None:
                if len(yonice) == 2:
                    emb=discord.Embed(color=discord.Colour.random(), title=f"📃 {question} 📃", description=f"1️⃣ : {yonice[0]}\n2️⃣ : {yonice[1]}")
                    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/1206514380645208104/1206514623445205012/poll.png?ex=65dc494e&is=65c9d44e&hm=1004d12afdc3d8e5604a1de864a78c43ee57eea693cb657e3f2de5c63cb1cc2e&')
                    msg=await interaction.channel.send(embed=emb)
                    await msg.add_reaction("1️⃣")
                    await msg.add_reaction("2️⃣")
                elif len(yonice) == 3:
                    emb=discord.Embed(color=discord.Colour.random(), title=f"📃 {question} 📃", description=f"1️⃣ : {yonice[0]}\n2️⃣ : {yonice[1]}\n3️⃣ : {yonice[2]}")
                    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/1206514380645208104/1206514623445205012/poll.png?ex=65dc494e&is=65c9d44e&hm=1004d12afdc3d8e5604a1de864a78c43ee57eea693cb657e3f2de5c63cb1cc2e&')
                    msg=await interaction.channel.send(embed=emb)
                    await msg.add_reaction("1️⃣")
                    await msg.add_reaction("2️⃣") 
                    await msg.add_reaction("3️⃣")
                elif len(yonice) == 4:
                    emb=discord.Embed(color=discord.Colour.random(), title=f"📃 {question} 📃", description=f"1️⃣ : {yonice[0]}\n2️⃣ : {yonice[1]}\n3️⃣ : {yonice[2]}\n4️⃣ : {yonice[3]}")
                    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/1206514380645208104/1206514623445205012/poll.png?ex=65dc494e&is=65c9d44e&hm=1004d12afdc3d8e5604a1de864a78c43ee57eea693cb657e3f2de5c63cb1cc2e&')
                    msg=await interaction.channel.send(embed=emb)
                    await msg.add_reaction("1️⃣")
                    await msg.add_reaction("2️⃣") 
                    await msg.add_reaction("3️⃣")
                    await msg.add_reaction("4️⃣")
                elif len(yonice) == 5:
                    emb=discord.Embed(color=discord.Colour.random(), title=f"📃 {question} 📃", description=f"1️⃣ : {yonice[0]}\n2️⃣ : {yonice[1]}\n3️⃣ : {yonice[2]}\n4️⃣ : {yonice[3]}\n5️⃣ : {yonice[4]}")
                    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/1206514380645208104/1206514623445205012/poll.png?ex=65dc494e&is=65c9d44e&hm=1004d12afdc3d8e5604a1de864a78c43ee57eea693cb657e3f2de5c63cb1cc2e&')
                    msg=await interaction.channel.send(embed=emb)
                    await msg.add_reaction("1️⃣")
                    await msg.add_reaction("2️⃣") 
                    await msg.add_reaction("3️⃣")
                    await msg.add_reaction("4️⃣")
                    await msg.add_reaction("5️⃣")    
            else:
                if len(yonice) == 2 :
                    emb=discord.Embed(color=discord.Colour.random(), title=f"📃 {question} 📃", description=f"1️⃣ : {yonice[0]}\n2️⃣ : {yonice[1]}")
                    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/1206514380645208104/1206514623445205012/poll.png?ex=65dc494e&is=65c9d44e&hm=1004d12afdc3d8e5604a1de864a78c43ee57eea693cb657e3f2de5c63cb1cc2e&')
                    msg=await interaction.channel.send(f"{role.mention}", embed=emb)
                    await msg.add_reaction("1️⃣")
                    await msg.add_reaction("2️⃣") 
                    
                elif len(yonice) == 3 :
                    emb=discord.Embed(color=discord.Colour.random(), title=f"📃 {question} 📃", description=f"1️⃣ : {yonice[0]}\n2️⃣ : {yonice[1]}\n3️⃣ : {yonice[2]}")
                    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/1206514380645208104/1206514623445205012/poll.png?ex=65dc494e&is=65c9d44e&hm=1004d12afdc3d8e5604a1de864a78c43ee57eea693cb657e3f2de5c63cb1cc2e&')
                    msg=await interaction.channel.send(f"{role.mention}", embed=emb)
                    await msg.add_reaction("1️⃣")
                    await msg.add_reaction("2️⃣") 
                    await msg.add_reaction("3️⃣")
                    
                elif len(yonice) == 4:
                    emb=discord.Embed(color=discord.Colour.random(), title=f"📃 {question} 📃", description=f"1️⃣ : {yonice[0]}\n2️⃣ : {yonice[1]}\n3️⃣ : {yonice[2]}\n4️⃣ : {yonice[3]}")
                    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/1206514380645208104/1206514623445205012/poll.png?ex=65dc494e&is=65c9d44e&hm=1004d12afdc3d8e5604a1de864a78c43ee57eea693cb657e3f2de5c63cb1cc2e&')
                    msg=await interaction.channel.send(f"{role.mention}", embed=emb)
                    await msg.add_reaction("1️⃣")
                    await msg.add_reaction("2️⃣") 
                    await msg.add_reaction("3️⃣")
                    await msg.add_reaction("4️⃣")

                elif len(yonice) == 5:
                    emb=discord.Embed(color=discord.Colour.random(), title=f"📃 {question} 📃", description=f"1️⃣ : {yonice[0]}\n2️⃣ : {yonice[1]}\n3️⃣ : {yonice[2]}\n4️⃣ : {yonice[3]}\n5️⃣ : {yonice[4]}")
                    emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/1206514380645208104/1206514623445205012/poll.png?ex=65dc494e&is=65c9d44e&hm=1004d12afdc3d8e5604a1de864a78c43ee57eea693cb657e3f2de5c63cb1cc2e&')
                    msg=await interaction.channel.send(f"{role.mention}", embed=emb)
                    await msg.add_reaction("1️⃣")
                    await msg.add_reaction("2️⃣") 
                    await msg.add_reaction("3️⃣")
                    await msg.add_reaction("4️⃣")
                    await msg.add_reaction("5️⃣")
        
            await interaction.delete_original_response()
        except Exception as e:
            print(e)
            await interaction.delete_original_response()
            await interaction.followup.send("An error occured, try again later.", ephemeral=True)

    @poll.error
    async def poll_error(interaction: discord.Interaction, error):
        await interaction.response.send_message("คุณไม่มีสิทธิ์ในการใช้คำสั่งนี้", ephemeral=True)

   
    #delete commands unused
    @bot.command(name='deletecommands', aliases=['clear'])
    async def delete_commands(ctx):
        bot.tree.clear_commands(guild=None)
        await bot.tree.sync()
        await ctx.send('Unused Commands deleted.')  

    
    

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)#ทำงานด้วยโทเคน

if __name__=="__main__":
    run()