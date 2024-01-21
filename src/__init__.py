import logging

logger = logging.getLogger("plex_observer")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("plex_observer.log")

formatter = logging.Formatter(
    "%(asctime)s %(module)12s:%(lineno)-4s %(levelname)-9s %(message)s"
)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def set_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
