# cogs/commands_general.py
import random
import discord
from discord.ext import commands

from config import ROLE_ID14


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
    項目: str = commands.flag(description="主題內容(Game name)")
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

    # ====== /揪團 ======
    @commands.hybrid_command(
        name="揪團",
        help="找人一起玩遊戲或聊天或看影片(Let's hang out together and play games.)",
    )
    async def hang_out(self, ctx: commands.Context, *, flags: hang_out_Flags):
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


async def setup(bot: commands.Bot):
    await bot.add_cog(GeneralCommands(bot))
