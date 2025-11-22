# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN1")

# 角色 ID
ROLE_ID10 = int(os.getenv("ROLE_ID10"))  # 銀
ROLE_ID11 = int(os.getenv("ROLE_ID11"))  # 紫
ROLE_ID12 = int(os.getenv("ROLE_ID12"))  # 金
ROLE_ID13 = int(os.getenv("ROLE_ID13"))  # 一次改名
ROLE_ID14 = int(os.getenv("ROLE_ID14"))  # 一次改名（揪團 ping 用）

# 頻道 ID（你 .env 裡已經有的）
CHANNEL_ID18 = int(os.getenv("CHANNEL_ID18"))  # 集合囉!小櫻花
CHANNEL_ID20 = int(os.getenv("CHANNEL_ID20"))  # 時光膠囊寄送
CHANNEL_ID21 = int(os.getenv("CHANNEL_ID21"))  # 時光膠囊回收

# === 時光膠囊頻道(每年更換) ===
TIME_CAPSULE_SOURCE_CHANNEL_ID = 1439139068549271673  # 抓訊息的原始頻道
TIME_CAPSULE_RELAY_CHANNEL_ID  = 1439139369515614249  # 收集／重發的頻道

# === tag ===
TAG_GUILD_ID = int(os.getenv("guild_id")) 
TAG_ROLE_ID = int(os.getenv("ROLE_ID15"))
TAG_STRING = os.getenv("STRING")

# === check ===
ROLE_ID16 = int(os.getenv("ROLE_ID16"))
ROLE_ID17 = int(os.getenv("ROLE_ID17"))
ROLE_ID18 = int(os.getenv("ROLE_ID18"))
ROLE_ID19 = int(os.getenv("ROLE_ID19"))
ROLE_ID20 = int(os.getenv("ROLE_ID20"))

ROLE_ID21 = int(os.getenv("ROLE_ID21"))
ROLE_ID22 = int(os.getenv("ROLE_ID22"))