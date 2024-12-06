from __future__ import annotations

from typing import TYPE_CHECKING

from openfund.console.commands.command import Command


if TYPE_CHECKING:
    from collections.abc import Callable


class AboutCommand(Command):
    name = "about"

    description = "Shows information about Openfund."

    def handle(self) -> int:
        from openfund.utils._compat import metadata

        # The metadata.version that we import for Python 3.7 is untyped, work around
        # that.
        version: Callable[[str], str] = metadata.version

        self.line(
            f"""\
<info>Openfund - Fund Management for Python

Version: {version('openfund')}

<comment>Openfund is a dependency manager tracking local dependencies of your projects\
 and libraries.
See <fg=blue>https://github.com/python-poetry/poetry</> for more information.</comment>\
"""
        )

        return 0
