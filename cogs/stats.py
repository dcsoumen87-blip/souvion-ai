
import os

import discord
from discord.ext import commands, tasks


STATS_CHANNEL_ID = int(os.getenv("STATS_CHANNEL_ID", "0"))


class StatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stats_message = None
        self.presence_index = 0

    def get_counts(self):
        servers = len(self.bot.guilds)

        # Add each server's member count.
        # Members in multiple servers are counted multiple times.
        members = sum(
            guild.member_count or len(guild.members)
            for guild in self.bot.guilds
        )

        return servers, members

    async def update_presence(self):
        if not self.bot.is_ready():
            return

        servers, members = self.get_counts()

        activities = [
            discord.Activity(
                type=discord.ActivityType.watching,
                name="Developer MOD TRYOUT"
            ),
            discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{members:,} members"
            ),
            discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{servers:,} servers"
            ),
        ]

        activity = activities[self.presence_index]

        await self.bot.change_presence(
            status=discord.Status.online,
            activity=activity
        )

        self.presence_index = (
            self.presence_index + 1
        ) % len(activities)

    def make_embed(self):
        servers, members = self.get_counts()

        embed = discord.Embed(
            title="🤖 Souvion AI — Live Statistics",
            description="Live bot reach across Discord.",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="👑 Developer",
            value="MOD TRYOUT",
            inline=False
        )

        embed.add_field(
            name="🌐 Servers",
            value=f"**{servers:,}**",
            inline=True
        )

        embed.add_field(
            name="👥 Members Served",
            value=f"**{members:,}**",
            inline=True
        )

        embed.set_footer(
            text="Souvion AI • Automatically updated"
        )

        return embed

    async def update_embed(self):
        if not self.bot.is_ready() or not STATS_CHANNEL_ID:
            return

        channel = self.bot.get_channel(STATS_CHANNEL_ID)

        if channel is None:
            try:
                channel = await self.bot.fetch_channel(
                    STATS_CHANNEL_ID
                )
            except discord.HTTPException as error:
                print(f"[STATS] Could not find channel: {error}")
                return

        if not hasattr(channel, "history"):
            print("[STATS] Configured channel is not a text channel.")
            return

        embed = self.make_embed()

        try:
            # Edit the existing message when possible.
            if self.stats_message is not None:
                try:
                    await self.stats_message.edit(embed=embed)
                    return
                except discord.NotFound:
                    self.stats_message = None
                except discord.HTTPException:
                    self.stats_message = None

            # Find the previous message after a restart.
            async for message in channel.history(limit=50):
                if (
                    message.author.id == self.bot.user.id
                    and message.embeds
                    and message.embeds[0].title
                    == "🤖 Souvion AI — Live Statistics"
                ):
                    self.stats_message = message
                    await message.edit(embed=embed)
                    print("[STATS] Existing stats message updated.")
                    return

            # Create a message if none exists.
            self.stats_message = await channel.send(embed=embed)
            print("[STATS] Stats message created.")

        except discord.Forbidden:
            print(
                "[STATS] Missing permissions. Allow View Channel, "
                "Read Message History, Send Messages and Embed Links."
            )
        except discord.HTTPException as error:
            print(f"[STATS] Embed update failed: {error}")

    async def refresh_all(self):
        await self.update_presence()
        await self.update_embed()

    @tasks.loop(seconds=15)
    async def rotate_presence(self):
        await self.update_presence()

    @rotate_presence.before_loop
    async def before_rotate_presence(self):
        await self.bot.wait_until_ready()

    @tasks.loop(minutes=10)
    async def refresh_stats(self):
        await self.update_embed()

    @refresh_stats.before_loop
    async def before_refresh_stats(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.update_embed()

        if not self.rotate_presence.is_running():
            self.rotate_presence.start()

        if not self.refresh_stats.is_running():
            self.refresh_stats.start()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"[STATS] Joined server: {guild.name}")
        await self.refresh_all()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        print(f"[STATS] Removed from server: {guild.name}")
        await self.refresh_all()


async def setup(bot):
    await bot.add_cog(StatsCog(bot))
      
