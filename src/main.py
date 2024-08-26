import asyncio
import logging
import os

import discord
import dotenv
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='../discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(name)s: %(message)s'))
logger.addHandler(handler)

dotenv.load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())
testGuild = discord.Object(id=os.getenv('TEST_GUILD'))  # for testing


@bot.event
async def on_ready() -> None:
    await bot.wait_until_ready()
    await bot.tree.sync()

    log_text = f"Logged in as: {bot.user}"
    logger.info(log_text)
    print(log_text)


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            log_text = f"Loaded {filename}"

            logger.info(log_text)
            print(log_text)


async def main():
    await load_extensions()
    await bot.start(token=BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
