# cogs/commands_general.py
import random
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import time
import os


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
    guild_id,
    one_pice,
    ten_pice,
    hun_pice,

    ROLE_ID26
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

GAME_OPTIONS: dict[str, dict] = {

    "apex": {"label": "APEX 英雄", "role_id": ROLE_GAME_ID25}, 
    "lol": {"label": "LOL 英雄聯盟", "role_id": ROLE_GAME_ID23}, 
    "valo": {"label": "特戰英豪", "role_id": ROLE_GAME_ID24}, 
    "garena": {"label": "傳說對決", "role_id": ROLE_GAME_ID28}, 
    "five": {"label": "第五人格", "role_id": ROLE_GAME_ID30}, 

    "delta": {"label": "三角洲行動", "role_id": ROLE_GAME_ID31}, 
    "six": {"label": "燕雲十六聲", "role_id": ROLE_GAME_ID37}, 
    "roblox": {"label": "ROBLOX", "role_id": ROLE_GAME_ID13},
    "決戰！平安京": {"label": "決戰！平安京", "role_id": ROLE_GAME_ID33}, 
    "Super Animal Royale": {"label": "Super Animal Royale", "role_id": ROLE_GAME_ID21}, 

    "maple": {"label": "楓之谷", "role_id": ROLE_GAME_ID15}, 
    "majsoul": {"label": "雀魂麻將", "role_id": ROLE_GAME_ID16}, 
    "repo": {"label": "REPO", "role_id": ROLE_GAME_ID17}, 
    "shope": {"label": "夢之形", "role_id": ROLE_GAME_ID22}, 
    "dream": {"label": "卡厄思夢境", "role_id": ROLE_GAME_ID1}, 

    "vitor": {"label": "勝利女神妮姬", "role_id": ROLE_GAME_ID6}, 
    "sky": {"label": "崩壞：星穹鐵道", "role_id": ROLE_GAME_ID3}, 
    "god": {"label": "原神", "role_id": ROLE_GAME_ID14}, 
    "wuth": {"label": "鳴潮", "role_id": ROLE_GAME_ID2},
    "zero": {"label": "絕區零", "role_id": ROLE_GAME_ID5},

    "talk": {"label": "聊天", "role_id": ROLE_GAME_ID12},
    "sing": {"label": "唱歌", "role_id": ROLE_GAME_ID8},
    "other": {"label": "其他遊戲", "role_id": ROLE_GAME_ID10},

}

# ====== 落櫻抽獎設定（可自由改）======

DRAW_PACKS = {
    1: {"label": "單抽", "need_role_id": one_pice, "times": 1},
    2: {"label": "十連抽", "need_role_id": ten_pice, "times": 10},
    3: {"label": "一百連抽", "need_role_id": hun_pice, "times": 100},
}

# 多個 gif 隨機播一個（路徑要存在）

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # .../cogs

GACHA_GIF_PATHS = [
    os.path.normpath(os.path.join(BASE_DIR, "..", "assets", "gacha", "111.gif")),
    os.path.normpath(os.path.join(BASE_DIR, "..", "assets", "gacha", "222.gif")),
    os.path.normpath(os.path.join(BASE_DIR, "..", "assets", "gacha", "333.gif")),
    os.path.normpath(os.path.join(BASE_DIR, "..", "assets", "gacha", "444.gif")),
    os.path.normpath(os.path.join(BASE_DIR, "..", "assets", "gacha", "555.gif")),
]

GACHA_GIF_STAY_SECONDS = 5

# 階梯式獎池（可自由新增刪減）
# 規則：每層先看 none(沒中) 的百分比，沒中才進下一層
LOOT_TABLE = {
    "1": {
        "none":10.0,
        "吉吉很開心地收到你的櫻花": 40.0,
        "要步要放個抽獎背景歌": 20.0,  # 你要也可以加
        "吉吉的祝福加持": 10.0,
    },
    "2": {
        "吉吉給你大大的抱抱": 490,
        "天選之人就是你！": 5,
    },
}

def roll_once_by_tiers(loot_table: dict[str, dict[str, float]]) -> str:
    tier_keys = sorted(loot_table.keys(), key=lambda x: int(x))
    for tk in tier_keys:
        tier = loot_table[tk]
        miss_pct = float(tier.get("none", 0.0))

        # 先判定 miss：miss 才去下一層
        if random.random() < (miss_pct / 100.0):
            continue

        # 沒 miss：從本層獎項（排除 none）依權重抽
        prizes = {k: float(v) for k, v in tier.items() if k != "none" and float(v) > 0}
        if not prizes:
            continue

        total = sum(prizes.values())
        r = random.random() * total
        acc = 0.0
        for name, w in prizes.items():
            acc += w
            if r <= acc:
                return name
        return next(iter(prizes.keys()))

    return "none"

def roll_many(times: int) -> list[str]:
    return [roll_once_by_tiers(LOOT_TABLE) for _ in range(times)]


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

# ====== 揪團用 UI 元件 ======
class HangoutModal(discord.ui.Modal):
    def __init__(self, ctx: commands.Context, game_key: str, game_name: str, voice_channel: discord.VoiceChannel):
        super().__init__(title="填寫揪團資訊")
        self.ctx = ctx
        self.game_key = game_key
        self.game_name = game_name
        self.voice_channel = voice_channel

        self.time_input = discord.ui.TextInput(
            label="時間(Time)",
            placeholder="例：今晚 20:00、現在、待定...",
            required=True,
            max_length=100,
        )
        self.add_item(self.time_input)

        self.people_input = discord.ui.TextInput(
            label="人數(People)",
            placeholder="例：還缺 3 人 / 4 人滿",
            required=True,
            max_length=50,
        )
        self.add_item(self.people_input)

        self.remark_input = discord.ui.TextInput(
            label="備註(Remark)",
            style=discord.TextStyle.paragraph,
            placeholder="可留空，預設為「無備註」",
            required=False,
            max_length=400,
        )
        self.add_item(self.remark_input)

    async def on_submit(self, interaction: discord.Interaction):
        """先回 interaction，再丟到背景 task 處理"""
        # 先 defer，避免 3 秒沒回應被判 timeout
        await interaction.response.defer(ephemeral=True, thinking=True)

        # 把真正的處理丟到背景 task，避免「感覺上」整個 bot 卡在這裡
        asyncio.create_task(self._process_submit(interaction))

    async def _process_submit(self, interaction: discord.Interaction):
        ctx = self.ctx
        guild = ctx.guild
        channel = ctx.channel

        時間 = self.time_input.value.strip() or "未填寫"
        人數 = self.people_input.value.strip() or "未填寫"
        備註 = self.remark_input.value.strip() or "無備註"

        game_info = GAME_OPTIONS.get(self.game_key)
        if game_info is None:
            try:
                await interaction.followup.send(
                    "發生錯誤：找不到對應的遊戲設定 QQ",
                    ephemeral=True,
                )
            except discord.HTTPException:
                pass
            return

        game_name = game_info["label"]
        game_role_id = game_info["role_id"]

        base_tag = f"<@&{ROLE_ID14}>"
        game_tag = f"<@&{game_role_id}>" if game_role_id else ""

        message_content = (
            f"## <:No_011:1166191020829069394> 新的揪團開啟囉 <:No_010:1133574932534665297> \n"
            f"主揪：{ctx.author.mention}\n"
            "╭⌕˚꒷ ͝ ꒦₍ᕱ.⑅.ᕱ₎꒦꒷ ͝ ꒦ ͝\n"
            f"<:No_001:1133419740166115359>項目(Item)：{game_name}\n"
            f"<:No_002:1133419757215953039>時間(Time)：{時間}\n"
            f"<:No_003:1133419774500671518>人數(People)：{人數}\n"
            f"<:No_004:1133419788014731325>備註(Remark)：{備註}\n"
            f"<:No_005:1133419804255076525>語音房連結(channel)：\n"
            f"<:No_011:1167260028315639889> https://discord.com/channels/{guild.id}/{self.voice_channel.id}\n"
            "╰ ꒷꒦꒷ ͝ ꒦₍ꐑxꐑ₎꒦ ͝ ꒷ ͝ ꒦\n"
        )

        try:
            # ping 身分組（失敗就算了，只印 log）
            try:
                await channel.send(f"{base_tag} {game_tag}".strip())
            except Exception as e:
                print(f"[DEBUG] 揪團: ping 身分組失敗：{e}")

            # 發揪團訊息
            try:
                msg = await channel.send(message_content)
            except Exception as e:
                print(f"[DEBUG] 揪團: 發揪團訊息失敗：{e}")
                await interaction.followup.send(
                    "揪團訊息送出失敗 QQ，請稍後再試。",
                    ephemeral=True,
                )
                return

            # 嘗試建立 thread
            try:
                if guild is not None and isinstance(channel, discord.TextChannel):
                    member_nick = ctx.author.nick or ctx.author.display_name
                    thread = await channel.create_thread(
                        name=f"{member_nick}",
                        message=msg,
                    )
                    await thread.send(
                        "布蕾布布蕾！\n布丁幫你創好專屬討論串囉\n結束之後記得在這裡講一聲喔"
                    )
                else:
                    print("[DEBUG] 揪團: 無法建立 thread（不是 guild 或不是文字頻道）")
            except Exception as e:
                print(f"[DEBUG] 揪團: 建立 thread 失敗：{e}")

            # 告知使用者完成（用 followup 因為前面已經 defer 了）
            await interaction.followup.send(
                "揪團已發布！一起玩吧 (๑•̀ㅂ•́)و✧",
                ephemeral=True,
            )

        except Exception as e:
            print(f"[DEBUG] 揪團: _process_submit 整體流程錯誤：{e}")
            try:
                await interaction.followup.send(
                    "發生未知錯誤，揪團可能沒有成功送出 QQ",
                    ephemeral=True,
                )
            except discord.HTTPException:
                # 真的完全送不出去就算了，只留 log
                pass


class GameSelect(discord.ui.Select):
    def __init__(self, ctx: commands.Context, voice_channel: discord.VoiceChannel):
        options = [
            discord.SelectOption(label=opt["label"], value=key)
            for key, opt in GAME_OPTIONS.items()
        ]

        super().__init__(
            placeholder="選擇這次揪團的遊戲",
            min_values=1,
            max_values=1,
            options=options,
        )

        self.ctx = ctx
        self.voice_channel = voice_channel

    async def callback(self, interaction: discord.Interaction):
        # 限制只能發起人使用選單
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                "只有發起揪團的人可以選擇遊戲喔～",
                ephemeral=True,
            )
            return

        game_key = self.values[0]
        game_info = GAME_OPTIONS.get(game_key)
        if game_info is None:
            await interaction.response.send_message(
                "這個遊戲不在清單裡 QQ",
                ephemeral=True,
            )
            return

        game_name = game_info["label"]

        # 打開 Modal 讓他填時間、人數、備註
        modal = HangoutModal(
            ctx=self.ctx,
            game_key=game_key,
            game_name=game_name,
            voice_channel=self.voice_channel,
        )
        await interaction.response.send_modal(modal)


class GameSelectView(discord.ui.View):
    def __init__(self, ctx: commands.Context, voice_channel: discord.VoiceChannel):
        super().__init__(timeout=60)
        self.add_item(GameSelect(ctx, voice_channel))

    async def on_timeout(self) -> None:
        # 超時後把選單 disable（避免一直可以點）
        for child in self.children:
            if isinstance(child, discord.ui.Select):
                child.disabled = True
        # 這裡沒辦法直接編輯訊息，因為沒有 msg 物件
        # 如果你想編輯，需要在建立 View 時把 message 存起來
        return


class GeneralCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ====== /hello ======
    @commands.hybrid_command(name="hello", help="跟布丁打招呼～")
    async def hello(self, ctx: commands.Context):
        await ctx.send("你好！")

    # ====== /落櫻抽獎 ======
    @commands.hybrid_command(name="落櫻抽獎", help="使用櫻花抽獎券抽獎")
    @app_commands.describe(抽數="選擇抽獎種類")
    @app_commands.choices(抽數=[
        app_commands.Choice(name="單抽", value=1),
        app_commands.Choice(name="十連抽", value=2),
        app_commands.Choice(name="一百連抽", value=3),
    ])
    async def sakura_gacha(
        self,
        ctx: commands.Context,
        抽數: app_commands.Choice[int],
    ):
        # slash 進來要 defer，避免 3 秒 timeout
        if ctx.interaction is not None:
            await ctx.defer()

        await self._run_sakura_gacha(ctx, 抽數.value)



    async def _run_sakura_gacha(self, ctx: commands.Context, pack_key: int):
        if ctx.guild is None:
            await ctx.send("這個指令只能在伺服器裡使用。")
            return

        if pack_key not in (1, 2, 3):
            await ctx.send("抽數只能是 1(單抽) / 2(十連抽) / 3(一百連抽)")
            return

        guild: discord.Guild = ctx.guild
        member: discord.Member = ctx.author

        pack = DRAW_PACKS.get(pack_key)
        if not pack:
            await ctx.send("抽數選項錯誤。")
            return

        need_role = guild.get_role(pack["need_role_id"])
        if need_role is None:
            await ctx.send("設定錯誤：找不到對應的抽獎券身分組（role id 不存在）。")
            return

        if need_role not in member.roles:
            await ctx.send(f"你沒有 `{need_role.name}`，不能使用 {pack['label']} 喔～")
            return

        # 2) 隨機播放 GIF
        gif_candidates = [p for p in GACHA_GIF_PATHS if os.path.exists(p)]
        gif_msg = None
        if gif_candidates:
            gif_path = random.choice(gif_candidates)
            try:
                gif_msg = await ctx.send(file=discord.File(gif_path))

                # ✅ 這裡開始算時間：訊息「已送出」後，固定停 3 秒
                await asyncio.sleep(GACHA_GIF_STAY_SECONDS)

            except Exception as e:
                print(f"[DEBUG] 抽獎 gif 送出失敗：{e}")

        # 3) 刪掉 GIF
        if gif_msg:
            try:
                await gif_msg.delete()
            except discord.HTTPException:
                pass

        # 4) 扣券
        try:
            await member.remove_roles(need_role, reason="使用落櫻抽獎券後自動扣除")
        except discord.HTTPException as e:
            print(f"[DEBUG] 移除抽獎券失敗：{e}")
            await ctx.send("抽獎券扣除失敗（Bot 權限/身分組階級不足），已中止抽獎。")
            return

        # 5) 抽獎
        times = int(pack["times"])
        results = roll_many(times)

        # 5.5) 如果抽到「天選之人」就給身分組
        if "天選之人就是你！" in results:
            win_role = guild.get_role(ROLE_ID26)
            if win_role is None:
                print("[DEBUG] 設定錯誤：找不到 ROLE_ID26 對應的身分組")
            else:
                if win_role not in member.roles:
                    try:
                        await member.add_roles(win_role, reason="落櫻抽獎：抽到天選之人")
                    except discord.HTTPException as e:
                        print(f"[DEBUG] 給天選身分組失敗：{e}")

        # 6) 統計
        counts: dict[str, int] = {}
        for r in results:
            counts[r] = counts.get(r, 0) + 1

        lines = [
            f"- {prize} × {c}"
            for prize, c in sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        ]

        embed = discord.Embed(
            title=f"🌸 落櫻抽獎結果｜{pack['label']} ({times} 抽)",
            description="\n".join(lines) if lines else "（沒有結果）",
            color=discord.Color.from_rgb(241, 174, 194),
        )
        extra = ""
        if "天選之人就是你！" in results:
            extra = "\n 恭喜你獲得了「天選之人」身分組！"

        await ctx.send(content=f"{member.mention} 消耗 `{need_role.name}`！抽獎完成！{extra}", embed=embed)


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

    # ====== /揪團：輸入 /揪團 就出選單 → 再出 Modal ======
    @commands.hybrid_command(
        name="揪團",
        help="找人一起玩遊戲或聊天或看影片(Let's hang out together and play games.)",
    )
    @app_commands.describe(
        頻道="選擇語音房(Voice channel)",
    )
    async def hang_out(
        self,
        ctx: commands.Context,
        頻道: discord.VoiceChannel,
    ):
        """
        使用方式：
        /揪團 頻道:<語音頻道>
        → Bot 回一則訊息，裡面有遊戲選單
        → 選好遊戲後會跳出 Modal 填「時間、人數、備註」
        → 送出後會發揪團貼文 + 嘗試開討論串
        """
        if ctx.guild is None:
            await ctx.send("這個指令只能在伺服器裡使用。")
            return

        view = GameSelectView(ctx, 頻道)

        try:
            await ctx.send(
                "請從下方選單選擇這次揪團的遊戲：",
                view=view,
            )
        except Exception as e:
            print(f"[DEBUG] /揪團: 送出選單訊息失敗：{e}")
            await ctx.send("發生錯誤，無法顯示遊戲選單 QQ，請稍後再試。")

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