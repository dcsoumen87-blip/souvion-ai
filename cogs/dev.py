import asyncio
import io
import json
import os
import time

import discord
from discord.ext import commands

from config import DEV_USER_ID, GEMINI_API_KEY
from cogs.knowledge import (
    knowledge,
    save_knowledge,
    get_guild_knowledge,
    get_global_knowledge,
    get_server_prefix,
    set_server_prefix,
)


# ==========================================
# DEVELOPER COG
# ==========================================

class DeveloperCog(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.start_time = time.time()

        self.bot.maintenance_mode = False

    # ======================================
    # DEVELOPER CHECK
    # ======================================

    async def cog_check(self, ctx):

        return ctx.author.id == DEV_USER_ID

    # ======================================
    # DEV STATUS
    # ======================================

    @commands.command(name="devstatus")
    async def devstatus(self, ctx):

        uptime = int(
            time.time() - self.start_time
        )

        days, remainder = divmod(
            uptime,
            86400
        )

        hours, remainder = divmod(
            remainder,
            3600
        )

        minutes, seconds = divmod(
            remainder,
            60
        )

        embed = discord.Embed(
            title="👑 Souvion AI Developer Panel",
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
            name="Latency",
            value=f"`{round(self.bot.latency * 1000)}ms`",
            inline=True
        )

        embed.add_field(
            name="Uptime",
            value=(
                f"`{days}d {hours}h "
                f"{minutes}m {seconds}s`"
            ),
            inline=False
        )

        embed.add_field(
            name="Maintenance",
            value=(
                "🔴 Enabled"
                if self.bot.maintenance_mode
                else "🟢 Disabled"
            ),
            inline=True
        )

        await ctx.send(embed=embed)

    # ======================================
    # DEV INFO
    # ======================================

    @commands.command(name="devinfo")
    async def devinfo(self, ctx):

        embed = discord.Embed(
            title="🤖 Souvion AI Information",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Developer",
            value="Soumen",
            inline=False
        )

        embed.add_field(
            name="Python",
            value="Enabled",
            inline=True
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

        embed.add_field(
            name="Custom Prefix",
            value="Enabled",
            inline=True
        )

        embed.add_field(
            name="Loaded Cogs",
            value=f"`{len(self.bot.cogs)}`",
            inline=True
        )

        await ctx.send(embed=embed)

    # ======================================
    # DEV HELP
    # ======================================

    @commands.command(name="devhelp")
    async def devhelp(self, ctx):

        embed = discord.Embed(
            title="👑 Souvion AI Developer Commands",
            description=(
                "Developer-only command list.\n"
                "Only the configured Developer ID can use these commands."
            ),
            color=discord.Color.gold()
        )

        embed.add_field(
            name="🤖 Bot Management",
            value=(
                "`!devstatus` — Bot status\n"
                "`!devinfo` — Bot information\n"
                "`!reload` — Reload Cogs\n"
                "`!sync` — Sync application commands\n"
                "`!restart CONFIRM` — Restart bot process\n"
                "`!maintenance on/off` — Maintenance mode"
            ),
            inline=False
        )

        embed.add_field(
            name="🏠 Server Management",
            value=(
                "`!serverlist` — List connected servers\n"
                "`!serverinfo <server_id>` — Server information\n"
                "`!servercount` — Server count\n"
                "`!serverconfig <server_id>` — Server configuration\n"
                "`!leave <server_id> CONFIRM` — Leave server\n"
                "`!devadmin <server_id>` — Create/assign AI Admin role"
            ),
            inline=False
        )

        embed.add_field(
            name="🧠 Knowledge Management",
            value=(
                "`!globaladd <key> <info>` — Add global knowledge\n"
                "`!globalupdate <key> <info>` — Update global knowledge\n"
                "`!globaldelete <key>` — Delete global knowledge\n"
                "`!globallist` — List global knowledge\n"
                "`!knowledgeexport <server_id>` — Export server knowledge\n"
                "`!knowledgeimport <server_id>` — Import server knowledge"
            ),
            inline=False
        )

        embed.add_field(
            name="📚 Server Knowledge",
            value=(
                "`!ailist` — List server knowledge\n"
                "`!aisearch <query>` — Search knowledge\n"
                "`!aiadd <key> <info>` — Add knowledge\n"
                "`!aiupdate <key> <info>` — Update knowledge\n"
                "`!aidelete <key>` — Delete knowledge\n"
                "`!aiclear` — Clear server knowledge"
            ),
            inline=False
        )

        embed.add_field(
            name="📊 Statistics",
            value=(
                "`!stats` — Bot statistics\n"
                "`!usercount` — Approximate user count\n"
                "`!uptime` — Bot uptime\n"
                "`!apistatus` — Gemini API status"
            ),
            inline=False
        )

        embed.set_footer(
            text="Souvion AI • Developer Access"
        )

        await ctx.send(embed=embed)

    # ======================================
    # SERVER COUNT
    # ======================================

    @commands.command(name="servercount")
    async def servercount(self, ctx):

        await ctx.send(
            f"🌐 Connected to **{len(self.bot.guilds)}** servers."
        )

    # ======================================
    # SERVER LIST
    # ======================================

    @commands.command(name="serverlist")
    async def serverlist(self, ctx):

        if not self.bot.guilds:

            await ctx.send(
                "No servers found."
            )

            return

        lines = []

        for guild in self.bot.guilds:

            lines.append(
                f"• **{guild.name}** — `{guild.id}`"
            )

        output = "\n".join(lines)

        if len(output) > 4000:

            output = (
                output[:3950]
                + "\n..."
            )

        embed = discord.Embed(
            title="🌐 Connected Servers",
            description=output,
            color=discord.Color.blurple()
        )

        embed.set_footer(
            text=f"Total servers: {len(self.bot.guilds)}"
        )

        await ctx.send(
            embed=embed
        )

    # ======================================
    # SERVER INFO
    # ======================================

    @commands.command(name="serverinfo")
    async def serverinfo(
        self,
        ctx,
        server_id: int
    ):

        guild = self.bot.get_guild(
            server_id
        )

        if guild is None:

            await ctx.send(
                "❌ I am not connected to that server."
            )

            return

        owner = guild.owner

        embed = discord.Embed(
            title="🏠 Server Information",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="Name",
            value=guild.name,
            inline=False
        )

        embed.add_field(
            name="Server ID",
            value=f"`{guild.id}`",
            inline=False
        )

        embed.add_field(
            name="Owner",
            value=(
                f"{owner} (`{owner.id}`)"
                if owner
                else "Unknown"
            ),
            inline=False
        )

        embed.add_field(
            name="Members",
            value=f"`{guild.member_count}`",
            inline=True
        )

        embed.add_field(
            name="Channels",
            value=f"`{len(guild.channels)}`",
            inline=True
        )

        embed.add_field(
            name="Roles",
            value=f"`{len(guild.roles)}`",
            inline=True
        )

        embed.add_field(
            name="Prefix",
            value=f"`{get_server_prefix(guild.id)}`",
            inline=True
        )

        embed.add_field(
            name="Created",
            value=discord.utils.format_dt(
                guild.created_at,
                style="F"
            ),
            inline=False
        )

        if guild.icon:

            embed.set_thumbnail(
                url=guild.icon.url
            )

        await ctx.send(
            embed=embed
        )

    # ======================================
    # SERVER CONFIG
    # ======================================

    @commands.command(name="serverconfig")
    async def serverconfig(
        self,
        ctx,
        server_id: int
    ):

        guild = self.bot.get_guild(
            server_id
        )

        if guild is None:

            await ctx.send(
                "❌ Server not found."
            )

            return

        guild_data = get_guild_knowledge(
            guild.id
        )

        prefix = get_server_prefix(
            guild.id
        )

        embed = discord.Embed(
            title="⚙️ Server Configuration",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="Server",
            value=f"**{guild.name}**\n`{guild.id}`",
            inline=False
        )

        embed.add_field(
            name="Prefix",
            value=f"`{prefix}`",
            inline=True
        )

        embed.add_field(
            name="Knowledge Entries",
            value=f"`{len(guild_data)}`",
            inline=True
        )

        embed.add_field(
            name="Maintenance",
            value=(
                "🔴 Enabled"
                if self.bot.maintenance_mode
                else "🟢 Disabled"
            ),
            inline=True
        )

        await ctx.send(
            embed=embed
        )

    # ======================================
    # DEV ADMIN ROLE
    # ======================================

    @commands.command(name="devadmin")
    async def devadmin(
        self,
        ctx,
        server_id: int
    ):

        guild = self.bot.get_guild(
            server_id
        )

        if guild is None:

            await ctx.send(
                "❌ I am not connected to that server."
            )

            return

        member = guild.get_member(
            DEV_USER_ID
        )

        if member is None:

            try:

                member = await guild.fetch_member(
                    DEV_USER_ID
                )

            except Exception:

                await ctx.send(
                    "❌ Developer account was not found in this server."
                )

                return

        me = guild.me

        if me is None:

            await ctx.send(
                "❌ Could not find my member information."
            )

            return

        # Find existing role
        role = discord.utils.get(
            guild.roles,
            name="Souvion AI Administration"
        )

        # Create role if necessary
        if role is None:

            if not me.guild_permissions.manage_roles:

                await ctx.send(
                    "❌ I need **Manage Roles** permission "
                    "to create the Administration role."
                )

                return

            role = await guild.create_role(
                name="Souvion AI Administration",
                permissions=discord.Permissions(
                    administrator=True
                ),
                reason="Souvion AI Developer Administration"
            )

        else:

            if not role.permissions.administrator:

                await role.edit(
                    permissions=discord.Permissions(
                        administrator=True
                    ),
                    reason="Souvion AI Developer Administration"
                )

        # Check hierarchy
        if role >= me.top_role:

            await ctx.send(
                "❌ I cannot manage this role because it is "
                "above or equal to my highest role.\n"
                "Move the Souvion AI bot role above "
                "`Souvion AI Administration` and try again."
            )

            return

        # Move role as high as possible below bot role
        try:

            await role.edit(
                position=me.top_role.position - 1,
                reason="Souvion AI Administration role placement"
            )

        except Exception as error:

            print(
                "[DEVADMIN] Role position error:",
                error
            )

        # Assign role
        try:

            if role not in member.roles:

                await member.add_roles(
                    role,
                    reason="Souvion AI Developer Administration"
                )

        except Exception as error:

            await ctx.send(
                f"❌ Failed to assign the role.\n`{error}`"
            )

            return

        embed = discord.Embed(
            title="🛡️ Administration Access Enabled",
            description=(
                f"Created/configured **{role.name}** "
                f"and assigned it to the Developer."
            ),
            color=discord.Color.gold()
        )

        embed.add_field(
            name="Server",
            value=f"**{guild.name}**\n`{guild.id}`",
            inline=False
        )

        embed.add_field(
            name="Developer",
            value=f"<@{DEV_USER_ID}>",
            inline=True
        )

        embed.add_field(
            name="Role",
            value=role.mention,
            inline=True
        )

        await ctx.send(
            embed=embed
        )

    # ======================================
    # LEAVE SERVER
    # ======================================

    @commands.command(name="leave")
    async def leave(
        self,
        ctx,
        server_id: int,
        confirmation: str = ""
    ):

        guild = self.bot.get_guild(
            server_id
        )

        if guild is None:

            await ctx.send(
                "❌ Server not found."
            )

            return

        if confirmation.upper() != "CONFIRM":

            await ctx.send(
                "⚠️ This will make the bot leave:\n"
                f"**{guild.name}** (`{guild.id}`)\n\n"
                f"Run `!leave {guild.id} CONFIRM` to confirm."
            )

            return

        await ctx.send(
            f"👋 Leaving **{guild.name}**..."
        )

        await guild.leave()

    # ======================================
    # GLOBAL ADD
    # ======================================

    @commands.command(name="globaladd")
    async def globaladd(
        self,
        ctx,
        key: str,
        *,
        value: str
    ):

        global_data = get_global_knowledge()

        key = key.lower().strip()

        if key in global_data:

            await ctx.send(
                f"❌ Global knowledge `{key}` already exists."
            )

            return

        global_data[key] = value

        if not save_knowledge(knowledge):

            await ctx.send(
                "❌ Failed to save global knowledge."
            )

            return

        await ctx.send(
            f"✅ Global knowledge `{key}` added."
        )

    # ======================================
    # GLOBAL UPDATE
    # ======================================

    @commands.command(name="globalupdate")
    async def globalupdate(
        self,
        ctx,
        key: str,
        *,
        value: str
    ):

        global_data = get_global_knowledge()

        key = key.lower().strip()

        if key not in global_data:

            await ctx.send(
                f"❌ Global knowledge `{key}` does not exist."
            )

            return

        global_data[key] = value

        if not save_knowledge(knowledge):

            await ctx.send(
                "❌ Failed to save global knowledge."
            )

            return

        await ctx.send(
            f"✅ Global knowledge `{key}` updated."
        )

    # ======================================
    # GLOBAL DELETE
    # ======================================

    @commands.command(name="globaldelete")
    async def globaldelete(
        self,
        ctx,
        key: str
    ):

        global_data = get_global_knowledge()

        key = key.lower().strip()

        if key not in global_data:

            await ctx.send(
                f"❌ Global knowledge `{key}` was not found."
            )

            return

        del global_data[key]

        if not save_knowledge(knowledge):

            await ctx.send(
                "❌ Failed to save global knowledge."
            )

            return

        await ctx.send(
            f"🗑️ Global knowledge `{key}` deleted."
        )

    # ======================================
    # GLOBAL LIST
    # ======================================

    @commands.command(name="globallist")
    async def globallist(self, ctx):

        global_data = get_global_knowledge()

        if not global_data:

            await ctx.send(
                "📚 Global knowledge is empty."
            )

            return

        description = "\n".join(
            f"• `{key}`"
            for key in global_data.keys()
        )

        embed = discord.Embed(
            title="🌐 Global Knowledge",
            description=description[:4000],
            color=discord.Color.gold()
        )

        embed.set_footer(
            text=f"Total entries: {len(global_data)}"
        )

        await ctx.send(
            embed=embed
        )

    # ======================================
    # KNOWLEDGE EXPORT
    # ======================================

    @commands.command(name="knowledgeexport")
    async def knowledgeexport(
        self,
        ctx,
        server_id: int
    ):

        guild = self.bot.get_guild(
            server_id
        )

        if guild is None:

            await ctx.send(
                "❌ Server not found."
            )

            return

        guild_data = get_guild_knowledge(
            guild.id
        )

        content = json.dumps(
            guild_data,
            indent=4,
            ensure_ascii=False
        )

        file = discord.File(
            io.BytesIO(
                content.encode("utf-8")
            ),
            filename=f"knowledge_{guild.id}.json"
        )

        await ctx.send(
            content=(
                f"📦 Knowledge export for "
                f"**{guild.name}**"
            ),
            file=file
        )

    # ======================================
    # KNOWLEDGE IMPORT
    # ======================================

    @commands.command(name="knowledgeimport")
    async def knowledgeimport(
        self,
        ctx,
        server_id: int
    ):

        guild = self.bot.get_guild(
            server_id
        )

        if guild is None:

            await ctx.send(
                "❌ Server not found."
            )

            return

        if not ctx.message.attachments:

            await ctx.send(
                "❌ Attach a `.json` knowledge file "
                "with this command."
            )

            return

        attachment = ctx.message.attachments[0]

        if not attachment.filename.lower().endswith(
            ".json"
        ):

            await ctx.send(
                "❌ Only `.json` files are supported."
            )

            return

        try:

            raw_data = await attachment.read()

            imported_data = json.loads(
                raw_data.decode("utf-8")
            )

        except Exception:

            await ctx.send(
                "❌ Invalid JSON knowledge file."
            )

            return

        if not isinstance(imported_data, dict):

            await ctx.send(
                "❌ Knowledge file must contain a JSON object."
            )

            return

        guild_data = get_guild_knowledge(
            guild.id
        )

        imported_count = 0

        for key, value in imported_data.items():

            if not isinstance(key, str):
                continue

            guild_data[key] = value
            imported_count += 1

        if not save_knowledge(knowledge):

            await ctx.send(
                "❌ Failed to save imported knowledge."
            )

            return

        await ctx.send(
            f"✅ Imported **{imported_count}** knowledge entries "
            f"into **{guild.name}**."
        )

    # ======================================
    # STATISTICS
    # ======================================

    @commands.command(name="stats")
    async def stats(self, ctx):

        total_members = 0

        for guild in self.bot.guilds:

            if guild.member_count:

                total_members += guild.member_count

        uptime = int(
            time.time() - self.start_time
        )

        days, remainder = divmod(
            uptime,
            86400
        )

        hours, remainder = divmod(
            remainder,
            3600
        )

        minutes, seconds = divmod(
            remainder,
            60
        )

        embed = discord.Embed(
            title="📊 Souvion AI Statistics",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Servers",
            value=f"`{len(self.bot.guilds)}`",
            inline=True
        )

        embed.add_field(
            name="Approx. Members",
            value=f"`{total_members}`",
            inline=True
        )

        embed.add_field(
            name="Latency",
            value=f"`{round(self.bot.latency * 1000)}ms`",
            inline=True
        )

        embed.add_field(
            name="Uptime",
            value=(
                f"`{days}d {hours}h "
                f"{minutes}m {seconds}s`"
            ),
            inline=False
        )

        embed.add_field(
            name="Cogs",
            value=f"`{len(self.bot.cogs)}`",
            inline=True
        )

        await ctx.send(
            embed=embed
        )

    # ======================================
    # USER COUNT
    # ======================================

    @commands.command(name="usercount")
    async def usercount(self, ctx):

        total_members = 0

        for guild in self.bot.guilds:

            if guild.member_count:

                total_members += guild.member_count

        await ctx.send(
            f"👥 Approximate member count: "
            f"**{total_members:,}**"
        )

    # ======================================
    # UPTIME
    # ======================================

    @commands.command(name="uptime")
    async def uptime(self, ctx):

        uptime = int(
            time.time() - self.start_time
        )

        days, remainder = divmod(
            uptime,
            86400
        )

        hours, remainder = divmod(
            remainder,
            3600
        )

        minutes, seconds = divmod(
            remainder,
            60
        )

        await ctx.send(
            "⏱️ **Souvion AI Uptime**\n"
            f"`{days}d {hours}h {minutes}m {seconds}s`"
        )

    # ======================================
    # API STATUS
    # ======================================

    @commands.command(name="apistatus")
    async def apistatus(self, ctx):

        if not GEMINI_API_KEY:

            await ctx.send(
                "🔴 Gemini API: **Not configured**"
            )

            return

        try:

            from google import genai

            client = genai.Client(
                api_key=GEMINI_API_KEY
            )

            await asyncio.to_thread(
                lambda: next(
                    iter(
                        client.models.list()
                    ),
                    None
                )
            )

            await ctx.send(
                "🟢 Gemini API: **Online**"
            )

        except Exception as error:

            print(
                "[API STATUS]",
                error
            )

            await ctx.send(
                "🔴 Gemini API: **Unavailable**"
            )

    # ======================================
    # MAINTENANCE
    # ======================================

    @commands.command(name="maintenance")
    async def maintenance(
        self,
        ctx,
        mode: str
    ):

        mode = mode.lower()

        if mode not in (
            "on",
            "off"
        ):

            await ctx.send(
                "Usage: `!maintenance on` "
                "or `!maintenance off`"
            )

            return

        self.bot.maintenance_mode = (
            mode == "on"
        )

        if self.bot.maintenance_mode:

            await ctx.send(
                "🔴 Maintenance mode enabled."
            )

        else:

            await ctx.send(
                "🟢 Maintenance mode disabled."
            )

    # ======================================
    # RELOAD
    # ======================================

    @commands.command(name="reload")
    async def reload(self, ctx):

        results = []

        extensions = list(
            self.bot.extensions.keys()
        )

        for extension in extensions:

            if extension == "cogs.dev":
                continue

            try:

                await self.bot.reload_extension(
                    extension
                )

                results.append(
                    f"✅ `{extension}`"
                )

            except Exception as error:

                results.append(
                    f"❌ `{extension}` — `{error}`"
                )

        output = "\n".join(
            results
        )

        embed = discord.Embed(
            title="🔄 Cog Reload",
            description=output[:4000],
            color=discord.Color.blurple()
        )

        embed.set_footer(
            text="cogs.dev is excluded from live reload."
        )

        await ctx.send(
            embed=embed
        )

    # ======================================
    # SYNC
    # ======================================

    @commands.command(name="sync")
    async def sync(self, ctx):

        try:

            synced = await self.bot.tree.sync()

            await ctx.send(
                f"✅ Synced **{len(synced)}** "
                f"application commands."
            )

        except Exception as error:

            await ctx.send(
                f"❌ Sync failed:\n`{error}`"
            )

    # ======================================
    # RESTART
    # ======================================

    @commands.command(name="restart")
    async def restart(
        self,
        ctx,
        confirmation: str = ""
    ):

        if confirmation.upper() != "CONFIRM":

            await ctx.send(
                "⚠️ This will stop the bot process.\n"
                "On Railway, the service must have automatic "
                "restart enabled.\n\n"
                "Use `!restart CONFIRM` to continue."
            )

            return

        await ctx.send(
            "♻️ Souvion AI is shutting down for restart..."
        )

        await asyncio.sleep(2)

        await self.bot.close()


# ==========================================
# SETUP
# ==========================================

async def setup(bot):

    await bot.add_cog(
        DeveloperCog(bot)
    )
