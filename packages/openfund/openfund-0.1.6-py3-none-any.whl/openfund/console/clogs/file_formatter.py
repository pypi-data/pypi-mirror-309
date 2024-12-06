from __future__ import annotations

import logging
import sys
import textwrap

from pathlib import Path
from typing import TYPE_CHECKING

from openfund.console.clogs.filters import OPENFUND_FILTER
from openfund.console.clogs.formatters import FORMATTERS


if TYPE_CHECKING:
    from logging import LogRecord


class FileFormatter(logging.Formatter):

    _format = "%(asctime)s - %(process)d | %(threadName)s | %(module)s.%(funcName)s:%(lineno)d - %(levelname)s -%(message)s"

    _datefmt = "%Y-%m-%d-%H:%M:%S"  # 时间

    def __init__(self, fmt=_format, datefmt=_datefmt, style="%") -> None:
        super().__init__(fmt, datefmt, style)
