# plex-observer
Plex observer is a discord bot that sends a message to prevent connections/disconnections in a specific channel.

```
git clone https://github.com/GuiEpi/plex-observer.git
```
## .env
```
TOKEN = discord_bot_token
PLEX_USER = plex_username
PLEX_PASS = plex_password
DISCORD_CHAN = 012345678910 
TIME = 1200 
```
> time in **seconds**
## deployment with docker
1. Change to the plex observer project directory.
```
cd ~/plex-observer
```
2. Build the docker container for the plex observer.
```
docker build -t plex-observer .
```
3. Run the docker container.

```
docker run -d plex-observer
```
> Running the bot with -d flag runs the container in detached mode (it runs in the background).