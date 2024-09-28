import os
import dotenv
import discord
from discord.ext import commands

from extras.CheckAdmin import check_admin

dotenv.load_dotenv()
TEST_GUILD_ID = os.getenv('TEST_GUILD')
testGuild = discord.Object(id=TEST_GUILD_ID)


class UtilityCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

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
        name="purge",
        description="Purge the last number commands in the channel",
    )
    async def purge(self, interaction: discord.Interaction, number: int) -> None:
        """
        Purge the last `messagesToDelete` commands in the channel

        :param interaction: The interaction object.
        :param number: Amount of messages to remove from the channel. Maximum is 100.
        """
        if not await check_admin(interaction):
            return

        if number > 100:
            number = 100

        await interaction.response.send_message("💥", ephemeral=True)
        await interaction.channel.purge(limit=number)


async def setup(bot):
    await bot.add_cog(UtilityCommands(bot))
