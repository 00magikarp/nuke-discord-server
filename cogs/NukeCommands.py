import os
import dotenv
import discord
from discord.ext import commands

from extras.ConfirmDenyButtons import ConfirmDenyButtons
from extras.CheckAdmin import check_admin

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

    @discord.app_commands.command(
        name="channels",
        description="Nuke all channels"
    )
    async def channels(self, interaction: discord.Interaction) -> None:
        if not await check_admin(interaction):
            return

        choices = ConfirmDenyButtons()
        await interaction.response.send_message(
            embed=discord.Embed(title="Nuke channels?", color=discord.Color.red()),
            content="",
            view=choices
        )
        await choices.wait()

        if not choices.response:
            await interaction.followup.send("Canceled")
            return

        for channel in interaction.guild.channels:
            try:
                await channel.delete()
            except (discord.Forbidden, discord.NotFound, discord.HTTPException):
                continue

    @discord.app_commands.command(
        name="roles",
        description="Nuke all roles"
    )
    async def roles(self, interaction: discord.Interaction) -> None:
        if not await check_admin(interaction):
            return

        choices = ConfirmDenyButtons()
        await interaction.response.send_message(
            embed=discord.Embed(title="Nuke roles?", color=discord.Color.red()),
            content="",
            view=choices
        )
        await choices.wait()

        if not choices.response:
            await interaction.followup.send("Canceled")
            return

        for role in interaction.guild.roles:
            if not (role.permissions.administrator or role.name == "@everyone"):
                try:
                    await role.delete()
                except (discord.Forbidden, discord.HTTPException):
                    continue

        await interaction.followup.send("💥", ephemeral=True)

    @discord.app_commands.command(
        name="users",
        description="Nuke all users"
    )
    async def users(self, interaction: discord.Interaction) -> None:
        if not await check_admin(interaction):
            return

        choices = ConfirmDenyButtons()
        await interaction.response.send_message(
            embed=discord.Embed(title="Nuke users?", color=discord.Color.red()),
            content="",
            view=choices
        )
        await choices.wait()

        if not choices.response:
            await interaction.followup.send("Canceled")
            return

        for user in interaction.guild.members:
            if not user.guild_permissions.administrator:
                await user.ban()

        await interaction.followup.send("💥", ephemeral=True)

    @discord.app_commands.command(
        name="all",
        description="Nuke EVERYTHING! (channels, roles, users; this is not a joke!)"
    )
    async def all(self, interaction: discord.Interaction) -> None:
        if not await check_admin(interaction):
            return

        choices = ConfirmDenyButtons()
        await interaction.response.send_message(
            embed=discord.Embed(title="Nuke everything?", color=discord.Color.red()),
            content="",
            view=choices
        )
        await choices.wait()

        if not choices.response:
            await interaction.followup.send("Canceled")
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
