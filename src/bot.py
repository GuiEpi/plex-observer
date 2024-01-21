import discord
from discord.ext import tasks
from src.observer import Observer
from configparser import ConfigParser
from src import logger

try:
    config = ConfigParser()
    config.read("./config.ini")
    settings = config["settings"]
    PLACES = settings.getint("places", 5)
    INTERVAL = settings.getint("interval", 10)

    plex_auth = config["plex"]
    USERNAME = plex_auth.get("username", None)
    PASSWORD = plex_auth.get("password", None)
    BASEURL = plex_auth.get("baseurl", None)
    TOKEN = plex_auth.get("token", None)
except KeyError as e:
    logger.error(f"Error in config.ini file: no section {e} provided.")
    exit(1)

client = discord.Client()


@client.event
async def on_ready():
    logger.info(f"{client.user} is ready and online!")
    try:
        observer = Observer(USERNAME, PASSWORD, BASEURL, TOKEN)
        updater.start(observer)
    except RuntimeError:
        logger.warning("A task has already been launched and is running.")
    except Exception as e:
        logger.error(f"Error in run task: {e}")
        exit(1)


@tasks.loop(seconds=INTERVAL)
async def updater(observer: Observer):
    observer.update()
    places_available = PLACES - observer.users
    status = get_status(places_available)
    game_message = get_game_message(places_available)
    await client.change_presence(status=status, activity=game_message)


def get_status(places_available: int) -> discord.Status:
    if places_available > round_up(50 / 100 * PLACES):
        status = discord.Status.online
    elif places_available < round_up(10 / 100 * PLACES):
        status = discord.Status.dnd
    elif places_available <= round_up(50 / 100 * PLACES):
        status = discord.Status.idle
    return status


def get_game_message(places_available: int) -> discord.Game:
    if places_available < 0:
        message = discord.Game(f"{-places_available} user(s) must log out!")
    elif places_available == 0:
        message = discord.Game(f"No place available!")
    else:
        message = discord.Game(f"Place(s) available: {places_available}/{PLACES}")
    return message


def round_up(number):
    return int(number) + (number % 1 > 0)
