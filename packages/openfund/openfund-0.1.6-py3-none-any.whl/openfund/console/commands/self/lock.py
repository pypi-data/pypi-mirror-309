from __future__ import annotations

from openfund.console.commands.lock import LockCommand
from openfund.console.commands.self.self_command import SelfCommand


class SelfLockCommand(SelfCommand, LockCommand):
    name = "self lock"
    description = "Lock the Poetry installation's system requirements."
    help = f"""\
The <c1>self lock</c1> command reads this Poetry installation's system requirements as \
specified in the <comment>{SelfCommand.get_default_system_pyproject_file()}</> file.

The system dependencies are locked in the <comment>\
{SelfCommand.get_default_system_pyproject_file().parent.joinpath("poetry.lock")}</> \
file.
"""
