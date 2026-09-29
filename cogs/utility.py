import discord
from discord.ext import commands


class UtilityCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ========================================================
    # PING
    # Available to EVERYONE
    # ========================================================

    @commands.command(name="ping")
    async def ping(self, ctx):

        latency = round(
            self.bot.latency * 1000
        )

        if latency < 100:
            status = "🟢 Excellent"
            color = discord.Color.green()

        elif latency < 200:
            status = "🟡 Good"
            color = discord.Color.gold()

        elif latency < 300:
            status = "🟠 Moderate"
            color = discord.Color.orange()

        else:
            status = "🔴 High"
            color = discord.Color.red()

        embed = discord.Embed(
            title="🏓 Souvion AI Ping",
            description=(
                f"**Bot Latency:** `{latency}ms`\n"
                f"**Status:** {status}"
            ),
            color=color
        )

        embed.set_footer(
            text=f"Requested by {ctx.author}"
        )

        await ctx.send(
            embed=embed
        )

    # ========================================================
    # BOT INFO
    # Available to EVERYONE
    # ========================================================

    @commands.command(name="botinfo")
    async def botinfo(self, ctx):

        latency = round(
            self.bot.latency * 1000
        )

        embed = discord.Embed(
            title="🤖 Souvion AI",
            description=(
                "Professional AI Assistant for Discord."
            ),
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="🏓 Ping",
            value=f"`{latency}ms`",
            inline=True
        )

        embed.add_field(
            name="🌐 Servers",
            value=f"`{len(self.bot.guilds)}`",
            inline=True
        )

        embed.add_field(
            name="👤 Bot",
            value=str(self.bot.user),
            inline=True
        )

        embed.add_field(
            name="🆔 Bot ID",
            value=f"`{self.bot.user.id}`",
            inline=False
        )

        embed.add_field(
            name="📡 Status",
            value="🟢 Online",
            inline=True
        )

        embed.set_footer(
            text="Souvion AI"
        )

        await ctx.send(
            embed=embed
        )


# ============================================================
# SETUP
# ============================================================

async def setup(bot):

    await bot.add_cog(
        UtilityCog(bot)
    )
