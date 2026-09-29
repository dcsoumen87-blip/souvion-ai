import discord
from discord.ext import commands

from config import DEV_USER_ID


# ==========================================
# DEVELOPER COG
# ==========================================

class DeveloperCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ======================================
    # DEVELOPER CHECK
    # ======================================

    async def cog_check(self, ctx):

        # Only the configured developer can use
        # commands inside this Cog.

        if ctx.author.id != DEV_USER_ID:
            return False

        return True

    # ======================================
    # DEV STATUS
    # ======================================

    @commands.command(name="devstatus")
    async def devstatus(self, ctx):

        embed = discord.Embed(
            title="Souvion AI Developer Panel",
            description="Developer status and bot information.",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="Bot",
            value=f"`{self.bot.user}`",
            inline=False
        )

        embed.add_field(
            name="Bot ID",
            value=f"`{self.bot.user.id}`",
            inline=True
        )

        embed.add_field(
            name="Servers",
            value=f"`{len(self.bot.guilds)}`",
            inline=True
        )

        embed.add_field(
            name="Status",
            value="🟢 Online",
            inline=True
        )

        await ctx.send(embed=embed)

    # ======================================
    # DEV INFO
    # ======================================

    @commands.command(name="devinfo")
    async def devinfo(self, ctx):

        embed = discord.Embed(
            title="Souvion AI",
            description="Developer information",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Developer",
            value="Soumen",
            inline=False
        )

        embed.add_field(
            name="Discord.py",
            value="Enabled",
            inline=True
        )

        embed.add_field(
            name="Gemini AI",
            value="Enabled",
            inline=True
        )

        embed.add_field(
            name="Knowledge System",
            value="Enabled",
            inline=True
        )

        await ctx.send(embed=embed)

    # ======================================
    # DEV HELP
    # ======================================

    @commands.command(name="devhelp")
    async def devhelp(self, ctx):

        embed = discord.Embed(
            title="Souvion AI Developer Commands",
            description="Commands available to the developer.",
            color=discord.Color.gold()
        )

        embed.add_field(
            name="!devstatus",
            value="Show bot status and statistics.",
            inline=False
        )

        embed.add_field(
            name="!devinfo",
            value="Show bot developer and system information.",
            inline=False
        )

        embed.add_field(
            name="!devhelp",
            value="Show this developer command list.",
            inline=False
        )

        embed.set_footer(
            text="Souvion AI • Developer Panel"
        )

        await ctx.send(embed=embed)


# ==========================================
# SETUP
# ==========================================

async def setup(bot):

    await bot.add_cog(DeveloperCog(bot))
