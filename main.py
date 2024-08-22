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
{bot.latency * 1000:.0f}ms"""
    )


@bot.tree.command(
    name="delete_all_channels",
    description="Delete all the channels in this server",
    guild=testGuild
)
async def delete_all_channels(interaction: discord.Interaction) -> None:
    for channel in interaction.guild.channels:
        await channel.delete()

    await interaction.response.send_message("💥", ephemeral=True)


@bot.tree.command(
    name="delete_all_roles",
    description="Delete all the roles in this server",
    guild=testGuild
)
async def delete_all_channels(interaction: discord.Interaction) -> None:
    print([role.name for role in interaction.guild.roles])
    for role in interaction.guild.roles:
        if role.name == "Nuker Bot" or role.name == "@everyone":
            continue
        await role.delete()

    await interaction.response.send_message("💥", ephemeral=True)


@bot.tree.command(
    name="ban_users",
    description="Ban all users in the server",
    guild=testGuild
)
async def ban_users(interaction: discord.Interaction) -> None:
    for user in interaction.guild.members:
        if user.guild_permissions.administrator:
            continue

        await user.ban()

    await interaction.response.send_message("💥", ephemeral=True)


bot.run(BOT_TOKEN)
