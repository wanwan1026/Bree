import discord
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  
bot2 = discord.Client(intents=intents)

@bot2.event
async def on_ready():
    print(f'Logged in as {bot2.user.name}')

@bot2.event
async def on_message(message):
    if message.author.bot:
        
        return 
    
    member = message.guild.get_member(message.author.id)
    
    if not is_valid_nickname(member.display_name):

        new_nickname = generate_valid_nickname(member.display_name)

        await member.edit(nick=new_nickname)

def is_valid_nickname(nickname):

    return nickname.startswith("‧˚✮₊") and nickname.endswith("ʕ̯•͡˔•̯᷅ʔ彡⁼³₌₃")

def generate_valid_nickname(original_name):

    prefix = "‧˚✮₊"
    suffix = "ʕ̯•͡˔•̯᷅ʔ彡⁼³₌₃"
    total_length = len(prefix) + len(suffix)
    new_name = original_name[:32 - total_length]
    new_nickname = prefix + new_name + suffix

    return new_nickname


bot2.run(os.getenv("BOT_TOKEN1"))  # 布丁
