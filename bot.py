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

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    sender.start()

@tasks.loop(seconds=int(os.getenv('TIME')))
async def sender():
    channel = bot.get_channel(int(os.getenv('DISCORD_CHAN')))
    watchers = []
    connexion = connection_observer(watchers)
    if connexion:
        await channel.send(embed=connexion)
    deconnection = disconnection_observer(watchers)
    if deconnection:
        await channel.send(embed=deconnection)

def connection_observer(watchers: list) -> discord.Embed:
    count = 0
    if plex.sessions():
        embed = embed_maker(desc='A user has logged in!')
        for session in plex.sessions():
            username = session.usernames[0]
            watchers.append(username)
            if session.type == "movie":
                title = session.title
            else:
                title = session.grandparentTitle
            for player in session.players:
                status = player.state
            if username not in session_.watchers.keys():
                count += 1
                session_.add(Watcher.create(username))
                if status == 'playing':
                    embed.add_field(name=username, value=f":arrow_forward: {title}", inline=False)
                elif status == 'paused':
                    embed.add_field(name=username, value=f":pause_button: {title}", inline=False)
        if count > 0:
            embed_footer_maker(embed)
            return embed

def disconnection_observer(watchers: list) -> discord.Embed:
    disconnected_users = session_.watch_disconnected_users(watchers)
    if disconnected_users:
        embed = embed_maker(desc="A user has logged out!")
        for user in disconnected_users:
            embed.add_field(name="[INFO]", value=f":stop_button: {user} disconnected.", inline=False)
        embed_footer_maker(embed)
        return embed
    
def embed_maker(desc: str) -> discord.Embed:
    embed=discord.Embed(title="Plex observer :eyes:", url="https://app.plex.tv/desktop/#!/", description=desc)
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Plex_logo_2022.svg/800px-Plex_logo_2022.svg.png?20220502185220")
    return embed

def embed_footer_maker(embed: discord.Embed) -> discord.Embed:
    if session_.places == -1:
        embed.set_footer(text="a user must log out")
    else:
        embed.set_footer(text=f"place(s) available: {session_.places}")

bot.run(os.getenv('TOKEN')) 