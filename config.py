import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DEV_USER_ID = int(os.getenv("DEV_USER_ID", "0"))

BOT_PREFIX = "!"
