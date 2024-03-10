from threading import Thread
import asyncio
from flask import Flask, render_template, request, session, redirect, url_for
from zenora import APIClient
from config1 import CLIENT_SECRET, TOKEN, OAUTH_URL, REDIRECT_URL
import discord 
from discord.ext import commands
from database import Database
# from bottest import bot, get_bot_guilds

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


app = Flask(__name__)
app.config["SECRET_KEY"] = "verysecret"
client = APIClient(TOKEN, client_secret=CLIENT_SECRET)
db = Database()


def bearer_client():
        if 'token' in session :
            bearer_client = APIClient(session.get('token'), bearer=True)
            current_user = bearer_client.users.get_current_user()
            print(db.check_admin(str(current_user.id)))
            if db.check_admin(str(current_user.id)) == False:
                db.add_admin(str(current_user.id), str(current_user.username))
        return current_user

@app.route("/")
def home():
    if 'token' in session :
        guild_client = APIClient(session.get('token'), bearer=True)
        guilds = guild_client.users.get_my_guilds()
        guilds_member = []
        user = bearer_client()
        for check_guild in guilds:
            for guild in bot.guilds:
            # for guild in current_guilds:   
                if check_guild.id == guild.id :
                    print(f'Bot is a member of {guild.name} (ID: {guild.id})')
                    if db.check_guild(str(check_guild.id)) == False:
                        db.add_guild(str(check_guild.id), str(user.id))
                    guilds_member.append(check_guild)

                       
        return render_template("index2.html", current_user=bearer_client(), guilds=guilds_member, oauth_url=OAUTH_URL)
    
    return render_template("index2.html", oauth_url=OAUTH_URL)

@app.route("/oauth/callback")
def callback():
    code = request.args['code']
    access_token = client.oauth.get_access_token(code, REDIRECT_URL).access_token
    session['token'] = access_token
    return redirect("/")


@app.route("/manage/<int:guildID>/setting")
def manage_guild(guildID):
    if 'token' in session :
        guild_client = APIClient(session.get('token'), bearer=True)
        guilds = guild_client.users.get_my_guilds()
        text_alert = db.check_alert_gui(guildID)
        current_guild = []
        channels = []

        for check_guild in guilds:
            for guild in bot.guilds:    
                print(f'Bot is a member of {guild.name} (ID: {guild.id})')
                if check_guild.id == guild.id == guildID:
                    current_guild.append(check_guild)
                    for role in guild.roles:
                        print(f"Rolename : {role.name} ID : {role.id}")

        for guild in bot.guilds:
            if guild.id == guildID:
                for channel in guild.channels:
                    print(f"{channel.name} and {channel.type}")
                    if str(channel.type) == "text":
                        channels.append(channel)


        return render_template("manage-bot2.html", current_user=bearer_client(), current_guild=current_guild, channels=channels, text_alert=text_alert)
    return redirect("/")

@app.route("/manage/<int:guildID>/response")
def manage_response(guildID):
    if 'token' in session :
        guild_client = APIClient(session.get('token'), bearer=True)
        guilds = guild_client.users.get_my_guilds()

        qa_setting = db.check_feedback_ch("qa", guildID)
        word, ans, type_ans, resIDs = db.check_question_ans(guildID)
        data = zip(word, ans, type_ans, resIDs)

        if qa_setting == []:
            qa_setting.append(0)

        current_guild = []
        channels = []
        for check_guild in guilds:
            for guild in bot.guilds:
                print(f'Bot is a member of {guild.name} (ID: {guild.id})')
                if check_guild.id == guild.id == guildID:
                    current_guild.append(check_guild)

        for guild in bot.guilds:
            if guild.id == guildID:
                for channel in guild.channels:
                    print(f"{channel.name} and {channel.type}")
                    if str(channel.type) == "text":
                        channels.append(channel)

        return render_template("manage-response2.html", current_user=bearer_client(), current_guild=current_guild, qa_settings=qa_setting, channels=channels,datas =data)
    return redirect("/")

@app.route("/manage/<int:guildID>/function")
def manage_function(guildID):
    if 'token' in session :
        guild_client = APIClient(session.get('token'), bearer=True)
        guilds = guild_client.users.get_my_guilds()
        current_guild = []
        channels = []
        roles = []
        register_setting = db.check_feedback_ch("register", guildID)
        profile_setting = db.check_feedback_ch("profile", guildID)
        plan_edit_setting = db.check_feedback_ch("plan-edit", guildID)
        plan_view_setting = db.check_feedback_ch("plan-view", guildID)
        groupwork_setting = db.check_feedback_ch("group", guildID)
        randoms_setting = db.check_feedback_ch("random", guildID)
        poll_setting = db.check_feedback_ch("poll", guildID)

        if register_setting == [] :
            register_setting.append(0)
        if profile_setting == [] :
            profile_setting.append(0)
        if plan_edit_setting == [] :
            plan_edit_setting.append(0)
        if plan_view_setting == [] :
            plan_view_setting.append(0)
        if groupwork_setting == [] :
            groupwork_setting.append(0)
        if randoms_setting == [] :
            randoms_setting.append(0)
        if poll_setting == []:
            poll_setting.append(0)

        print(f"resigter = {register_setting}")
        print(f"pofile   = {profile_setting}")
        print(f"plan     = {plan_edit_setting}")
        print(f"view     = {plan_view_setting}")         
        print(f"group    = {groupwork_setting}")
        print(f"random   = {randoms_setting}")
        print(f"poll     = {poll_setting}")

        for check_guild in guilds:
            for guild in bot.guilds:
                print(f'Bot is a member of {guild.name} (ID: {guild.id})')
                if check_guild.id == guild.id == guildID:
                    current_guild.append(check_guild)
                    for role in guild.roles:
                        roles.append(role)
                        # print(f"Rolename : {role.name} ID : {role.id}")

        for guild in bot.guilds:
            if guild.id == guildID:
                for channel in guild.channels:
                    if str(channel.type) == "text":
                        channels.append(channel)


        return render_template("manage-func2.html", current_user=bearer_client(), current_guild=current_guild, channels=channels, registers=register_setting,profiles=profile_setting, plan_edits=plan_edit_setting, plan_views=plan_view_setting, groups=groupwork_setting, randoms=randoms_setting, polls=poll_setting, roles=roles)

    return redirect("/")

# submit
@app.route("/submit-func_ch/<int:guildID>", methods=['POST'])
def submit_function(guildID):
    register = request.form['register']
    profile = request.form['profile']
    plan = request.form['study_plan_edit']
    view = request.form['study_plan_view']
    group = request.form['groupwork']
    ranbom = request.form['randoms']
    poll = request.form['poll']
    register_channels = request.form.getlist('register_channels')
    profile_channels = request.form.getlist('profile_channels')
    plan_channels = request.form.getlist('plan_edit_channels')
    view_plan_channels = request.form.getlist('plan_view_channels')
    group_channels = request.form.getlist('groupwork_channels')
    random_channels = request.form.getlist('randoms_channels')
    poll_channels = request.form.getlist('poll_channels')
    role_setting = request.form['role']


    if register == "1":
        register_channels = []
    if profile == "1" :
        profile_channels = []
    if plan == "1" :
        plan_channels = []
    if view == "1" :
        view_plan_channels = []
    if group == "1" :
        group_channels = []
    if ranbom == "1" :
        random_channels = []
    if poll == "1" :
        poll_channels = []
    # FuncName, channel_reply, GuildID
    print(role_setting)
    db.insert_feedback_ch("register", str(register_channels), guildID, role_setting)
    db.insert_feedback_ch("profile", str(profile_channels), guildID, role_setting)
    db.insert_feedback_ch("plan-edit", str(plan_channels), guildID, role_setting)
    db.insert_feedback_ch("plan-view", str(view_plan_channels), guildID, role_setting)
    db.insert_feedback_ch("group", str(group_channels), guildID, role_setting)
    db.insert_feedback_ch("random", str(random_channels), guildID, role_setting)
    db.insert_feedback_ch("poll", str(poll_channels), guildID, role_setting)

    print(f"register\n{register_channels}")
    print(f"profile\n{profile_channels}")
    print(f"plan eidt\n{plan_channels}")
    print(f"plan view\n{view_plan_channels}")
    print(f"group\n{group_channels}")
    print(f"random\n{random_channels}")
    print(f"poll\n{poll_channels}")

    target_url = url_for('manage_function', guildID=guildID)
    return redirect(target_url)
    # return redirect(f"/manage/{guildID}/function")

@app.route("/submit-alert/<int:guildID>", methods=['POST'])
def submit_alert(guildID):
    userId = bearer_client()
    userId = userId.id
    text_alert = request.form['text-alert']
    
    print(type(text_alert))
    db.insert_alert_gui(guildID, str(text_alert), str(userId))
    
    target_url = url_for('manage_guild', guildID=guildID)
    return redirect(target_url)
    # return render_template("test.html", current_user=bearer_client())

@app.route("/submit-response/<int:guildID>", methods=['POST'])
def submit_response(guildID):
    qa_channels = request.form.getlist('qa_channels')
    word = request.form['word']
    ans = request.form['answer']
    type_ans = request.form['type_ans']
    qa = request.form['qa']

    if qa == "1" :
        qa_channels = []
        
    print(f"channel = {qa_channels}")
    print(f"word    = {word}")
    print(f"ans     = {ans}")
    print(f"type    = {type_ans}")
    db.insert_feedback_ch("qa", str(qa_channels), guildID, "0")
    db.question_ans(word, ans, guildID, type_ans)


    target_url = url_for('manage_response', guildID=guildID)
    return redirect(target_url)
    # return render_template("test.html", current_user=bearer_client())

@app.route("/submit-delete/<int:guildID>", methods=['POST'])
def submit_delete(guildID):
    resID = request.form['res-item']

    print(f" Res: {resID}")
    db.delete_question(resID)

    target_url = url_for('manage_response', guildID=guildID)
    return redirect(target_url)
    # return render_template("test.html", current_user=bearer_client())

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')


# function run flask with separate Thread
def flask_thread(func):
    thread = Thread(target=func)
    print('Start Separate Thread From Bot')
    thread.start()    

def run():
    app.run(port=5001, use_reloader=False, debug=True)


if __name__ == '__main__':
    flask_thread(func=run)
    bot.run(TOKEN)



