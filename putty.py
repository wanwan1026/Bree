# putty.py
import discord
from discord.ext import commands

from config import BOT_TOKEN  # 從 config 拿 token

print(discord.__version__)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

putty = commands.Bot(command_prefix='/', intents=intents)

# 要載入的 cogs
INITIAL_EXTENSIONS = [
    "cogs.events",
    "cogs.commands_general",
]


@putty.event
async def setup_hook():
    """
    discord.py 2.x 推薦在這裡 load_extension
    這樣在 bot 啟動前就會把 Cog 載好
    """
    for ext in INITIAL_EXTENSIONS:
        try:
            await putty.load_extension(ext)
            print(f"Loaded extension: {ext}")
        except Exception as e:
            print(f"Failed to load extension {ext}: {e}")


if __name__ == "__main__":
    putty.run(BOT_TOKEN)
