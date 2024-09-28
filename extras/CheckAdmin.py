import discord


async def check_admin(interaction: discord.Interaction) -> bool:
    """
    Check if the author of the command as administrator permissions in the guild,
    and sends an ephemeral message if they don't.

    :param interaction: The current :class:`discord.Interaction`
    :return: If the author has admin
    """

    if not interaction.permissions.administrator:
        await interaction.response.send_message("Hey! You can't run this command...", ephemeral=True)
        return False

    return True
