import asyncio
import discord
from discord.ext import commands

from config import DISCORD_TOKEN, BOT_PREFIX
from cogs.knowledge import get_server_prefix


# ==========================================
# DISCORD INTENTS
# ==========================================

intents = discord.Intents.default()

intents.message_content = True
intents.members = True


# ==========================================
# DYNAMIC PREFIX
# ==========================================

def get_prefix(bot, message):

    # Default prefix for DMs
    if message.guild is None:
        return BOT_PREFIX

    try:
        return get_server_prefix(message.guild.id)

    except Exception as error:
        print("[PREFIX] Error:", error)
        return BOT_PREFIX


# ==========================================
# BOT
# ==========================================

bot = commands.Bot(
    command_prefix=get_prefix,
    intents=intents,
    help_command=None
)


# ==========================================
# BOT STATE
# ==========================================

bot.maintenance_mode = False


# ==========================================
# COGS
# ==========================================

COGS = [
    "cogs.ai",
    "cogs.dev",
    "cogs.knowledge",
    "cogs.help",
    "cogs.utility",
    "cogs.stats",
]


async def load_cogs():

    for cog in COGS:

        try:

            await bot.load_extension(cog)

            print(f"[COG] Loaded: {cog}")

        except Exception as error:

            print(f"[COG] Failed to load: {cog}")
            print(f"[ERROR] {error}")


# ==========================================
# BOT READY
# ==========================================

@bot.event
async def on_ready():

    print("=" * 50)
    print("SOUVION AI")
    print("=" * 50)

    print(f"Bot       : {bot.user}")
    print(f"Bot ID    : {bot.user.id}")
    print(f"Servers   : {len(bot.guilds)}")
    print("Status    : ONLINE")

    print("=" * 50)


# ==========================================
# MESSAGE HANDLER
# ==========================================

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    await bot.process_commands(message)


# ==========================================
# COMMAND ERROR HANDLER
# ==========================================

@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.MissingRequiredArgument):

        await ctx.send(
            "❌ Missing required argument."
        )

        return

    if isinstance(error, commands.BadArgument):

        await ctx.send(
            "❌ Invalid argument provided."
        )

        return

    if isinstance(error, commands.MissingPermissions):

        await ctx.send(
            "❌ You do not have permission to use this command."
        )

        return

    if isinstance(error, commands.CheckFailure):

        return

    print("=" * 50)
    print("COMMAND ERROR")
    print(error)
    print("=" * 50)


# ==========================================
# START BOT
# ==========================================

async def main():

    if not DISCORD_TOKEN:

        raise RuntimeError(
            "DISCORD_TOKEN is missing. "
            "Please add it to Railway Variables."
        )

    print("[SYSTEM] Loading Souvion AI...")

    await load_cogs()

    print("[SYSTEM] Starting Discord bot...")

    await bot.start(DISCORD_TOKEN)


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        print("[SYSTEM] Bot stopped.")

    except Exception as error:

        print("=" * 50)
        print("FATAL ERROR")
        print(error)
        print("=" * 50)
