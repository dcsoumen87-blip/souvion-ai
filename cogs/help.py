import discord
from discord.ext import commands

from config import DEV_USER_ID
from cogs.knowledge import (
    get_server_prefix,
    can_manage_server_knowledge,
)


# ==========================================
# HELP CATEGORY VIEW
# ==========================================

class HelpSelect(discord.ui.Select):

    def __init__(self, bot, is_developer, is_admin):

        self.bot = bot
        self.is_developer = is_developer
        self.is_admin = is_admin

        options = [
            discord.SelectOption(
                label="AI Assistant",
                description="AI commands and usage",
                emoji="🤖",
                value="ai"
            ),
            discord.SelectOption(
                label="Server",
                description="Server management commands",
                emoji="🛡️",
                value="server"
            ),
            discord.SelectOption(
                label="Knowledge",
                description="Server knowledge commands",
                emoji="📚",
                value="knowledge"
            ),
            discord.SelectOption(
                label="Utility",
                description="Utility and information commands",
                emoji="⚙️",
                value="utility"
            ),
        ]

        if is_developer:

            options.append(
                discord.SelectOption(
                    label="Developer",
                    description="Developer-only commands",
                    emoji="👑",
                    value="developer"
                )
            )

        super().__init__(
            placeholder="Select a category...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction):

        category = self.values[0]

        embed = self.build_embed(
            category,
            interaction
        )

        await interaction.response.edit_message(
            embed=embed,
            view=self.view
        )

    # ======================================
    # BUILD CATEGORY EMBED
    # ======================================

    def build_embed(
        self,
        category,
        interaction
    ):

        guild = interaction.guild

        prefix = (
            get_server_prefix(guild.id)
            if guild
            else "!"
        )

        # ==================================
        # AI
        # ==================================

        if category == "ai":

            embed = discord.Embed(
                title="🤖 Souvion AI",
                description=(
                    "Ask Souvion AI anything by mentioning the bot."
                ),
                color=discord.Color.blurple()
            )

            embed.add_field(
                name="💬 Ask AI",
                value=(
                    f"**Usage:**\n"
                    f"`<@{self.bot.user.id}> your question`\n\n"
                    f"Example:\n"
                    f"`<@{self.bot.user.id}> What is Discord?`"
                ),
                inline=False
            )

            embed.add_field(
                name="🌐 Supported Languages",
                value=(
                    "English\n"
                    "বাংলা\n"
                    "Hinglish"
                ),
                inline=True
            )

            embed.add_field(
                name="🧠 Knowledge",
                value=(
                    "Souvion AI can use global and "
                    "server-specific knowledge."
                ),
                inline=True
            )

            return embed

        # ==================================
        # SERVER
        # ==================================

        if category == "server":

            embed = discord.Embed(
                title="🛡️ Server Commands",
                description=(
                    "Commands related to this Discord server."
                ),
                color=discord.Color.green()
            )

            embed.add_field(
                name="📌 Prefix",
                value=(
                    f"`{prefix}prefix <new_prefix>`\n"
                    "Change this server's command prefix."
                ),
                inline=False
            )

            embed.add_field(
                name="ℹ️ Server Info",
                value=(
                    f"`{prefix}serverinfo`\n"
                    "View server information."
                ),
                inline=False
            )

            if self.is_admin:

                embed.add_field(
                    name="👮 Administrator",
                    value=(
                        f"`{prefix}aiadd <key> <information>`\n"
                        f"`{prefix}aiupdate <key> <information>`\n"
                        f"`{prefix}aidelete <key>`\n"
                        f"`{prefix}ailist`\n"
                        f"`{prefix}aisearch <query>`\n"
                        f"`{prefix}aiclear`"
                    ),
                    inline=False
                )

            return embed

        # ==================================
        # KNOWLEDGE
        # ==================================

        if category == "knowledge":

            embed = discord.Embed(
                title="📚 Knowledge Commands",
                description=(
                    "Manage the knowledge used by Souvion AI."
                ),
                color=discord.Color.orange()
            )

            if self.is_admin:

                embed.add_field(
                    name="🧠 Server Knowledge",
                    value=(
                        f"`{prefix}aiadd <key> <information>`\n"
                        f"`{prefix}aiupdate <key> <information>`\n"
                        f"`{prefix}aidelete <key>`\n"
                        f"`{prefix}ailist`\n"
                        f"`{prefix}aisearch <query>`\n"
                        f"`{prefix}aiclear`"
                    ),
                    inline=False
                )

                embed.add_field(
                    name="🔐 Permission",
                    value=(
                        "Only Server Administrators and "
                        "the Developer can manage server knowledge."
                    ),
                    inline=False
                )

            else:

                embed.add_field(
                    name="📖 Access",
                    value=(
                        "You can ask the AI questions using "
                        "a bot mention.\n\n"
                        "Knowledge management is restricted "
                        "to Server Administrators and the Developer."
                    ),
                    inline=False
                )

            return embed

        # ==================================
        # UTILITY
        # ==================================

        if category == "utility":

            embed = discord.Embed(
                title="⚙️ Utility Commands",
                description=(
                    "General Souvion AI utilities."
                ),
                color=discord.Color.teal()
            )

            embed.add_field(
                name="❓ Help",
                value=(
                    f"`{prefix}help`\n"
                    "Open this Help Panel."
                ),
                inline=False
            )

            embed.add_field(
                name="🔧 Prefix",
                value=(
                    f"`{prefix}prefix <new_prefix>`\n"
                    "Available to Server Administrators."
                ),
                inline=False
            )

            return embed

        # ==================================
        # DEVELOPER
        # ==================================

        if category == "developer":

            if not self.is_developer:

                return discord.Embed(
                    title="❌ Access Denied",
                    description=(
                        "Developer commands are restricted."
                    ),
                    color=discord.Color.red()
                )

            embed = discord.Embed(
                title="👑 Developer Commands",
                description=(
                    "Souvion AI Developer control panel."
                ),
                color=discord.Color.gold()
            )

            embed.add_field(
                name="🤖 Bot Management",
                value=(
                    f"`{prefix}devstatus`\n"
                    f"`{prefix}devinfo`\n"
                    f"`{prefix}devhelp`\n"
                    f"`{prefix}reload`\n"
                    f"`{prefix}sync`\n"
                    f"`{prefix}restart CONFIRM`\n"
                    f"`{prefix}maintenance on/off`"
                ),
                inline=False
            )

            embed.add_field(
                name="🏠 Server Management",
                value=(
                    f"`{prefix}serverlist`\n"
                    f"`{prefix}serverinfo <server_id>`\n"
                    f"`{prefix}servercount`\n"
                    f"`{prefix}serverconfig <server_id>`\n"
                    f"`{prefix}leave <server_id> CONFIRM`\n"
                    f"`{prefix}devadmin <server_id>`"
                ),
                inline=False
            )

            embed.add_field(
                name="🧠 Global Knowledge",
                value=(
                    f"`{prefix}globaladd <key> <information>`\n"
                    f"`{prefix}globalupdate <key> <information>`\n"
                    f"`{prefix}globaldelete <key>`\n"
                    f"`{prefix}globallist`"
                ),
                inline=False
            )

            embed.add_field(
                name="📦 Import / Export",
                value=(
                    f"`{prefix}knowledgeexport <server_id>`\n"
                    f"`{prefix}knowledgeimport <server_id>`"
                ),
                inline=False
            )

            embed.add_field(
                name="📊 Statistics",
                value=(
                    f"`{prefix}stats`\n"
                    f"`{prefix}usercount`\n"
                    f"`{prefix}uptime`\n"
                    f"`{prefix}apistatus`"
                ),
                inline=False
            )

            return embed

        return discord.Embed(
            title="Souvion AI",
            description="Select a category.",
            color=discord.Color.blurple()
        )


# ==========================================
# HELP VIEW
# ==========================================

class HelpView(discord.ui.View):

    def __init__(
        self,
        bot,
        author,
        is_developer,
        is_admin
    ):

        super().__init__(
            timeout=180
        )

        self.author = author
        self.bot = bot

        self.add_item(
            HelpSelect(
                bot,
                is_developer,
                is_admin
            )
        )

    async def interaction_check(
        self,
        interaction
    ):

        if interaction.user.id != self.author.id:

            await interaction.response.send_message(
                "❌ This Help Panel belongs to another user.",
                ephemeral=True
            )

            return False

        return True


# ==========================================
# HELP COG
# ==========================================

class HelpCog(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    # ======================================
    # HELP COMMAND
    # ======================================

    @commands.command(name="help")
    async def help_command(
        self,
        ctx
    ):

        is_developer = (
            ctx.author.id == DEV_USER_ID
        )

        is_admin = False

        if ctx.guild:

            is_admin = (
                ctx.author.guild_permissions.administrator
            )

        prefix = (
            get_server_prefix(ctx.guild.id)
            if ctx.guild
            else "!"
        )

        embed = discord.Embed(
            title="🤖 Souvion AI",
            description=(
                "### AI Assistant & Server Management\n\n"
                "Select a category from the menu below "
                "to view available commands."
            ),
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="📌 Server Prefix",
            value=f"`{prefix}`",
            inline=True
        )

        embed.add_field(
            name="👤 Your Access",
            value=(
                "👑 Developer"
                if is_developer
                else (
                    "🛡️ Server Administrator"
                    if is_admin
                    else "👤 Member"
                )
            ),
            inline=True
        )

        embed.add_field(
            name="🤖 AI",
            value=(
                f"Mention **{self.bot.user.display_name}** "
                "to ask a question."
            ),
            inline=False
        )

        embed.set_footer(
            text="Souvion AI • Developed by Soumen"
        )

        if self.bot.user.avatar:

            embed.set_thumbnail(
                url=self.bot.user.avatar.url
            )

        view = HelpView(
            self.bot,
            ctx.author,
            is_developer,
            is_admin
        )

        await ctx.send(
            embed=embed,
            view=view
        )


# ==========================================
# SETUP
# ==========================================

async def setup(bot):

    await bot.add_cog(
        HelpCog(bot)
          )
