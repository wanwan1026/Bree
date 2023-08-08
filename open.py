#導入 Discord.py           
import discord
from discord.ext import commands
import re
import time
import json
import random

from dotenv import load_dotenv
import os
load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# 設置您要監聽的頻道 ID
guild_id = int(os.getenv("guild_id")) #伺服器 ID
CHANNEL_ID = int(os.getenv("CHANNEL_ID")) #架上有幾盤布蕾
CHANNEL_ID2 = int(os.getenv("CHANNEL_ID2")) #離開
CHANNEL_ID3 = int(os.getenv("CHANNEL_ID3")) # ban
CHANNEL_ID4 = int(os.getenv("CHANNEL_ID4")) #規則
CHANNEL_ID5 = int(os.getenv("CHANNEL_ID5")) #指南
CHANNEL_ID6 = int(os.getenv("CHANNEL_ID6")) #櫃台(新手詢問處)
CHANNEL_ID7 = int(os.getenv("CHANNEL_ID7")) #自介
CHANNEL_ID8 = int(os.getenv("CHANNEL_ID8")) #遊戲
CHANNEL_ID9 = int(os.getenv("CHANNEL_ID9")) #身分
CHANNEL_ID10 = int(os.getenv("CHANNEL_ID10")) #管理指令區
CHANNEL_ID11 = int(os.getenv("CHANNEL_ID11")) #改名區
CHANNEL_ID12 = int(os.getenv("CHANNEL_ID12")) #改名區
id_card = int(os.getenv("id_card")) #一次改名卡

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
            # 從使用者身分組中移除一次性改名卡身分組
            rename_role = discord.utils.get(message.guild.roles, id=id_card)
            if rename_role:
                await message.author.remove_roles(rename_role)                
        except discord.errors.Forbidden:
            await message.channel.send("Bot 出現錯誤，請洽模組櫻花。")

    # ----- 改名區(v) -----

    # ----- 布蕾答案書(^) -----

    if message.channel.id == CHANNEL_ID12:
        context = classify_dialogue(message)
        data_folder = "data"
        json_file_name = context
        json_file_path = os.path.join(data_folder, json_file_name)

        try:
            json_data = read_json_file(json_file_path)
            num_answers = len(json_data)
            random_number = random.randint(1, num_answers)
            selected_answer = json_data[str(random_number)]["answer"]

            await message.channel.send(selected_answer)
        except FileNotFoundError:
            await message.channel.send("找不到指定的 JSON 檔案：file1.json")
        except json.JSONDecodeError:
            await message.channel.send("無法解析 JSON 檔案：file1.json")

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

    embed = discord.Embed(color=discord.Color(0xFFB6C1))
    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    embed.set_author(name=member.display_name, icon_url=avatar_url)
    # embed.set_thumbnail(url=avatar_url)  # Use member.avatar.url to get the avatar URL.
    embed.set_image(url=avatar_url)
    embed.add_field(name='使用者名稱', value=member.display_name, inline=True)
    embed.add_field(name='加好友 ID', value=f"{member.name}#{member.discriminator}", inline=True)
    embed.add_field(name='自訂狀態', value=member.activity.name if member.activity else '無', inline=False)
    embed.add_field(name='Nitro', value=member.premium_since, inline=False)
    locale = member.guild.preferred_locale
    embed.add_field(name='語言', value=locale, inline=False)    
    sorted_roles = sorted(member.roles, key=lambda role: role.position, reverse=True)
    roles_ids = [f"<@&{role.id}>" if role.id != CHANNEL_ID2 else '無' for role in sorted_roles]
    roles_str = '\n'.join(roles_ids)
    embed.add_field(name='擁有角色', value=roles_str, inline=False)
    embed.add_field(name='加入伺服器時間', value=member.joined_at, inline=False)
    embed.add_field(name='建立 Discord 帳號時間', value=member.created_at, inline=False)

    
    member_link = f"<@!{member.id}>"
    message = f"{member_link} 帶走了一盤布蕾ﾍ( ﾟ∀ﾟ;)ﾉ"
    await channel.send(content=message,embed=embed)

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

def read_json_file(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as f:
        data = json.load(f)
    return data

# 定義關鍵字的情境分類和對應的 JSON 檔案
keywords = {
    "ask.json": ["請問","嗎","為甚麼","怎麼","可以問個問題嗎", "有事想問"],    
    "greet.json": ["你好", "嗨", "哈囉", "Hello", "Hi", "您好"],
    "thanks.json": ["謝謝", "感謝", "多謝"],
    "like.json": ["喜歡布蕾"],
    "hat.json": ["討厭布蕾","不喜歡布蕾"],
}

# 根據對話中的關鍵字分類情境
def classify_dialogue(message):
    for context, keywords_list in keywords.items():
        for keyword in keywords_list:
            if keyword in message.content:
                return context
    return "ask.json"  # 預設為 "ask" 情境

#TOKEN 在剛剛 Discord Developer 那邊「BOT」頁面裡面
bot.run(os.getenv("BOT_TOKEN2")) #布蕾
