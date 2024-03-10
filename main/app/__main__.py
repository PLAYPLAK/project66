from app import app, bottest
from config1 import CLIENT_SECRET, TOKEN, OAUTH_URL, REDIRECT_URL

if __name__ == "__main__":
    bottest.run(TOKEN)
    app.run(debug=True, port=5000)