import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

print(discord.__version__)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  
bot2 = commands.Bot(command_prefix='/', intents=intents)

@bot2.event
async def on_ready():
    try:
        synced = await bot2.tree.sync()
        print(f"Synced {synced} commands")
    except Exception as e:
        print("An error occurred while syncing: ", e)
    print(f'Logged in as {bot2.user.name}')

@bot2.event
async def on_message(message):
    if message.author.bot:

        return 
    
    member = message.guild.get_member(message.author.id)
    
    if not is_valid_nickname(member.display_name):

        new_nickname = generate_valid_nickname(member.display_name)

        await member.edit(nick=new_nickname)
    
    await bot2.process_commands(message)

def is_valid_nickname(nickname):

    return nickname.startswith("‧˚✮₊") and nickname.endswith("ʕ̯•͡˔•̯᷅ʔ彡⁼³₌₃")

def generate_valid_nickname(original_name):

    prefix = "‧˚✮₊"
    suffix = "ʕ̯•͡˔•̯᷅ʔ彡⁼³₌₃"
    total_length = len(prefix) + len(suffix)
    new_name = original_name[:32 - total_length]
    new_nickname = prefix + new_name + suffix

    return new_nickname

@bot2.hybrid_command(name='hello', help='Greets the user')  
async def hello(ctx):
    await ctx.send('你好！')

bot2.run(os.getenv("BOT_TOKEN1"))  # 布丁
