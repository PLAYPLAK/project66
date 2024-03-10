from urllib import parse

TOKEN = "Your Bot Token"
CLIENT_SECRET = "Your Client Secret"
CLIENT_ID = "Your Client ID"
REDIRECT_URL = "http://localhost:5001/oauth/callback"
OAUTH_URL = f"https://discord.com/api/oauth2/authorize?client_id=123456789&response_type=code&redirect_uri={parse.quote(REDIRECT_URL)}&scope=identify+guilds+email+connections+guilds.members.read+guilds.join+gdm.join"

