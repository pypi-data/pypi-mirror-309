from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from openfund.plugins.base_plugin import BasePlugin


if TYPE_CHECKING:
    from cleo.io.io import IO

    from openfund.pyopenfund import Openfund


class Plugin(BasePlugin):
    """
    Generic plugin not related to the console application.
    """

    group = "openfund.plugin"

    @abstractmethod
    def activate(self, openfund: Openfund, io: IO) -> None:
        raise NotImplementedError()
