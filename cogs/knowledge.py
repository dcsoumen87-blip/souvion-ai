import os
import json
import discord
from discord.ext import commands

from config import DEV_USER_ID


# ==========================================
# KNOWLEDGE CONFIGURATION
# ==========================================

DATA_DIR = "data"
KNOWLEDGE_FILE = os.path.join(
    DATA_DIR,
    "knowledge.json"
)


# ==========================================
# KNOWLEDGE MANAGER
# ==========================================

def ensure_data_file():

    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(KNOWLEDGE_FILE):

        with open(
            KNOWLEDGE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                {},
                file,
                indent=4,
                ensure_ascii=False
            )


def load_knowledge():

    ensure_data_file()

    try:

        with open(
            KNOWLEDGE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, dict):
                return data

            return {}

    except Exception as error:

        print("[KNOWLEDGE] Load error:", error)

        return {}


def save_knowledge(data):

    ensure_data_file()

    try:

        with open(
            KNOWLEDGE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except Exception as error:

        print("[KNOWLEDGE] Save error:", error)

        return False


knowledge = load_knowledge()


# ==========================================
# SERVER KNOWLEDGE
# ==========================================

def get_guild_knowledge(guild_id):

    guild_id = str(guild_id)

    if guild_id not in knowledge:

        knowledge[guild_id] = {}

    return knowledge[guild_id]


# ==========================================
# AI KNOWLEDGE TEXT
# ==========================================

def get_knowledge_text(guild_id=None):

    if guild_id is None:

        return "No server knowledge is available."

    guild_id = str(guild_id)

    guild_data = knowledge.get(
        guild_id,
        {}
    )

    if not guild_data:

        return "No server-specific knowledge is available."

    lines = []

    for key, value in guild_data.items():

        lines.append(
            f"[{key}]\n{value}"
        )

    return "\n\n".join(lines)


# ==========================================
# DEVELOPER CHECK
# ==========================================

def is_developer(ctx):

    return (
        ctx.author.id == DEV_USER_ID
    )


# ==========================================
# KNOWLEDGE COG
# ==========================================

class KnowledgeCog(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    # ======================================
    # ADD KNOWLEDGE
    # ======================================

    @commands.command(name="aiadd")
    async def aiadd(
        self,
        ctx,
        key: str,
        *,
        value: str
    ):

        if not is_developer(ctx):
            return

        if ctx.guild is None:

            await ctx.send(
                "❌ This command can only be used inside a server."
            )

            return

        guild_data = get_guild_knowledge(
            ctx.guild.id
        )

        key = key.lower().strip()

        if key in guild_data:

            await ctx.send(
                f"❌ `{key}` already exists.\n"
                f"Use `!aiupdate {key} <information>` to update it."
            )

            return

        guild_data[key] = value

        if not save_knowledge(knowledge):

            await ctx.send(
                "❌ Failed to save the knowledge."
            )

            return

        await ctx.send(
            f"✅ **Knowledge Added**\n\n"
            f"**Key:** `{key}`\n"
            f"**Information:** {value}"
        )

    # ======================================
    # UPDATE KNOWLEDGE
    # ======================================

    @commands.command(name="aiupdate")
    async def aiupdate(
        self,
        ctx,
        key: str,
        *,
        value: str
    ):

        if not is_developer(ctx):
            return

        if ctx.guild is None:

            await ctx.send(
                "❌ This command can only be used inside a server."
            )

            return

        guild_data = get_guild_knowledge(
            ctx.guild.id
        )

        key = key.lower().strip()

        if key not in guild_data:

            await ctx.send(
                f"❌ Knowledge `{key}` does not exist.\n"
                f"Use `!aiadd {key} <information>` to create it."
            )

            return

        guild_data[key] = value

        if not save_knowledge(knowledge):

            await ctx.send(
                "❌ Failed to save the knowledge."
            )

            return

        await ctx.send(
            f"✅ **Knowledge Updated**\n\n"
            f"**Key:** `{key}`\n"
            f"**Information:** {value}"
        )

    # ======================================
    # DELETE KNOWLEDGE
    # ======================================

    @commands.command(name="aidelete")
    async def aidelete(
        self,
        ctx,
        key: str
    ):

        if not is_developer(ctx):
            return

        if ctx.guild is None:

            await ctx.send(
                "❌ This command can only be used inside a server."
            )

            return

        guild_data = get_guild_knowledge(
            ctx.guild.id
        )

        key = key.lower().strip()

        if key not in guild_data:

            await ctx.send(
                f"❌ Knowledge `{key}` was not found."
            )

            return

        del guild_data[key]

        if not save_knowledge(knowledge):

            await ctx.send(
                "❌ Failed to save the
