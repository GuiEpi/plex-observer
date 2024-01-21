import argparse
from src.bot import client
from configparser import ConfigParser
from src import set_stream_handler

config = ConfigParser()
config.read("./config.ini")

parser = argparse.ArgumentParser(
    prog="plex-observer",
    description="Check the number of users connected to your plex server.",
)
parser.add_argument(
    "-e",
    "--env",
    type=str,
    choices=["prod", "dev"],
    default="prod",
    help="Environment to run the bot in.",
)


def main():
    args = parser.parse_args()
    if args.env == "prod":
        TOKEN = config.get("discord", f"token")
    else:
        set_stream_handler()
        TOKEN = config.get("discord", f"token_{args.env}")
    client.run(TOKEN)


if __name__ == "__main__":
    main()
