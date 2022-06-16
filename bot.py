from collections import deque
from matplotlib.pyplot import title
from plexapi.myplex import MyPlexAccount
from dotenv import load_dotenv
from discord.ext import commands, tasks
from Session import Session
from Watcher import Watcher
import discord
import os 

load_dotenv() # load all the variables from the env file

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
            await channel.send(f"{user} disconnected.")

def plex_observer() -> discord.embeds.Embed or list:
    users = []
    if plex.sessions():
        for session in plex.sessions():
            username = session.usernames[0]
            users.append(username)
            title = session.grandparentTitle
            sub_title = session.title
            for player in session.players:
                status = player.state
            if username not in session_.watchers.keys():
                embed=discord.Embed(title="Plex observer", url="https://app.plex.tv/desktop/#!/", description="who watche(s) plex?")
                embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Plex_logo_2022.svg/800px-Plex_logo_2022.svg.png?20220502185220")
                session_.add(Watcher.create(username, title, status))
                for key in session_.watchers.keys():
                    if status == 'playing':
                        embed.add_field(name=session_.watchers[key].name, value=f":arrow_forward: {session_.watchers[key].title}", inline=False)
                    elif status == 'paused':
                        embed.add_field(name=session_.watchers[key].name, value=f":pause_button: {session_.watchers[key].title}", inline=False)
                place = place_available(len(users))
                if place == -1:
                    embed.set_footer(text="a user must log out")
                else:
                    embed.set_footer(text=f"place(s) available: {place}")
                return embed
    disconnected_user = []
    for account in accounts:
        if account not in users:
            if account in session_.watchers.keys():
                session_.delete(account)
                disconnected_user.append(account)
    return disconnected_user
    
def place_available(count: int) -> int:
    if count == 0:
        return 2
    elif count == 1:
        return 1
    elif count == 2:
        return 0
    elif count > 2:
        return -1

bot.run(os.getenv('TOKEN')) 