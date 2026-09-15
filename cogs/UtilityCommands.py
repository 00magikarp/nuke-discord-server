import os
import sys

import dotenv
import discord
from discord.ext import commands

from extras.checks import check_admin

dotenv.load_dotenv()
TEST_GUILD_ID = os.getenv('TEST_GUILD')
LOCKDOWN_ROLE = os.getenv('LOCKDOWN_ROLE')
ANNOUNCEMENT_CHANNEL = os.getenv('ANNOUNCEMENT_CHANNEL')
testGuild = discord.Object(id=TEST_GUILD_ID)


class UtilityCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.in_lockdown: bool = False

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @discord.app_commands.command(
        name="ping",
        description="Check latency of bot"
    )
    async def ping(self, interaction: discord.Interaction) -> None:
        """
        Check the latency of the bot.

        :param interaction: The interaction object.
        """
        await interaction.response.send_message(
            f"""🏓 Pong!
{self.bot.latency * 1000:.1f}ms"""
        )

    @discord.app_commands.command(
        name="purge_channel",
        description="Purge the last number messages in this channel",
    )
    async def purge_channel(self, interaction: discord.Interaction, number: int) -> None:
        """
        Purge the last `messagesToDelete` messages in the channel

        :param interaction: The interaction object.
        :param number: Amount of messages to remove from the channel. Maximum is 250.
        """
        if not await check_admin(interaction):
            return

        if number > 250:
            number = 250

        await interaction.response.send_message("💥", ephemeral=True)
        await interaction.channel.purge(limit=number)

    @discord.app_commands.command(
        name="purge_user",
        description="Purge the last number messages by a user in this channel"
    )
    async def purge_user(self, interaction: discord.Interaction, user: discord.Member, number: int) -> None:
        """
        Purge the last `messagesToDelete` messages by the user. Only works in channel it's ran in.

        :param interaction: The interaction object.
        :param user: User to purge messages by.
        :param number: Amount of messages to remove from the channel. Maximum is 250.
        """
        if not await check_admin(interaction):
            return

        if number > 250:
            number = 250

        await interaction.response.send_message("💥", ephemeral=True)
        await interaction.channel.purge(limit=number, check=lambda m: m.author.id == user.id)

    @discord.app_commands.command(
        name="lockdown",
        description="Lockdown the server, no new messages or viewing channels",
    )
    async def lockdown(self, interaction: discord.Interaction) -> None:
        """
        Lockdown the server, no new messages or viewing channels

        :param interaction: The interaction object.
        """
        if not await check_admin(interaction):
            return

        if not self.in_lockdown:
            self.in_lockdown = True
            await interaction.response.send_message("Server has entered LOCKDOWN.")
            if interaction.channel_id != int(ANNOUNCEMENT_CHANNEL):
                await interaction.guild.get_channel(int(ANNOUNCEMENT_CHANNEL)).send("Server has entered LOCKDOWN.")
        else:
            self.in_lockdown = False
            await interaction.response.send_message("Server has exited LOCKDOWN.")
            if interaction.channel_id != int(ANNOUNCEMENT_CHANNEL):
                await interaction.guild.get_channel(int(ANNOUNCEMENT_CHANNEL)).send("Server has exited LOCKDOWN.")

        lockdown_role: discord.Role = interaction.guild.get_role(int(LOCKDOWN_ROLE))
        for user in interaction.guild.members:
            if self.in_lockdown and not user.bot:
                await user.add_roles(lockdown_role)
            elif not self.in_lockdown and not user.bot:
                await user.remove_roles(lockdown_role)


async def setup(bot):
    await bot.add_cog(UtilityCommands(bot))
