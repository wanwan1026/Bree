import discord
from discord.ext import commands
from config import BOT_TOKEN, guild_id as GUILD_ID

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

putty = commands.Bot(command_prefix='!', intents=intents)  # ✅ 不要用 '/'

INITIAL_EXTENSIONS = [
    "cogs.events",
    "cogs.commands_general",
]

@putty.event
async def setup_hook():
    for ext in INITIAL_EXTENSIONS:
        await putty.load_extension(ext)
        print(f"Loaded extension: {ext}")

    guild = discord.Object(id=GUILD_ID)

    # ✅ 清乾淨再同步，避免重複/殘留
    putty.tree.clear_commands(guild=guild)
    await putty.tree.sync(guild=guild)
    print("✅ Clean-synced app commands to guild")

if __name__ == "__main__":
    putty.run(BOT_TOKEN)
