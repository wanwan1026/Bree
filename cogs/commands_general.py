# cogs/commands_general.py
import random
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

from config import (
    ROLE_ID14,
    TAG_GUILD_ID,
    TAG_ROLE_ID,
    TAG_STRING,
    ROLE_ID16,
    ROLE_ID17,
    ROLE_ID18,
    ROLE_ID19,
    ROLE_ID20,
    ROLE_ID21,
    ROLE_ID22,
    ROLE_GAME_ID1,
    ROLE_GAME_ID2,
    ROLE_GAME_ID3,
    ROLE_GAME_ID4,
    ROLE_GAME_ID5,
    ROLE_GAME_ID6,
    ROLE_GAME_ID7,
    ROLE_GAME_ID8,
    ROLE_GAME_ID9,
    ROLE_GAME_ID10,
    ROLE_GAME_ID11,
    ROLE_GAME_ID12,
    ROLE_GAME_ID13,
    ROLE_GAME_ID14,
    ROLE_GAME_ID15,
    ROLE_GAME_ID16,
    ROLE_GAME_ID17,
    ROLE_GAME_ID18,
    ROLE_GAME_ID19,
    ROLE_GAME_ID20,
    ROLE_GAME_ID21,
    ROLE_GAME_ID22,
    ROLE_GAME_ID23,
    ROLE_GAME_ID24,
    ROLE_GAME_ID25,
    ROLE_GAME_ID26,
    ROLE_GAME_ID27,
    ROLE_GAME_ID28,
    ROLE_GAME_ID29,
    ROLE_GAME_ID30,
    ROLE_GAME_ID31,
    ROLE_GAME_ID32,
    ROLE_GAME_ID33,
    ROLE_GAME_ID34,
    ROLE_GAME_ID35,
    ROLE_GAME_ID36,
    ROLE_GAME_ID37,
    guild_id
)

GAME_ROLE_IDS = [
    ROLE_GAME_ID1,
    ROLE_GAME_ID2,
    ROLE_GAME_ID3,
    ROLE_GAME_ID4,
    ROLE_GAME_ID5,
    ROLE_GAME_ID6,
    ROLE_GAME_ID7,
    ROLE_GAME_ID8,
    ROLE_GAME_ID9,
    ROLE_GAME_ID10,
    ROLE_GAME_ID11,
    ROLE_GAME_ID12,
    ROLE_GAME_ID13,
    ROLE_GAME_ID14,
    ROLE_GAME_ID15,
    ROLE_GAME_ID16,
    ROLE_GAME_ID17,
    ROLE_GAME_ID18,
    ROLE_GAME_ID19,
    ROLE_GAME_ID20,
    ROLE_GAME_ID21,
    ROLE_GAME_ID22,
    ROLE_GAME_ID23,
    ROLE_GAME_ID24,
    ROLE_GAME_ID25,
    ROLE_GAME_ID26,
    ROLE_GAME_ID27,
    ROLE_GAME_ID28,
    ROLE_GAME_ID29,
    ROLE_GAME_ID30,
    ROLE_GAME_ID31,
    ROLE_GAME_ID32,
    ROLE_GAME_ID33,
    ROLE_GAME_ID34,
    ROLE_GAME_ID35,
    ROLE_GAME_ID36,
    ROLE_GAME_ID37,
]


def build_game_role_map(guild: discord.Guild) -> dict[str, int]:
    """
    從設定好的 ROLE_GAME_ID* 建立 {角色名稱: 角色ID} 對照表
    """
    game_role_map: dict[str, int] = {}

    print(f"[DEBUG] build_game_role_map: guild={guild.id} start")

    for role_id in GAME_ROLE_IDS:
        role = guild.get_role(role_id)
        if role:
            game_role_map[role.name] = role.id

    print(
        f"[DEBUG] build_game_role_map: 完成，總數={len(game_role_map)}，名稱={list(game_role_map.keys())}"
    )
    return game_role_map


def member_has_server_tag(member: discord.Member) -> bool:
    """
    跟 events.py 裡一樣的邏輯：
    - primary_guild.id 要是 TAG_GUILD_ID
    - primary_guild.tag 要等於 TAG_STRING
    - enabled 不是 False
    """
    pg = getattr(member, "primary_guild", None)
    if pg is None:
        return False

    pg_id = getattr(pg, "id", None)
    pg_tag = getattr(pg, "tag", None)
    enabled = getattr(pg, "enabled", None)

    if pg_id != TAG_GUILD_ID:
        return False
    if pg_tag != TAG_STRING:
        return False
    if enabled is False:
        return False

    return True


# ===== Flag 定義們 =====
class vip_add_member_Flags(commands.FlagConverter):
    頻道: discord.VoiceChannel = commands.flag(description="選擇語音房")
    成員: discord.Member = commands.flag(description="選擇成員")


class vip_remove_member_Flags(commands.FlagConverter):
    頻道: discord.VoiceChannel = commands.flag(description="選擇語音房")
    成員: discord.Member = commands.flag(description="選擇成員")


class vip_view_Flags(commands.FlagConverter):
    頻道: discord.VoiceChannel = commands.flag(description="選擇語音房")


class hang_out_Flags(commands.FlagConverter):
    # 現在只給文字版指令用，斜線指令改用參數 & autocomplete
    時間: str = commands.flag(description="開始時間(Starting time)")
    人數: str = commands.flag(description="需求人數(People needed)")
    備註: str = commands.flag(description="備註(Remark)")
    頻道: discord.VoiceChannel = commands.flag(description="選擇語音房(Voice channel)")


class draw_Flags(commands.FlagConverter):
    活動主題: str = commands.flag(description="抽取的主題內容")
    身分組: commands.Greedy[discord.Role] = commands.flag(description="要抽取的身分組")
    數量: int = commands.flag(description="要抽取幾位得獎者")
    獎項內容: str = commands.flag(description="抽取的獎項內容")
    限制身分組: commands.Greedy[discord.Role] = commands.flag(
        description="得獎人必須擁有的身分組",
        default=[],
    )


class GeneralCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ====== /hello ======
    @commands.hybrid_command(name="hello", help="跟布丁打招呼～")
    async def hello(self, ctx: commands.Context):
        await ctx.send("你好！")

    # ====== /增加vip房成員 ======
    @commands.hybrid_command(name="增加vip房成員", help="將指定成員加入 vip 語音房 !")
    async def vip_add_member(self, ctx: commands.Context, *, flags: vip_add_member_Flags):
        channel = flags.頻道
        member = flags.成員

        if not channel:
            await ctx.send("未填入 channel ！")
            return

        if not member:
            await ctx.send("未填入 member ！")
            return

        voice_channel = channel
        permissions = voice_channel.permissions_for(ctx.author)

        if permissions.priority_speaker:
            await voice_channel.set_permissions(member, view_channel=True)
            await ctx.send(f"{member.mention} 已加入 {voice_channel.name} VIP 語音房")
        else:
            await ctx.send("您並未擁有該語音房權限！")

    # ====== /移除vip房成員 ======
    @commands.hybrid_command(name="移除vip房成員", help="將指定成員移出 vip 語音房 !")
    async def vip_remove_member(
        self,
        ctx: commands.Context,
        *,
        flags: vip_remove_member_Flags,
    ):
        channel = flags.頻道
        member = flags.成員

        if not channel:
            await ctx.send("未填入 channel ！")
            return

        if not member:
            await ctx.send("未填入 member ！")
            return

        voice_channel = channel
        permissions = voice_channel.permissions_for(ctx.author)

        if permissions.priority_speaker:
            await voice_channel.set_permissions(member, view_channel=False)
            await ctx.send(f"{member.mention} 已移出 {voice_channel.name} VIP 語音房")
        else:
            await ctx.send("您並未擁有該語音房權限！")

    # ====== /檢視vip房成員列表 ======
    @commands.hybrid_command(name="檢視vip房成員列表", help="列出指定語音頻道的成員列表")
    async def vip_view(self, ctx: commands.Context, *, flags: vip_view_Flags):
        channel = flags.頻道

        if not channel:
            await ctx.send("布丁找不到這個語音頻道！")
            return

        viewers = []
        for overwrite in channel.overwrites:
            if isinstance(overwrite, discord.Member):
                permissions = channel.permissions_for(overwrite)
                if permissions.view_channel:
                    viewers.append(overwrite)

        if viewers:
            embed = discord.Embed(
                title=f"具有檢視權限的成員列表 ({len(viewers)}人)",
                color=discord.Color.from_rgb(241, 174, 194),
            )
            for member in viewers:
                embed.add_field(
                    name=member.display_name,
                    value=member.mention,
                    inline=False,
                )

            await ctx.send(embed=embed)
        else:
            await ctx.send("沒有任何成員具有該語音頻道的檢視權限！")

    # ====== /揪團（斜線指令：項目用 autocomplete） ======
    @commands.hybrid_command(
        name="揪團",
        help="找人一起玩遊戲或聊天或看影片(Let's hang out together and play games.)",
    )
    @app_commands.describe(
        項目="選擇遊戲(Game name)",
        時間="開始時間(Starting time)",
        人數="需求人數(People needed)",
        備註="備註(Remark)",
        頻道="選擇語音房(Voice channel)",
    )
    async def hang_out(
        self,
        ctx: commands.Context,
        項目: str,
        時間: str,
        人數: str,
        頻道: discord.VoiceChannel,
        備註: Optional[str] = "無備註",
    ):
        """
        斜線版：/揪團 項目 <autocomplete> ...
        文字版依然可以寫：/揪團 項目:xxx 時間:xx ...（取決於你怎麼用）
        """
        print(f"[DEBUG] /揪團 被呼叫：項目={項目}, 時間={時間}, 人數={人數}, 備註={備註}, 頻道={getattr(頻道, 'id', None)}")

        if ctx.guild is None:
            await ctx.send("這個指令只能在伺服器裡使用。")
            return

        # 取得「名稱 -> role_id」對照
        game_role_map = build_game_role_map(ctx.guild)
        game_role_id = game_role_map.get(項目)

        # 準備要 @ 的身分組
        mentions = [f"<@&{ROLE_ID14}>"]
        if game_role_id:
            mentions.append(f"<@&{game_role_id}>")
        else:
            # 找不到對應的遊戲身分組，印個 log 幫 debug
            print(f"[DEBUG] /揪團: 在 game_role_map 裡找不到項目='{項目}' 對應的身分組")

        role_mention = " ".join(mentions)

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

        # 先 ping 身分組
        await ctx.send(role_mention)

        # 再發揪團內容
        msg = await ctx.send(message_content)
        member_nick = ctx.author.nick or ctx.author.display_name

        # ✅ 用「頻道」來建立 thread，而不是 msg.create_thread()
        channel = ctx.channel

        try:
            # 只有在有 guild 的情況下才建 thread（避免 DM 出錯）
            if ctx.guild is not None and isinstance(channel, discord.TextChannel):
                thread = await channel.create_thread(
                    name=f"{member_nick}",
                    message=msg,      # 把這則訊息當作 thread 的起始訊息
                )
                await thread.send(
                    "布蕾布布蕾！\n布丁幫你創好專屬討論串囉\n結束之後記得在這裡講一聲喔"
                )
            else:
                print("[DEBUG] /揪團: 無法建立 thread（不是 guild 或不是文字頻道）")
        except Exception as e:
            print(f"[DEBUG] /揪團: 建立 thread 失敗：{e}")


    # ====== /揪團：項目 autocomplete（用遊戲身分組名稱） ======
    @hang_out.autocomplete("項目")
    async def hang_out_game_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ):
        guild = interaction.guild
        if guild is None:
            return []

        game_role_map = build_game_role_map(guild)  # {名稱: ID}

        # 依照名稱排序，讓列表比較穩定
        names = sorted(game_role_map.keys())

        choices: list[app_commands.Choice[str]] = []
        for name in names:
            # 沒輸入就全部丟，打字就做簡單包含過濾
            if not current or current.lower() in name.lower():
                choices.append(app_commands.Choice(name=name, value=name))

        # 一次最多只能給 Discord 25 個
        print(f"[DEBUG] autocomplete: current='{current}', 回傳 {len(choices[:25])} 個選項")
        return choices[:25]

    # ====== /隨機抽獎 ======
    @commands.hybrid_command(name="隨機抽獎", help="從指定身分組抽出得獎者")
    async def draw(self, ctx: commands.Context, *, flags: draw_Flags):
        活動主題 = flags.活動主題
        身分組 = flags.身分組
        數量 = flags.數量
        獎項內容 = flags.獎項內容
        限制身分組 = flags.限制身分組

        if 數量 <= 0:
            await ctx.send("抽獎人數必須是正整數！")
            return

        # 收集所有目標身分組成員
        all_members = set()
        for role in 身分組:
            all_members.update(role.members)

        # 如果有指定「限制身分組」，再過濾一次
        if 限制身分組:
            filtered_members = [
                member
                for member in all_members
                if any(role in member.roles for role in 限制身分組)
            ]
            all_members = filtered_members
        else:
            all_members = list(all_members)

        if not all_members:
            await ctx.send("沒有符合條件的成員可以抽獎 QQ")
            return

        # 抽出得獎者
        winners = random.sample(list(all_members), min(len(all_members), 數量))

        winner_names = "\n".join(member.mention for member in winners)

        # 建立抽獎清單 embed
        embed = discord.Embed(
            title="抽獎清單",
            color=discord.Color.from_rgb(241, 174, 194),
        )
        member_list = ", ".join(member.mention for member in all_members)
        embed.add_field(name="成員", value=member_list, inline=False)

        await ctx.send(embed=embed)

        message_content = (
            "## ε✦°·得獎公告·°✦з\n"
            "︶꒷︶︶୨୧︶︶꒷𓈊꒷︶︶୨୧︶︶꒷︶\n"
            "### 恭喜 🎉🎉🎉\n"
            f"{winner_names}\n"
            f"### 參與 {活動主題}\n"
            f"### 幸運獲得了 {獎項內容}！\n"
            "\n"
            "︶꒷︶︶୨୧︶︶꒷︶꒷︶︶୨୧︶︶꒷︶\n"
        )
        await ctx.send(message_content)

    # ====== /檢查身分組 ======
    @commands.hybrid_command(
        name="檢查身分組",
        help="同時檢查 TAG 身分組與 16~20 是否符合 21 & 22 依賴規則。",
    )
    async def check_roles_all(self, ctx: commands.Context):
        guild = ctx.guild
        if guild is None:
            await ctx.send("這個指令只能在伺服器裡使用。")
            return

        if guild.id != TAG_GUILD_ID:
            await ctx.send("這個伺服器不是設定中的 TAG_GUILD_ID，無法執行檢查。")
            return

        tag_role = guild.get_role(TAG_ROLE_ID)
        if tag_role is None:
            await ctx.send("找不到 TAG 身分組，請檢查 TAG_ROLE_ID 設定。")
            return

        # 主要身分組與必要身分組
        main_role_ids = [ROLE_ID16, ROLE_ID17, ROLE_ID18, ROLE_ID19, ROLE_ID20]
        required_role_ids = [ROLE_ID21, ROLE_ID22]

        main_roles = [guild.get_role(rid) for rid in main_role_ids]
        required_roles = [guild.get_role(rid) for rid in required_role_ids]

        # 過濾掉 None
        main_roles = [r for r in main_roles if r is not None]
        required_roles = [r for r in required_roles if r is not None]

        if not main_roles:
            await ctx.send("找不到任何主身分組 (16~20)，請檢查設定。")
            return
        if len(required_roles) < 2:
            await ctx.send("必要身分組 (21 / 22) 少於 2 個，請檢查設定。")
            return

        await ctx.send("開始檢查 TAG 與身分組依賴，可能需要一些時間，請稍候……")

        BATCH_SIZE = 50
        idx = 0
        tag_removed = 0
        dep_cleaned = 0

        # 🔹 只檢查「有相關身分組」的成員，不全伺服器掃
        members_to_check = set()

        # 有 TAG_ROLE 的人（要做 TAG 檢查）
        members_to_check.update(tag_role.members)

        # 有 16~20 其中任一個的人（要做依賴檢查）
        for r in main_roles:
            members_to_check.update(r.members)

        # 迴圈裡就不用 fetch_members 了，直接跑這個集合
        for member in list(members_to_check):
            if member.bot:
                continue

            # ===== 1. TAG 檢查：沒有伺服器 TAG 就收回 TAG_ROLE_ID =====
            if tag_role in member.roles and not member_has_server_tag(member):
                try:
                    await member.remove_roles(
                        tag_role,
                        reason="手動檢查：未使用伺服器 TAG → 自動收回",
                    )
                    tag_removed += 1
                except discord.HTTPException as e:
                    print(f"[手動TAG收回失敗] {member}：{e}")

            # ===== 2. 依賴檢查：16~20 需要同時擁有 21 & 22 =====
            has_main = any(r in member.roles for r in main_roles)
            if has_main:
                has_all_required = all(r in member.roles for r in required_roles)
                if not has_all_required:
                    roles_to_remove = [r for r in main_roles if r in member.roles]
                    if roles_to_remove:
                        try:
                            await member.remove_roles(
                                *roles_to_remove,
                                reason="手動檢查：缺少 21/22 → 自動收回 16~20",
                            )
                            dep_cleaned += 1
                        except discord.HTTPException as e:
                            print(f"[手動依賴收回失敗] {member}：{e}")

            idx += 1
            if idx % BATCH_SIZE == 0:
                await asyncio.sleep(1)

        await ctx.send(
            f"✅ 檢查完成：\n"
            f"- 收回 TAG 身分組：{tag_removed} 人\n"
            f"- 因缺少 21/22 而移除 16~20：{dep_cleaned} 人"
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(GeneralCommands(bot))
