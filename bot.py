from collections import deque
from matplotlib.pyplot import title
from plexapi.myplex import MyPlexAccount
from dotenv import load_dotenv
from discord.ext import commands, tasks
from Session import Session
from Watcher import Watcher
import discord
import os 

load_dotenv() 

try:
    account = MyPlexAccount(os.getenv('PLEX_USER'), os.getenv('PLEX_PASS'))
    plex = account.resources()[0].connect() # returns a PlexServer instance
    print('Connected to the plex api!')
except:
    print('Impossible to connect to plex api..')
    print('Check if your credentials are correct.')
    print('If so, check if your plex server is operational.')

bot = commands.Bot(command_prefix='$')

session_ = Session.create()

accounts = []
for account in plex.systemAccounts():
    if account.name:
        accounts.append(account.name)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    sender.start()

@tasks.loop(seconds=int(os.getenv('TIME')))
async def sender():
    channel = bot.get_channel(int(os.getenv('DISCORD_CHAN')))
    resp = plex_observer()
    if type(resp) is discord.embeds.Embed:
        await channel.send(embed=resp)
    elif type(resp) is list:
        for user in resp:
            embed = embed_maker(desc="A user has logged out!")
            embed.add_field(name="[INFO]", value=f":stop_button: {user} disconnected.", inline=False)
            embed_footer_maker(embed)
            await channel.send(embed=embed)

def plex_observer() -> discord.Embed or list:
    users = []
    if plex.sessions():
        for session in plex.sessions():
            username = session.usernames[0]
            users.append(username)
            if session.type == "movie":
                title = session.title
            else:
                title = session.grandparentTitle
            for player in session.players:
                status = player.state
            if username not in session_.watchers.keys():
                session_.add(Watcher.create(username, title, status))
                embed = embed_maker(desc='A user has logged in!')
                for key in session_.watchers.keys():
                    if status == 'playing':
                        embed.add_field(name=session_.watchers[key].name, value=f":arrow_forward: {session_.watchers[key].title}", inline=False)
                    elif status == 'paused':
                        embed.add_field(name=session_.watchers[key].name, value=f":pause_button: {session_.watchers[key].title}", inline=False)
                embed_footer_maker(embed)
                return embed
    disconnected_user = []
    for account in accounts:
        if account not in users:
            if account in session_.watchers.keys():
                session_.delete(account)
                disconnected_user.append(account)
    return disconnected_user
    
def embed_maker(desc: str) -> discord.Embed:
    embed=discord.Embed(title="Plex observer :eyes:", url="https://app.plex.tv/desktop/#!/", description=desc)
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Plex_logo_2022.svg/800px-Plex_logo_2022.svg.png?20220502185220")
    return embed

def embed_footer_maker(embed) -> discord.Embed:
    if session_.places == -1:
        embed.set_footer(text="a user must log out")
    else:
        embed.set_footer(text=f"place(s) available: {session_.places}")

bot.run(os.getenv('TOKEN')) 