# cogs/events.py
import asyncio
import discord
from discord.ext import commands, tasks

from config import (
    TIME_CAPSULE_SOURCE_CHANNEL_ID,
    TIME_CAPSULE_RELAY_CHANNEL_ID,
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
)


def is_valid_nickname(nickname: str) -> bool:
    prefix = "‧˚✮₊"
    suffix = "ʕ̯•͡˔•̯᷅ʔ彡⁼³₌₃"
    return nickname.startswith(prefix) and nickname.endswith(suffix)


def generate_valid_nickname(original_name: str) -> str:
    prefix = "‧˚✮₊"
    suffix = "ʕ̯•͡˔•̯᷅ʔ彡⁼³₌₃"
    total_length = len(prefix) + len(suffix)
    # Discord 暱稱上限 32 字
    new_name = original_name[: 32 - total_length]
    new_nickname = prefix + new_name + suffix
    return new_nickname


def member_has_server_tag(member: discord.Member) -> bool:
    """
    使用 Discord 2024 的「伺服器標籤 / Guild Tag」新功能來判斷：
    - 這個成員的 primary_guild 是否是我們指定的 TAG_GUILD_ID
    - tag 文字是否等於 TAG_STRING
    - enabled 如果明確是 False，視為沒在展示 TAG
    """
    pg = getattr(member, "primary_guild", None)
    if pg is None:
        return False

    pg_id = getattr(pg, "id", None)
    pg_tag = getattr(pg, "tag", None)
    enabled = getattr(pg, "enabled", None)  # 可能是 True / False / None

    if pg_id != TAG_GUILD_ID:
        return False
    if pg_tag != TAG_STRING:
        return False
    # 如果系統明確說「沒開啟」，就視為沒 TAG
    if enabled is False:
        return False

    return True


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # ＝＝＝＝＝ TAG 自動發 / 收回用的暫存結構 ＝＝＝＝＝
        self.grant_queue: asyncio.Queue[int] = asyncio.Queue()
        self.pending_grants: set[int] = set()  # user_id 集合，避免重複排隊

        # 啟動背景 task（會先跑 before_loop → 等 bot.ready）
        self.process_grant_queue.start()
        self.check_role_members.start()
        self.check_role_dependencies.start()

    # ========= on_ready =========
    @commands.Cog.listener()
    async def on_ready(self):
        try:
            synced = await self.bot.tree.sync()
            print(f"Synced {len(synced)} commands")
        except Exception as e:
            print("An error occurred while syncing: ", e)

        print("目前登入身份：", self.bot.user)
        game = discord.Game("布蕾布布蕾 ! ")
        await self.bot.change_presence(
            status=discord.Status.idle,
            activity=game,
        )

    # ========= 語音房暱稱檢查 =========
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # 只有「進入」語音時才檢查
        if before.channel is None and after.channel is not None:
            display_name = getattr(member, "display_name", None)
            if display_name:
                if not is_valid_nickname(display_name):
                    new_nickname = generate_valid_nickname(display_name)
                    try:
                        await member.edit(nick=new_nickname)
                    except discord.Forbidden:
                        print(f"權限錯誤 : 無法更改 {display_name} 的暱稱")
                    except Exception as e:
                        print(f"未知錯誤 : {e}")

    # ========= on_message =========
    # 時光膠囊 + TAG 排隊發身分組 + 最後 process_commands
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # 不理其他機器人
        if message.author.bot:
            return

        # ====== 1. 時光膠囊功能 ======
        if message.channel.id == TIME_CAPSULE_SOURCE_CHANNEL_ID:
            channel_act00 = self.bot.get_channel(TIME_CAPSULE_SOURCE_CHANNEL_ID)
            channel_act = self.bot.get_channel(TIME_CAPSULE_RELAY_CHANNEL_ID)

            member_link = f"<@!{message.author.id}>"
            max_retries = 3
            retry_delay = 5

            for attempt in range(1, max_retries + 1):
                try:
                    if len(message.content) <= 1900:
                        # 回覆原頻道
                        if channel_act00:
                            await channel_act00.send(
                                f"{member_link} 感謝您的參與*ଘ(੭*ˊᗜˋ)੭* ੈ✧‧₊˚"
                            )
                        # 轉送到膠囊展示頻道
                        if channel_act:
                            await channel_act.send(
                                "︶꒷︶︶୨୧︶︶꒷𓈊꒷︶︶୨୧︶︶꒷︶\n"
                                f"{member_link}\n"
                                "留下的時光訊息：\n\n"
                                f"{message.content}\n\n"
                                "︶꒷︶︶୨୧︶︶꒷︶꒷︶︶୨୧︶︶꒷︶",
                                files=[await f.to_file() for f in message.attachments],
                            )
                    else:
                        if channel_act00:
                            await channel_act00.send("字數不可以超過 1900 字唷")

                    # 不管上面哪一步成功，只要沒丟出錯誤就刪除訊息並結束
                    await message.delete()
                    break
                except Exception as e:
                    print(f"時光膠囊發送失敗（第 {attempt} 次），重試中：{e}")
                    if attempt < max_retries:
                        await asyncio.sleep(retry_delay)

        # ====== 2. 伺服器 TAG → 排入自動發放佇列 ======
        # 只處理指定伺服器的訊息
        if message.guild is not None and message.guild.id == TAG_GUILD_ID:
            guild = message.guild
            role = guild.get_role(TAG_ROLE_ID)
            member: discord.Member = message.author

            if role is not None:
                # 已經有角色就不用排隊（之後由定期檢查負責收回）
                if role not in member.roles:
                    if member_has_server_tag(member) and member.id not in self.pending_grants:
                        await self.grant_queue.put(member.id)
                        self.pending_grants.add(member.id)
                        print(f"排入發放佇列：{member}（TAG 符合 {TAG_STRING}）")

        # ====== 3. 交給指令系統處理 ======
        await self.bot.process_commands(message)

    # ======================================
    # 背景 worker：每秒處理固定數量的發放
    # ======================================
    @tasks.loop(seconds=1)
    async def process_grant_queue(self):
        guild = self.bot.get_guild(TAG_GUILD_ID)
        if guild is None:
            return

        role = guild.get_role(TAG_ROLE_ID)
        if role is None:
            return

        MAX_PER_TICK = 10  # 每秒最多幫幾個人發

        for _ in range(MAX_PER_TICK):
            if self.grant_queue.empty():
                break

            user_id = await self.grant_queue.get()
            self.pending_grants.discard(user_id)

            member = guild.get_member(user_id)
            if member is None:
                continue
            if role in member.roles:
                continue

            if member_has_server_tag(member):
                try:
                    await member.add_roles(role, reason="使用伺服器 TAG → 自動發放")
                    print(f"[發放完成] {member}")
                except discord.HTTPException as e:
                    print(f"發放給 {member} 時失敗：{e}")
            else:
                # 安全起見：如果到這一步已經沒有 TAG，就不發
                print(f"[略過發放] {member} 目前已沒有符合的伺服器 TAG")

    @process_grant_queue.before_loop
    async def before_process_grant_queue(self):
        await self.bot.wait_until_ready()
        print("發放佇列處理 worker 已啟動")

    # ==============================
    # 定期檢查：把沒 TAG 的人收回角色
    # ==============================
    @tasks.loop(minutes=30)
    async def check_role_members(self):
        try:
            guild = self.bot.get_guild(TAG_GUILD_ID)
            if guild is None:
                print("[check_role_members] 找不到 guild，直接跳出本輪")
                return

            role = guild.get_role(TAG_ROLE_ID)
            if role is None:
                print("[check_role_members] 找不到角色，直接跳出本輪")
                return

            print("開始檢查：擁有身分組的成員是否仍然使用伺服器 TAG")

            BATCH_SIZE = 20
            removed_count = 0

            for idx, member in enumerate(list(role.members), start=1):
                if member.bot:
                    continue

                still_has_tag = member_has_server_tag(member)

                pg = getattr(member, "primary_guild", None)
                pg_id = getattr(pg, "id", None)
                pg_tag = getattr(pg, "tag", None)
                print(
                    f"[TAG檢查] {member} | primary_guild.id={pg_id} | "
                    f"primary_guild.tag={pg_tag} | 判定 still_has_tag={still_has_tag}"
                )

                if not still_has_tag:
                    try:
                        await member.remove_roles(role, reason="未使用伺服器 TAG → 自動收回")
                        removed_count += 1
                        print(f"[自動收回] {member}")
                    except discord.HTTPException as e:
                        print(f"收回 {member} 失敗：{e}")

                if idx % BATCH_SIZE == 0:
                    await asyncio.sleep(1)

            print(f"檢查完成，本輪共收回 {removed_count} 人的身分組\n")

        except Exception as e:
            # ⚠️ 這個一定要有，這樣 loop 出錯不會直接死掉
            import traceback

            print("[check_role_members] 迴圈內發生未捕捉錯誤，已攔截避免 loop 停止")
            traceback.print_exception(type(e), e, e.__traceback__)

    # ==============================
    # 定期檢查：身分組依賴關係
    # 16~20 這幾個只要缺 21 或 22，就全部拔掉
    # ==============================
    @tasks.loop(minutes=30)
    async def check_role_dependencies(self):
        try:
            guild = self.bot.get_guild(TAG_GUILD_ID)
            if guild is None:
                print("[check_role_dependencies] 找不到 guild，直接跳出本輪")
                return

            # 主要身分組（任一個就算）
            main_role_ids = [ROLE_ID16, ROLE_ID17, ROLE_ID18, ROLE_ID19, ROLE_ID20]
            required_role_ids = [ROLE_ID21, ROLE_ID22]

            main_roles = [guild.get_role(rid) for rid in main_role_ids]
            required_roles = [guild.get_role(rid) for rid in required_role_ids]

            # 過濾掉 None（避免哪個角色被刪掉）
            main_roles = [r for r in main_roles if r is not None]
            required_roles = [r for r in required_roles if r is not None]

            if not main_roles:
                print("[check_role_dependencies] 找不到任何 main 角色，直接跳出本輪")
                return
            if len(required_roles) < 2:
                print("[check_role_dependencies] 必要角色少於 2 個（21 / 22），請檢查設定")
                # 你也可以選擇 return
                # return

            print("開始檢查：身分組依賴 (16~20 需要同時擁有 21 & 22)")

            BATCH_SIZE = 50
            idx = 0
            cleaned_members = 0

            # ✅ 只檢查「有 16~20 的成員」
            members_to_check: set[discord.Member] = set()
            for r in main_roles:
                members_to_check.update(r.members)

            for member in list(members_to_check):
                if member.bot:
                    continue

                # 理論上這裡一定是 True，但保險再判一次
                has_main = any(r in member.roles for r in main_roles)
                if not has_main:
                    continue

                # 是否同時擁有 21 & 22
                has_all_required = all(r in member.roles for r in required_roles)

                print(
                    f"[依賴檢查] {member} | has_main={has_main} | "
                    f"has_all_required={has_all_required}"
                )

                # 只要缺 21 或 22 就拔掉 16~20
                if not has_all_required:
                    roles_to_remove = [r for r in main_roles if r in member.roles]
                    if roles_to_remove:
                        try:
                            await member.remove_roles(
                                *roles_to_remove,
                                reason="缺少必要身分組 (21/22) → 自動收回 16~20"
                            )
                            cleaned_members += 1
                            print(f"[依賴收回] {member}，移除 {len(roles_to_remove)} 個主身分組")
                        except discord.HTTPException as e:
                            print(f"[依賴收回失敗] {member}：{e}")

                idx += 1
                if idx % BATCH_SIZE == 0:
                    await asyncio.sleep(1)

            print(f"依賴檢查完成，本輪共處理 {cleaned_members} 位成員\n")

        except Exception as e:
            import traceback

            print("[check_role_dependencies] 迴圈內發生未捕捉錯誤，已攔截避免 loop 停止")
            traceback.print_exception(type(e), e, e.__traceback__)

    @check_role_dependencies.before_loop
    async def before_check_role_dependencies(self):
        await self.bot.wait_until_ready()
        print("身分組依賴檢查 task 已啟動")



    @check_role_members.before_loop
    async def before_check_role_members(self):
        await self.bot.wait_until_ready()
        print("身分組成員 TAG 檢查 task 已啟動")


async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))
