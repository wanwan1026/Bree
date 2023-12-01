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

COLOR_ID1 = int(os.getenv("COLOR_ID1"))
COLOR_ID2 = int(os.getenv("COLOR_ID2"))
COLOR_ID3 = int(os.getenv("COLOR_ID3"))
COLOR_ID4 = int(os.getenv("COLOR_ID4"))
COLOR_ID5 = int(os.getenv("COLOR_ID5"))
COLOR_ID6 = int(os.getenv("COLOR_ID6"))
COLOR_ID7 = int(os.getenv("COLOR_ID7"))
COLOR_ID8 = int(os.getenv("COLOR_ID8"))
COLOR_ID9 = int(os.getenv("COLOR_ID9"))
COLOR_ID10 = int(os.getenv("COLOR_ID10"))
COLOR_ID11 = int(os.getenv("COLOR_ID11"))
COLOR_ID12 = int(os.getenv("COLOR_ID12"))
COLOR_ID13 = int(os.getenv("COLOR_ID13"))
COLOR_ID14 = int(os.getenv("COLOR_ID14"))
COLOR_ID15 = int(os.getenv("COLOR_ID15"))
COLOR_ID16 = int(os.getenv("COLOR_ID16"))
COLOR_ID17 = int(os.getenv("COLOR_ID17"))
COLOR_ID18 = int(os.getenv("COLOR_ID18"))
COLOR_ID19 = int(os.getenv("COLOR_ID19"))
COLOR_ID20 = int(os.getenv("COLOR_ID20"))
COLOR_MES = int(os.getenv("COLOR_MES"))
COLOR_MEMBER = int(os.getenv("COLOR_MEMBER"))

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


emoji_roles = {
    "🌺":COLOR_ID1, 
    "🍑":COLOR_ID2, 
    "💗":COLOR_ID3, 
    "🎀":COLOR_ID4, 
    "🍊":COLOR_ID5,
    "🌞":COLOR_ID6, 
    "🌕":COLOR_ID7, 
    "🌿":COLOR_ID8, 
    "🍏":COLOR_ID9, 
    "🍀":COLOR_ID10,
    "🐳":COLOR_ID11, 
    "🌧️":COLOR_ID12, 
    "🌀":COLOR_ID13, 
    "📘":COLOR_ID14, 
    "🍇":COLOR_ID15,
    "🍆":COLOR_ID16, 
    "💜":COLOR_ID17, 
    "🔮":COLOR_ID18, 
    "🦔":COLOR_ID19, 
    "🌚":COLOR_ID20
}

pt_mess = COLOR_MES
pt_member = COLOR_MEMBER

processing = False

@putty.event
async def on_raw_reaction_add(payload):
    # 確保反應發生在指定的訊息上
    if payload.message_id == pt_mess:
        global processing

        # 檢查是否處於處理中，如果是，忽略並清除該成員的表情反應
        if processing:
            guild = putty.get_guild(payload.guild_id)
            member2 = guild.get_member(payload.user_id)
            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.remove_reaction(payload.emoji, member2)
            print(f"Ignored rapid click for {member2.display_name}")
            return

        # 將處理中設為 True，表示開始處理
        processing = True

        try:
            guild = putty.get_guild(payload.guild_id)
            member = guild.get_member(pt_member)
            member2 = guild.get_member(payload.user_id)

            # 檢查反應的表情符號是否在映射中
            emoji = str(payload.emoji)

            if emoji in emoji_roles:
                await clear_member_roles(member)
                role_id = emoji_roles[emoji]

                # 根據身分組的 ID 查找身分組
                role = discord.utils.get(guild.roles, id=int(role_id))
                
                # 確保身份組存在並給予成員
                if role:
                    await member.add_roles(role)
                    channel = guild.get_channel(payload.channel_id)
                    message = await channel.fetch_message(payload.message_id)
                    await message.remove_reaction(payload.emoji, member2)
                    print(f'Added role {role.name} to {member.display_name}')
                else:
                    print(f"Error - Role with ID {role_id} not found.")
        finally:
            # 處理完畢後，將 reset_processing 設為 True，表示處理結束
            putty.loop.create_task(reset_processing())

# 處理完畢後，過一段時間將處理中設為 False，以避免長時間處於處理中狀態
async def reset_processing():
    await asyncio.sleep(1)  # 5 秒後將處理中設為 False
    global processing
    processing = False

async def clear_member_roles(member):
    # 清除成員在 emoji_roles 內包含的現有身份組
    for emoji, role_id in emoji_roles.items():
        role = member.guild.get_role(int(role_id))
        if role and role in member.roles:
            await member.remove_roles(role)
            print(f'Removed role {role.name} from {member.display_name}')

@putty.hybrid_command(name='hello', help='Greets the user')  
async def hello(ctx):
    await ctx.send('你好！')

putty.run(os.getenv("BOT_TOKEN1"))  # 布丁
