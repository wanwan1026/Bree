import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

print(discord.__version__)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  
putty = commands.Bot(command_prefix='/', intents=intents)

@putty.event
async def on_ready():
    try:
        synced = await putty.tree.sync()
        print(f"Synced {synced} commands")
    except Exception as e:
        print("An error occurred while syncing: ", e)
    print('目前登入身份：', putty.user)
    game = discord.Game('布蕾布布蕾 ! ')
    #discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await putty.change_presence(status=discord.Status.idle, activity=game)

@putty.event
async def on_message(message):
    if message.author.bot:

        return 
    
    await putty.process_commands(message)

@putty.hybrid_command(name='hello', help='Greets the user')  
async def hello(ctx):
    await ctx.send('你好！')

putty.run(os.getenv("BOT_TOKEN1"))  # 布丁
