import os
import dotenv
import discord
from discord.ext import commands

dotenv.load_dotenv()
TEST_GUILD_ID = os.getenv('TEST_GUILD')
testGuild = discord.Object(id=TEST_GUILD_ID)


class UtilityCommands(commands.Cog):
    def __init__(self, bot):
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


async def setup(bot):
    await bot.add_cog(UtilityCommands(bot))
