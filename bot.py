import discord
import json
from discord.ext import tasks
from datetime import datetime
bot = discord.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    f = open("config.json","r")
    config = json.load(f)
    channel = bot.get_channel(config["channel"])
    if channel:
        try:
            msg = await channel.fetch_message(config["message"])
        except:
            msg = None
        if msg:
            guild = bot.get_guild(config['guild'])
            awabot = guild.get_member(config['bot'])
            if awabot.status == discord.Status.online:
                await msg.edit(embed=discord.Embed(title="Status", description=f"🟢 AwaBot est en ligne <t:{int(datetime.now().timestamp()) + c['time-before-reload']}:R>", color=0x00ff00))
            else:
                await msg.edit(embed=discord.Embed(title="Status", description=f"🔴 AwaBot est hors ligne <t:{int(datetime.now().timestamp()) + c['time-before-reload']}:R>", color=0xff0000))
        else:
            guild = bot.get_guild(config['guild'])
            awabot = guild.get_member(config['user'])
            if awabot.status == discord.Status.online:
                mseg=await channel.send(embed=discord.Embed(title="Status", description=f"🟢 {awabot.mention} est en ligne\n Prochain rechargement: <t:{int(datetime.now().timestamp()) + c['time-before-reload']}:R>", color=0x00ff00))
            else:
                mseg=await channel.send(embed=discord.Embed(title="Status", description=f"🔴 {awabot.mention} est hors ligne\n Prochain rechargement: <t:{int(datetime.now().timestamp()) + c['time-before-reload']}:R> ", color=0xff0000))
            
            new=json.dumps({"channel": channel.id, "message": mseg.id})
            f = open("config.json","w")
            f.write(new)
            f.close()
    if not check.is_running():
        
        check.start()
        
c = json.load(open("config.json","r")) 
@tasks.loop(seconds=c['time-before-reload'])
async def check():
    f = open("config.json","r")
    config = json.load(f)
    channel = bot.get_channel(config["channel"])
    if channel:
        try:
            msg = await channel.fetch_message(config["message"])
        except:
            msg = None
        if msg:
            guild = bot.get_guild(config['guild'])
            awabot = guild.get_member(config['bot'])
            if awabot.status == discord.Status.online:
                await msg.edit(embed=discord.Embed(title="Status", description=f"🟢 {awabot.mention} est en ligne\n Prochain rechargement: <t:{int(datetime.now().timestamp()) + c['time-before-reload']}:R>", color=0x00ff00))
            else:
                await msg.edit(embed=discord.Embed(title="Status", description=f"🔴 {awabot.mention} est hors ligne\n Prochain rechargement: <t:{int(datetime.now().timestamp()) + c['time-before-reload']}:R>", color=0xff0000))
                for users in config['owner']:
                    user = bot.get_user(users)
                    await user.send(f"{awabot.mention} est hors ligne <t:{int(datetime.now().timestamp())}>")
                    
                    
c = json.load(open("config.json","r"))
bot.run(c['token'])