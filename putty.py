import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import json
import asyncio
import random

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
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:

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

def is_valid_nickname(nickname):

    return nickname.startswith("‧˚✮₊") and nickname.endswith("ʕ̯•͡˔•̯᷅ʔ彡⁼³₌₃")

def generate_valid_nickname(original_name):

    prefix = "‧˚✮₊"
    suffix = "ʕ̯•͡˔•̯᷅ʔ彡⁼³₌₃"
    total_length = len(prefix) + len(suffix)
    new_name = original_name[:32 - total_length]
    new_nickname = prefix + new_name + suffix

    return new_nickname

@putty.event
async def on_message(message):
    if message.author.bot:

        return 
    
    # ----- 時光抓訊息(^) -----

    if message.channel.id == 1312609405350576240:

        channel_act00 = putty.get_channel(1312609405350576240) #post channel
        channel_act = putty.get_channel(1312610532032909435) # recard channel
        member_link = f"<@!{message.author.id}>"
        max_retries = 3  # 最大重試次數
        retry_delay = 5  # 重試之間的延遲（秒）

        for _ in range(max_retries):
            try:
                #if message.content.startswith("<:No_011:1133635937855881367> 致 2025 的我："):
                if len(message.content) <= 1900:
                    await channel_act00.send(f"{member_link} 感謝您的參與*ଘ(੭*ˊᗜˋ)੭* ੈ✧‧₊˚")
                    await channel_act.send(f"︶꒷︶︶୨୧︶︶꒷𓈊꒷︶︶୨୧︶︶꒷︶\n{member_link}\n留下的時光訊息：\n\n{message.content}\n\n︶꒷︶︶୨୧︶︶꒷︶꒷︶︶୨୧︶︶꒷︶", files=[await f.to_file() for f in message.attachments])
                else:
                    await channel_act00.send("字數不可以超過 1900 字唷")
                await message.delete()
                break  # 成功後跳出循環
            except Exception as e:
                await asyncio.sleep(retry_delay)  # 等待一段時間後重試

    # ----- 時光抓訊息(v) -----
        
    await putty.process_commands(message)

@putty.hybrid_command(name='hello', help='跟布丁打招呼～')  
async def hello(ctx):
    await ctx.send('你好！')

class vip_add_member_Flags(commands.FlagConverter):
    頻道: discord.VoiceChannel = commands.flag(description='選擇語音房')
    成員: discord.Member = commands.flag(description='選擇成員')
@putty.hybrid_command(name='增加vip房成員', help='將指定成員加入 vip 語音房 !')
async def vip_add_member(ctx,  *, flags: vip_add_member_Flags):

    channel = flags.頻道
    member = flags.成員

    if not channel:
        await ctx.send("未填入 channel ！")
        return

    if not member:
        await ctx.send("未填入 member ！")
        return
    
    if member:
        if channel:
            channel_id = channel.id
            voice_channel = putty.get_channel(channel_id)
            permissions = channel.permissions_for(ctx.author)
            if permissions.priority_speaker:
                await voice_channel.set_permissions(member, view_channel=True)
                await ctx.send(f"{member.mention} 已加入 {voice_channel.name} VIP 語音房")
            else:
                await ctx.send("您並未擁有該語音房權限！")
        else:
            await ctx.send("布丁看不懂 ！")
    else:
        await ctx.send("布丁看不懂 ！")

class vip_remove_member_Flags(commands.FlagConverter):
    頻道: discord.VoiceChannel = commands.flag(description='選擇語音房')
    成員: discord.Member = commands.flag(description='選擇成員')
@putty.hybrid_command(name='移除vip房成員', help='將指定成員移出 vip 語音房 !')
async def vip_remove_member(ctx,  *, flags: vip_remove_member_Flags): 

    channel = flags.頻道
    member = flags.成員


    if not channel:
        await ctx.send("未填入 channel ！")
        return

    if not member:
        await ctx.send("未填入 member ！")
        return
    
    if member:
        if channel:
            channel_id = channel.id
            voice_channel = putty.get_channel(channel_id)
            permissions = channel.permissions_for(ctx.author)
            if permissions.priority_speaker:
                await voice_channel.set_permissions(member, view_channel=False)
                await ctx.send(f"{member.mention} 已移出 {voice_channel.name} VIP 語音房")
            else:
                await ctx.send("您並未擁有該語音房權限！")
        else:
            await ctx.send("布丁看不懂 ！")
    else:
        await ctx.send("布丁看不懂 ！")

class vip_view_Flags(commands.FlagConverter):
    頻道: discord.VoiceChannel = commands.flag(description='選擇語音房')
@putty.hybrid_command(name='檢視vip房成員列表', help='列出指定語音頻道的成員列表')
async def vip_view(ctx,  *, flags: vip_view_Flags):

    channel = flags.頻道

    if not channel:
        await ctx.send('布丁找不到這個語音頻道！')
        return

    viewers = []
    for overwrite in channel.overwrites:
        if isinstance(overwrite, discord.Member):
            permissions = channel.permissions_for(overwrite)
            if permissions.view_channel:
                viewers.append(overwrite)

    if viewers:
        embed = discord.Embed(title=f'具有檢視權限的成員列表 ({len(viewers)}人)', color=discord.Color.from_rgb(241, 174, 194))
        for member in viewers:
            embed.add_field(name=member.display_name, value=member.mention, inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send('沒有任何成員具有該語音頻道的檢視權限！')

class hang_out_Flags(commands.FlagConverter):
    項目: str = commands.flag(description='主題內容(Game name)')
    時間: str = commands.flag(description='開始時間(Starting time)')
    人數: str = commands.flag(description='需求人數(People needed)')
    備註: str = commands.flag(description='備註(Remark)')
    頻道: discord.VoiceChannel = commands.flag(description='選擇語音房(Voice channel)')   
@putty.hybrid_command(name='揪團', help="找人一起玩遊戲或聊天或看影片(Let's hang out together and play games.)")
async def hang_out(ctx,  *, flags: hang_out_Flags):

    項目 = flags.項目
    時間 = flags.時間
    人數 = flags.人數
    備註 = flags.備註
    頻道 = flags.頻道

    role_mention = f"<@&{ROLE_ID14}>"

    message_content = (
        f"## <:No_011:1166191020829069394> 新的揪團開啟囉 <:No_010:1133574932534665297> \n"
        f"主揪：{ctx.author.mention}\n"
        "╭⌕˚꒷ ͝ ꒦₍ᕱ.⑅.ᕱ₎꒦꒷ ͝ ꒦ ͝\n"
        f"<:No_001:1133419740166115359>項目(Item)：{項目}\n"
        f"<:No_002:1133419757215953039>時間(Time)：{時間}\n"
        f"<:No_003:1133419774500671518>人數(People)：{人數}\n"
        f"<:No_004:1133419788014731325>備註(Remark)：{備註}\n"
        f"<:No_005:1133419804255076525>語音房連結(channel)：\n"
        f"<:No_011:1167260028315639889> https://discord.com/channels/{ctx.guild.id}/{頻道.id}\n"
        "╰ ꒷꒦꒷ ͝ ꒦₍ꐑxꐑ₎꒦ ͝ ꒷ ͝ ꒦\n"
    )

    channel2 = ctx.channel
    await channel2.send(f"{role_mention}")

    message = await ctx.send(message_content)
    member_nick = ctx.author.nick or ctx.author.display_name
    thread = await message.create_thread(name=f"{member_nick}")
    await thread.send("布蕾布布蕾！\n布丁幫你創好專屬討論串囉\n結束之後記得講一聲喔")

class draw_Flags(commands.FlagConverter):
    活動主題: str = commands.flag(description='抽取的主題內容') 
    身分組: commands.Greedy[discord.Role] = commands.flag(description='要抽取的身分組')
    數量: int = commands.flag(description='要抽取幾位得獎者') 
    獎項內容: str = commands.flag(description='抽取的獎項內容') 
    限制身分組: commands.Greedy[discord.Role] = commands.flag(description='得獎人必須擁有的身分組', default=[])

@putty.hybrid_command(name='隨機抽獎', help="從指定身分組抽出得獎者")
async def draw(ctx,  *, flags: draw_Flags):
    活動主題 = flags.活動主題
    身分組 = flags.身分組
    數量 = flags.數量
    獎項內容 = flags.獎項內容
    限制身分組 = flags.限制身分組
    
    # 檢查參數是否有效
    if 數量 <= 0:
        await ctx.send("抽獎人數必須是正整數！")
        return

    # 獲取所有被提及的身分組成員，並去除重複
    all_members = set()
    for role in 身分組:
        all_members.update(role.members)

    # 如果指定了限制身分組，則進行過濾
    if 限制身分組:
        filtered_members = [
            member for member in all_members 
            if any(role in member.roles for role in 限制身分組)
        ]
        all_members = filtered_members
    else:
        filtered_members = list(all_members)
        all_members = filtered_members

    # 從所有被提及的身分組成員中隨機選擇指定數量的成員作為中獎者
    winners = random.sample(list(all_members), min(len(all_members), 數量))

    # 在頻道中發送抽獎結果
    winner_names = "\n".join([member.mention for member in winners])

    # 創建 Embed 來顯示抽獎清單
    embed = discord.Embed(title="抽獎清單", color=discord.Color.from_rgb(241, 174, 194))

    # 添加所有參加抽獎的成員到 Embed
    member_list = ", ".join([member.mention for member in all_members])
    embed.add_field(name="成員", value=member_list, inline=False)

    # 發送 Embed 到頻道中
    await ctx.send(embed=embed)
    message_content = (
        "## ε✦°·得獎公告·°✦з\n"
        "︶꒷︶︶୨୧︶︶꒷𓈊꒷︶︶୨୧︶︶꒷︶\n"
        "### 恭喜 🎉🎉🎉\n"
        f"{winner_names}\n"
        f"### 參與 {活動主題}\n" 
        f"### 幸運獲得了 {獎項內容}！\n"
        f"\n"
        "︶꒷︶︶୨୧︶︶꒷︶꒷︶︶୨୧︶︶꒷︶\n"
    )
    await ctx.send(message_content)

putty.run(os.getenv("BOT_TOKEN1"))  # 布丁
