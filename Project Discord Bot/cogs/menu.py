import discord
import random
from datetime import datetime
from discord.ext import commands 


class Menu(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def sub(self, ctx,a:int,b:int):
        await ctx.send(a-b)

    @commands.command(aliases=['เช็คไอดี','ไอดี'])
    async def checkid(self, ctx):
        await ctx.send(f'your ID is : {ctx.author.id}')

    @commands.command()
    async def avatar(self, ctx):
        await ctx.send(f'{ctx.author.avatar}')


    @commands.command(aliases=['random','สุ่ม'])
    async def choices(self, ctx, *options):
        await ctx.send(random.choice(options))


    @commands.command(aliases=['โปรไฟล์','โปร'])
    async def profile(self, ctx, who : discord.Member):

        embed = discord.Embed(
            title=f"{who.display_name}",
            description=f"AKA : {who.name}",
            color=discord.Color.green()
        )
        embed.add_field(
            name='Name',
            value=f'{who.name}'
        )
        embed.add_field(
            name='Student ID',
            value='64015087'
        )
        embed.set_thumbnail(url=f'{who.avatar}')

        await ctx.send(embed=embed)

    @commands.command(aliases=['developers'])
    async def dev(self, ctx):
        devs = [
            {'FirstName': 'Piyarot', 'LastName': 'Khantichat', 'Student ID': '64015087', 
                'Color': discord.Color.green(), 'ThumbnailURL': 'https://www.ce.kmitl.ac.th/api/profile/download/64015087'},
            {'FirstName': 'Saran', 'LastName': 'Kantad', 'Student ID': '64015134',
                'Color': discord.Color.blue(), 'ThumbnailURL': 'https://www.ce.kmitl.ac.th/api/profile/download/64015134'},
            {'FirstName': 'Parinya', 'LastName': 'Donpradu', 'Student ID': '64015082',
                'Color': discord.Color.orange(), 'ThumbnailURL': 'https://www.ce.kmitl.ac.th/api/profile/download/64015082'}
        ]

        for dev_info in devs:
            current_time = datetime.now().strftime('%H:%M น. %d/%m/%Y')

            embed = discord.Embed(
                title="Developer",
                description="",
                color=dev_info['Color']
            )

            name_field = f"{dev_info['FirstName']} {dev_info['LastName']}"
            embed.add_field(name='Name', value=name_field)

            student_id_field = f"\n{dev_info['Student ID']}"
            embed.add_field(name='Student ID', value=student_id_field)

            embed.set_thumbnail(url=dev_info['ThumbnailURL'])
            embed.set_footer(
                text=current_time, icon_url='https://encrypted-tbn2.gstatic.com/faviconV2?url=https://freepik.com&client=VFE&size=64&type=FAVICON&fallback_opts=TYPE,SIZE,URL&nfrp=2')

            await ctx.send(embed=embed)

    @commands.command()
    async def joined(self, ctx, who : discord.Member ):
        await ctx.send(who)
        
async def setup(bot):
    await bot.add_cog(Menu(bot))