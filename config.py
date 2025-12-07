# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN3")

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

ROLE_GAME_ID1 = int(os.getenv("ROLE_GAME_ID1"))
ROLE_GAME_ID2 = int(os.getenv("ROLE_GAME_ID2"))
ROLE_GAME_ID3 = int(os.getenv("ROLE_GAME_ID3"))
ROLE_GAME_ID4 = int(os.getenv("ROLE_GAME_ID4"))
ROLE_GAME_ID5 = int(os.getenv("ROLE_GAME_ID5"))
ROLE_GAME_ID6 = int(os.getenv("ROLE_GAME_ID6"))
ROLE_GAME_ID7 = int(os.getenv("ROLE_GAME_ID7"))
ROLE_GAME_ID8 = int(os.getenv("ROLE_GAME_ID8"))
ROLE_GAME_ID9 = int(os.getenv("ROLE_GAME_ID9"))
ROLE_GAME_ID10 = int(os.getenv("ROLE_GAME_ID10"))
ROLE_GAME_ID11 = int(os.getenv("ROLE_GAME_ID11"))
ROLE_GAME_ID12 = int(os.getenv("ROLE_GAME_ID12"))
ROLE_GAME_ID13 = int(os.getenv("ROLE_GAME_ID13"))
ROLE_GAME_ID14 = int(os.getenv("ROLE_GAME_ID14"))
ROLE_GAME_ID15 = int(os.getenv("ROLE_GAME_ID15"))
ROLE_GAME_ID16 = int(os.getenv("ROLE_GAME_ID16"))
ROLE_GAME_ID17 = int(os.getenv("ROLE_GAME_ID17"))
ROLE_GAME_ID18 = int(os.getenv("ROLE_GAME_ID18"))
ROLE_GAME_ID19 = int(os.getenv("ROLE_GAME_ID19"))
ROLE_GAME_ID20 = int(os.getenv("ROLE_GAME_ID20"))
ROLE_GAME_ID21 = int(os.getenv("ROLE_GAME_ID21"))
ROLE_GAME_ID22 = int(os.getenv("ROLE_GAME_ID22"))
ROLE_GAME_ID23 = int(os.getenv("ROLE_GAME_ID23"))
ROLE_GAME_ID24 = int(os.getenv("ROLE_GAME_ID24"))
ROLE_GAME_ID25 = int(os.getenv("ROLE_GAME_ID25"))
ROLE_GAME_ID26 = int(os.getenv("ROLE_GAME_ID26"))
ROLE_GAME_ID27 = int(os.getenv("ROLE_GAME_ID27"))
ROLE_GAME_ID28 = int(os.getenv("ROLE_GAME_ID28"))
ROLE_GAME_ID29 = int(os.getenv("ROLE_GAME_ID29"))
ROLE_GAME_ID30 = int(os.getenv("ROLE_GAME_ID30"))
ROLE_GAME_ID31 = int(os.getenv("ROLE_GAME_ID31"))
ROLE_GAME_ID32 = int(os.getenv("ROLE_GAME_ID32"))
ROLE_GAME_ID33 = int(os.getenv("ROLE_GAME_ID33"))
ROLE_GAME_ID34 = int(os.getenv("ROLE_GAME_ID34"))
ROLE_GAME_ID35 = int(os.getenv("ROLE_GAME_ID35"))
ROLE_GAME_ID36 = int(os.getenv("ROLE_GAME_ID36"))
ROLE_GAME_ID37 = int(os.getenv("ROLE_GAME_ID37"))

guild_id = int(os.getenv("guild_id"))