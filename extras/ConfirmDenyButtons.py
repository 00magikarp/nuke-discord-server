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
    async def confirm_button(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        button.disabled = True
        self.response = True
        self.stop()

    @discord.ui.button(
        label="Nevermind",
        style=discord.ButtonStyle.red
    )
    async def confirm_button(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        button.disabled = True
        self.response = False
        self.stop()
