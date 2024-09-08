import os
import dotenv
import discord
from discord.ext import commands

dotenv.load_dotenv()
TEST_GUILD_ID = os.getenv('TEST_GUILD')
testGuild = discord.Object(id=TEST_GUILD_ID)


class NukeCommands(commands.GroupCog, name="nuke", description="Nuke commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @staticmethod
    async def check_admin(interaction: discord.Interaction) -> bool:
        """
        Check if the author of the command as administrator permissions in the guild,
        and sends an ephemeral message if they don't.

        :param interaction: The current discord.Interaction
        :return: True if the author has admin
        """

        if not interaction.permissions.administrator:
            await interaction.response.send_message("Hey! You can't run this command...", ephemeral=True)
            return False

        return True

    @discord.app_commands.command(
        name="channels",
        description="Nuke all channels"
    )
    async def channels(self, interaction: discord.Interaction) -> None:
        if not await self.check_admin(interaction):
            return

        for channel in interaction.guild.channels:
            try:
                await channel.delete()
            except Exception as e:
                print(e)

    @discord.app_commands.command(
        name="roles",
        description="Nuke all roles"
    )
    async def roles(self, interaction: discord.Interaction) -> None:
        if not await self.check_admin(interaction):
            return

        for role in interaction.guild.roles:
            if not (role.permissions.administrator or role.name == "@everyone"):
                try:
                    await role.delete()
                except Exception as e:
                    print(e)

        await interaction.response.send_message("💥", ephemeral=True)

    @discord.app_commands.command(
        name="users",
        description="Nuke all users"
    )
    async def users(self, interaction: discord.Interaction) -> None:
        if not await self.check_admin(interaction):
            return

        for user in interaction.guild.members:
            if not user.guild_permissions.administrator:
                await user.ban()

        await interaction.response.send_message("💥", ephemeral=True)

    @discord.app_commands.command(
        name="all",
        description="Nuke EVERYTHING! (channels, roles, users; this is not a joke!)"
    )
    async def all(self, interaction: discord.Interaction) -> None:
        if not await self.check_admin(interaction):
            return

        for channel in interaction.guild.channels:
            try:
                await channel.delete()
            except Exception as e:
                print(e)

        for role in interaction.guild.roles:
            if not (role.permissions.administrator or role.name == "@everyone"):
                try:
                    await role.delete()
                except Exception as e:
                    print(e)

        for user in interaction.guild.members:
            if not user.guild_permissions.administrator:
                await user.ban()


async def setup(bot):
    await bot.add_cog(NukeCommands(bot))
