import discord
from discord.ext import commands, tasks
from plexapi.myplex import MyPlexAccount
import os 
from dotenv import load_dotenv

load_dotenv() # load all the variables from the env file
bot = commands.Bot(command_prefix="!")

account = MyPlexAccount(os.getenv('PLEX_USER'), os.getenv('PLEX_PASS'))
plex = account.resources()[0].connect() # returns a PlexServer instance

print("Connected to Plex API")

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    sender.start()

def watcher():
    count = 0
    embed=discord.Embed(title="Plex watcher", url="https://app.plex.tv/desktop/#!/", description="who watches plex?")
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Plex_logo_2022.svg/800px-Plex_logo_2022.svg.png?20220502185220")
    if plex.sessions():
        for session in plex.sessions():
            count += 1
            username = session.usernames[0]
            title = session.grandparentTitle
            sub_title = session.title
            for player in session.players:
                status = player.state
            if status == 'playing':
                embed.add_field(name=username, value=f":arrow_forward: {title}", inline=False)
            elif status == 'paused':
                embed.add_field(name=username, value=f":pause_button: {title}", inline=False)
        if count == 1:
            embed.set_footer(text="place available: 1")
        elif count >= 2:
            embed.set_footer(text="place available: 0")
    else:
        embed.set_footer(text="places available: 2")
    return embed
       
@tasks.loop(seconds=int(os.getenv('TIME')))
async def sender():
    print("watch...")
    channel = bot.get_channel(int(os.getenv('DISCORD_CHAN')))
    embed = watcher()
    await channel.send(embed=embed)

bot.run(os.getenv('TOKEN')) 