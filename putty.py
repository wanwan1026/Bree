import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import json
import asyncio

load_dotenv()

print(discord.__version__)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  
putty = commands.Bot(command_prefix='/', intents=intents)

CHANNEL_ID18 = int(os.getenv("CHANNEL_ID18")) # 揪團頻道
ROLE_ID10 = int(os.getenv("ROLE_ID10")) # 銀
ROLE_ID11 = int(os.getenv("ROLE_ID11")) # 紫
ROLE_ID12 = int(os.getenv("ROLE_ID12")) # 金
ROLE_ID13 = int(os.getenv("ROLE_ID13")) # 一次改名
ROLE_ID14 = int(os.getenv("ROLE_ID14")) # 揪團

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
    
    if message.channel.id == CHANNEL_ID18:
        # 確保訊息不是由機器人發送且在指定頻道

        # 開啟討論串
        role_mention = f"<@&{ROLE_ID14}>"
        member_nick = message.author.nick or message.author.display_name
        thread = await message.create_thread(name=f"{member_nick}")
        await thread.send("布蕾布布蕾！\n布丁幫你創好專屬討論串囉\n結束之後記得講一聲喔")
        await message.channel.send(f"{role_mention}\n{member_nick}開啟新的揪團囉 ! ")
        # await message.reply(f"{role_mention}\n{member_nick} 已經開啟揪團")

        
    await putty.process_commands(message)

@putty.hybrid_command(name='hello', help='Greets the user')  
async def hello(ctx):
    await ctx.send('你好！')

putty.run(os.getenv("BOT_TOKEN1"))  # 布丁
