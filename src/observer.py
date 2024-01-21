from plexapi.server import PlexServer
from plexapi.exceptions import NotFound, Unauthorized
from plexapi.myplex import MyPlexAccount
from plexapi.video import Episode
from src import logger


class CredidentialsNotProvided(Exception):
    pass


class BadCredentialsException(Exception):
    pass


class Observer:
    def __init__(
        self,
        username: str = None,
        password: str = None,
        baseurl: str = None,
        token: str = None,
    ):
        if (not username and not password) and (not baseurl and not token):
            raise CredidentialsNotProvided(
                "You must provide a username and password or a baseurl and token in config.ini file."
            )
        self.plex = self._connection(username, password, baseurl, token)
        self.users: int = None

    def update(self) -> int:
        try:
            self.users = 0
            for video in self.plex.sessions():
                state = video.players[0].state if video.players else None
                if state and state != "paused":
                    self.users += 1
            return self.users
        except Exception as e:
            logger.warning(f"Impossible to update number of users.\n{e}")

    def _connection(
        self, username, password, baseurl, token
    ) -> PlexServer | MyPlexAccount:
        try:
            self.plex = self._fetch_plex_instance(username, password, baseurl, token)
            return self.plex
        except Unauthorized:
            raise BadCredentialsException("Invalid username or password.")
        except NotFound:
            raise BadCredentialsException("Invalid baseurl or token.")

    def _video_title_episode(self, video) -> str:
        if video.type == Episode.TYPE:
            return f"{video.grandparentTitle} s{video.seasonNumber}e{video.index}"
        return video.title

    def _fetch_plex_instance(
        self, username, password, baseurl, token
    ) -> PlexServer | MyPlexAccount:
        username = username
        password = password
        baseurl = baseurl
        token = token
        if baseurl:
            logger.info(f"Connecting to Plex server: {baseurl}")
            return PlexServer(baseurl, token)
        logger.info(f"Logging into MyPlex with user {username}")
        user = MyPlexAccount(username, password)
        host = user.resources()[0]
        return host.connect()
