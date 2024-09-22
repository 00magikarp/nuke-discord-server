import asyncio
import logging
import enum
import os

import discord
import dotenv
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(name)s: %(message)s'))
logger.addHandler(handler)

dotenv.load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())
testGuild = discord.Object(id=os.getenv('TEST_GUILD'))  # for testing


class LoggerModes(enum.Enum):
    """
    Custom class to pass enum members into the :func:`log` function.

    Options for the mode are:
        :attr:`LoggerModes.INFO`

        :attr:`LoggerModes.WARNING`

        :attr:`LoggerModes.DEBUG`
    """
    INFO = 1
    WARNING = 2
    DEBUG = 3


def log(text: str, logger_mode: LoggerModes) -> None:
    """
    \"Custom\" Logger
    Prints to console and calls `logger.info`

    :param text: The text to be logged
    :param logger_mode: The mode of logging, from the enum object :class:`LoggerModes`
    """

    match logger_mode:
        case logger_mode.INFO:
            logger.info(text)
        case logger_mode.WARNING:
            logger.warning(text)
        case logger_mode.DEBUG:
            logger.debug(text)
        case _:
            logger.warning(f"Attempt to log [[{text}]] failed; defaulted to warning log")

    print(text)
    return


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename.endswith("Commands.py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            log(f"Loaded cog.{filename}", LoggerModes.INFO)


@bot.event
async def on_app_command_completion(interaction: discord.Interaction, command: discord.app_commands.Command) -> None:
    server = interaction.guild.name
    user = interaction.user

    log(f"[[{user}]] RAN [[{command.name}]] IN [[{server}]]", LoggerModes.INFO)


@bot.event
async def on_ready() -> None:
    await bot.wait_until_ready()
    await bot.tree.sync()

    log_text = f"Logged in as: {bot.user}"
    logger.info(log_text)
    print(log_text)


async def main():
    await load_extensions()
    await bot.start(token=BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
