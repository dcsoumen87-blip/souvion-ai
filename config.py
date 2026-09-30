import os


# ==============================
# DISCORD
# ==============================

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


# ==============================
# AI PROVIDERS
# ==============================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# ==============================
# DEVELOPER
# ==============================

DEV_USER_ID = int(
    os.getenv("DEV_USER_ID", "0")
)


# ==============================
# BOT
# ==============================

BOT_PREFIX = "!"


# ==============================
# GITHUB STORAGE
# ==============================

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

GITHUB_REPO = os.getenv(
    "GITHUB_REPO"
)

GITHUB_BRANCH = os.getenv(
    "GITHUB_BRANCH",
    "main"
)

GITHUB_KNOWLEDGE_PATH = os.getenv(
    "GITHUB_KNOWLEDGE_PATH",
    "data/knowledge.json"
)
