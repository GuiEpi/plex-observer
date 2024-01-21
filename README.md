![Project Image](https://raw.githubusercontent.com/GuiEpi/plex-observer/master/assets/mtcc_nfo_builder.png)

# Plex Observer

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) 
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
![Python 3.11](https://img.shields.io/badge/python-3.11-blue)


Plex Observer is a Discord bot that monitors a Plex server and updates the bot's status based on the number of available slots on the server.

## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.11
- [Poetry](https://python-poetry.org/docs/)

### Installation

1. Clone the repo
```bash
git clone https://github.com/GuiEpi/plex-observer.git
```
2. Navigate to the project directory
```bash
cd plex-observer
```
3. Set the Python version for the environment
```bash
poetry env use 3.11
```
4. Install dependencies
```bash
poetry install
```
> Note: The project uses Python 3.11 due to an issue with the multidict dependency in Python 3.12.

## ⚙️ Configuration
Plex Observer requires minimal configuration to function. You need to provide a Discord bot token and Plex credentials (either a username and password or a baseurl and token).

An minimal example configuration file is provided as `example.config.ini`. Simply replace `<discord-bot-token>`, `<plex-username>` and `<plex-username>` with yours and rename the file to `config.ini`.

Here's an example of a fully specified `config.ini` file:
```ini
[settings]
places = 10
interval = 10

[discord]
token = NDY3NzE1NTAbUjYwMzg2ODI2.DiuplA.T336twFYOlzcHqcU1xV5skYyHX0
token_dev = BuZbzE1NTAyJIUhdvYwMzg2ODI2.JaopjB.T529twFYOlzcHqcU1uEK78jx

[plex]
username = johndoe
password = kodi-stinks
baseurl = http://127.0.0.1:32400
token = XBHSMSJSDJ763JSm
```

## 🕹 Usage
To run Plex Observer, execute the following command:
```bash
poetry run python3 src/main.py
```
You can specify the environment (prod or dev) with the -e or --env argument:
```bash
poetry run python3 src/main.py --env dev
```

## 🐳 Docker Deployment
You can also deploy Plex Observer using Docker:
```bash
docker build -t plex-observer .
docker run -d plex-observer
```
> * `-t plex-observer`: This flag is used in the `docker build` command. The `-t` stands for "tag". It tags the image with the name `plex-observer` so you can easily refer to the image later.
> * `-d`: This flag is used in the `docker run` command. The `-d` stands for "detached". It means that Docker will run your container in the background and print the container ID.


## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📝 License
This project is licensed under the MIT License.