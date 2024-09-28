import os
import discord
import json
from discord.ext import tasks
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

bot = discord.Bot(intents=discord.Intents.all())

ALREADY_OFFLINE = False
def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def save_config(config):
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

async def update_message(channel, message_id, description, color):
    try:
        msg = await channel.fetch_message(message_id)
        await msg.edit(embed=discord.Embed(title="Status", description=description, color=color))
    except discord.NotFound:
        msg = await channel.send(embed=discord.Embed(title="Status", description=description, color=color))
        return msg.id
    return message_id

@bot.event
async def on_ready():
    config = load_config()
    channel = bot.get_channel(config["channel"])
    if channel:
        guild = bot.get_guild(config['guild'])
        awabot = guild.get_member(config['bot'])
        status = "🟢 AwaBot est en ligne\n Prochaine vérification: " if awabot.status != discord.Status.offline else "🔴 AwaBot est hors ligne\n Prochaine vérification: "
        color = 0x00ff00 if awabot.status == discord.Status.online else 0xff0000
        description = f"{status} <t:{int(datetime.now().timestamp()) + config['time-before-reload']}:R>"
        config["message"] = await update_message(channel, config.get("message"), description, color)
        save_config(config)
    if not check.is_running():
        check.start()

@tasks.loop(seconds=load_config()['time-before-reload'])
async def check():
    global ALREADY_OFFLINE
    config = load_config()
    channel = bot.get_channel(config["channel"])
    if channel:
        guild = bot.get_guild(config['guild'])
        awabot = guild.get_member(config['bot'])
        status = "🟢 AwaBot est en ligne\n Prochaine vérification: " if awabot.status != discord.Status.offline else "🔴 AwaBot est hors ligne\n Prochaine vérification: "
        color = 0x00ff00 if awabot.status != discord.Status.offline else 0xff0000
        description = f"{status} <t:{int(datetime.now().timestamp()) + config['time-before-reload']}:R>"
        config["message"] = await update_message(channel, config.get("message"), description, color)
        save_config(config)
        if not ALREADY_OFFLINE and awabot.status == discord.Status.offline:
            for user_id in config['owner']:
                user = bot.get_user(user_id)
                await user.send(f"{awabot.mention} est hors ligne <t:{int(datetime.now().timestamp())}>")
            ALREADY_OFFLINE = True

bot.run(os.getenv("TOKEN"))