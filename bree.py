#導入 Discord.py           
import discord
from discord.ext import commands
import re
import time
import json
import random
import asyncio
import psutil
from datetime import datetime

from dotenv import load_dotenv
import os
load_dotenv()

intents = discord.Intents.all()
bree = commands.Bot(command_prefix='!', intents=intents)

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
CHANNEL_ID13 = int(os.getenv("CHANNEL_ID13")) # ban 留存
CHANNEL_ID14 = int(os.getenv("CHANNEL_ID14")) # 自介發布
CHANNEL_ID15 = int(os.getenv("CHANNEL_ID15")) # 自介留存
CHANNEL_ID17 = int(os.getenv("CHANNEL_ID17")) # 流水麵線
id_card = int(os.getenv("id_card")) #一次改名卡

ROLE_ID1 = int(os.getenv("ROLE_ID1")) 
ROLE_ID2 = int(os.getenv("ROLE_ID2")) 
ROLE_ID3 = int(os.getenv("ROLE_ID3")) 
ROLE_ID4 = int(os.getenv("ROLE_ID4")) 
ROLE_ID5 = int(os.getenv("ROLE_ID5")) 
ROLE_ID6 = int(os.getenv("ROLE_ID6")) 
ROLE_ID7 = int(os.getenv("ROLE_ID7")) 
ROLE_ID8 = int(os.getenv("ROLE_ID8")) 
ROLE_ID9 = int(os.getenv("ROLE_ID9")) 

@bree.event
async def on_ready():
    print('目前登入身份：', bree.user)
    game = discord.Game('布丁布布丁 ! ')
    #discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await bree.change_presence(status=discord.Status.idle, activity=game)

# 紀錄最后一次使用改名功能的時間的字典
last_rename_time = {}

@bree.event
async def on_message(message):

    # 確認訊息不是由機器人自己發送
    if message.author == bree.user:
        return
    
    # 私訊
    if message.guild is None:
        return
    
    # ----- BAN 掉發其他群鏈結的成員(^) -----

    # 獲取機器人所在伺服器的 ID
    bot_guild_id = guild_id    

    if contains_http_or_https(message.content):
        # 如果消息包含 Discord 伺服器邀請連結     
        link_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        links = re.findall(link_pattern, message.content)
        if not message.author.guild_permissions.manage_messages:
            for link in links:
                if "discord.gg" in link:
                    invite_code = link.split('/')[-1]
                    try:
                        invite = await bree.fetch_invite(invite_code)
                        if invite is not None and invite.guild.id != bot_guild_id:
                            
                            channel_ban = bree.get_channel(CHANNEL_ID13)
                            await channel_ban.send(f"{message.author.global_name} 在頻道：{message.channel}，傳送違法訊息：{message.content}") 

                            # 停權該成員
                            role = discord.utils.get(message.guild.roles, id=ROLE_ID8)
                            if role is not None and role in message.author.roles:
                                pass
                            else:
                                await message.author.ban(reason="散布 Discord 伺服器邀請連結")
                            # 刪除該訊息
                            try:
                                # 刪除該訊息
                                await message.delete()
                                if role is not None and role in message.author.roles:
                                    await message.channel.send(f"{message.author.global_name} 請勿傳送違規訊息！")
                                else:
                                    await message.channel.send(f"{message.author.global_name} 你不乖乖布蕾要把你吃掉！")
                            except discord.NotFound:
                                pass
                                if role is not None and role in message.author.roles:
                                    await message.channel.send(f"{message.author.global_name} 請勿傳送違規訊息！")
                                else:
                                    await message.channel.send(f"{message.author.global_name} 你不乖乖布蕾要把你吃掉！")
                        else:
                            await message.channel.send(f"{message.author.global_name} 布蕾很開心有你幫忙宣傳！")
                    except discord.errors.NotFound:
                        pass    

        # 使用正規表達式檢查訊息是否包含 Line 群組邀請連結
        line_invitation_pattern = r"https://line.me/R/ti/g/"
        if re.search(line_invitation_pattern, message.content):
            if not message.author.guild_permissions.manage_messages:

                channel_ban = bree.get_channel(CHANNEL_ID13)
                await channel_ban.send(f"{message.author.global_name} 在頻道：{message.channel}，傳送違法訊息：{message.content}")

                # 停權該成員
                role = discord.utils.get(message.guild.roles, id=ROLE_ID8)
                if role is not None and role in message.author.roles:
                    pass
                else:
                    await message.author.ban(reason="散布 Line 群組邀請連結")
                # 刪除該訊息
                try:
                    # 刪除該訊息
                    await message.delete()
                    if role is not None and role in message.author.roles:
                        await message.channel.send(f"{message.author.global_name} 請勿傳送違規訊息！")
                    else:
                        await message.channel.send(f"{message.author.global_name} 因為不乖乖被布蕾吃掉了！")
                except discord.NotFound:
                    pass
                    # 發送一條新訊息通知該成員已遭剔除
                    if role is not None and role in message.author.roles:
                        await message.channel.send(f"{message.author.global_name} 請勿傳送違規訊息！")
                    else:
                        await message.channel.send(f"{message.author.global_name} 因為不乖乖被布蕾吃掉了！")

        # 使用正規表達式檢查訊息是否包含 LINE 社群邀請連結
        line_community_pattern = r"https://line.me/ti/g2/"
        if re.search(line_community_pattern, message.content):
            if not message.author.guild_permissions.manage_messages:

                channel_ban = bree.get_channel(CHANNEL_ID13)
                await channel_ban.send(f"{message.author.global_name} 在頻道：{message.channel}，傳送違法訊息：{message.content}")

                # 停權該成員
                role = discord.utils.get(message.guild.roles, id=ROLE_ID8)
                if role is not None and role in message.author.roles:
                    pass
                else:
                    await message.author.ban(reason="散布 LINE 社群邀請連結")
                # 刪除該訊息
                try:
                    # 刪除該訊息
                    await message.delete()
                    if role is not None and role in message.author.roles:
                        await message.channel.send(f"{message.author.global_name} 請勿傳送違規訊息！")
                    else:
                        await message.channel.send(f"{message.author.global_name} 因為不乖乖被布蕾吃掉了！")
                except discord.NotFound:
                    pass
                    # 發送一條新訊息通知該成員已遭剔除
                    if role is not None and role in message.author.roles:
                        await message.channel.send(f"{message.author.global_name} 請勿傳送違規訊息！")
                    else:
                        await message.channel.send(f"{message.author.global_name} 因為不乖乖被布蕾吃掉了！")

    # ----- BAN 掉發其他群鏈結的成員(v) -----

    # ----- 改名區(^) -----

    if message.channel.id == CHANNEL_ID11:

        user = message.author
        user_id = user.id

        # 上次改名的时间
        last_time = last_rename_time.get(user_id)

        if last_time is not None:
            # 计算距离上次改名的时间间隔
            current_time = datetime.now()
            time_diff = current_time - last_time

            # 如果距离上次改名超过一定时间（例如1天），允许使用改名区
            if time_diff.total_seconds() < 600 :
                await message.channel.send("最近十分鐘內改過暱稱，請稍候再試 ~")
                return

        # 輸入的文字
        user_input = message.content

        # if is_valid_nickname(user_input) == False :
        #     re_message = "暱稱包含特殊字符，請重新輸入。"
        #     await message.channel.send(re_message)
        #     return

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
            last_rename_time[user_id] = datetime.now()      
            # 從使用者身分組中移除一次性改名卡身分組
            rename_role = discord.utils.get(message.guild.roles, id=id_card)
            if rename_role:
                await message.author.remove_roles(rename_role)                
        except discord.errors.Forbidden:
            await message.channel.send("Bot 出現錯誤，請洽櫻花管管")
        except Exception as e:
            await message.channel.send("Bot 出現錯誤，請洽櫻花管管")

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

            max_retries = 3  # 最大重試次數
            retry_delay = 5  # 重試之間的延遲（秒）

            for _ in range(max_retries):
                try:
                    await message.channel.send(selected_answer)
                    break  # 如果成功發送訊息，則退出循環
                except Exception as e:
                    await asyncio.sleep(retry_delay)           
        except FileNotFoundError:
            await message.channel.send("Bot 出現錯誤，請洽模組櫻花。")
        except json.JSONDecodeError:
            await message.channel.send("Bot 出現錯誤，請洽模組櫻花。")

    # ----- 布蕾答案書(v) -----

    # ----- 自介抓訊息(^) -----

    if message.channel.id == CHANNEL_ID14:

        channel_act00 = bree.get_channel(CHANNEL_ID14)
        channel_act = bree.get_channel(CHANNEL_ID15)
        member_link = f"<@!{message.author.id}>"

        max_retries = 5  # 最大重試次數
        retry_delay = 5  # 重試之間的延遲（秒）

        for _ in range(max_retries):
            try:
                await message.author.send(f"{member_link} \n### 已經成功發布自介囉 (❍ᴥ❍ʋ)\n￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣\n> * 聊天等級 10 等後可以看別人的自我介紹！ \n> * 歡迎各位成員邀請親朋好友入群同樂！\n> \n> * DC群連結：https://discord.gg/UHP9UnZXQr")
                # await channel_act00.send(f"{member_link} 已經成功發布囉 (❍ᴥ❍ʋ)")                
                await channel_act.send(f"{member_link} \n {message.content}", files=[await f.to_file() for f in message.attachments])
                await message.delete()
                break  # 成功後跳出循環
            except Exception as e:
                await asyncio.sleep(retry_delay)  # 等待一段時間後重試
    
    # ----- 自介抓訊息(v) -----

    # ----- 訊息改名(^) -----
    
    if message.author is not None and not message.author.bot and message.guild is not None:
        member = message.guild.get_member(message.author.id)
        
        if member is not None and hasattr(member, 'display_name') and member.display_name is not None:
            if not is_valid_nickname(member.display_name):
                new_nickname = generate_valid_nickname(member.display_name)
                try:
                    await member.edit(nick=new_nickname)
                    # print(f"已將暱稱更改為 {member.display_name} ")
                except discord.Forbidden:
                    print(f"權限錯誤 : 無法更改 {member.display_name} 的暱稱")
                except Exception as e:
                    print(f"未知錯誤 : {e}")

    # ----- 訊息改名(v) -----
    
def contains_http_or_https(message_content):
    return 'http' in message_content or 'https' in message_content

def is_valid_nickname(nickname):

    # 检查是否包含特殊字符
    special_characters = "!@#$%^&*()_+={}[]|\:;'<>,.?/~`"
    special_characters = special_characters.replace(".", "")
    if any(char in special_characters for char in nickname):
        return False

    return True

def is_valid_nickname(nickname):

    return nickname.startswith("‧˚✮₊") and nickname.endswith("ʕ̯•͡˔•̯᷅ʔ彡⁼³₌₃")

def generate_valid_nickname(original_name):

    prefix = "‧˚✮₊"
    suffix = "ʕ̯•͡˔•̯᷅ʔ彡⁼³₌₃"
    total_length = len(prefix) + len(suffix)
    new_name = original_name[:32 - total_length]
    new_nickname = prefix + new_name + suffix

    return new_nickname

# 監聽成員加入事件
@bree.event
async def on_member_join(member):

    # 取得新成員的名稱和 ID
    new_member_name = member.global_name

    if new_member_name is None:
        # 如果新成員名稱為 None，則使用預設名稱或其他處理方式
        new_member_name = member.display_name

    # 計算 prefix 和 suffix 的長度
    prefix = "‧˚✮₊"
    suffix = "ʕ̯•͡˔•̯᷅ʔ彡⁼³₌₃"
    total_length = len(prefix) + len(suffix)

    # 截斷 new_member_name，確保暱稱長度不超過 32 字元
    new_member_name = new_member_name[:32 - total_length]

    # 設置新成員的暱稱
    new_nickname = prefix + new_member_name + suffix
    max_retries = 3  # 最大重試次數
    retry_delay = 5  # 重試之間的延遲（秒）
    for _ in range(max_retries):
        try:
            await member.edit(nick=new_nickname)
            break  # 成功後跳出循環
        except Exception as e:
            await asyncio.sleep(retry_delay)  # 等待一段時間後重試

    # 更新架上有幾盤布蕾
    guild = member.guild
    channel = bree.get_channel(CHANNEL_ID) 
    # 執行 update_channel_name 函式，限制每 5 分鐘執行一次
    global last_executed_time
    current_time = time.time()
    if current_time - last_executed_time >= 300:
        max_retries = 3  # 最大重試次數
        retry_delay = 5  # 重試之間的延遲（秒）
        for _ in range(max_retries):
            try:
                await update_channel_name(guild, channel)
                last_executed_time = current_time                
                break  # 成功後跳出循環
            except Exception as e:
                await asyncio.sleep(retry_delay)  # 等待一段時間後重試

# 監聽成員離開事件
@bree.event
async def on_member_remove(member):

    channel = bree.get_channel(CHANNEL_ID2)

    embed = discord.Embed(color=discord.Color(0xFFB6C1))
    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    embed.set_author(name=member.display_name, icon_url=avatar_url)
    embed.set_thumbnail(url=avatar_url)  # Use member.avatar.url to get the avatar URL.
    # embed.set_image(url=avatar_url)
    embed.add_field(name='使用者名稱', value=member.display_name, inline=True)
    embed.add_field(name='加好友 ID', value=f"{member.name}#{member.discriminator}", inline=True)
    activity = member.activity
    activity_name = activity.name if activity else '無'
    embed.add_field(name='自訂狀態', value=activity_name, inline=False)
    embed.add_field(name='Nitro', value=member.premium_since, inline=False)
    locale = member.guild.preferred_locale
    embed.add_field(name='語言', value=locale, inline=False)   

    # 要過濾的身分組 ID
    filtered_role_ids = [ROLE_ID1, ROLE_ID2,ROLE_ID3, ROLE_ID4,ROLE_ID5, ROLE_ID6,ROLE_ID7,ROLE_ID9] 
    # 過濾掉特定身分組
    remaining_roles = [role for role in member.roles if role.id not in filtered_role_ids]
    if remaining_roles:
        sorted_roles = sorted(remaining_roles, key=lambda role: role.position, reverse=True)
        roles_ids = [f"<@&{role.id}>" for role in sorted_roles]
        roles_str = '\n'.join(roles_ids)
    else:
        roles_str = '無'

    embed.add_field(name='擁有角色', value=roles_str, inline=False)
    embed.add_field(name='加入伺服器時間', value=member.joined_at, inline=False)
    embed.add_field(name='建立 Discord 帳號時間', value=member.created_at, inline=False)

    
    member_link = f"<@!{member.id}>"
    message = f"{member_link} 帶走了一盤布蕾ﾍ( ﾟ∀ﾟ;)ﾉ"
    await channel.send(content=message,embed=embed)

    # 更新架上有幾盤布蕾
    guild = member.guild
    channel = bree.get_channel(CHANNEL_ID) 
    # 執行 update_channel_name 函式，限制每 5 分鐘執行一次
    global last_executed_time
    current_time = time.time()
    if current_time - last_executed_time >= 300:
        max_retries = 3  # 最大重試次數
        retry_delay = 5  # 重試之間的延遲（秒）
        for _ in range(max_retries):
            try:
                await update_channel_name(guild, channel)
                last_executed_time = current_time
                break  # 成功後跳出循環
            except Exception as e:
                await asyncio.sleep(retry_delay)  # 等待一段時間後重試
  
@bree.event
async def on_member_ban(guild, user):
    member = guild.get_member(user.id)
    target_channel = bree.get_channel(CHANNEL_ID3)    
    w1_channel = bree.get_channel(CHANNEL_ID4)

    embed = discord.Embed(color=discord.Color(0xFFB6C1))
    avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
    embed.set_author(name=user.display_name, icon_url=avatar_url)
    embed.set_thumbnail(url=avatar_url)  # Use member.avatar.url to get the avatar URL.
    # embed.set_image(url=avatar_url)
    embed.add_field(name='使用者名稱', value=user.display_name, inline=True)
    embed.add_field(name='加好友 ID', value=f"{user.name}#{user.discriminator}", inline=True)
    activity = member.activity
    activity_name = activity.name if activity else '無'
    embed.add_field(name='自訂狀態', value=activity_name, inline=False)
    embed.add_field(name='Nitro', value=user.premium_since, inline=False)
    locale = user.guild.preferred_locale
    embed.add_field(name='語言', value=locale, inline=False)   

    # 要過濾的身分組 ID
    filtered_role_ids = [ROLE_ID1, ROLE_ID2,ROLE_ID3, ROLE_ID4,ROLE_ID5, ROLE_ID6,ROLE_ID7,ROLE_ID9] 
    # 過濾掉特定身分組
    remaining_roles = [role for role in user.roles if role.id not in filtered_role_ids]
    if remaining_roles:
        sorted_roles = sorted(remaining_roles, key=lambda role: role.position, reverse=True)
        roles_ids = [f"<@&{role.id}>" for role in sorted_roles]
        roles_str = '\n'.join(roles_ids)
    else:
        roles_str = '無'

    embed.add_field(name='擁有角色', value=roles_str, inline=False)
    embed.add_field(name='加入伺服器時間', value=user.joined_at, inline=False)
    embed.add_field(name='建立 Discord 帳號時間', value=user.created_at, inline=False)
    message = f"因 {user.display_name} 屢次違反伺服器 {w1_channel.mention} 故而送往報銷室報廢。"

    await target_channel.send(content=message,embed=embed)

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
    "greet.json": ["你好", "嗨", "哈囉", "Hello", "Hi", "您好", "早安", "午安", "晚安"],
    "thanks.json": ["謝謝", "感謝", "多謝"],
    "like.json": ["喜歡布蕾","愛布蕾"],
    "hat.json": ["討厭布蕾","不喜歡布蕾"],
    "ask.json": ["請問","嗎","為甚麼","怎麼","可以問個問題嗎", "有事想問"],
}

# 根據對話中的關鍵字分類情境
def classify_dialogue(message):
    for context, keywords_list in keywords.items():
        for keyword in keywords_list:
            if keyword in message.content:
                return context
    return "ask.json"  # 預設為 "ask" 情境

#TOKEN 在剛剛 Discord Developer 那邊「BOT」頁面裡面
bree.run(os.getenv("BOT_TOKEN2")) #布蕾
