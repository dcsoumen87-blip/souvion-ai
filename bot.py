import os
import json
import discord
from discord.ext import commands
from google import genai
from google.genai import types

# =========================
# CONFIG
# =========================

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEV_USER_ID = int(os.getenv("DEV_USER_ID", "0"))

if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing")

# Gemini client
ai = genai.Client(api_key=GEMINI_API_KEY)

# =========================
# DISCORD
# =========================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

# =========================
# KNOWLEDGE BASE
# =========================

KNOWLEDGE_FILE = "knowledge.json"


def load_knowledge():
    if not os.path.exists(KNOWLEDGE_FILE):
        return {}

    try:
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_knowledge(data):
    with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


knowledge = load_knowledge()


# =========================
# AI SYSTEM PROMPT
# =========================

def build_prompt(user_question):

    knowledge_text = ""

    if knowledge:
        knowledge_text = "\n\nSERVER KNOWLEDGE:\n"

        for key, value in knowledge.items():
            knowledge_text += f"\n[{key}]\n{value}\n"

    return f"""
You are Souvion AI, an AI assistant for a Discord server.

Developer:
Name: Soumen

IMPORTANT RULES:

1. Be helpful, friendly and natural.
2. Answer general questions like a normal AI assistant.
3. You can communicate in Bengali, English and Hinglish.
4. For Discord server-related questions, use the SERVER KNOWLEDGE below.
5. Never invent server-specific information.
6. If server information is unavailable, clearly say that you do not have that information.
7. Never reveal API keys, Discord tokens or internal configuration.
8. Do not claim that you remember previous conversations.
9. If someone asks who developed you, answer:
   "I was developed by Soumen."

{knowledge_text}

USER QUESTION:
{user_question}
"""


# =========================
# EVENTS
# =========================

@bot.event
async def on_ready():
    print("=" * 40)
    print(f"Logged in as: {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print("Souvion AI is online!")
    print("=" * 40)


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    # Process developer commands
    await bot.process_commands(message)

    # Only respond when mentioned
    if bot.user not in message.mentions:
        return

    question = message.content

    # Remove bot mention
    question = question.replace(
        f"<@{bot.user.id}>", ""
    ).replace(
        f"<@!{bot.user.id}>", ""
    ).strip()

    if not question:
        await message.reply(
            "Please ask me something!"
        )
        return

    try:

        async with message.channel.typing():

            response = ai.models.generate_content(
                model="gemini-2.5-flash",
                contents=build_prompt(question),
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=800
                )
            )

        answer = response.text.strip()

        if not answer:
            answer = "Sorry, I could not generate a response."

        # Discord message limit protection
        if len(answer) > 1900:
            answer = answer[:1900] + "..."

        await message.reply(answer)

    except Exception as e:

        print("AI ERROR:", repr(e))

        await message.reply(
            "⚠️ There was a problem generating the AI response. Please try again later."
        )


# =========================
# DEVELOPER CHECK
# =========================

def is_dev(ctx):

    return ctx.author.id == DEV_USER_ID


# =========================
# DEVELOPER COMMANDS
# =========================

@bot.command(name="devstatus")
async def devstatus(ctx):

    if not is_dev(ctx):
        return

    await ctx.send(
        "👑 **Souvion AI Developer Panel**\n"
        f"Bot: `{bot.user}`\n"
        f"Knowledge Entries: `{len(knowledge)}`\n"
        "Status: `ONLINE`"
    )


@bot.command(name="aiadd")
async def aiadd(ctx, key: str, *, value: str):

    if not is_dev(ctx):
        return

    knowledge[key.lower()] = value
    save_knowledge(knowledge)

    await ctx.send(
        f"✅ Knowledge added:\n"
        f"**{key}** → {value}"
    )


@bot.command(name="aiupdate")
async def aiupdate(ctx, key: str, *, value: str):

    if not is_dev(ctx):
        return

    key = key.lower()

    if key not in knowledge:
        await ctx.send(
            f"❌ No knowledge entry found with the name `{key}`."
        )
        return

    knowledge[key] = value
    save_knowledge(knowledge)

    await ctx.send(
        f"✅ Knowledge updated: `{key}`"
    )


@bot.command(name="aidelete")
async def aidelete(ctx, key: str):

    if not is_dev(ctx):
        return

    key = key.lower()

    if key not in knowledge:
        await ctx.send(
            f"❌ No knowledge entry found with the name `{key}`."
        )
        return

    del knowledge[key]
    save_knowledge(knowledge)

    await ctx.send(
        f"🗑️ Knowledge deleted: `{key}`"
    )


@bot.command(name="ailist")
async def ailist(ctx):

    if not is_dev(ctx):
        return

    if not knowledge:
        await ctx.send(
            "📚 The Knowledge Base is currently empty."
        )
        return

    entries = "\n".join(
        f"• `{key}`"
        for key in knowledge
    )

    await ctx.send(
        f"📚 **Knowledge Base**\n\n{entries}"
    )


@bot.command(name="aiclear")
async def aiclear(ctx):

    if not is_dev(ctx):
        return

    knowledge.clear()
    save_knowledge(knowledge)

    await ctx.send(
        "🗑️ The entire Knowledge Base has been cleared."
    )


# =========================
# RUN
# =========================

bot.run(DISCORD_TOKEN)
