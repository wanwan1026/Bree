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

ROLE_ID10 = int(os.getenv("ROLE_ID10")) # 銀
ROLE_ID11 = int(os.getenv("ROLE_ID11")) # 紫
ROLE_ID12 = int(os.getenv("ROLE_ID12")) # 金
ROLE_ID13 = int(os.getenv("ROLE_ID13")) # 一次改名
ROLE_ID14 = int(os.getenv("ROLE_ID14")) # 一次改名
CHANNEL_ID18 = int(os.getenv("CHANNEL_ID18")) # 集合囉!小櫻花
CHANNEL_ID20 = int(os.getenv("CHANNEL_ID20")) # 時光膠囊寄送
CHANNEL_ID21 = int(os.getenv("CHANNEL_ID21")) # 時光膠囊回收

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
    
    # ----- 時光抓訊息(^) -----

    if message.channel.id == CHANNEL_ID20:

        channel_act00 = putty.get_channel(CHANNEL_ID20)
        channel_act = putty.get_channel(CHANNEL_ID21)
        member_link = f"<@!{message.author.id}>"
        max_retries = 3  # 最大重試次數
        retry_delay = 5  # 重試之間的延遲（秒）

        for _ in range(max_retries):
            try:
                if message.content.startswith("<:No_011:1133635937855881367> 致 2025 的我："):
                    await channel_act00.send(f"{member_link} 感謝您的參與*ଘ(੭*ˊᗜˋ)੭* ੈ✧‧₊˚")
                    await channel_act.send(f"{member_link} 的時光訊息：\n{message.content}", files=[await f.to_file() for f in message.attachments])
                else:
                   await channel_act00.send(f"{member_link}\n請依照指定開頭發布唷ヽ( ^ω^ ゞ )\n指定開頭如下\n────────只是分隔線────────")
                   await channel_act00.send("<:No_011:1133635937855881367> 致 2025 的我：")
                await message.delete()
                break  # 成功後跳出循環
            except Exception as e:
                await asyncio.sleep(retry_delay)  # 等待一段時間後重試

    # ----- 時光抓訊息(v) -----
    
    if message.channel.id == CHANNEL_ID18:
        # 確保訊息不是由機器人發送且在指定頻道
        role_mention = f"<@&{ROLE_ID14}>"
        if message.content.startswith('╭⌕˚꒷ ͝ ꒦₍ᕱ.⑅.ᕱ₎꒦꒷ ͝ ꒦ ͝'):
            # 開啟討論串
            member_nick = message.author.nick or message.author.display_name
            thread = await message.create_thread(name=f"{member_nick}")
            await thread.send("布蕾布布蕾！\n布丁幫你創好專屬討論串囉\n結束之後記得講一聲喔")
            await message.channel.send(f"{role_mention}\n{member_nick}開啟新的揪團囉 ! ")
            # await message.reply(f"{role_mention}\n{member_nick} 已經開啟揪團")
        else:
            await message.delete()
            user = message.author
            await user.send(f"請複製以下發文格式才可以順利開啟揪團喔！\n另外此頻道是用來揪團並非閒聊，請注意使用方式！\n揪團頻道傳送門：https://discord.com/channels/1071783924998623253/1169289511788892190\n────────只是分隔線────────")
            await user.send("╭⌕˚꒷ ͝ ꒦₍ᕱ.⑅.ᕱ₎꒦꒷ ͝ ꒦ ͝\n꒰1๑ 項目：\nৎ2୭ 時間：\n꒰3๑ 人數：\nৎ4୭ 備註：\n꒰5๑ 語音房連結：\n╰ ꒷꒦꒷ ͝ ꒦₍ꐑxꐑ₎꒦ ͝ ꒷ ͝ ꒦")
        
    await putty.process_commands(message)

@putty.hybrid_command(name='hello', help='Greets the user')  
async def hello(ctx):
    await ctx.send('你好！')

putty.run(os.getenv("BOT_TOKEN1"))  # 布丁
