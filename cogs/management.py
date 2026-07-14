from __future__ import annotations

import datetime as dt

import discord
from discord import app_commands
from discord.ext import commands


class Management(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="help", description="Show the available management commands.")
    async def help(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title="Server Management Commands", color=discord.Color.blurple())
        embed.add_field(name="General", value="/ping, /serverinfo, /userinfo", inline=False)
        embed.add_field(name="Moderation", value="/purge, /kick, /ban, /unban, /timeout, /untimeout", inline=False)
        embed.add_field(name="Channels", value="/slowmode, /lock, /unlock, /topic, /renamechannel, /createchannel, /deletechannel", inline=False)
        embed.add_field(name="Roles and Members", value="/nick, /roleadd, /roleremove, /createrole, /deleterole", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="ping", description="Check bot latency.")
    async def ping(self, interaction: discord.Interaction) -> None:
        latency_ms = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong: {latency_ms}ms", ephemeral=True)

    @app_commands.command(name="serverinfo", description="Show information about this server.")
    async def serverinfo(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return

        embed = discord.Embed(title=guild.name, color=discord.Color.blurple())
        embed.add_field(name="Members", value=str(guild.member_count or 0), inline=True)
        embed.add_field(name="Roles", value=str(len(guild.roles)), inline=True)
        embed.add_field(name="Channels", value=str(len(guild.channels)), inline=True)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="userinfo", description="Show information about a member.")
    @app_commands.describe(member="The member to inspect")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member | None = None) -> None:
        member = member or interaction.user  # type: ignore[assignment]

        embed = discord.Embed(title=str(member), color=discord.Color.green())
        embed.add_field(name="ID", value=str(member.id), inline=True)
        embed.add_field(name="Joined", value=member.joined_at.isoformat() if getattr(member, "joined_at", None) else "Unknown", inline=True)
        embed.add_field(name="Created", value=member.created_at.isoformat(), inline=True)
        if isinstance(member, discord.Member) and member.display_avatar:
            embed.set_thumbnail(url=member.display_avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="purge", description="Delete a number of messages from the current channel.")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(amount="How many messages to delete")
    async def purge(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]) -> None:
        if interaction.channel is None or not isinstance(interaction.channel, discord.TextChannel):
            await interaction.response.send_message("This command can only be used in a text channel.", ephemeral=True)
            return

        deleted = await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"Deleted {len(deleted)} messages.", ephemeral=True)

    @app_commands.command(name="kick", description="Kick a member from the server.")
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.describe(member="The member to kick", reason="Reason for the action")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str | None = None) -> None:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"Kicked {member.mention}.", ephemeral=True)

    @app_commands.command(name="ban", description="Ban a member from the server.")
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.describe(member="The member to ban", reason="Reason for the action", delete_message_days="Delete recent message history")
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str | None = None,
        delete_message_days: app_commands.Range[int, 0, 7] = 0,
    ) -> None:
        await member.ban(reason=reason, delete_message_days=delete_message_days)
        await interaction.response.send_message(f"Banned {member.mention}.", ephemeral=True)

    @app_commands.command(name="unban", description="Unban a user by ID.")
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.describe(user_id="The Discord user ID to unban", reason="Reason for the action")
    async def unban(self, interaction: discord.Interaction, user_id: str, reason: str | None = None) -> None:
        try:
            target_id = int(user_id)
        except ValueError:
            await interaction.response.send_message("Please provide a valid numeric user ID.", ephemeral=True)
            return

        if interaction.guild is None:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return

        user = discord.Object(id=target_id)
        await interaction.guild.unban(user, reason=reason)
        await interaction.response.send_message(f"Unbanned user ID {target_id}.", ephemeral=True)

    @app_commands.command(name="timeout", description="Timeout a member for a period of minutes.")
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.describe(member="The member to timeout", minutes="Duration in minutes", reason="Reason for the action")
    async def timeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        minutes: app_commands.Range[int, 1, 40320],
        reason: str | None = None,
    ) -> None:
        until = dt.datetime.now(dt.UTC) + dt.timedelta(minutes=minutes)
        await member.timeout(until, reason=reason)
        await interaction.response.send_message(f"Timed out {member.mention} for {minutes} minute(s).", ephemeral=True)

    @app_commands.command(name="untimeout", description="Remove a member timeout.")
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.describe(member="The member to clear", reason="Reason for the action")
    async def untimeout(self, interaction: discord.Interaction, member: discord.Member, reason: str | None = None) -> None:
        await member.timeout(None, reason=reason)
        await interaction.response.send_message(f"Removed timeout from {member.mention}.", ephemeral=True)

    @app_commands.command(name="slowmode", description="Set slowmode for the current channel.")
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.describe(seconds="Slowmode delay in seconds")
    async def slowmode(self, interaction: discord.Interaction, seconds: app_commands.Range[int, 0, 21600]) -> None:
        channel = interaction.channel
        if channel is None or not hasattr(channel, "edit"):
            await interaction.response.send_message("This command can only be used in a channel.", ephemeral=True)
            return

        await channel.edit(slowmode_delay=seconds)
        await interaction.response.send_message(f"Set slowmode to {seconds} second(s).", ephemeral=True)

    @app_commands.command(name="lock", description="Lock the current channel for @everyone.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction) -> None:
        channel = interaction.channel
        if interaction.guild is None or not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message("This command can only be used in a text channel.", ephemeral=True)
            return

        await channel.set_permissions(interaction.guild.default_role, send_messages=False)
        await interaction.response.send_message(f"Locked {channel.mention}.", ephemeral=True)

    @app_commands.command(name="unlock", description="Unlock the current channel for @everyone.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction) -> None:
        channel = interaction.channel
        if interaction.guild is None or not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message("This command can only be used in a text channel.", ephemeral=True)
            return

        await channel.set_permissions(interaction.guild.default_role, send_messages=None)
        await interaction.response.send_message(f"Unlocked {channel.mention}.", ephemeral=True)

    @app_commands.command(name="topic", description="Set the topic for the current text channel.")
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.describe(topic="The new topic text")
    async def topic(self, interaction: discord.Interaction, topic: str) -> None:
        channel = interaction.channel
        if not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message("This command can only be used in a text channel.", ephemeral=True)
            return

        await channel.edit(topic=topic)
        await interaction.response.send_message(f"Updated the topic for {channel.mention}.", ephemeral=True)

    @app_commands.command(name="renamechannel", description="Rename the current channel.")
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.describe(name="The new channel name")
    async def renamechannel(self, interaction: discord.Interaction, name: str) -> None:
        channel = interaction.channel
        if channel is None or not hasattr(channel, "edit"):
            await interaction.response.send_message("This command can only be used in a channel.", ephemeral=True)
            return

        await channel.edit(name=name)
        await interaction.response.send_message(f"Renamed the channel to {name}.", ephemeral=True)

    @app_commands.command(name="createchannel", description="Create a new text channel in the server.")
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.describe(name="Channel name", category="Optional category name", topic="Optional topic")
    async def createchannel(
        self,
        interaction: discord.Interaction,
        name: str,
        category: str | None = None,
        topic: str | None = None,
    ) -> None:
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return

        category_channel = discord.utils.get(guild.categories, name=category) if category else None
        new_channel = await guild.create_text_channel(name=name, category=category_channel, topic=topic)
        await interaction.response.send_message(f"Created {new_channel.mention}.", ephemeral=True)

    @app_commands.command(name="deletechannel", description="Delete the current channel.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def deletechannel(self, interaction: discord.Interaction) -> None:
        channel = interaction.channel
        if channel is None or not hasattr(channel, "delete"):
            await interaction.response.send_message("This command can only be used in a channel.", ephemeral=True)
            return

        await interaction.response.send_message("Deleting this channel.", ephemeral=True)
        await channel.delete()

    @app_commands.command(name="nick", description="Set a server nickname for a member.")
    @app_commands.checks.has_permissions(manage_nicknames=True)
    @app_commands.describe(member="The member to update", nickname="The new nickname")
    async def nick(self, interaction: discord.Interaction, member: discord.Member, nickname: str | None = None) -> None:
        await member.edit(nick=nickname)
        if nickname:
            await interaction.response.send_message(f"Changed {member.mention}'s nickname to {nickname}.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Cleared {member.mention}'s nickname.", ephemeral=True)

    @app_commands.command(name="roleadd", description="Add a role to a member.")
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.describe(member="The member to update", role="The role to add")
    async def roleadd(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role) -> None:
        await member.add_roles(role)
        await interaction.response.send_message(f"Added {role.mention} to {member.mention}.", ephemeral=True)

    @app_commands.command(name="roleremove", description="Remove a role from a member.")
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.describe(member="The member to update", role="The role to remove")
    async def roleremove(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role) -> None:
        await member.remove_roles(role)
        await interaction.response.send_message(f"Removed {role.mention} from {member.mention}.", ephemeral=True)

    @app_commands.command(name="createrole", description="Create a new role.")
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.describe(name="Role name", hoist="Show role members separately", mentionable="Allow @role mentions")
    async def createrole(
        self,
        interaction: discord.Interaction,
        name: str,
        hoist: bool = False,
        mentionable: bool = False,
    ) -> None:
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return

        role = await guild.create_role(name=name, hoist=hoist, mentionable=mentionable)
        await interaction.response.send_message(f"Created {role.mention}.", ephemeral=True)

    @app_commands.command(name="deleterole", description="Delete a role.")
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.describe(role="The role to delete")
    async def deleterole(self, interaction: discord.Interaction, role: discord.Role) -> None:
        await role.delete()
        await interaction.response.send_message(f"Deleted {role.name}.", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Management(bot))
