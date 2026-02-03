import os
import discord
from discord.ext import commands
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # needed to read message text
bot = commands.Bot(command_prefix="!", intents=intents)

client = discord.Client(intents=intents)

@bot.command()
async def ping(ctx: commands.Context):
    await ctx.send("pong")

@bot.tree.command(name="ping", description="Responds with pong")
async def slash_ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (id={bot.user.id})")

    GUILD_ID = 123456789012345678
    guild = discord.Object(id=GUILD_ID)

    bot.tree.copy_global_to(guild=guild)
    synced = await bot.tree.sync(guild=guild)
    print(f"Synced {len(synced)} slash command(s) to guild {GUILD_ID}")


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (id={client.user.id})")

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    if message.content == "!ping":
        await message.channel.send("pong")

client.run(TOKEN)
