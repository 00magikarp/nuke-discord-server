import os
import dotenv
import discord
from discord.ext import commands

dotenv.load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
TEST_GUILD = os.getenv('TEST_GUILD')

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())
testGuild = discord.Object(id=TEST_GUILD)


@bot.event
async def on_ready() -> None:
    await bot.tree.sync()
    print(f'Logged in as: {bot.user}')


@bot.event
async def on_message(message) -> None:
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


@bot.tree.command(
    name="echo",
    description="Repeat what you said",
    guild=testGuild
)
@discord.app_commands.describe(message="The message to echo")
async def echo(interaction: discord.Interaction, message: str) -> None:
    await interaction.response.send_message(message, ephemeral=True)


@bot.tree.command(
    name="ping",
    description="Check latency of bot",
    guild=testGuild
)
async def ping(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(
f"""🏓 Pong!
{bot.latency*1000:.0f}ms"""
    )

bot.run(BOT_TOKEN)
