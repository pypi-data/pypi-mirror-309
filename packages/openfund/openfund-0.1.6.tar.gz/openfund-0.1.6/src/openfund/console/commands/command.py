from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from cleo.commands.command import Command as BaseCommand
from cleo.exceptions import CleoValueError


if TYPE_CHECKING:
    from openfund.console.application import Application
    from openfund.pyopenfund import Openfund


class Command(BaseCommand):
    loggers: list[str] = []

    _openfund: Openfund | None = None

    @property
    def openfund(self) -> Openfund:
        if self._openfund is None:
            return self.get_application().openfund

        return self._openfund

    def set_openfund(self, openfund: Openfund) -> None:
        self._openfund = openfund

    def get_application(self) -> Application:
        from openfund.console.application import Application

        application = self.application
        assert isinstance(application, Application)
        return application

    def reset_openfund(self) -> None:
        self.get_application().reset_openfund()

    def option(self, name: str, default: Any = None) -> Any:
        try:
            return super().option(name)
        except CleoValueError:
            return default
