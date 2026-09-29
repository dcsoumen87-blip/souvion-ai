import os
import json
import discord
from discord.ext import commands

from config import DEV_USER_ID, BOT_PREFIX


# ==========================================
# DATA CONFIGURATION
# ==========================================

DATA_DIR = "data"

KNOWLEDGE_FILE = os.path.join(
    DATA_DIR,
    "knowledge.json"
)


# ==========================================
# FILE MANAGEMENT
# ==========================================

def ensure_data_file():

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    if not os.path.exists(KNOWLEDGE_FILE):

        with open(
            KNOWLEDGE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                {
                    "_global": {},
                    "_prefixes": {}
                },
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

            if not isinstance(data, dict):
                return {
                    "_global": {},
                    "_prefixes": {}
                }

            if "_global" not in data:
                data["_global"] = {}

            if "_prefixes" not in data:
                data["_prefixes"] = {}

            return data

    except Exception as error:

        print("[KNOWLEDGE] Load error:", error)

        return {
            "_global": {},
            "_prefixes": {}
        }


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
# PREFIX SYSTEM
# ==========================================

def get_server_prefix(guild_id):

    guild_id = str(guild_id)

    prefix = knowledge.get(
        "_prefixes",
        {}
    ).get(
        guild_id
    )

    if not prefix:
        return BOT_PREFIX

    return prefix


def set_server_prefix(guild_id, prefix):

    guild_id = str(guild_id)

    if "_prefixes" not in knowledge:
        knowledge["_prefixes"] = {}

    knowledge["_prefixes"][guild_id] = prefix

    return save_knowledge(knowledge)


# ==========================================
# GLOBAL KNOWLEDGE
# ==========================================

def get_global_knowledge():

    return knowledge.get(
        "_global",
        {}
    )


def get_global_knowledge_text():

    global_data = get_global_knowledge()

    if not global_data:

        return "No global knowledge is available."

    lines = []

    for key, value in global_data.items():

        lines.append(
            f"[{key}]\n{value}"
        )

    return "\n\n".join(lines)


# ==========================================
# SERVER KNOWLEDGE
# ==========================================

def get_guild_knowledge(guild_id):

    guild_id = str(guild_id)

    if guild_id not in knowledge:

        knowledge[guild_id] = {}

    return knowledge[guild_id]


def get_knowledge_text(guild_id=None):

    global_data = get_global_knowledge()

    lines = []

    # Global knowledge
    for key, value in global_data.items():

        lines.append(
            f"[GLOBAL: {key}]\n{value}"
        )

    # Server knowledge
    if guild_id is not None:

        guild_data = knowledge.get(
            str(guild_id),
            {}
        )

        for key, value in guild_data.items():

            lines.append(
                f"[SERVER: {key}]\n{value}"
            )

    if not lines:

        return "No knowledge is available."

    return "\n\n".join(lines)


# ==========================================
# PERMISSION SYSTEM
# ==========================================

def is_developer(ctx):

    return (
        ctx.author.id == DEV_USER_ID
    )


def is_server_admin(ctx):

    if ctx.guild is None:
        return False

    return (
        ctx.author.guild_permissions.administrator
    )


def can_manage_server_knowledge(ctx):

    return (
        is_developer(ctx)
        or is_server_admin(ctx)
    )


# ==========================================
# KNOWLEDGE COG
# ==========================================

class KnowledgeCog(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    # ======================================
    # PREFIX COMMAND
    # ======================================

    @commands.command(name="prefix")
    async def prefix(
        self,
        ctx,
        new_prefix: str
    ):

        if ctx.guild is None:

            await ctx.send(
                "❌ This command can only be used inside a server."
            )

            return

        if not can_manage_server_knowledge(ctx):

            await ctx.send(
                "❌ Only the Developer or a Server Administrator "
                "can change the server prefix."
            )

            return

        if len(new_prefix) > 5:

            await ctx.send(
                "❌ Prefix can contain a maximum of 5 characters."
            )

            return

        if new_prefix.isspace():

            await ctx.send(
                "❌ Prefix cannot contain only spaces."
            )

            return

        if new_prefix in ("@", "#"):

            await ctx.send(
                "❌ This prefix cannot be used."
            )

            return

        if not set_server_prefix(
            ctx.guild.id,
            new_prefix
        ):

            await ctx.send(
                "❌ Failed to save the server prefix."
            )

            return

        await ctx.send(
            f"✅ Server prefix has been changed to "
            f"`{new_prefix}`"
        )


    # ======================================
    # ADD SERVER KNOWLEDGE
    # ======================================

    @commands.command(name="aiadd")
    async def aiadd(
        self,
        ctx,
        key: str,
        *,
        value: str
    ):

        if ctx.guild is None:

            await ctx.send(
                "❌ This command can only be used inside a server."
            )

            return

        if not can_manage_server_knowledge(ctx):
            return

        guild_data = get_guild_knowledge(
            ctx.guild.id
        )

        key = key.lower().strip()

        if key in guild_data:

            await ctx.send(
                f"❌ `{key}` already exists.\n"
                f"Use `aiupdate {key} <information>` to update it."
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
    # UPDATE SERVER KNOWLEDGE
    # ======================================

    @commands.command(name="aiupdate")
    async def aiupdate(
        self,
        ctx,
        key: str,
        *,
        value: str
    ):

        if ctx.guild is None:

            await ctx.send(
                "❌ This command can only be used inside a server."
            )

            return

        if not can_manage_server_knowledge(ctx):
            return

        guild_data = get_guild_knowledge(
            ctx.guild.id
        )

        key = key.lower().strip()

        if key not in guild_data:

            await ctx.send(
                f"❌ Knowledge `{key}` does not exist."
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
    # DELETE SERVER KNOWLEDGE
    # ======================================

    @commands.command(name="aidelete")
    async def aidelete(
        self,
        ctx,
        key: str
    ):

        if ctx.guild is None:

            await ctx.send(
                "❌ This command can only be used inside a server."
            )

            return

        if not can_manage_server_knowledge(ctx):
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
                "❌ Failed to save the knowledge."
            )

            return

        await ctx.send(
            f"🗑️ Knowledge `{key}` has been deleted."
        )


    # ======================================
    # LIST SERVER KNOWLEDGE
    # ======================================

    @commands.command(name="ailist")
    async def ailist(self, ctx):

        if ctx.guild is None:

            await ctx.send(
                "❌ This command can only be used inside a server."
            )

            return

        if not can_manage_server_knowledge(ctx):
            return

        guild_data = get_guild_knowledge(
            ctx.guild.id
        )

        if not guild_data:

            await ctx.send(
                "📚 The server Knowledge Base is empty."
            )

            return

        keys = list(
            guild_data.keys()
        )

        description = "\n".join(
            f"• `{key}`"
            for key in keys
        )

        embed = discord.Embed(
            title="📚 Server Knowledge Base",
            description=description,
            color=discord.Color.blurple()
        )

        embed.set_footer(
            text=f"Total entries: {len(keys)}"
        )

        await ctx.send(
            embed=embed
        )


    # ======================================
    # SEARCH SERVER KNOWLEDGE
    # ======================================

    @commands.command(name="aisearch")
    async def aisearch(
        self,
        ctx,
        *,
        query: str
    ):

        if ctx.guild is None:

            await ctx.send(
                "❌ This command can only be used inside a server."
            )

            return

        if not can_manage_server_knowledge(ctx):
            return

        guild_data = get_guild_knowledge(
            ctx.guild.id
        )

        query = query.lower().strip()

        results = []

        for key, value in guild_data.items():

            if (
                query in key.lower()
                or query in value.lower()
            ):

                results.append(
                    f"**{key}**\n{value}"
                )

        if not results:

            await ctx.send(
                f"🔍 No knowledge found for `{query}`."
            )

            return

        embed = discord.Embed(
            title="🔎 Knowledge Search",
            description="\n\n".join(results)[:4000],
            color=discord.Color.green()
        )

        await ctx.send(
            embed=embed
        )


    # ======================================
    # CLEAR SERVER KNOWLEDGE
    # ======================================

    @commands.command(name="aiclear")
    async def aiclear(self, ctx):

        if ctx.guild is None:

            await ctx.send(
                "❌ This command can only be used inside a server."
            )

            return

        if not can_manage_server_knowledge(ctx):
            return

        guild_id = str(
            ctx.guild.id
        )

        if guild_id not in knowledge:

            await ctx.send(
                "📚 This server has no knowledge to clear."
            )

            return

        knowledge[guild_id] = {}

        if not save_knowledge(knowledge):

            await ctx.send(
                "❌ Failed to clear the knowledge."
            )

            return

        await ctx.send(
            "🗑️ All knowledge for this server has been cleared."
        )


# ==========================================
# SETUP
# ==========================================

async def setup(bot):

    await bot.add_cog(
        KnowledgeCog(bot)
    )
