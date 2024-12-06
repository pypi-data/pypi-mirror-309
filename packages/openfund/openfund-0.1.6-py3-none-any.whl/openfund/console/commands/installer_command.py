from __future__ import annotations

from typing import TYPE_CHECKING

from openfund.console.commands.env_command import EnvCommand
from openfund.console.commands.group_command import GroupCommand


if TYPE_CHECKING:
    from openfund.installation.installer import Installer


class InstallerCommand(GroupCommand, EnvCommand):
    def __init__(self) -> None:
        # Set in openfund.console.application.Application.configure_installer
        self._installer: Installer | None = None

        super().__init__()

    def reset_openfund(self) -> None:
        super().reset_openfund()

        self.installer.set_package(self.openfund.package)
        self.installer.set_locker(self.openfund.locker)

    @property
    def installer(self) -> Installer:
        assert self._installer is not None
        return self._installer

    def set_installer(self, installer: Installer) -> None:
        self._installer = installer
