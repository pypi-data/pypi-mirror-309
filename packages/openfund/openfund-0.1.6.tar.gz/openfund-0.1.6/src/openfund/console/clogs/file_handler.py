from __future__ import annotations

from logging.handlers import TimedRotatingFileHandler


class FileHandler(TimedRotatingFileHandler):
    def __init__(
        self,
        filename,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding=None,
        delay=False,
        utc=False,
    ) -> None:
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc)
