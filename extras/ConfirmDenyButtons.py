import discord


class ConfirmDenyButtons(discord.ui.View):
    """
    Custom buttons class for confirming/denying actions made by the bot.

    Changes :attr:`self.response` to `True` if "Confirm" button is clicked,
    and :attr:`self.response` to `False` if "Nevermind" button is clicked.
    """
    def __init__(self, *, timeout=60):
        super().__init__(timeout=timeout)
        self.response = None

    @discord.ui.button(
        label="Confirm",
        style=discord.ButtonStyle.green
    )
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.response = True

        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.button(
        label="Nevermind",
        style=discord.ButtonStyle.red
    )
    async def deny_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.response = False

        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)
        self.stop()
