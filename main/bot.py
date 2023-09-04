import discord
import json
import re
from discord.ext import commands
from datetime import datetime

# กำหนดค่า Token ที่คุณคัดลอกมาจาก Developer Portal
TOKEN = 'MTEzNjU5MTEzNDk3NDU1NDE5Mw.GQy8Zs.ZEZC8dKWJQ0GkE5DGO1bYBDAEpZVcI--T1iETg'

# สร้างบอทเป็น Client ของ discord.py
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

#Load json data
def load_json(file):
    with open(file, encoding='utf-8') as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)


# Store JSON data
response_data = load_json("bot.json")

#Respone data
def get_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    
    print(split_message)

    score_list = []

    # Check all the responses
    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        # Check if there are any required words
        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        # Amount of required words should match the required score
        if required_score == len(required_words):
            # print(required_score == len(required_words))
            # Check each word the user has typed
            for word in split_message:
                # If the word is in the response, add to the score
                if word in response["user_input"]:
                    response_score += 1

        # Add score to list
        score_list.append(response_score)
        # Debugging: Find the best phrase
        # print(response_score, response["user_input"])

    # Find the best response and return it if they're not all 0
    best_response = max(score_list)
    response_index = score_list.index(best_response)

    if input_string == "":
        return "Please type something so we can chat :("

    # If there is no good response, return a random one.
    if best_response != 0:
        return response_data[response_index]["bot_response"]

# เหตุการณ์เมื่อบอทเรียกพร้อมใช้งาน
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    # ตั้งค่าสถานะของบอท
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="เกมส์"))


# คำสั่ง !hello ที่บอทจะตอบกลับ
@bot.command()
async def test(ctx):
    await ctx.send('Hello, I am your Discord bot!')


@bot.command()
async def checkid(ctx):
    await ctx.send(f'your ID is : {ctx.author.id}')


@bot.command()
async def avatar(ctx):
    await ctx.send(f'{ctx.author.avatar}')


@bot.command()
async def profile(ctx):

    embed = discord.Embed(
        title=f"{ctx.author.display_name}",
        description=f"AKA : {ctx.author.name}",
        color=discord.Color.green()
    )
    embed.add_field(
        name='Name',
        value=f'{ctx.author.name}'
    )
    embed.add_field(
        name='Student ID',
        value='64015087'
    )
    embed.set_thumbnail(url=f'{ctx.author.avatar}')

    await ctx.send(embed=embed)


@bot.command()
async def add(ctx, a: int, b: int):
    result = a + b
    await ctx.send(f"The result of {a} + {b} is {result}")


@bot.command()
async def dev(ctx):
    devs = [
        {'FirstName': 'Piyarot', 'LastName': 'Khantichat', 'Student ID': '64015087', 'Color': discord.Color.green(
        ), 'ThumbnailURL': 'https://img.freepik.com/premium-photo/japanese-girl-cherry-blossom-tree-landscape-anime-manga-illustration_691560-7776.jpg?w=2000'},
        {'FirstName': 'John', 'LastName': 'Doe', 'Student ID': '12345678',
            'Color': discord.Color.blue(), 'ThumbnailURL': 'https://example.com/john.jpg'},
        {'FirstName': 'Jane', 'LastName': 'Smith', 'Student ID': '87654321',
            'Color': discord.Color.orange(), 'ThumbnailURL': 'https://example.com/jane.jpg'}
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



# ตอบกลับข้อความ


@bot.event
async def on_message(message):
    if message.author == bot.user:  # ไม่ตอบกลับถ้าข้อความเป็นของบอทเอง
        return

    else:
        text = get_response(message.content)
        
        await message.channel.send(f'{message.author.mention} {text}')

    await bot.process_commands(message)


# รันบอทด้วย Token
bot.run(TOKEN)
