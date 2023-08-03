#導入 Discord.py           
import discord
from discord.ext import commands
import re
import time

from dotenv import load_dotenv
import os
load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# 設置您要監聽的頻道 ID
guild_id = os.getenv("guild_id") #伺服器 ID
CHANNEL_ID = os.getenv("CHANNEL_ID") #架上有幾盤布蕾
CHANNEL_ID2 = os.getenv("CHANNEL_ID2") #離開
CHANNEL_ID3 = os.getenv("CHANNEL_ID3") # ban
CHANNEL_ID4 = os.getenv("CHANNEL_ID4") #規則
CHANNEL_ID5 = os.getenv("CHANNEL_ID5") #指南
CHANNEL_ID6 = os.getenv("CHANNEL_ID6") #櫃台(新手詢問處)
CHANNEL_ID7 = os.getenv("CHANNEL_ID7") #自介
CHANNEL_ID8 = os.getenv("CHANNEL_ID8") #遊戲
CHANNEL_ID9 = os.getenv("CHANNEL_ID9") #身分
CHANNEL_ID10 = os.getenv("CHANNEL_ID10") #管理指令區
CHANNEL_ID11 = os.getenv("CHANNEL_ID11") #改名區

@bot.event
async def on_ready():
    print('目前登入身份：', bot.user)
    game = discord.Game('布丁布布丁 ! ')
    #discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await bot.change_presence(status=discord.Status.idle, activity=game)

@bot.event
async def on_message(message):

    # 確認訊息不是由機器人自己發送
    if message.author == bot.user:
        return
    
    # ----- BAN 掉發其他群鏈結的成員(^) -----

    # 獲取機器人所在伺服器的 ID
    bot_guild_id = guild_id

    # 如果消息是機器人所在伺服器的邀請連結，則忽略
    if message.guild.id == bot_guild_id and 'discord.gg/' in message.content:
        return       

    # 如果消息包含 Discord 伺服器邀請連結
    if 'discord.gg/' in message.content:
        if not message.author.guild_permissions.manage_messages:
            # 停權該成員
            await message.author.ban(reason="散布 Discord 伺服器邀請連結")
            # 刪除該訊息
            try:
                # 刪除該訊息
                await message.delete()
            except discord.NotFound:
                pass
            # 發送一條新訊息通知該成員已遭剔除
            await message.channel.send(f"{message.author.name} 因為不乖乖被布蕾吃掉了！")

    # 使用正規表達式檢查訊息是否包含 Line 群組邀請連結
    line_invitation_pattern = r"https://line.me/R/ti/g/"
    if re.search(line_invitation_pattern, message.content):
        if not message.author.guild_permissions.manage_messages:
            # 停權該成員
            await message.author.ban(reason="散布 Line 群組邀請連結")
            # 刪除該訊息
            try:
                # 刪除該訊息
                await message.delete()
            except discord.NotFound:
                pass
            # 發送一條新訊息通知該成員已遭剔除
            await message.channel.send(f"{message.author.name} 因為不乖乖被布蕾吃掉了！")

    # 使用正規表達式檢查訊息是否包含 LINE 社群邀請連結
    line_community_pattern = r"https://line.me/ti/g2/"
    if re.search(line_community_pattern, message.content):
        if not message.author.guild_permissions.manage_messages:
            # 停權該成員
            await message.author.ban(reason="散布 LINE 社群邀請連結")
            # 刪除該訊息
            try:
                # 刪除該訊息
                await message.delete()
            except discord.NotFound:
                pass
            # 發送一條新訊息通知該成員已遭剔除
            await message.channel.send(f"{message.author.name} 因為不乖乖被布蕾吃掉了！")

    # ----- BAN 掉發其他群鏈結的成員(v) -----

    # ----- 改名區(^) -----

    if message.channel.id == CHANNEL_ID11:

        # 輸入的文字
        user_input = message.content

        # 計算 prefix 和 suffix 的長度
        prefix = "‧˚✮₊"
        suffix = "ʕ̯•͡˔•̯᷅ʔ彡⁼³₌₃"
        total_length = len(prefix) + len(suffix)

        # 確保暱稱長度不超過 32 字元
        if len(user_input) + total_length > 32:
            reminder_message = "暱稱長度過長，請重新輸入。"
            await message.channel.send(reminder_message)
            return 
        new_member_name = user_input[:32 - total_length]

        # 重組暱稱
        new_nickname = prefix + new_member_name + suffix

        # 設置新成員的暱稱
        try:
            # 更改暱稱
            await message.author.edit(nick=new_nickname)
            await message.channel.send(f"已將您的暱稱更改為 {new_nickname}")          
            # # 從使用者身分組中移除一次性改名卡身分組
            rename_role = discord.utils.get(message.guild.roles, id=1135494950595874826)
            if rename_role:
                await message.author.remove_roles(rename_role)                
        except discord.errors.Forbidden:
            await message.channel.send("Bot 出現錯誤，請洽模組櫻花。")

    # ----- 改名區(v) -----

    # ----- 布蕾答案書(^) -----



    # ----- 布蕾答案書(v) -----

# 監聽成員加入事件
@bot.event
async def on_member_join(member):

    # 取得新成員的名稱和 ID
    new_member_name = member.display_name

    # 計算 prefix 和 suffix 的長度
    prefix = "‧˚✮₊"
    suffix = "ʕ̯•͡˔•̯᷅ʔ彡⁼³₌₃"
    total_length = len(prefix) + len(suffix)

    # 截斷 new_member_name，確保暱稱長度不超過 32 字元
    new_member_name = new_member_name[:32 - total_length]

    # 設置新成員的暱稱
    new_nickname = prefix + new_member_name + suffix
    await member.edit(nick=new_nickname)

    # 更新架上有幾盤布蕾
    guild = member.guild
    channel = bot.get_channel(CHANNEL_ID) 
    # 執行 update_channel_name 函式，限制每 5 分鐘執行一次
    global last_executed_time
    current_time = time.time()
    if current_time - last_executed_time >= 300:
        await update_channel_name(guild, channel)
        last_executed_time = current_time

# 監聽成員離開事件
@bot.event
async def on_member_remove(member):

    channel = bot.get_channel(CHANNEL_ID2)
    member_link = f"<@!{member.id}>"
    message = f"{member_link} 帶走了一盤布蕾ﾍ( ﾟ∀ﾟ;)ﾉ"
    await channel.send(message)

    # 更新架上有幾盤布蕾
    guild = member.guild
    channel = bot.get_channel(CHANNEL_ID) 
    # 執行 update_channel_name 函式，限制每 5 分鐘執行一次
    global last_executed_time
    current_time = time.time()
    if current_time - last_executed_time >= 300:
        await update_channel_name(guild, channel)
        last_executed_time = current_time
  

@bot.event
async def on_member_ban(guild, user):

    target_channel = bot.get_channel(CHANNEL_ID3)    
    w1_channel = bot.get_channel(CHANNEL_ID4)
    await target_channel.send(f"因 {user.name} 屢次違反伺服器 {w1_channel.mention} 故而送往報銷室報廢。")

# 記錄上一次執行 update_channel_name 的時間戳
last_executed_time = 0

async def update_channel_name(guild, channel):
    # 更新頻道名稱
    member_count = guild.member_count
    new_channel_name = f'架上有{member_count}盤布蕾'
    await channel.edit(name=new_channel_name)

#TOKEN 在剛剛 Discord Developer 那邊「BOT」頁面裡面
bot.run(os.getenv("BOT_TOKEN2")) #布蕾
